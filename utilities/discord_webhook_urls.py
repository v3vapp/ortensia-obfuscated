
from dotenv import load_dotenv
load_dotenv()

import os

discord_server_backtest= os.getenv('discord_server_backtest')
discord_server_backtest_debug= os.getenv('discord_server_backtest_debug')
discord_server_backtest_error= os.getenv('discord_server_backtest_error')
discord_server_database= os.getenv('discord_server_database')
discord_server_binance_report= os.getenv('discord_server_binance_report')
discord_server_binancetestnet_report= os.getenv('discord_server_binancetestnet_report')
discord_server_trade_debug= os.getenv('discord_server_trade_debug')
discord_server_order_message= os.getenv('discord_server_order_message')
discord_server_trade_system_log= os.getenv('discord_server_trade_system_log')
discord_server_trade_system_error= os.getenv('discord_server_trade_system_error')
discord_server_googleCloudStorage= os.getenv('discord_server_googleCloudStorage')
discord_server_vm= os.getenv('discord_server_vm')