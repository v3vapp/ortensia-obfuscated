import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_module")
import time
from global_module.config import ccxt_exchange
from binance.client import Client
from binance.enums import HistoricalKlinesType


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

start_time_data = time.time()

try:
    binance = ccxt_exchange.connect_binance()

    client = Client(ccxt_exchange.binance_api_key, ccxt_exchange.binance_api_secret)

    li_symbols = ccxt_exchange.fetch_all_symbols(binance)

    for i in range(len(li_symbols)):

        t = li_symbols[i]
        # klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 JAN, 2022",klines_type=HistoricalKlinesType.FUTURES)
        klines = client.get_historical_klines(f"{t}", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC",klines_type=HistoricalKlinesType.FUTURES)

        log.info(t)

except Exception as e:
    log.info(f"{t} is {e}")


elapse_sec = time.time() - start_time_data
log.info(f" Elapse -> {elapse_sec}sec")



# elapse_sec = time.time() - start_time_data
# elapse_min = elapse_sec/60

# bars = len(klines)

# bars_in_min = bars/elapse_min

# log.info(f"Spent {round(elapse_min,1)} min for {bars} bars ({round(bars_in_min,1)} bars/min)")

# Avarage Fetch time.
#  0.7min for 103223bars (156733.4bars/min) 
#  1.8min for 278907bars (158719.2bars/min)
#  2.6min for 408517bars (155960.5bars/min)
