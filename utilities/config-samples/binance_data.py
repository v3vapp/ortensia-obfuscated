import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))

from time import sleep

from pprint import pprint
from binance import Client
import pw
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

# TODO: CLOUD LOG is NOT ready!

# logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")

# ccxtでBinanceに接続

# def connect_binance(real_mode):
#     # for multiproccessing, make 1 sec gap when connecting to excahnge to avoid error.
#     sleep(1)

#     if real_mode == True:
#         try:
#             exchange = ccxt.binance({"apiKey": pw.binance_api_key,\
#                                 "secret": pw.binance_api_secret,
#                                 'options': {'defaultType': 'future'},\
#                                 'enableRateLimit': True})
#             exchangeName = "BINANCE_FUTURE"
#             log.info(f"Connnected to binance. This func returns [exchange, {exchangeName}]")
#         except Exception as e:
#             log.exception(f"{e}")
#         return exchange, exchangeName

#     elif real_mode == False:

#         try:
#             exchange = ccxt.binance({"apiKey": pw.test_binance_api_key,\
#                                     "secret": pw.test_binance_api_secret,
#                                     'options': {'defaultType': 'future'},\
#                                     'enableRateLimit': True})
#             exchange.set_sandbox_mode(True)
#             exchangeName = "BINANCE_TESTNET"
#             log.info(f"Connnected to binance. This func returns [exchange, {exchangeName}]")
#         except Exception as e:
#             log.exception(f"This func returns [exchange, exchangeName] reason -> {e}")
#         return exchange, exchangeName

#     else:
#         return "error", "Error. Input [True] for REAL, [False] for TESTNET."


# #########################################################################

    
def fetch_all_symbols():
    client = Client(pw.binance_api_key, pw.binance_api_secret)

    print("Login Success")
    
    exchange_info = client.futures_exchange_info()
    exchange_info['symbols']

    tickerSymbol_list = []

    for i in exchange_info['symbols']:

        if "USDT" in i['symbol'] and  "_" not in i['symbol']:
            tickerSymbol_list.append(i['symbol'])
    
    return tickerSymbol_list

##------------##------------##------------##------------##------------

def TESTNET_fetch_all_symbols():

    client = Client(pw.test_binance_api_key, pw.test_binance_api_secret, testnet=True)

    print("Login Success TESTNET")
    
    exchange_info = client.futures_exchange_info()
    exchange_info['symbols']

    tickerSymbol_list = []

    for i in exchange_info['symbols']:

        if "USDT" in i['symbol'] and  "_" not in i['symbol']:
            tickerSymbol_list.append(i['symbol'])
    
    return tickerSymbol_list


# #------------------------------------------------------------------------------------------------------------------

# def fetch_balance(exchange):
#     balance = exchange.fetch_balance()
#     return balance

# def fetch_contracts(exchange, symbol):
#     position  = exchange.fetch_positions([f"{symbol.replace('USDT','/USDT')}"]) 
#     contracts = position[0]['contracts']
#     return contracts

# def fetch_entryPrice(exchange,symbol):
#     position    = exchange.fetch_positions([f"{symbol.replace('USDT','/USDT')}"]) 
#     entryPrice  = position[0]['entryPrice']
#     return entryPrice

# def fetch_notional(exchange, symbol):
#     position = exchange.fetch_positions([f"{symbol.replace('USDT','/USDT')}"]) 
#     notional = position[0]['notional']
#     return round(notional,1)

# def fetch_side(exchange, symbol):
#     position = exchange.fetch_positions([f"{symbol.replace('USDT','/USDT')}"]) 
#     side     = position[0]['side']
#     return side

# def fetch_unrealizedPnl(exchange, symbol):
#     position = exchange.fetch_positions([f"{symbol.replace('USDT','/USDT')}"]) 
#     unrealizedPnl = position[0]['unrealizedPnl']
#     return unrealizedPnl

# def set_leverage(exchange):
#     symbol = "BTCUSDT"
#     LEVERAGE = 25  #レバレッジ限度を設定可能（銘柄によって倍率が異なる）基本はMAXでいい。

#     exchange.set_leverage(LEVERAGE, symbol, params = {})

# def fetch_ask_bid(exchange, symbol):
#     order_book = exchange.fetch_order_book(symbol)
#     ask = order_book['asks'][0][0]
#     bid = order_book['bids'][0][0]
#     return ask, bid

# def fetch_leverage_max(exchange):
#     x = exchange.markets(["BTC/USDT"])
#     return x



if __name__  == "__main__":

# Python

    a = fetch_all_symbols()

    print(a)
    print(len(a))