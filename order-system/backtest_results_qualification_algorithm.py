import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import os, logging, sqlite3
import pandas as pd
from rich.logging import RichHandler
from google.cloud import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

def run(strategy, sessionTime, session, bucket_name, bucket_client, bucket, stage):

    result_columns = {  'params':[],
                        'UNFINISHED_profit':[],
                        'netProfit':[],
                        'RESULT_ASSET':[],
                        "PAPER_LOSS":[],
                        'SAMPLE_SIZE':[],
                        'ENTRY_TIMES':[],
                        'EXIT_TIMES':[]}

    df_qualify = pd.DataFrame(columns = result_columns)

    logging.info("Going to qualify. Please wait.")

    for file in bucket_client.list_blobs(bucket_name):

        if ".csv" in file.name and f"{stage}" in file.name and f"{strategy}" in file.name and f"{sessionTime}" in file.name:
        
            df_result = pd.read_csv(f'gs://{bucket_name}/{file.name}')

            # TODO: Qual Params
            require_trade_freq_days = 3 # once in X days
            maxAllow_unfinished_profit = -8 # %

            # Setting Require SmapleSize
            backtested_total_days = df_result["DAYS"][0]
            require_SampleSize = int(backtested_total_days/require_trade_freq_days)

            try:
                df_result = df_result.sort_values(by="RESULT_ASSET", ascending=False)
                df_result.drop(df_result.loc[df_result['RESULT_ASSET']<= 100].index, inplace=True)

                #_________________________________________________________________________________________________________
                # FIXME: Disabled for Testing

                df_result.drop(df_result.loc[df_result['UNFINISHED_profit']<= maxAllow_unfinished_profit].index, inplace=True)
                
                # df_result.drop(df_result.loc[df_result['SAMPLE_SIZE']<=require_SampleSize].index, inplace=True)
                #__________________________________________________________________________________________________________

                df_result.reset_index(drop=True, inplace=True)
                df_s       = df_result.iloc[0]
                df_temp    = pd.DataFrame(df_s).T
                df_qualify = pd.concat([df_qualify, df_temp], axis=0)
                log.info(f"OK. {file.name}")
                
            except Exception as e:
                log.info(f"SKIP. {file.name}. reason -> {e}")
                continue

    # Top 10 Conditions
    df_qualify = df_qualify.sort_values('RESULT_ASSET', ascending = False)
    df_qualify.reset_index(drop = True, inplace = True)

    # YOU MUST WRITE & RE CSV THEN "TO_SQL". Otherwise, Data will be Blob in DB.
    session = f"{strategy}_{sessionTime}"

    os.makedirs(f"{working_dir}/static/QUALIFY", exist_ok=True)

    df_qualify.to_csv(f"{working_dir}/static/QUALIFY/{session}.csv", index=False)

    df_qualify = pd.read_csv(f"{working_dir}/static/QUALIFY/{session}.csv")
    # _______________________________________________________________________________
    # Insert to test.db
    
    con = sqlite3.connect(f"{outside_dir}/test.db")

    df_qualify.to_sql(f'{session}', con, if_exists='replace', index = False)

    logging.info(f"Database Location @{outside_dir}")

    #---------------------------------------- UPLOAD ----------------------------------------------------------

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"./config/googleCloud_project.json"
    
    client_storage = storage.Client()
    
    bucket_name = "project_bucket"
    
    bucket = client_storage.get_bucket(bucket_name)

    googleCloudStorage_path = f'QUALIFY/{session}.csv'
    local_path = f'{working_dir}/static/{googleCloudStorage_path}'
    
    df_qualify.to_csv(local_path, index=False)
    
    blob_data = bucket.blob(googleCloudStorage_path)
    
    blob_data.upload_from_filename(local_path)
    
    logging.info(f"Successfully Uploaded QUALIFY Result -> {local_path}")

    list_symbols = fetch_symbols(session)

    return list_symbols


#==================================================================
# list_symbols Exracted

def fetch_symbols(session):

    connection = sqlite3.connect(f"{outside_dir}/test.db")

    connection.row_factory = lambda cursor, row: row[0]

    c = connection.cursor()

    sql = f"SELECT SYMBOL FROM {session}"
    c.execute(sql)

    list_symbols = c.fetchall()

    return list_symbols

# TEST #

if __name__ == "__main__": 

    import setup

    sessionInfo = setup.run()

    session = sessionInfo[2]

    run(sessionInfo[0], sessionInfo[1], session, sessionInfo[3], sessionInfo[4], sessionInfo[5], sessionInfo[6])

    list_symbols = fetch_symbols(session)

    print(list_symbols)