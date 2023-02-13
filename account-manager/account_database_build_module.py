import sys, pathlib, os
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/tools")

import time_data, sys, logging, time_data, sqlite3, pathlib
from pprint import pprint
from binance import Client
from multiprocessing import Process
import pandas as pd
from config import pw
from tools import googleCloudStorage, report

from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
#________________________________________________________
def delete_table(exchangeName):
    con = sqlite3.connect(f"{outside_dir}/project.db")
    cur = con.cursor()
    cur.execute(f"Drop Table if exists account_{exchangeName}")
    con.close()
    log.info(f"deleted account_{exchangeName}")
#________________________________________________________

def get(exchangeName):
    try:
        if exchangeName == "BINANCETESTNET":
            client = Client(pw.test_binance_api_key, pw.test_binance_api_secret, testnet=True)
        elif exchangeName == "BINANCE":
            client = Client(pw.binance_api_key, pw.binance_api_secret)

        con = sqlite3.connect(f"{outside_dir}/project.db")
        cur = con.cursor()

        unixtime_data = int(time_data.time_data())

        all_position_data = client.futures_position_information()

        balance_data  = client.futures_account_balance()
        open_position = []

        for i in range(len(all_position_data)):
            positionAmt     = float(all_position_data[i]["positionAmt"])
            if positionAmt != 0:
                open_position.append(all_position_data[i])

        data = [(str(exchangeName), int(unixtime_data), str(balance_data), str(open_position),),]

        cur.execute(f"CREATE TABLE IF NOT EXISTS account_{exchangeName} (exchangeName, unixtime_data, balance, position)")

        cur.executemany(f"INSERT INTO account_{exchangeName} VALUES(?,?,?,?)", data)
        con.commit()
        con.close()

        report.new_account_data(exchangeName)

    except Exception as e:

        report.error(e, "Error save_account.py -> Error happend when I'm trying to get new account balance and position data.")
#________________________________________________________

def upload(exchangeName):
    try:
        os.makedirs(f"static/ACCOUNT", exist_ok=True)
        bucket_name  = "project_bucket"

        con = sqlite3.connect(f"{outside_dir}/project.db")
        db_df = pd.read_sql_query(f"SELECT * FROM account_{exchangeName}", con)

        googleCloudStorage_path = f'ACCOUNT/account_{exchangeName}.csv'
        local_path = f'{working_dir}/static/{googleCloudStorage_path}'

        db_df.to_csv(local_path, index=False)

        googleCloudStorage.upload(bucket_name, local_path, googleCloudStorage_path)
        #____________________________________________________

        unixtime_data = int(time_data.time_data())
        googleCloudStorage_backup_path = f'ACCOUNT/BACKUP/{exchangeName}_{unixtime_data}.csv'

        googleCloudStorage.upload(bucket_name, local_path, googleCloudStorage_backup_path)

        report.upload_googleCloudStorage(exchangeName)

    except Exception as e:

        report.error(e, "Error save_account.py -> Error happend when I'm trying to upload account database to GoogleCloudStorage.")


def multi_delete_table():

    param1 = Process(target=delete_table, args=('BINANCE',))
    param2 = Process(target=delete_table, args=('BINANCETESTNET',))
    param1.start()
    param2.start()
    param1.join()
    param2.join()
#________________________________________________________

def multi_get():

    param1 = Process(target=get, args=('BINANCE',))
    param2 = Process(target=get, args=('BINANCETESTNET',))
    param1.start()
    param2.start()
    param1.join()
    param2.join()
#________________________________________________________

def multi_upload():
    param1 = Process(target=upload, args=('BINANCE',))
    param2 = Process(target=upload, args=('BINANCETESTNET',))
    param1.start()
    param2.start()
    param1.join()
    param2.join()

#________________________________________________________

if __name__ == "__main__":
    multi_delete_table()
    multi_get()
    multi_upload()