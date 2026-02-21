import asyncio
import json
import os
import sys
import time
from aiohttp import web
from datetime import datetime

# Add project root to sys.path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CryptoDevTools.solana import SolanaSwapListener
from CryptoDevTools.solana.helpers.CandleAggregator import CandleAggregator

# In-memory storage for candles
historical_candles = []
current_candle = None
connected_clients = set()

# Helper constants
RPC_URL = "https://greer-651y13-fast-mainnet.helius-rpc.com"
WSS_URL = "wss://greer-651y13-fast-mainnet.helius-rpc.com"
TOKEN_MINT = "4du67Lp42navoc7zvh42689yz1CRjzWycjp1qsRDpump" 

async def broadcast_update(candle):
    """Broadcasts a candle update to all connected WebSocket clients."""
    if not connected_clients:
        return
    
    # Format for TradingView
    msg = json.dumps({
        "type": "update",
        "candle": {
            "time": candle["start_time"] * 1000, # TV expects milliseconds
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["sol_volume"]
        }
    })
    
    for ws in list(connected_clients):
        try:
            await ws.send_str(msg)
        except Exception as e:
            print(f"Error sending to WS: {e}")
            connected_clients.discard(ws)

def on_candle_close(candle):
    historical_candles.append(candle)
    asyncio.create_task(broadcast_update(candle))

def on_candle_update(candle):
    global current_candle
    current_candle = candle
    asyncio.create_task(broadcast_update(candle))

# --- Web Server Routes ---

async def handle_index(request):
    """Serve the main HTML page."""
    return web.FileResponse(os.path.join(os.path.dirname(__file__), '..', '..', 'web', 'index.html'))

async def handle_history(request):
    """Return historical candles for TradingView."""
    # TradingView UDF format
    t = []
    o = []
    h = []
    l = []
    c = []
    v = []
    
    all_candles = historical_candles.copy()
    if current_candle:
        all_candles.append(current_candle)
        
    for candle in all_candles:
        t.append(candle["start_time"])
        o.append(candle["open"])
        h.append(candle["high"])
        l.append(candle["low"])
        c.append(candle["close"])
        v.append(candle["sol_volume"])
        
    if not t:
        return web.json_response({"s": "no_data"})
        
    return web.json_response({
        "s": "ok",
        "t": t,
        "o": o,
        "h": h,
        "l": l,
        "c": c,
        "v": v
    })

async def websocket_handler(request):
    """Handle WebSocket connections for real-time updates."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    connected_clients.add(ws)
    print(f"Client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for msg in ws:
            pass # We only send data, don't expect to receive much
    finally:
        connected_clients.discard(ws)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")
        
    return ws

async def start_background_tasks(app):
    """Start the Solana listener in the background."""
    listener = SolanaSwapListener(RPC_URL, WSS_URL)
    # 10-second candles for fast updates
    aggregator = CandleAggregator(
        timeframe_seconds=10, 
        on_candle_close=on_candle_close,
        on_candle_update=on_candle_update
    )

    async def on_swap(data):
        aggregator.process_swap(data)

    print(f"Starting Solana listener for {TOKEN_MINT}...")
    app['listener_task'] = asyncio.create_task(listener.start(TOKEN_MINT, on_swap))

async def cleanup_background_tasks(app):
    app['listener_task'].cancel()
    await app['listener_task']

def main():
    app = web.Application()
    
    # Setup routes
    app.router.add_get('/', handle_index)
    app.router.add_get('/api/history', handle_history)
    app.router.add_get('/ws', websocket_handler)
    
    # Serve static files (charting_library and our custom JS)
    web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'web'))
    app.router.add_static('/static/', path=web_dir, name='static')
    
    # Background tasks
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    print("Starting server at http://localhost:8080")
    web.run_app(app, port=8080)

if __name__ == '__main__':
    main()
