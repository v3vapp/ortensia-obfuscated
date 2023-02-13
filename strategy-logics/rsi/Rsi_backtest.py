import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
import Rsi_dataframe, Rsi_logic
from benchmark import module as backtest_module
import numpy as np
import joblib as job
import warnings
warnings.simplefilter('ignore', FutureWarning)
warnings.filterwarnings('ignore')

# rsiLength
param1_min,param1_max,param1_cut = 10,30,20
# RSI_ENTRY_LONG
param2_LONG_min,param2_LONG_max,param2_LONG_cut = 20,40,20
# RSI_ENTRY_SHORT
param2_SHORT_min,param2_SHORT_max,param2_SHORT_cut = 60,80,20
# RSI_EXIT_
param3_min,param3_max,param3_cut = 40,60,20
#____________________________________________________________________________________________________________

def run(df_kline, timeFrame, strategy, input_rsiLength, input_rsiEntry, input_rsiExit):

    df = Rsi_dataframe.run(df_kline, timeFrame, input_rsiLength,  False)
    side = list(strategy)[-1] 

    indexLen   = len(df)
    data_openTime = df["openTime"].tolist()
    data_close = df["close"].tolist()
    dataHigh  = df["high"].tolist()
    dataLow   = df["low"].tolist()
    data_RSI   = df["rsi"].tolist()

    entryPrice = df_counter = backtestPyramiding = unfinishedProfit = indexEntry = indexExit = 0 

    list_netp      = []
    entryTimes     = []
    exitTimes      = []
    list_paperLoss = []

    for index in np.arange(indexLen):
        close    = data_close[index]
        time     = int(data_openTime[index])
        rsi      = data_RSI[index]
        last_rsi = data_RSI[index-1]

        if side == "L":
            if Rsi_logic.long_entry(rsi, last_rsi, input_rsiEntry, input_rsiExit, False, backtestPyramiding):

                indexEntry, entryPrice, backtestPyramiding, entryTimes, time = \
                backtest_module.func_backtest_entry(index, close, 1, entryTimes, time)

            if Rsi_logic.long_exit(rsi, input_rsiExit, False, backtestPyramiding):

                indexExit,exitPrice,backtestPyramiding,list_netp,exitTimes,list_paperLoss = \
                backtest_module.func_backtest_exit(\
                side, index, close, 0, list_netp,exitTimes,list_paperLoss,time,entryPrice,indexEntry, indexExit,dataHigh,dataLow)

        if side == "S":
            if Rsi_logic.SHORT_ENTRY(rsi, last_rsi, input_rsiEntry, input_rsiExit, False, backtestPyramiding):

                indexEntry, entryPrice, backtestPyramiding, entryTimes, time = \
                backtest_module.func_backtest_entry(index, close, 1, entryTimes, time)

            if Rsi_logic.shortExit(rsi, input_rsiExit, False, backtestPyramiding):

                indexExit,exitPrice,backtestPyramiding,list_netp,exitTimes,list_paperLoss = \
                backtest_module.func_backtest_exit(\
                side, index, close, 0,list_netp,exitTimes,list_paperLoss,time,entryPrice,indexEntry, indexExit,dataHigh,dataLow)

        if df_counter == df["close"].count()-1 and backtestPyramiding > 0:
            exitPrice = close
            backtestPyramiding = 0
            unfinishedProfit = round(((exitPrice/entryPrice - 1)*100),2)

        df_counter += 1

    return unfinishedProfit, list_netp, list_paperLoss, entryTimes, exitTimes
#____________________________________________________________________________________________________________

def batch(worker, strategy, df_kline, timeFrame, stage):

    def single_backtest(df_kline, timeFrame, param1, param2, param3):
        
        list_params = [param1, param2, param3]
        unfinishedProfit, list_netp, list_paperLoss, entryTimes, exitTimes = \
                run(df_kline.copy(), timeFrame, strategy, param1, param2, param3)

        return list_params, unfinishedProfit, list_netp, list_paperLoss, entryTimes, exitTimes

    if strategy == "RsiL":
        param2_min, param2_max, param2_cut = param2_LONG_min, param2_LONG_max, param2_LONG_cut 
    if strategy == "RsiS":
        param2_min, param2_max, param2_cut = param2_SHORT_min, param2_SHORT_max, param2_SHORT_cut 

    if stage == "DEBUG":
        param1_cut, param2_cut, param3_cut = 6,6,6
    if stage == "TEST":
        param1_cut, param2_cut, param3_cut = 8,8,8

    backtest_result = job.Parallel(n_jobs=worker, verbose=5)\
                        (job.delayed(single_backtest)\
                        (df_kline, timeFrame, param1, param2, param3)\
                        for param1 in backtest_module.param1Range(param1_min, param1_max, param1_cut)\
                        for param2 in backtest_module.param2Range(param2_min, param2_max, param2_cut)\
                        for param3 in backtest_module.param3Range(param3_min, param3_max, param3_cut))

    return backtest_result
#____________________________________________________________________________________________________________

if __name__ == "__main__":

    import pandas as pd

    df_kline = pd.read_csv(f"/home/username/project/static/SAMPLE/kline/kline1m_6h.csv")

    strategy = "RsiL"
    #strategy = "RsiS"

    if strategy == "RsiL":
        input_rsiEntry = 40

    if strategy == "RsiS":
        input_rsiEntry = 60

    input_rsiLength = 30
    input_rsiExit = 50

    data = run(df_kline, 5, strategy, input_rsiLength, input_rsiEntry, input_rsiExit)

    print(data)

    unfinishedProfit = data[0]
    list_netp = data[1]
    list_paperLoss = data[2]
    entryTimes = data[3]
    exitTimes = data[4]

    print(f"entryTimes {entryTimes}")
    print(f"exitTimes {exitTimes}")
    print(f"list_netp {list_netp}")
    print(f"list_paperLoss {list_paperLoss}")
    print(f"unfinishedProfit {unfinishedProfit}")
    