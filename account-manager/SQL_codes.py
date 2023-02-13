import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")

import logging, sqlite3, time, pprint

logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")

def balance(exchange_name) : 

    # データベースの位置を正しく指定できているか要チェック(project_db/db.pyで作成したDatabaseを指定)
    con = sqlite3.connect(f"{outside_dir}/project.db")

    #ここでDBからデータを取得
    #targer_exchange = "BINANCE"
    res = con.execute(f'SELECT * FROM account_{exchange_name} ORDER BY rowid DESC LIMIT 1440;')

    # Create Empty List
    exchange = []

    #取得した順番通りに列を指定し、リストに追加保存していく。
    for row in reversed(res.fetchall()) : 
        exchange.append(row[0])

    # Returnning Lists for CharJS
    return exchange

# ----------------------------------------------------------
# TESTING Script is OK
if __name__ == "__main__":

    exchange = balance("BINANCE")

    pprint.pprint(exchange)