import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")
import sqlite3, math, time
from pprint import pprint
import pandas as pd
import pandas_ta as ta
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#==================================================================
# list_symbols

def fetch_qual_symbols(session):

    connection = sqlite3.connect(f"{outside_dir}/project.db")

    connection.row_factory = lambda cursor, row: row[0]

    c = connection.cursor()

    sql = f"SELECT symbol FROM {session}"
    c.execute(sql)

    list_symbols = c.fetchall()

    return list_symbols

#_______________________________________________________________
# Dataframe

def create_trade_df(session, symbol):

    connection = sqlite3.connect(f"{outside_dir}/project.db")
    c = connection.cursor()

    sql = f"SELECT * FROM {session} WHERE symbol = '{symbol}'"
    c.execute(sql)

    #_______________________________________________________________
    # params

    params_column_names = list(map(lambda x: x[0], c.description))

    params_data = c.fetchone()

    df_params = pd.DataFrame([params_data], columns=params_column_names)

    coreLine    = float(df_params.loc[0, 'coreLine'])
    trendLine   = float(df_params.loc[0, 'trendLine'])
    trueRange      = float(df_params.loc[0, 'trueRange'])
    atr     = float(df_params.loc[0, 'atr'])

    max_param = max(coreLine, trendLine, trueRange, atr)

    #_______________________________________________________________
    # KLINE

    kline_sample = f"kline_1m_{symbol}_BINANCE_TESTNET"

    sql = f"SELECT * FROM {kline_sample} ORDER BY rowid DESC LIMIT {max_param}"
    c.execute(sql)

    kline_column_names = list(map(lambda x: x[0], c.description))

    kline = c.fetchall()

    df = pd.DataFrame(kline, columns=kline_column_names)

    df = df.iloc[::-1]

    # #_______________________________________________________________
    # # Indicator DataFrame

    df["close"]  = df["close"].apply(lambda x: float(x))
    df["high"]   = df["high"].apply(lambda x: float(x))
    df["low"]    = df["low"].apply(lambda x: float(x))
    df["volume"] = df["volume"].apply(lambda x: float(x))

    # [step 1] TrueRange = max(arg_TR) - min(arg_TR) 
    df["HIghestRange"] = df["high"].rolling(int(trueRange/2)).max()
    df["lowestRange"]  = df["low"].rolling(int(trueRange/2)).min()

    # [step 2] normATR = Average(trueRange/close, input_ATRlength)
    df["normATR"] = ta.normATR(df[f"HIghestRange"], df[f"lowestRange"], df["close"].shift(1), length = atr)

    # [step 3] coreLine, upper=(coreLine+normATR), lower=(coreLine-normATR)
    df["coreLine"] = ta.vwma(df["close"], df["volume"], length=coreLine)
    df["Upper"] = df["coreLine"] + (df["coreLine"] * (df["normATR"]*0.01))
    df["lower"] = df["coreLine"] - (df["coreLine"] * (df["normATR"]*0.01))

    # [step 4] trendLine Line
    df["trendLine"] = ta.vwma(df["close"], df["volume"], length=trendLine)

    df.dropna(inplace = True)
    df = df.reset_index(drop=True)

    return df



#===========================================================
if __name__ == "__main__":

    session = "Diviation_Long_2022_1004_0313_Qualify"

    list_symbols = fetch_qual_symbols(session)

    for symbol in list_symbols:

        print(symbol)

        df = create_trade_df(session, symbol)
        print(df)

        Upper  = df['Upper'].iloc[-1]
        lower  = df['lower'].iloc[-1]
        coreLine   = df['coreLine'].iloc[-1]
        trendLine  = df['trendLine'].iloc[-1]
        close  = df['close'].iloc[-1]

        print(f"close = {close}")







