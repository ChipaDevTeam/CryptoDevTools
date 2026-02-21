const configurationData = {
    supported_resolutions: ['10S', '1', '5', '15', '30', '60', '1D', '1W', '1M'],
    exchanges: [{
        value: 'Solana',
        name: 'Solana',
        desc: 'Solana Network',
    }],
    symbols_types: [{
        name: 'crypto',
        value: 'crypto',
    }],
};

const lastBarsCache = new Map();
let ws = null;
let realtimeCallback = null;

const datafeed = {
    onReady: (callback) => {
        console.log('[onReady]: Method call');
        setTimeout(() => callback(configurationData));
    },

    searchSymbols: async (userInput, exchange, symbolType, onResultReadyCallback) => {
        console.log('[searchSymbols]: Method call');
        onResultReadyCallback([]);
    },

    resolveSymbol: async (symbolName, onSymbolResolvedCallback, onResolveErrorCallback, extension) => {
        console.log('[resolveSymbol]: Method call', symbolName);
        const symbolInfo = {
            ticker: symbolName,
            name: symbolName,
            description: symbolName,
            type: 'crypto',
            session: '24x7',
            timezone: 'Etc/UTC',
            exchange: 'Solana',
            minmov: 1,
            pricescale: 1000000000, // 9 decimal places for SOL
            has_intraday: true,
            has_seconds: true,
            seconds_multipliers: ['10'],
            intraday_multipliers: ['1', '5', '15', '30', '60'],
            supported_resolutions: configurationData.supported_resolutions,
            volume_precision: 8,
            data_status: 'streaming',
        };
        setTimeout(() => onSymbolResolvedCallback(symbolInfo));
    },

    getBars: async (symbolInfo, resolution, periodParams, onHistoryCallback, onErrorCallback) => {
        const { from, to, firstDataRequest } = periodParams;
        console.log('[getBars]: Method call', symbolInfo, resolution, from, to);

        if (!firstDataRequest) {
            // We already returned all available history in the first request
            onHistoryCallback([], { noData: true });
            return;
        }

        try {
            // We only have one endpoint for history right now
            const response = await fetch('/api/history');
            const data = await response.json();

            if (data.s !== 'ok' || data.t.length === 0) {
                onHistoryCallback([], { noData: true });
                return;
            }

            let bars = [];
            for (let i = 0; i < data.t.length; ++i) {
                const time = data.t[i] * 1000; // Convert to ms
                if (data.t[i] >= from && data.t[i] < to) {
                    bars.push({
                        time: time,
                        open: data.o[i],
                        high: data.h[i],
                        low: data.l[i],
                        close: data.c[i],
                        volume: data.v[i],
                    });
                }
            }

            if (bars.length > 0) {
                lastBarsCache.set(symbolInfo.full_name, { ...bars[bars.length - 1] });
            }

            console.log(`[getBars]: returned ${bars.length} bar(s)`);
            onHistoryCallback(bars, { noData: bars.length === 0 });
        } catch (error) {
            console.log('[getBars]: Get error', error);
            onErrorCallback(error);
        }
    },

    subscribeBars: (symbolInfo, resolution, onRealtimeCallback, subscriberUID, onResetCacheNeededCallback) => {
        console.log('[subscribeBars]: Method call with subscriberUID:', subscriberUID);
        realtimeCallback = onRealtimeCallback;

        if (!ws) {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'update' && realtimeCallback) {
                    const candle = data.candle;
                    // candle.time is already in ms from the server
                    realtimeCallback({
                        time: candle.time,
                        open: candle.open,
                        high: candle.high,
                        low: candle.low,
                        close: candle.close,
                        volume: candle.volume
                    });
                }
            };

            ws.onclose = () => {
                console.log('[subscribeBars]: WebSocket closed');
                ws = null;
            };
        }
    },

    unsubscribeBars: (subscriberUID) => {
        console.log('[unsubscribeBars]: Method call with subscriberUID:', subscriberUID);
        realtimeCallback = null;
    },
};

window.addEventListener('DOMContentLoaded', () => {
    const widget = new TradingView.widget({
        symbol: 'TOKEN/SOL',
        interval: '10S',
        fullscreen: true,
        container: 'tv_chart_container',
        datafeed: datafeed,
        library_path: '/static/charting_library/',
