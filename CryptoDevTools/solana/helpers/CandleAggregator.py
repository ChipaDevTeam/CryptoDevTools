import time
from typing import Dict, Callable, Optional

class CandleAggregator:
    """
    Aggregates real-time swap data into OHLCV candles.
    """
    def __init__(self, timeframe_seconds: int, on_candle_close: Callable[[Dict], None], on_candle_update: Optional[Callable[[Dict], None]] = None):
        self.timeframe = timeframe_seconds
        self.on_candle_close = on_candle_close
        self.on_candle_update = on_candle_update
        self.current_candle: Optional[Dict] = None

    def process_swap(self, swap_data: Dict):
        """
        Process a single swap event and update the current candle.
        """
        price = swap_data.get("price_per_token")
        if not price or price <= 0:
            return

        # Use swap timestamp or current time
        ts = swap_data.get("timestamp") or int(time.time())
        
        # Align timestamp to the start of the timeframe
        candle_start = (ts // self.timeframe) * self.timeframe

        swap_type = swap_data.get("type")
        
        # Determine SOL volume and Token volume
        if swap_type == "buy":
            sol_volume = swap_data.get("amount_in", 0.0)
            token_volume = swap_data.get("amount_out", 0.0)
        else:
            sol_volume = swap_data.get("amount_out", 0.0)
            token_volume = swap_data.get("amount_in", 0.0)

        if self.current_candle is None:
            self._init_candle(candle_start, price, sol_volume, token_volume, swap_type)
        elif candle_start > self.current_candle["start_time"]:
            # Close old candle
            self.on_candle_close(self.current_candle)
            # Start new candle
            self._init_candle(candle_start, price, sol_volume, token_volume, swap_type)
        else:
            # Update current candle
            self.current_candle["high"] = max(self.current_candle["high"], price)
            self.current_candle["low"] = min(self.current_candle["low"], price)
            self.current_candle["close"] = price
            self.current_candle["sol_volume"] += sol_volume
            self.current_candle["token_volume"] += token_volume
            self.current_candle["trades"] += 1
            
            if swap_type == "buy":
                self.current_candle["buy_volume"] += sol_volume
            else:
                self.current_candle["sell_volume"] += sol_volume
                
        if self.on_candle_update and self.current_candle:
            self.on_candle_update(self.current_candle)

    def _init_candle(self, start_time: int, price: float, sol_volume: float, token_volume: float, swap_type: str):
        self.current_candle = {
            "start_time": start_time,
            "open": price,
            "high": price,
            "low": price,
            "close": price,
            "sol_volume": sol_volume,
            "token_volume": token_volume,
            "buy_volume": sol_volume if swap_type == "buy" else 0.0,
            "sell_volume": sol_volume if swap_type == "sell" else 0.0,
            "trades": 1
        }
