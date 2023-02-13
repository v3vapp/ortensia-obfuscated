
from dotenv import load_dotenv
load_dotenv()

import os
binance_api_key = os.getenv('binance_api_key')
binance_api_secret = os.getenv('binance_api_secret')

test_binance_api_key = os.getenv('test_binance_api_key')
test_binance_api_secret = os.getenv('test_binance_api_secret')

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
aws_region = os.getenv('aws_region')
aws_instance = os.getenv('aws_instance')


