from binance.enums import HistoricalKlinesType
from binance import Client
from pprint import pprint
import time

test_binance_api_key    = "d1e2770df3b64f0663c292bea424fa91fb4c07bcde476c319d35f2fe01059675"
test_binance_api_secret = "14bf9fe1a0a3e3674bf61a3cf9181567f205c2c50e7ed859fc16e3702cf6ffa0"

CLIENT = Client(test_binance_api_key, test_binance_api_secret,  {"time_dataout": 99999}, testnet=True)
CLIENT_KLINE = Client(test_binance_api_key, test_binance_api_secret,  {"time_dataout": 99999}, testnet=True)



symbol = "ATOMUSDT"

info = CLIENT.futures_exchange_info()

total_symbols = info['symbols']

len_symbols = len(total_symbols)

for i in (range(len_symbols)):
    pair = total_symbols[i]['pair']
    if pair == symbol:
        pricePrecision = info['symbols'][i]['pricePrecision']
        quantityPrecision = info['symbols'][i]['quantityPrecision']
        print(pricePrecision)
        print(quantityPrecision)


"""

{   
'baseAsset': 'ATOM',
'baseAssetPrecision': 8,
'contractType': 'PERPETUAL',
'deliveryDate': 4133404800000,
'filters': [{'filterType': 'PRICE_FILTER',
            'maxPrice': '721.550',
            'minPrice': '0.432',
            'tickSize': '0.001'},
            {'filterType': 'LOT_SIZE',
            'maxQty': '10000',
            'minQty': '0.01',
            'stepSize': '0.01'},
            {'filterType': 'MARKET_LOT_SIZE',
            'maxQty': '100000',
            'minQty': '0.01',
            'stepSize': '0.01'},
            {'filterType': 'MAX_NUM_ORDERS', 'limit': 200},
            {'filterType': 'MAX_NUM_ALGO_ORDERS', 'limit': 10},
            {'filterType': 'MIN_NOTIONAL', 'notional': '10'},
            {'filterType': 'PERCENT_PRICE',
            'multiplierDecimal': '4',
            'multiplierDown': '0.9000',
            'multiplierUp': '1.1000'}],
'liquidationFee': '0.020000',
'maintMarginPercent': '2.5000',
'marginAsset': 'USDT',
'marketTakeBound': '0.10',
'onboardDate': 1569398400000,
'orderTypes': ['LIMIT',
                'MARKET',
                'STOP',
                'STOP_MARKET',
                'TAKE_profit',
                'TAKE_profit_MARKET',
                'TRAILING_STOP_MARKET'],
'pair': 'ATOMUSDT',
'pricePrecision': 3,
'quantityPrecision': 2,
'quoteAsset': 'USDT',
'quotePrecision': 8,
'requiredMarginPercent': '5.0000',
'settlePlan': 0,
'status': 'TRADING',
'symbol': 'ATOMUSDT',
'time_dataInForce': ['GTC', 'IOC', 'FOK', 'GTX'],
'triggerProtect': '0.0500',
'underlyingSubType': [],
'underlyingType': 'COIN'
}

"""