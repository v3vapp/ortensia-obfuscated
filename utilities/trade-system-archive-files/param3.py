
import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
import joblib as job
from tqdm import tqdm
import param_range
from strategy.Rsix import rsiBacktest
import module

from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)


def run(worker, symbol, strategy, df_origin, days, start, end, stage):

    def single_backtest(df_origin, param1, param2=False, param3=False,):

        list_params = [param1,param2, param3]

        entrytime_datas, exitTime_datas, list_netp, list_paperLoss, unfinishedProfit, sample_size = \
                rsiBacktest.run(df_origin.copy(), strategy, param1, param2, param3)

        return list_params, unfinishedProfit, list_netp, list_paperLoss, sample_size, entrytime_datas, exitTime_datas
    #______________________________________________________________________________________________________________________________
    
    # preset params
    if strategy == "RsiL" or strategy == "RsiS":
        
        param1_min, param1_max, param1_cut = rsiBacktest.param1_min, rsiBacktest.param1_max, rsiBacktest.param1_cut 

        if strategy == "RsiL":
            param2_min, param2_max, param2_cut = rsiBacktest.param2_LONG_min, rsiBacktest.param2_LONG_max, rsiBacktest.param2_LONG_cut 
        if strategy == "RsiS":
            param2_min, param2_max, param2_cut = rsiBacktest.param2_SHORT_min, rsiBacktest.param2_SHORT_max, rsiBacktest.param2_SHORT_cut 

        param3_min, param3_max, param3_cut = rsiBacktest.param3_min , rsiBacktest.param3_max, rsiBacktest.param3_cut 

    if stage == "DEBUG":
        param1_cut, param2_cut, param3_cut = 4,4,4
    #_______________________________________________________________________________________________________________________________

    list_range_1st, list_step   = create_range_1st( param1_min, param1_max, param1_cut,\
                                                    param2_min, param2_max, param2_cut,\
                                                    param3_min, param3_max, param3_cut)
    
    backtestResultData_1st      = param_job(worker, single_backtest, df_origin, list_range_1st)

    df_backtestResult_1st       = module.create_backtest_result_df(backtestResultData_1st)

    # 2nd stage
    # list_range_2nd              = create_range_2nd(df_backtestResult_1st,   list_step[0], int(param1_cut/2),\
    #                                                                         list_step[1], int(param2_cut/2),\
    #                                                                         list_step[2], int(param3_cut/2))

    # backtestResultData_2nd      = param_job(worker, single_backtest, df_origin, list_range_2nd)

    # df_backtestResult_2nd       = module.create_backtest_result_df(backtestResultData_2nd)

    df_backtestResult           = module.create_df_backtest( symbol, strategy, days, start, end, df_backtestResult_1st)

    return df_backtestResult
#________________________________________________________________________________________________________________________________________________

def param_job(worker, single_backtest, df_origin, list_range):

    range_param1 = list_range[0]
    range_param2 = list_range[1]
    range_param3 = list_range[2]

    result = job.Parallel(n_jobs=worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_origin, param1, param2, param3)\
                        for param1 in tqdm(range_param1)\
                        for param2 in range_param2\
                        for param3 in range_param3)
    return result
#_______________________________________________________________________________________________________________________________________________

def create_range_1st(   param1_min, param1_max, param1_cut,\
                        param2_min, param2_max, param2_cut,\
                        param3_min, param3_max, param3_cut):

    param1Range, param1_step = param_range.param1Range(param1_min, param1_max, param1_cut)
    param2Range, param2_step = param_range.param2Range(param2_min, param2_max, param2_cut)
    param3Range, param3_step = param_range.param3Range(param3_min, param3_max, param3_cut)

    list_range = [param1Range, param2Range, param3Range]
    list_step = [param1_step, param2_step, param3_step]

    return list_range, list_step

#___________________________________________________________________________

def create_range_2nd(df_result,\
                    param1_step_1st, param1_cut_2nd,\
                    param2_step_1st, param2_cut_2nd,\
                    param3_step_1st, param3_cut_2nd):

    list_BEST_Params_1st = param_range.create_BEST_params_list(df_result)

    param1Range_2nd = param_range.best_param1Range(param1_step_1st, list_BEST_Params_1st[0], param1_cut_2nd)
    param2Range_2nd = param_range.best_param2Range(param2_step_1st, list_BEST_Params_1st[1], param2_cut_2nd)
    param3Range_2nd = param_range.best_param3Range(param3_step_1st, list_BEST_Params_1st[2], param3_cut_2nd)

    list_range_2nd = [param1Range_2nd, param2Range_2nd, param3Range_2nd]
    
    return list_range_2nd

