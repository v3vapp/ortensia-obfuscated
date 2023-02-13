import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
import setup, qualify, kline, stream, session
import multiprocessing
import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")


def run(exchangeClient, session, exchangeID, candletime_dataFrame, list_symbols):
    try:
        id_0 = multiprocessing.Process(name="", target=kline.run,   args=(session, exchangeID, candletime_dataFrame, list_symbols))
        id_1 = multiprocessing.Process(name="", target=stream.run,  args=(session, exchangeID, candletime_dataFrame, list_symbols))
        id_2 = multiprocessing.Process(name="", target=session.run, args=(exchangeClient, session, exchangeID, candletime_dataFrame, list_symbols))
        id_0.start()
        id_1.start()
        id_2.start()
    except Exception as e:
        logging.warning(e)


if __name__ == "__main__":

    strategy, sessiontime_data, session, bucket_name, bucket_client,\
    bucket, stage, exchangeID, candletime_dataFrame, exchangeClient = setup.run()

    list_symbols = qualify.run(strategy, sessiontime_data, session, bucket_name, bucket_client, bucket, stage)

    run(exchangeClient, session, exchangeID, candletime_dataFrame, list_symbols)




