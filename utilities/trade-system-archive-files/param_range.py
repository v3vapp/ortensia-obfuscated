import numpy as np

def param1Range(param1_min, param1_max, param1_cut):
    param1_step  = int((param1_max - param1_min) /param1_cut)
    range_param1 = np.arange(param1_min, param1_max+1, param1_step)
    return range_param1, param1_step

def param2Range(param2_min, param2_max, param2_cut):
    param2_step  = int((param2_max - param2_min) /param2_cut)
    range_param2 = np.arange(param2_min, param2_max+1, param2_step)
    return range_param2, param2_step

def param3Range(param3_min, param3_max, param3_cut):
    param3_step  = int((param3_max - param3_min) /param3_cut)
    range_param3 = np.arange(param3_min, param3_max+1, param3_step)
    return range_param3, param3_step

def param4Range(param4_min, param4_max, param4_cut):
    param4_step = int((param4_max - param4_min) / param4_cut)
    range_param4 = np.arange(param4_min, param4_max+1, param4_step)
    return range_param4, param4_step
#____________________________________________________________

def create_BEST_params_list(df_result):
    # FIXME: 
    df_result = df_result.sort_values(by="GAIN_SUM", ascending=False)
    df_result.reset_index(drop=True, inplace=True)

    list_bestParams = df_result.loc[0,"params"]

    return list_bestParams
#____________________________________________________________

def best_param1Range(param1_step_1st, param1_BEST_1st, param1_cut_2nd):

    if param1_BEST_1st < param1_step_1st:
        param1_min_2nd = param1_BEST_1st
    else:
        param1_min_2nd = param1_BEST_1st - param1_step_1st

    param1_max_2nd   = param1_BEST_1st + param1_step_1st
    param1_step_2nd  = int((param1_max_2nd - param1_min_2nd)/param1_cut_2nd)
    param1Range_2nd = np.arange(param1_min_2nd, param1_max_2nd + 1, param1_step_2nd)

    return param1Range_2nd


def best_param2Range(param2_step_1st, param2_BEST_1st, param2_cut_2nd):

    if param2_BEST_1st < param2_step_1st:
        param2_min_2nd = param2_BEST_1st
    else:
        param2_min_2nd = param2_BEST_1st - param2_step_1st

    param2_max_2nd   = param2_BEST_1st + param2_step_1st
    param2_step_2nd  = int((param2_max_2nd - param2_min_2nd)/param2_cut_2nd)
    param2Range_2nd = np.arange(param2_min_2nd, param2_max_2nd + 1, param2_step_2nd)

    return param2Range_2nd


def best_param3Range(param3_step_1st, param3_BEST_1st, param3_cut_2nd):

    if param3_BEST_1st < param3_step_1st:
        param3_min_2nd = param3_BEST_1st
    else:
        param3_min_2nd = param3_BEST_1st - param3_step_1st

    param3_max_2nd   = param3_BEST_1st + param3_step_1st
    param3_step_2nd  = int((param3_max_2nd - param3_min_2nd)/param3_cut_2nd)
    param3Range_2nd = np.arange(param3_min_2nd, param3_max_2nd + 1, param3_step_2nd)

    return param3Range_2nd


def best_param4Range(param4_step_1st, param4_BEST_1st, param4_cut_2nd):

    if param4_BEST_1st < param4_step_1st:
        param4_min_2nd = param4_BEST_1st
    else:
        param4_min_2nd = param4_BEST_1st - param4_step_1st

    param4_max_2nd   = param4_BEST_1st + param4_step_1st
    param4_step_2nd  = int((param4_max_2nd - param4_min_2nd)/param4_cut_2nd)
    param4Range_2nd = np.arange(param4_min_2nd, param4_max_2nd + 1, param4_step_2nd)

    return param4Range_2nd