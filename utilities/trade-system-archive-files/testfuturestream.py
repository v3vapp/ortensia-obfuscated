import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_module")

import os, time, sys, logging, time, schedule, sqlite3, json, websocket
from global_module.config import ccxt_exchange
from global_module.strategy import Diviation_Long, Diviation_Short

from time_dataout_decorator import time_dataout

import rich
from rich import pretty, print
from rich.console import Console
import time
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

# --------------------------------------------------------------------------------------------------------

# day_sec = 1440*60

# @time_dataout(day_sec)
def func():

    binance, excahngeName = ccxt_exchange.connect_binance()

    def on_error(ws, error):
        print(error) 

    def on_message(ws, message):

        """
        {
            "stream": "footballusdt@kline_1m",
            "data": {
                "e": "kline",               // Event type  
                "E": 1665585162179,         // Event time
                "s": "FOOTBALLUSDT",
                "k": {
                    "t": 1665585120000,     // Kline start time
                    "T": 1665585179999,     // Kline close time
                    "s": "FOOTBALLUSDT",
                    "i": "1m",
                    "f": 6426372,           // First trade ID
                    "L": 6426383,           // Last trade ID
                    "o": "865.92000",
                    "c": "865.67000",
                    "h": "865.92000",
                    "l": "865.56000",
                    "v": "4.26",            // Base asset volume
                    "n": 12,                // Number of trades
                    "x": False,             // Is this kline closed?
                    "q": "3688.3413000",    // Quote asset volume
                    "V": "1.73",            // Taker buy base asset volume
                    "Q": "1497.9851000",    // Taker buy quote asset volume
                    "B": "0",               // Ignore
                },
            },
        }
        """

        stream_data             = json.loads(message)

        data                    = stream_data["data"]

        symbol                  = str(data['s'])
        candle                  = data['k']
        Tick                    = float(candle['c'])
        opentime_data                = candle['t']
        open                    = candle['o']
        high                    = candle['h']
        low                     = candle['l']
        close                   = candle['c']
        volume                  = candle['v']
        closetime_data               = candle['T']
        quoteAssetVolume        = candle['q']
        trades                  = candle['n']
        takerBuyBaseAssetVolume = candle['V']
        takerBuyQuoteAssetVolume= candle['Q']
        is_candle_closed        = candle['x']

        kline_stream = [ ( opentime_data,\
                        open,\
                        high,\
                        low,\
                        close,\
                        volume,\
                        closetime_data,\
                        quoteAssetVolume,\
                        trades,\
                        takerBuyBaseAssetVolume,\
                        takerBuyQuoteAssetVolume,\
                        bool(is_candle_closed),\
                        ) ]

        log.info(stream_data)


    #---------------------------------------------------------------------------------------------------

    # List Up All The symbols
    # li_symbols =  ccxt_exchange.fetch_all_symbols(binance)

    # # Prefix Stream EndPoint
    # Sockets_li = ["wss://fstream.binance.com:9443/ws/",]

    # # Create Strings
    # for index, symbol in enumerate(li_symbols):
        
    #     symbol = symbol.lower()
    #     tf = "1m"

    #     data = f'{symbol}@kline_{tf}/'
    #     Sockets_li.append(data)

    # # List to String
    # SOCKET = ''.join(Sockets_li)
    # # Remove "/" at last
    # SOCKET = SOCKET[:-1]

    # SOCKET ="wss://fstream.binance.com/stream?streams=footballusdt@kline_1m/btcusdt@markPrice"
    SOCKET ="wss://fstream.binance.com/stream?streams=footballusdt@kline_1m"

    # Let's Stream #
    ws = websocket.WebSocketApp(SOCKET, on_message=on_message, on_error=on_error)
    ws.run_forever()



# TEST #
if __name__ == "__main__":
    func()




