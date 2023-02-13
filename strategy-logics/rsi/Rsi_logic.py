
import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))

from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)
"""
------------------------------- LONG ---------------------------------
"""
def long_entry(rsi, rsiLast, rsiLongEntry, rsiExit, trading = True, backtestPyramiding = False):
    #log.warning(f"{rsi},{rsiLast},{rsiLongEntry}")
    try:
        entryCond      = rsi      < rsiLongEntry
        lastEntryCond = rsiLast < rsiLongEntry
        doNotEntryCond = rsiLongEntry >= rsiExit #if entry is worth than exit. this is exceptional.

        if trading == True:
            if entryCond and not lastEntryCond and not doNotEntryCond:
                return True

        # backtest mode
        elif trading == False:
            if entryCond and not lastEntryCond and not doNotEntryCond and backtestPyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL ENTRY Logic -> {e}")

#___________________________________________________________________________

def long_exit(rsi, rsiExit, trading = True, backtestPyramiding = False):
    try:
        exitCond = rsi > rsiExit

        if trading == True:
            if exitCond:
                return True

        # backtest mode
        elif trading == False:
            if exitCond and backtestPyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL EXIT Logic -> {e}")

"""
------------------------------- SHORT ---------------------------------
"""

def SHORT_ENTRY(rsi, rsiLast, rsiShortEntry, rsiExit, trading = True, backtestPyramiding = 0):
    try:
        entryCond      = rsi > rsiShortEntry 
        lastEntryCond  = rsiLast > rsiShortEntry 
        doNotEntryCond = rsiShortEntry <= rsiExit

        if trading == True:
            if entryCond and not lastEntryCond and not doNotEntryCond:
                return True

        # backtest mode
        elif trading == False:
            if entryCond and not lastEntryCond  and not doNotEntryCond and backtestPyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiS ENTRY Logic -> {e}")
#___________________________________________________________________________

def shortExit(rsi, rsiExit, trading = True, backtestPyramiding = 0):
    try:
        exitCond = rsi < rsiExit

        if trading == True:
            if exitCond:
                return True

        # backtest mode
        elif trading == False:
            if exitCond and backtestPyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiS EXIT Logic -> {e}")



# ____________________________________________________________________________________________
# ____________________________________________________________________________________________

# test
if __name__ == "__main__":

    rsi         = 30
    rsiLast    = 50
    rsiLongEntry   = 40
    trading     = False
    backtestPyramiding = 0

    entry = long_entry(rsi, rsiLast, rsiLongEntry, trading, backtestPyramiding)

    print(f"entry is ... {entry}")
    #______________________________

    rsi         = 50
    rsiExit    = 40
    backtestPyramiding = 1

    exit = long_exit(rsi, rsiExit, trading, backtestPyramiding)

    print(f"exit is ... {exit}")