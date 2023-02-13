import sys, pathlib, sqlite3
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/tools")
import sys, logging, pathlib, os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import analyze
from tools import report
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
#___________________________________________________________________________________

def run(exchangeName, debug = False):
    try:
        connection = sqlite3.connect(f"{outside_dir}/project.db")
        c = connection.cursor()

        c.execute(f'SELECT * FROM account_{exchangeName}') 

        account_data = c.fetchone()

        data_time_data = analyze.func_datatime_data_data(account_data)

        position_data = analyze.func_position_data(account_data)

        list_entryPrice = position_data[0]
        list_isAutoAddMargin = position_data[1]
        list_isolatedMargin = position_data[2]
        list_isolatedWallet = position_data[3]
        list_leverage = position_data[4]
        list_liquidationPrice = position_data[5]
        list_marginType = position_data[6]
        list_markPrice = position_data[7]
        list_maxNotionalValue = position_data[8]
        list_notional = position_data[9]
        list_positionAmt = position_data[10]
        list_positionSide = position_data[11]
        list_positionsymbol = position_data[12]
        list_unRealizedprofit = position_data[13]
        list_uptime = position_data[14]
        total_notional = position_data[15]
        list_all_positive_notional = position_data[16]
        list_positionsymbolAndSide = position_data[17]
        total_LONG_notional = position_data[18]
        total_Short_notional = position_data[19]
        total_unRealizedprofitLoss = position_data[20]
        total_unRealized_profitONLY = position_data[21]
        total_unRealized_LossONLY = position_data[21]

        balance_data = analyze.func_balance_data(account_data)

        list_asset = balance_data[0]
        list_balance = balance_data[1]
        list_withdrawAvailable = balance_data[2]
        total_balance = balance_data[4]
        total_withdrawAvailable = balance_data[5]

        connection.close()

        line = analyze.create_list(exchangeName, debug)

        list_data_time_data = line[0]
        list_total_balance = line[1]
        list_total_withdrawAvailable = line[2]
        list_total_notional = line[3]
        list_total_LONG_notional = line[4]
        list_total_SHORT_notional = line[5]
        list_total_unRealizedprofitLoss = line[6]
        list_total_unRealized_profitONLY = line[7]
        list_total_unRealized_LossONLY_Negative = line[8]
        #________________________________________________________________________________________________
        
        fig = plt.figure(figsize=(10, 15), dpi=72)
        fig.suptitle(f'{exchangeName} {data_time_data} UTC', fontsize=13)

        gs = GridSpec(5, 5)

        ax10_1 = plt.subplot(gs[0, :4])
        ax10_2 = plt.subplot(gs[0, 4:])

        ax15_1 = plt.subplot(gs[1, 0:2])
        ax15_2 = plt.subplot(gs[1, 2:3])
        ax15_3 = plt.subplot(gs[1, 3:4])
        ax15_4 = plt.subplot(gs[1, 4:5])

        ax20_1 = plt.subplot(gs[2, :4])
        ax20_2 = plt.subplot(gs[2, 4:])

        ax30_1 = plt.subplot(gs[3, :4])
        ax30_2 = plt.subplot(gs[3, 4:])

        ax40_1 = plt.subplot(gs[4, :4])
        ax40_2 = plt.subplot(gs[4, 4:])

        # # Balance
        ax10_1.set_title(f'Balance ${round(total_balance,1)}')

        ax10_1.yaxis.set_label_position("right")
        ax10_1.yaxis.tick_right()
        ax10_1.plot(list_data_time_data, list_total_balance, marker="o", label="balance")
        ax10_1.legend(loc='upper left')

        ax10_2.pie(list_balance, labels=list_asset, autopct='%1.1f%%', shadow=True, startangle=90)
        ax10_2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        #unRealizedprofitLoss

        ax15_1.set_title(f'unRealizedprofitLoss ${round(total_unRealizedprofitLoss,1)}')

        ax15_1.yaxis.set_label_position("right")
        ax15_1.yaxis.tick_right()
        ax15_1.plot(list_data_time_data, list_total_unRealizedprofitLoss, marker="o", label="unRealizedprofitLoss")

        ax15_2.set_title(f'unRealized profit  ${round(total_unRealized_profitONLY,1)}')
        ax15_2.yaxis.set_label_position("right")
        ax15_2.yaxis.tick_right()
        ax15_2.plot(list_data_time_data, list_total_unRealized_profitONLY, marker="o", label="unRealized profit")

        ax15_2.set_title(f'unRealized Loss  ${round(total_unRealized_LossONLY*-1,1)}')
        ax15_3.yaxis.set_label_position("right")
        ax15_3.yaxis.tick_right()
        ax15_3.plot(list_data_time_data, list_total_unRealized_LossONLY_Negative, marker="o", label="unRealized Loss")

        if total_unRealized_profitONLY == 0:
            total_unRealized_profitONLY = 0.001
        ax15_4.pie([total_unRealized_profitONLY, total_unRealized_LossONLY], labels=["profit","Loss"], autopct='%1.1f%%', shadow=True, startangle=90)
        ax15_4.axis('equal') 

        # # Withdraw
        ax20_1.set_title(f'Withdrawable ${round(total_withdrawAvailable,1)}')
        ax20_1.yaxis.set_label_position("right")
        ax20_1.yaxis.tick_right()
        ax20_1.plot(list_data_time_data, list_total_withdrawAvailable, marker="o", label="withdrawAvailable")
        ax20_1.legend(loc='upper left')

        ax20_2.pie(list_withdrawAvailable, labels=list_asset, autopct='%1.1f%%', shadow=True, startangle=90)
        ax20_2.axis('equal') 

        # Position
        ax30_1.set_title(f'Posititon ${round(total_notional,1)}')

        ax30_1.yaxis.set_label_position("right")
        ax30_1.yaxis.tick_right()
        ax30_1.plot(list_data_time_data, list_total_notional, marker="o", label="notional")
        ax30_1.legend(loc='upper left')

        ax30_2.pie(list_all_positive_notional, labels=list_positionsymbolAndSide, autopct='%1.1f%%',shadow=True, startangle=90)
        ax30_2.axis('equal')  

        # Side
        ax40_1.set_title(f'LONG vs SHORT $({round(total_LONG_notional,1)} vs {round(total_Short_notional,1)})')

        ax40_1.yaxis.set_label_position("right")
        ax40_1.yaxis.tick_right()
        ax40_1.plot(list_data_time_data, list_total_LONG_notional, marker="o", label="LONG_notional")
        ax40_1.plot(list_data_time_data, list_total_SHORT_notional, marker="o", label="SHORT_notional")
        ax40_1.legend(loc='upper left')

        if total_LONG_notional > 0 or total_Short_notional > 0:
            ax40_2.pie([total_LONG_notional, total_Short_notional], labels=["LONG","SHORT"], autopct='%1.1f%%',shadow=True, startangle=90)
            ax40_2.axis('equal') 
        else:
            ax40_2.text(0.4, 0.5, "No Data", size=20)

        #___________________________________________________________
        plt.gcf().autofmt_xdate()

        local_path = f"{working_dir}/static/TEMP"

        os.makedirs(local_path, exist_ok=True)
        file_path = f'{local_path}/report_{exchangeName}.png'

        fig.savefig(file_path)

        report.account(exchangeName, file_path, debug)

    except Exception as e:
        report.error(e, "Error database/investment_report.py -> Error happend when I'm trying to create/plot new account balance and position report.")


#____________________________________________________

if __name__ == "__main__":

    run("BINANCETESTNET", debug = True)
