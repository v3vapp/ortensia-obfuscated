
import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
import joblib as job
from tqdm import tqdm
from strategy.Devi import Devi_backtest
from strategy.Rsix import rsiBacktest
import numpy as np
import module
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)
warnings.filterwarnings('ignore')
#______________________________________________________________________________________________________________________________
    

def param2(worker, strategy, df_kline, stage):

    def single_backtest(df_kline, param1, param2):
        list_params = [param1, param2]
        entrytime_datas, exitTime_datas, list_netp, list_paperLoss, unfinishedProfit, sample_size = \
                rsiBacktest.run(df_kline.copy(), strategy, param1, param2)
        return list_params, unfinishedProfit, list_netp, list_paperLoss, sample_size, entrytime_datas, exitTime_datas
    
    if strategy == "RsiL" or strategy == "RsiS":
        param1_min, param1_max, param1_cut = rsiBacktest.param1_min, rsiBacktest.param1_max, rsiBacktest.param1_cut 
        param2_min, param2_max, param2_cut = rsiBacktest.param2_SHORT_min, rsiBacktest.param2_SHORT_max, rsiBacktest.param2_SHORT_cut 

    if stage == "DEBUG":
        param1_cut, param2_cut = 4,4

    backtest_result = job.Parallel(n_jobs=worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, param1, param2)\
                        for param1 in tqdm(param1Range(param1_min, param1_max, param1_cut))\
                        for param2 in param2Range(param2_min, param2_max, param2_cut))
    return backtest_result

#______________________________________________________________________________________________________________________________


def param3(worker, strategy, df_kline, stage):

    def single_backtest(df_kline, param1, param2, param3):
        list_params = [param1, param2, param3]
        unfinishedProfit, list_netp, list_paperLoss, sample_size, entrytime_datas, exitTime_datas = \
                rsiBacktest.run(df_kline.copy(), strategy, param1, param2, param3)
        return list_params, unfinishedProfit, list_netp, list_paperLoss, sample_size, entrytime_datas, exitTime_datas

    if strategy == "RsiL" or strategy == "RsiS":
        
        param1_min, param1_max, param1_cut = rsiBacktest.param1_min, rsiBacktest.param1_max, rsiBacktest.param1_cut 

        if strategy == "RsiL":
            param2_min, param2_max, param2_cut = rsiBacktest.param2_LONG_min, rsiBacktest.param2_LONG_max, rsiBacktest.param2_LONG_cut 
        if strategy == "RsiS":
            param2_min, param2_max, param2_cut = rsiBacktest.param2_SHORT_min, rsiBacktest.param2_SHORT_max, rsiBacktest.param2_SHORT_cut 

        param3_min, param3_max, param3_cut = rsiBacktest.param3_min , rsiBacktest.param3_max, rsiBacktest.param3_cut 

    if stage == "DEBUG":
        param1_cut, param2_cut, param3_cut = 4,4,4
    if stage == "TEST":
        param1_cut, param2_cut, param3_cut = 8,8,8

    backtest_result = job.Parallel(n_jobs=worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, param1, param2, param3)\
                        for param1 in tqdm(param1Range(param1_min, param1_max, param1_cut))\
                        for param2 in param2Range(param2_min, param2_max, param2_cut)\
                        for param3 in param3Range(param3_min, param3_max, param3_cut))

    return backtest_result

#______________________________________________________________________________________________________________________________


def param4(worker, strategy, df_kline, stage):

    def single_backtest(df_kline, param1, param2, param3, param4):
        list_params = [param1, param2, param3, param4]
        unfinishedProfit, list_netp, list_paperLoss, sample_size, entrytime_datas, exitTime_datas = \
            Devi_backtest.run(df_kline.copy(), strategy, param1, param2, param3, param4)
        return list_params, unfinishedProfit, list_netp, list_paperLoss, sample_size, entrytime_datas, exitTime_datas
    
    if strategy == "DeviL" or strategy == "DeviS":
        param1_min, param1_max, param1_cut = Devi_backtest.param1_min,  Devi_backtest.param1_max, Devi_backtest.param1_cut # atr
        param2_min, param2_max, param2_cut = Devi_backtest.param2_min,  Devi_backtest.param2_max, Devi_backtest.param2_cut # coreLine
        param3_min, param3_max, param3_cut = Devi_backtest.param3_min , Devi_backtest.param3_max, Devi_backtest.param3_cut # trueRange
        param4_min, param4_max, param4_cut = Devi_backtest.param4_min,  Devi_backtest.param4_max, Devi_backtest.param4_cut # trendLine
    
    if stage == "DEBUG":
        param1_cut, param2_cut, param3_cut, param4_cut = 4,4,4,4

    backtest_result = job.Parallel(n_jobs=worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, param1, param2, param3, param4)\
                        for param1 in tqdm(param1Range(param1_min, param1_max, param1_cut))\
                        for param2 in param2Range(param2_min, param2_max, param2_cut)\
                        for param3 in param3Range(param3_min, param3_max, param3_cut)\
                        for param4 in param4Range(param4_min, param4_max, param4_cut))

    return backtest_result


#__________________________________________________________________

def param1Range(param1_min, param1_max, param1_cut):
    param1_step  = int((param1_max - param1_min) /param1_cut)
    range_param1 = np.arange(param1_min, param1_max+1, param1_step)
    return range_param1

def param2Range(param2_min, param2_max, param2_cut):
    param2_step  = int((param2_max - param2_min) /param2_cut)
    range_param2 = np.arange(param2_min, param2_max+1, param2_step)
    return range_param2

def param3Range(param3_min, param3_max, param3_cut):
    param3_step  = int((param3_max - param3_min) /param3_cut)
    range_param3 = np.arange(param3_min, param3_max+1, param3_step)
    return range_param3

def param4Range(param4_min, param4_max, param4_cut):
    param4_step = int((param4_max - param4_min) / param4_cut)
    range_param4 = np.arange(param4_min, param4_max+1, param4_step)
    return range_param4