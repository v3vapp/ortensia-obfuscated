import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
from config import pw
import inquirer, os
from google.api_coreLine import page_iterator
from google.cloud import storage 
from binance.client import Client

#____________________________________________________________________________________________________ 

def _item_to_value(iterator, item):
    return item

def backtest_sessions(bucket_name, prefix):
    if prefix and not prefix.endswith('/'):
        prefix += '/'

    extra_params = {
        "projection": "noAcl",
        "prefix": prefix,
        "delimiter": '/'}

    googleCloudStorage = storage.Client()

    path = "/b/" + bucket_name + "/o"

    iterator = page_iterator.HTTPIterator(
        client=googleCloudStorage,
        api_request=googleCloudStorage._connection.api_request,
        path=path,
        items_key='prefixes',
        item_to_value=_item_to_value,
        extra_params=extra_params,)

    dir_list_tmp = []

    for dir in iterator:
        dir = dir.replace(prefix,"").replace("/","")
        dir_list_tmp.append(dir)

    dir_list= []

    for dir in reversed(dir_list_tmp):
        dir_list.append(dir)

    return dir_list

#____________________________________________________________________________________________________ 

def run():
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{working_dir}/config/googleCloud_project.json"

    project_id  = "MarketStar"
    bucket_name = "project_bucket"
    bucket_client = storage.Client(project_id)
    bucket      = bucket_client.get_bucket(bucket_name)

    stage_questions  = [inquirer.List('stage', message="Which Stage?", choices=["DEBUG", "TEST",'PRODUCTION'],),]
    stage_answers    = inquirer.prompt(stage_questions)
    stage            = stage_answers["stage"]

    # TODO:
    list_strategy = ["DeviL", "DeviS", "RsiL", "RsiS"]

    strategy_questions = [inquirer.List('strategy', message="Which strategy?", choices=list_strategy,),]
    strategy_answers   = inquirer.prompt(strategy_questions)
    strategy           = strategy_answers["strategy"]

    # Fetch Backtest sessions from googleCloudStorage bucket #
    prefix = f'{stage}/{strategy}'

    session_list = backtest_sessions(bucket_name, prefix)

    session_questions = [inquirer.List('session', message="Which session?", choices=session_list,),]
    session_answers   = inquirer.prompt(session_questions)
    sessiontime_data       = session_answers["session"]

    exchangeID_questions = [inquirer.List('exchangeID', message="Which Exchange?", choices=["BINANCETESTNET", "BINANCE"],),]
    exchangeID_answers   = inquirer.prompt(exchangeID_questions)
    exchangeID           = exchangeID_answers["exchangeID"]

    candletime_dataFrame_questions = [inquirer.List('candletime_dataFrame', message="Which candletime_dataFrame?", choices=["1m", "5m", "15m"],),]
    candletime_dataFrame_answers   = inquirer.prompt(candletime_dataFrame_questions)
    candletime_dataFrame           = candletime_dataFrame_answers["candletime_dataFrame"]

    session = f"{strategy}_{sessiontime_data}"

    if exchangeID == "BINANCE":
        exchangeClient = Client(pw.binance_api_key, pw.binance_api_secret)

    elif exchangeID == "BINANCETESTNET":
        exchangeClient = Client(pw.test_binance_api_key, pw.test_binance_api_secret, {"time_dataout": 10}, testnet = True)

    #_____________________________________________
    return strategy, sessiontime_data, session, bucket_name, bucket_client, bucket, stage, exchangeID, candletime_dataFrame, exchangeClient

#____________________________________________________________________________________________________ 

if __name__ == "__main__": 

    sessionInfo = run()

    print(sessionInfo)

    strategy    = sessionInfo[0]
    sessiontime_data = sessionInfo[1]
    session     = sessionInfo[2]
    bucket_name =  sessionInfo[3]
    bucket_client = sessionInfo[4]
    bucket      = sessionInfo[5]
    stage       = sessionInfo[6]
    exchangeID  =  sessionInfo[7]
    candletime_dataFrame =  sessionInfo[8]
    exchangeClient  = sessionInfo[9]

    print(f"{sessionInfo[6]}, {sessionInfo[2]}")