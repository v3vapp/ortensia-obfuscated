import time, sys, logging, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
import module, order
from timeout_decorator import timeout, TimeoutError
import schedule

from strategy.Devi import Devi_trading
from strategy.Rsix import Rsi_trading

from datetime import datetime, timedelta, time
import time
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

################################################################################
# LOGIC

def session_logic(exchangeClient, session, sessionPhase, exchangeID, candleTimeFrame, list_symbols):
    try:
        session_dead_list = []
        for symbol in list_symbols:
            try:
                params, df_kline_from_db = module.fetch_params_kline(session, symbol, exchangeID, candleTimeFrame)
                #______________________________________________________________________________________________
                # TODO: Devi / Rsi / ... add.
                if "DeviL_" in session or "DeviS_" in session:
                    entryLogic, exitLogic = Devi_trading.run(params, df_kline_from_db, session)
                    
                if "RsiL_" in session or "RsiS_" in session:
                    entryLogic, exitLogic = Rsi_trading.run(params, df_kline_from_db, session)
                #______________________________________________________________________________________________

                dead_or_alive = order.run(exchangeClient, symbol, session, sessionPhase, entryLogic, exitLogic)

                session_dead_list.append(dead_or_alive)            

                if all(session_dead_list) == True and len(session_dead_list) == len(list_symbols):
                    print(f"All symbols are Dead. Thus, This session {session} is going to die. good bye.")
                    quit()
                
            except Exception as e:
                log.warning(f"ERROR in strategy... {session} {symbol}... {e}")
                continue

        print(f"session Dead Count -> {session_dead_list.count(True)}/{len(list_symbols)}")

    except Exception as e:
        log.info(f"ERROR -> {e}")


################################################################################
# Alive & Dying session

sessionDays = 5
sessionInterval = 30

@timeout(sessionDays * 86400)
def alive_phase(exchangeClient, session, sessionPhase, exchangeID, candleTimeFrame, list_symbols):

    log.info(f"session starting @{session}")

    # Maybe, I dont want to trade every 10s. But It's fine. because, if contracts != 0, no entry anyway.
    schedule.every(sessionInterval).seconds.\
        do(session_logic, exchangeClient, session, sessionPhase, exchangeID, candleTimeFrame, list_symbols).\
        tag('scheduleTag_ALIVE')

    while True:
        schedule.run_pending()
        time.sleep(1)

def dying_phase(exchangeClient, session, sessionPhase, exchangeID, candleTimeFrame, list_symbols):

    log.info(f"Dying session starting @{session}")

    schedule.every(sessionInterval).seconds.\
        do(session_logic, exchangeClient, session, sessionPhase, exchangeID, candleTimeFrame, list_symbols).\
        tag('scheduleTag_DYING')
    
    while True:
        schedule.run_pending()
        time.sleep(1)

################################################################################
# Combine and make it work! 

def run(exchangeClient, session, exchangeID, candleTimeFrame, list_symbols):

    alive = True

    try:
        alive_phase(exchangeClient, session, alive, exchangeID, candleTimeFrame, list_symbols)
    # Need timeout exception to timeout Alive-phase properly.
    except TimeoutError:
        log.info("Alive Phase is Timeout")

    # Quit Alive schedule. Without this code, alive-phase remains on dying phase.
    schedule.clear('scheduleTag_ALIVE')

    alive = False
    
    dying_phase(exchangeClient, session, alive, exchangeID, candleTimeFrame, list_symbols)

#_______________________________________________________________________________________________________

# TEST RUN #
if __name__ == "__main__":

    import setup

    sessionInfo = setup.run()

    print(sessionInfo)

    strategy        = sessionInfo[0]
    sessionTime     = sessionInfo[1]
    session         = sessionInfo[2]
    bucket_name     = sessionInfo[3]
    bucket_client   = sessionInfo[4]
    bucket          = sessionInfo[5]
    stage           = sessionInfo[6]
    exchangeID      = sessionInfo[7]
    candleTimeFrame = sessionInfo[8]
    exchangeClient  = sessionInfo[9]

    list_symbols = ["BTCUSDT", "ETHUSDT"]

    run(exchangeClient, session, exchangeID, candleTimeFrame, list_symbols)









