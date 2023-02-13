import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent  
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import os
import matplotlib.pyplot as plt
import pandas as pd
from pandas import time_datastamp # Don't remove
import numpy as np
import time, logging
from strategy import Devi
from batch import module as bt_module
import pandas_ta as ta
logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")

# TODO: This system going to be ploted by Chart.js (project.com)

def plot_indicator(strategy):

    os.makedirs(f"{working_dir}/static/TEMP/", exist_ok=True)

    df_param = pd.read_csv(f"/home/username/project/static/TEST/DeviL/202211110706/BTCUSDT.csv")

    symbol  = df_param["symbol"][0] 
    atr     = df_param["atr"][0] 
    trueRange      = df_param["trueRange"][0] 
    coreLine    = df_param["coreLine"][0] 
    trendLine   = df_param["trendLine"][0] 

    print(f"target -> {symbol}")

    df_kline = bt_module.kline(symbol, 2, 1)
    df_kline = Devi.create_df(df_kline, atr, coreLine, trueRange, trendLine, trading=True)
    
    show_range = int(100)

    x_opentime_data = df_kline['opentime_data'].tail(show_range)
    y_close = df_kline['close'].tail(show_range)
    y_trendLine = df_kline['trendLine'].tail(show_range)
    y_upper = df_kline['Upper'].tail(show_range)
    y_lower = df_kline['lower'].tail(show_range)
    y_coreLine  = df_kline['coreLine'].tail(show_range)

    fig = plt.figure(figsize=(25, 7), dpi=72)
    fig.suptitle(f'test indi', fontsize=13)

    ax = fig.add_subplot(111)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.plot(x_opentime_data,y_close, marker="o", label="close")
    ax.plot(x_opentime_data,y_trendLine, marker="o", label="trendLine")
    ax.plot(x_opentime_data,y_upper, marker="o", label="upper")
    ax.plot(x_opentime_data,y_lower, marker="o", label="lower")
    ax.plot(x_opentime_data,y_coreLine, marker="o", label="coreLine")

    ax.legend(loc = 'lower left') 

    ax.set_title(symbol, fontsize=10)

    plt.gcf().autofmt_xdate()

    plt.autoscale(enable=True, axis='both', tight=False)    

    plt.savefig(f"{strategy}_{symbol}.png", dpi = 72)

    # plt.clf()
    # plt.close()


if __name__ =="__main__":
    strategy = "DeviL"
    plot_indicator(strategy)