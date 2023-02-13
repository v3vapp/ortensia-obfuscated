import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent  
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")

import matplotlib.pyplot as plt
import pandas as pd
from pandas import time_datastamp # Don't remove
import numpy as np
import time, logging

logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")


def qualify_data(df, i):

    tickerSymbol          = df['tickerSymbol'][i]
    strategy        = df['strategy'][i]
    days            = df['days'][i]
    start           = df['start'][i]
    end             = df['end'][i]
    coreLine            = df['coreLine'][i]
    trueRange              = df['trueRange'][i]
    atr             = df['atr'][i]
    trendLine           = df['trendLine'][i]
    resultAsset     = df['resultAsset'][i]
    sampleSize      = df['sampleSize'][i]
    # winningRatio       = df['winningRatio'][i]
    # avgprofit       = df['avgprofit'][i]
    # avgLoss         = df['avgLoss'][i]
    # maxprofit       = df['maxprofit'][i]
    # maxLoss         = df['maxLoss'][i]
    unfinishedProfit = df['unfinishedProfit'][i]
    netProfit       = df['netProfit'][i]
    latentLoss      = df['latentLoss'][i]
    # entrytime_datas      = df['entrytime_datas'][i]
    exitTime_datas       = df['exitTime_datas'][i]

    # NET_profit_001を{eval}を使ってstringからlistにしている。次に{map}でリスト内のデータをすべて1/100する関数を適応させる。結果がmapオブジェクトの型で返されるのでlistに戻している。
    #if __name__ == "__main__": 

    netProfit_raw       = list(map(lambda x: x * 0.01, eval(netProfit)))
    netProfit           = list(eval(netProfit))

    latentLoss_raw       = list(map(lambda x: x * 0.01, eval(latentLoss)))
    latentLoss           = list(eval(latentLoss))

    exitTime_datas           = eval(exitTime_datas)
    #Long_or_Short       = eval(Long_or_Short)

    # else:
    #     netProfit_raw       = list(map(lambda x: x * 0.01, netProfit))
    #     netProfit           = list(netProfit)

    #     latentLoss_raw       = list(map(lambda x: x * 0.01, latentLoss))
    #     latentLoss           = list(latentLoss)

    exitTime_datas.insert(0, start) 
    list_netp   = [0]
    list_asset  = [100]
    list_latentLoss = [0]
    list_worst  = [100]
    list_trades = [0]
    #list_side   = ["None"]
    
    #profit = netProfit_raw
    trades = len(netProfit_raw)
    
    for trade, profit, result, bad, loss in zip(range(1,trades+1), netProfit_raw, netProfit, latentLoss_raw, latentLoss):

        asset = list_asset[-1]*(1 + profit)
        worst = list_asset[-1]*(1 + bad)

        list_asset  = np.append(list_asset,  asset)
        list_worst  = np.append(list_worst, worst)

        list_trades = np.append(list_trades, trade)
        #list_side   = np.append(list_side,   side)
        list_netp   = np.append(list_netp,   result)
        list_latentLoss = np.append(list_latentLoss, loss)

    now = time.time.now().strftime_data('%Y/%m/%d %H:%M')

    longColor = dict(facecolor="#2b6eff",
                edgecolor="#2b6eff",
                alpha=0.5,
                linewidth=2,
                linestyle="-")
    shortColor = dict(facecolor="#ff61ca",
                edgecolor="#ff61ca",
                alpha=0.5,
                linewidth=2,
                linestyle="-")
    latenLossColor = dict(facecolor="#420303",
                edgecolor="#420303",
                alpha=0.0,
                linewidth=2,
                linestyle="-")
    text_info = f"\n\
            sampleSize:   {sampleSize} tades\n\
            resultAsset:  $ {round(resultAsset,1)}\n\
            unfinished:    {round(unfinishedProfit,1)} %\n\
            \n\
            coreLine:         {round(coreLine,1)}\n\
            trueRange:          {round(trueRange,1)}\n\
            atr:          {round(atr,1)}\n\
            trendLine:         {round(trendLine,1)}\n"

    return tickerSymbol, strategy, days, exitTime_datas, list_netp, list_latentLoss, list_asset,\
        list_worst, list_trades, now, longColor, shortColor, latenLossColor, text_info


def plot_qualify(df, exportName_img):

    row_count, col_count = df.shape    

    ncol = 1
    nrow = int(np.ceil(row_count/ncol))

    print(f"ncol = {ncol}, nrow = {nrow}")
    plt.figure(figsize=(30,160))

    for iter, (row) in enumerate(df.iterrows()):
        
        ax = plt.subplot2grid((nrow, ncol), (iter//ncol, iter%ncol))

        tickerSymbol, strategy, days, exitTime_datas, list_netp, list_latentLoss, list_asset,\
        list_worst, list_trades, now, longColor, shortColor, latenLossColor, text_info\
        = qualify_data(df, iter)

        ax.plot(list_trades, list_asset, marker='o', label="Asset", color='black')
        ax.plot(list_trades, list_worst, marker='o', label="Worst", color='red')
        #ax.axhline(y=200, xmin=0, xmax=1, linestyle="dashed", color = "gray")
        ax.set_xticks(range(len(exitTime_datas)), exitTime_datas)   
        ax.legend(loc = 'lower right') 

        for i in range(len(exitTime_datas)):
            if "Long" in strategy:
                ax.text(list_trades[i], list_asset[i], f" #{list_trades[i]}, {(list_netp[i])}%", bbox=longColor)
            if "Short" in strategy:
                ax.text(list_trades[i], list_asset[i], f" #{list_trades[i]}, {(list_netp[i])}%", bbox=shortColor)
            if list_trades[i] != 0:
                ax.text(list_trades[i], list_worst[i], f"{list_latentLoss[i]}%", bbox=latenLossColor)
                
        ax.text(0, 100, text_info)
        ax.set_title(tickerSymbol)


    plt.gcf().autofmt_xdate()
    plt.autoscale(enable=True, axis='both', tight=False) 

    logging.info("Generating Chart Image...")
    plt.savefig(exportName_img)


if __name__ == "__main__": 


    exportName_img = f"{project_dir}/static/Diviation_Long_2022_1004_0313_Qualify.png"

    df = pd.read_csv(f"{project_dir}/static/Diviation_Long_2022_1004_0313_Qualify.csv")
    plot_qualify(df, exportName_img)
    logging.info("qualify image OK")

    # plot_indicator()
    # logging.info("indicator image OK")

    logging.info("All cahrt has created successfuly")
