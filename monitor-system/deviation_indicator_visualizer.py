import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent  
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import os
import matplotlib.pyplot as plt
import pandas as pd
from pandas import time_datastamp # Don't remove
import numpy as np
import time, logging
from strategy import DeviL

logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")

# TODO: This system going to be ploted by Chart.js (project.com)

def plot_indicator(strategy):

    os.makedirs(f"{working_dir}/static/indicator/", exist_ok=True)

    try:
        df_useme = pd.read_csv(f"{working_dir}/static/indicator/latest.csv")

        row_count, col_count = df_useme.shape    

        ncol = 1
        nrow = int(np.ceil(row_count/ncol))

        print(f"ncol = {ncol}, nrow = {nrow}")
        plt.figure(figsize=(30,180))

        for i, (row) in enumerate(df_useme.iterrows()):

            print(f"{i} / {row_count}")
            print("into the loop")

            symbol  = df_useme["tickerSymbol"][i] 
            atr     = df_useme["atr"][i] 
            tr      = df_useme["trueRange"][i] 
            coreLine    = df_useme["coreLine"][i] 
            trendLine   = df_useme["trendLine"][i] 

            print(f"target -> {symbol}")

            df = pd.read_csv(f"remorder/stream_db/{symbol}.csv")

            df = DeviL.create_df(df, tr, atr, trendLine, coreLine)
            
            show_range = int(1440*3)

            df['opentime_data'] = df['opentime_data']/1000
            df['opentime_data'] = pd.to_time(df['opentime_data'].astype(int), unit='s')

            x_opentime_data = df['opentime_data'].tail(show_range)
            y_close = df['close'].tail(show_range)
            y_trendLine = df['trendLine'].tail(show_range)
            y_upper = df['Upper'].tail(show_range)
            y_lower = df['lower'].tail(show_range)
            y_coreLine  = df['coreLine'].tail(show_range)

            plt.plot(x_opentime_data,y_close)
            plt.plot(x_opentime_data,y_trendLine)
            plt.plot(x_opentime_data,y_upper)
            plt.plot(x_opentime_data,y_lower)
            plt.plot(x_opentime_data,y_coreLine)

            #plt.legend(loc = 'lower right') 

            plt.title(symbol)

            plt.gcf().autofmt_xdate()

            plt.autoscale(enable=True, axis='both', tight=False)    

            plt.savefig(f"remorder/stream_db/indicator/{symbol}.png", dpi = 50)

            plt.clf()
            plt.close()
    except:
        logging.info("chart has created.")
        pass

if __name__ =="__main__":
    strategy = "Diviation_Long"
    plot_indicator(strategy)