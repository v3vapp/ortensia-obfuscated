import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
import pandas_ta as ta
import pandas as pd
import numpy as np
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
import warnings
warnings.simplefilter('ignore', FutureWarning)

def run(df, time_dataFrame, rsiLength, trading=True):

    # create time_dataFrame #
    df['openDatetime_data'] = pd.to_time((df['opentime_data']/1000).astype(int), unit='s')

    if time_dataFrame <= 60:
        df = df.loc[df["openDatetime_data"].dt.minute % time_dataFrame == 0]
        # df["time_dataFrame"] = np.select(conditions, [1], default=0)

    if time_dataFrame > 60:
        df = df.loc[df["openDatetime_data"].dt.minute == 00] # keep only HOURS xx:00
        df = df.loc[df["openDatetime_data"].dt.hour % (time_dataFrame/60) == 0] 
        
    df.reset_index(drop=True, inplace=True)

    df["close"]  = df["close"].apply(lambda x: float(x))
    df["high"]   = df["high"].apply(lambda x: float(x))
    df["low"]    = df["low"].apply(lambda x: float(x))
    df["volume"] = df["volume"].apply(lambda x: float(x))

    df["rsi"] = ta.rsi(df['close'], length = rsiLength)
    df.to_csv("test.csv")

    # When backtesting drop N/A
    if trading == False:
        df.dropna(inplace = True)

    df = df.reset_index(drop=True)

    return df

#_____________________________________________

if __name__ == "__main__":

    df = pd.read_csv(f"/home/username/project/static/SAMPLE/kline/kline1m_5days.csv")

    rsiLength = 12
    tf = 240

    df_rsi = run(df, tf, rsiLength, trading=False)

    print(df_rsi)

    cols = list(df_rsi.columns.values)

    df_rsi = df_rsi[['open', 'high', 'low', 'close','opentime_data',  'volume', 'closetime_data', 'quoteAssetVolume', 'trades', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume', 'Ignore', 'rsi']]
    
    print(df_rsi)

    import matplotlib.pyplot as plt

    df_rsi['opentime_data'] = df_rsi['opentime_data']/1000
    df_rsi['opentime_data'] = pd.to_time((df_rsi['opentime_data']/1000).astype(int), unit='s')

    plt.plot(df_rsi["opentime_data"], df_rsi["rsi"])

    plt.gcf().autofmt_xdate()
    plt.show()