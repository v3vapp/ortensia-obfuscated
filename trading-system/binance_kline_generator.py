import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
from config import pw
from binance.client import Client
from binance.enums import HistoricalKlinesType
import numpy as np
import sqlite3, math, time, logging, multiprocessing
import ast
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

# --------------------------------------------------------------------------------------------------------

def tableName(session, symbol, exchangeID, candleTimeFrame) :

    if "BINANCE" in exchangeID:
        exchangeID = "BINANCE"

    TableName = f"kline{candleTimeFrame}_{exchangeID}_{session}_{symbol}"

    return TableName

#__________________________________________________________________________

def reset_table(session, exchangeID, candleTimeFrame, list_symbols):

    # Remove all existing symbol-kline-table for this session.

    connection = sqlite3.connect(f"{outside_dir}/project.db")
    c = connection.cursor()

    for i in range(len(list_symbols)):

        symbol = list_symbols[i]

        tableName = tableName(session, symbol, exchangeID, candleTimeFrame)

        # Clean IF Same "session strategy ticker" Table 
        c.execute(f"Drop Table if exists {tableName}")

    log.info("Reset Kline Database")

    connection.close()


#_________________________________________________________________________________
# FIXME: USE REAL KLINE DATA!
def history(session, process_id, exchangeID, candleTimeFrame, list_symbols):

    exchangeClient = Client(pw.binance_api_key, pw.binance_api_secret)

    total_process = 3

    connection = sqlite3.connect(f"{outside_dir}/project.db")
    c = connection.cursor()

    #__________________________________________________________________________

    start_time = time.time()

    list_symbols = np.array_split(list_symbols, total_process) #-> [array([1, 2, 3, 4]), array([5, 6, 7]), array([ 8,  9, 10])]

    list_symbols_part = list_symbols[process_id]

    print(f"List for {process_id}. {list_symbols_part}")

    for i in range(len(list_symbols_part)):

        while True:
            try:
                symbol = list_symbols_part[i]
                tableName = tableName(session, symbol, exchangeID, candleTimeFrame)

                # create table
                c.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(\
                                'openTime',\
                                'open',\
                                'high',\
                                'low',\
                                'close',\
                                'volume',\
                                'closeTime',\
                                'quoteAssetVolume',\
                                'trades',\
                                'takerBuyBaseAssetVolume',\
                                'takerBuyQuoteAssetVolume',\
                                'Ignore')")

                sql = f"SELECT Params FROM {session} WHERE SYMBOL = '{symbol}'"

                c.execute(sql)

                # Transform data
                params_data = c.fetchone()                  # ('[9110, 343, 120, 5280]',) 
                params_data = params_data[0]                # '[9110, 343, 120, 5280]'
                params_data = ast.literal_eval(params_data) # [9110, 343, 120, 5280]

                max_param = max(params_data) + 2880 # 2 days buffer

                fetch_days = math.ceil(max_param/1440)
                            
                kline_history = exchangeClient.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, f"{fetch_days} day ago UTC", klines_type=HistoricalKlinesType.FUTURES)
                
                #print(f"{params_data} -> {max_param}, {fetch_days} days")
                #print(kline_history[0])

                used_weight_1m = int(exchangeClient.response.headers['x-mbx-used-weight-1m'])

                log.info(f"New History {symbol} {fetch_days}days id_{process_id}. Limit {used_weight_1m}/2400")

                c.executemany(f"INSERT INTO {tableName} VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", kline_history)

                # Delete latest record because it's wrong and unfinished tick data.
                c.execute(f'DELETE FROM {tableName} ORDER BY rowid DESC LIMIT 1;')

                # Adding symbol Column for stream data. IDK if its ness. NO
                c.execute(f"ALTER TABLE {tableName} ADD COLUMN SYMBOL TEXT NOT NULL DEFAULT {symbol}")

                connection.commit()

                break

            except Exception as e:

                used_weight_1m = int(exchangeClient.response.headers['x-mbx-used-weight-1m'])

                log.info(f"{used_weight_1m} weigh now. History kline fetching error @{symbol}. Waiting few sec. reason-> {e}")
                
                time.sleep(3)

    elapse_sec = time.time() - start_time

    log.info(f"_________Kline Database process_id -> {process_id} finish. Elapse -> {round(elapse_sec,1)}sec____________")


def run(session, exchangeID, candleTimeFrame, list_symbols):
    try:
        # Multi proccess # 
        # 3 workers are MAX possible multi-processes cuz of request weight! 

        reset_table(session, exchangeID, candleTimeFrame, list_symbols)

        id_0 = multiprocessing.Process(name="", target=history, args=(session, 0, exchangeID, candleTimeFrame, list_symbols))
        id_1 = multiprocessing.Process(name="", target=history, args=(session, 1, exchangeID, candleTimeFrame, list_symbols))
        id_2 = multiprocessing.Process(name="", target=history, args=(session, 2, exchangeID, candleTimeFrame, list_symbols))

        # RUN MULTI PROCESS #
        id_0.start()
        id_1.start()
        id_2.start()

        # RUN MULTI PROCESS #
        id_0.join()
        id_1.join()
        id_2.join()

        log.info(f"================= Kline is READY! {session} ====================")

    except Exception as e:
        logging.warning(e)

#_________________________________________________________________________________________

if __name__ == "__main__": 

    from trade import setup

    sessionInfo = setup.run()

    session         = sessionInfo[2]
    exchangeID      = sessionInfo[7]
    candleTimeFrame = sessionInfo[8]
    # exchangeClient  = sessionInfo[9]

    list_symbols = ["BTCUSDT", "ETHUSDT"]
    
    run(session, exchangeID, candleTimeFrame, list_symbols)