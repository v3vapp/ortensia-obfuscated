from binance.enums import HistoricalKlinesType
from binance import Client
from pprint import pprint
import time

test_binance_api_key    = ""
test_binance_api_secret = ""

CLIENT = Client(test_binance_api_key, test_binance_api_secret,  {"time_dataout": 99999}, testnet=True)
CLIENT_KLINE = Client(test_binance_api_key, test_binance_api_secret,  {"time_dataout": 99999}, testnet=True)

used_weight_1m = int(CLIENT_KLINE.response.headers['x-mbx-used-weight-1m'])

print(used_weight_1m)

# info = client.get_exchange_info()
# info["rateLimits"]

symbol_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]

for symbol in symbol_list:

    print(symbol)

    while True:

        try:

            head = CLIENT_KLINE.response.headers
            used_weight_1m = int(head['x-mbx-used-weight-1m'])

            s = time.time()

            hist = CLIENT_KLINE.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "60 day ago UTC", klines_type=HistoricalKlinesType.FUTURES)

            print(hist[0])

            head = CLIENT_KLINE.response.headers
            used_weight_1m = int(head['x-mbx-used-weight-1m'])
            
            elpse = time.time() - s 

            print(f"Request weight is -> {used_weight_1m} (1m), {round(elpse,1)} sec")

            time.sleep(1)

            break

        except Exception as e:

            head = CLIENT_KLINE.response.headers
            used_weight_1m = int(head['x-mbx-used-weight-1m'])
            
            elpse = time.time() - s 

            print(f"Too much request weight? reason {e}. waiting...-> {used_weight_1m} (1m), waiting {round(elpse,1)} sec")

            time.sleep(10)