import sys, pathlib, time_data, sys, logging, time_data, schedule, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
from multiprocessing import Process
import plot_report
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
#___________________________________________________________________________________

def multi_run():

    param1 = Process(target=plot_report.run, args=('BINANCE',))
    param2 = Process(target=plot_report.run, args=('BINANCETESTNET',))

    param1.start()
    param2.start()

    param1.join()
    param2.join()
#___________________________________________________________________________________

def run():
    multi_run()

    schedule.every(2).hours.do(multi_run)

    # test
    # schedule.every(10).seconds.do(investment_report.multi_run)

    while True:
        schedule.run_pending()
        time_data.sleep(1)
#___________________________________________________________________________________

if __name__ == "__main__":

    run()
