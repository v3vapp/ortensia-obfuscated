
import sys, pathlib, logging, warnings
warnings.simplefilter('ignore', FutureWarning)
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/trade")
import Rsi_dataframe, Rsi_logic

#__________________________________________________________________________

def run(params, df_kline_from_db, session, testmode = False):

    RSI_LENGTH = params[0]
    RSI_ENTRY  = params[1]
    rsiExit   = params[2]

    df_Rsi = Rsi_dataframe.run(df_kline_from_db, RSI_LENGTH)

    rsi      = df_Rsi['rsi'].iloc[-1]
    last_rsi = df_Rsi['rsi'].iloc[-2]

    if "RsiL" in session:
        if Rsi_logic.long_entry(rsi, last_rsi, RSI_ENTRY):
            entryLogic = True
        else:
            entryLogic = False

        if Rsi_logic.long_exit(rsi, rsiExit):
            exitLogic = True
        else:
            exitLogic = False

    if "RsiS" in session:
        if Rsi_logic.SHORT_ENTRY(rsi, last_rsi, RSI_ENTRY):
            entryLogic = True
        else:
            entryLogic = False

        if Rsi_logic.shortExit(rsi, rsiExit):
            exitLogic = True
        else:
            exitLogic = False
    
    if testmode == True:
        # FIXME: TEST ENTRY
        entryLogic = True
        exitLogic = False  

    return entryLogic, exitLogic

#_________________________________________

if __name__ == "__main__":

    from trade import setup

    sessionInfo = setup.run()

    strategy        = sessionInfo[0]
    sessiontime_data     = sessionInfo[1]
    session         = sessionInfo[2]
    bucket_name     = sessionInfo[3]
    bucket_client   = sessionInfo[4]
    bucket          = sessionInfo[5]
    stage           = sessionInfo[6]
    exchangeID      = sessionInfo[7]
    candletime_dataFrame = sessionInfo[8]
    exchangeClient  = sessionInfo[9]

    # run(params, df_kline_from_db, session, testmode = False)