import sys, pathlib, time, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
sys.path.append(f"{str(working_dir)}/tools")
import vm, discorder

logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")
#_____________________________________________________________________________________

def error(e, message):

    server = "error"
    embed_title = e

    logging.warning(e)
    try:
        discorder.send(message, embed_title, server = server)
    except Exception as e:
        logging.warning(f"Error. sending Discort ERROR report -> {e}")
#_____________________________________________________________________________________

def backtest(info_type, discord_server, list_symbol, list_strategy, time_datar_symbol, time_datar_strategy, time_datar_global,\
                symbol, strategy, activationtime_data, symbol_counter, strategy_counter, total_backtest_counter):

    session = f"{strategy}{activationtime_data}"

    elapse_symbol = round((time.time() - time_datar_symbol)/60,1)
    elapse_strategy = round((time.time() - time_datar_strategy)/60,1)
    elapse_global = round((time.time() - time_datar_global)/60,1)

    len_list_strategy = int(len(list_strategy))
    len_list_symbol = int(len(list_symbol))

    total_backtest = len_list_strategy* len_list_symbol

    symbols_left = len_list_symbol - symbol_counter
    average_singele_backtest_time_data = elapse_strategy/symbol_counter

    estimation_min = float(round(symbols_left * average_singele_backtest_time_data,1))
    estimation_hour = round(estimation_min/60,1)

    if info_type == "symbol":
        server = discord_server
        title = f"Finished -> {symbol}/{strategy}"

        embed_description = f"Progress(symbol): {symbol_counter}/{len_list_symbol}\n\
        Progress(strategy): {strategy_counter}/{len_list_strategy}\n\
        Progress(Total): {total_backtest_counter}/{total_backtest}\n\
        Elapsed (symbol), {symbol}, {elapse_symbol} min.\n\
        Elapsed (strategy), {strategy}, {elapse_strategy} min.\n\
        Elapsed (Total), {elapse_global}min.\n\
        Estimation(strategy), {estimation_min}min ({estimation_hour}/h) to Finish {strategy}."

    elif info_type == "strategy":
        server = discord_server
        title = f"Finished --->>> {strategy} <<---"

        embed_description = f"Progress(strategy): {strategy_counter}/{len_list_strategy}\n\
        Progress(Total): {total_backtest_counter}/{total_backtest}\n\
        Elapsed (strategy), {strategy}, {elapse_strategy} min.\n\
        Elapsed (Total), {elapse_global}min.\n\
        strategy List ->\n\
        {list_strategy}\n\
        symbol List ->\n\
        {list_symbol}"

    logging.info(embed_description)
    
    try:
        discorder.send(title, session, embed_description, username = vm.googleCloud_instance, server = server)
    except Exception as e:
        logging.warning(f"Error. sending backtest report -> {e}")
#_____________________________________________________________________________________

def upload_googleCloudStorage(exchangeName = "exchangeName Unknown"):

    server = "googleCloudStorage"
    message = f"Success Upload to googleCloudStorage -> {exchangeName}"

    logging.info(message)

    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending upload_googleCloudStorage report for {exchangeName} -> {e}")

#_____________________________________________________________________________________

def new_account_data(exchangeName):

    server = "database"
    message = f"Success new position/balance data -> {exchangeName}"
    logging.info(message)
    
    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending new_account_data report for {exchangeName} -> {e}")

#_____________________________________________________________________________________

def account(exchangeName, file_path, debug):

    if debug == False:
        
        if exchangeName == "BINANCE":        
            server = "binance_report"

        elif exchangeName == "BINANCETESTNET":
            server = "binancetestnet_report"
    else:
        server = "debug"

    message = f"New report arrived for {exchangeName}!"

    logging.info(f"New report for {exchangeName}")

    try:
        discorder.send(file_path = file_path, server = server)
    except Exception as e:
        logging.warning(f"Error. sending investment report for {exchangeName} -> {e}")
#_____________________________________________________________________________________

def trade_system_log(message, debug = False):

    if debug == False:
        server = "trade_system_log"
    else:
        server = "trade_debug"

    logging.info(message)

    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending order report -> {e}")
#_____________________________________________________________________________________


def trade_system_error(message, debug = False):

    if debug == False:
        server = "trade_system_erorr"
    else:
        server = "trade_debug"

    logging.info(message)

    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending order report -> {e}")

#_____________________________________________________________________________________

def ORDER(message, embed_title, embed_description, debug = False):

    if debug == False:
        server = "order_message"
    else:
        server = "trade_debug"

    logging.info(message)
    logging.info(embed_title)
    logging.info(embed_description)

    try:

        # if detail == False:
        #     discorder.send(message, server = server)
        # else:
        discorder.send(message, embed_title, embed_description, server = server)

    except Exception as e:
        logging.warning(f"Error. sending order report -> {e}")



if __name__ == "__main__":
    import os

    exchangeName = "BINANCETESTNET"

    local_path = f"{working_dir}/static/TEMP"

    os.makedirs(local_path, exist_ok=True)
    file_path = f'{local_path}/report_{exchangeName}.png'

    account(exchangeName, file_path)