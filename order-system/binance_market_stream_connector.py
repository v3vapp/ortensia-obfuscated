import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import kline
import sqlite3, json, websocket, logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

#_____________________________________________________________

def run(session, exchangeID, candletime_dataFrame, list_symbols):

    connection = sqlite3.connect(f"{outside_dir}/project.db")
    c = connection.cursor()


    def on_error(ws, error):
        print(error) 

    def on_message(ws, message):

        # システムをアップデートした際、データベースが消えないよう、プロジェクトの外（並列）にデータベースを作成する
        con = sqlite3.connect(f"{outside_dir}/project.db")
        cur = con.cursor()

        stream_data             = json.loads(message)
        data                    = stream_data["data"]
        streamSymbol            = str(data['s'])
        candle                  = data['k']
        #Tick                   = float(candle['c'])
        opentime_data           = candle['t']
        open                    = candle['o']
        high                    = candle['h']
        low                     = candle['l']
        close                   = candle['c']
        volume                  = candle['v']
        closetime_data          = candle['T']
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
                        str(streamSymbol),\
                        ) ]

        # log.info(kline_stream)

        if is_candle_closed == True:
            try:
                tableName = kline.tableName(session, streamSymbol, exchangeID, candletime_dataFrame)
                cur.executemany(f"INSERT INTO {tableName} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", kline_stream)
                con.commit()
                log.info(f"Fetched {streamSymbol}")

            except Exception as e:
                logging.info(f"{e}")

    #---------------------------------------------------------------------------------------------------
    # List Up All The symbols

    # Prefix Stream EndPoint (Not stream.binance  USE -> fstream.binance for FUTURES)
    Sockets_li = ["wss://fstream.binance.com/stream?streams=",]

    for symbol in list_symbols:
        
        symbol = symbol.lower()
        candletime_dataFrame = "1m"

        data = f'{symbol}@kline_{candletime_dataFrame}/'
        Sockets_li.append(data)

    # List to String
    SOCKET = ''.join(Sockets_li)
    # Remove "/" at last
    SOCKET = SOCKET[:-1]

    # Let's Stream #
    ws = websocket.WebSocketApp(SOCKET, on_message=on_message, on_error=on_error)
    ws.run_forever()

#_________________________________________________________________________________________

if __name__ == "__main__": 

    from trade import setup

    sessionInfo = setup.run()

    session         = sessionInfo[2]
    exchangeID      = sessionInfo[7]
    candletime_dataFrame = sessionInfo[8]
    exchangeClient  = sessionInfo[9]
    
    list_symbols = ["BTCUSDT", "ETHUSDT"]

    run(session, exchangeID, candletime_dataFrame, list_symbols)
