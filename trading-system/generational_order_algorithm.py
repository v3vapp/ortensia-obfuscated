import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/tools")
from tools import report
from config import pw
from time import sleep
from pprint import pprint
from binance.enums import *


def run(exchangeClient, symbol, session, session_phase, entryLogic, exitLogic, debug=False):
    try:
        sessionID = f"{session}_{symbol}"

        # position_info _________________

        for i in range(5):
            try:
                position_all  = exchangeClient.futures_position_information()
                is_hedge_mode = exchangeClient.futures_get_position_mode()
                break
            
            except Exception as e:
                report.trade_system_error(f"API Request Failed for position_info. Retrying in a sec. return. -> {e}", debug)
                sleep(1)

        # Target symbol Notional Position
        position_symbol = list(filter(lambda item : item['symbol'] == symbol, position_all))
        position_symbol_notional = float(position_symbol[0]["notional"])

        # Total Notional Position
        position_total_notioal = 0
        for i in range(len(position_all)):
            position_total_notioal += float(position_all[i]["notional"])

        # WALLET ___________________________________________________________________________________________________________________

        for i in range(5):
            try:  
                balance_data      = exchangeClient.futures_account_balance()
                balance_USDT      = balance_data[3]
                balance_totalUSDT = float(balance_USDT["balance"])
                balance_freeUSDT  = float(balance_USDT["withdrawAvailable"])
                break
            except Exception as e:
                report.trade_system_error(f"API Request Faild for futures_account_balance. Retrying in 3 sec. return -> {e}", debug)
                sleep(1)

        # Leverage ____________________________________________________________________________________________________________________

        # Current Leverage -------------------------------------------------------------
        current_leverage = position_total_notioal/balance_freeUSDT # free of total??????

        # Max Leverage on the target symbol --------------------------------------------
        ignore_this_symbol = False

        for i in range(5):
            try:
                leverage_bracket = exchangeClient.futures_leverage_bracket(symbol = symbol)
                break
            except Exception as e:    
                if e.message == "symbol is closed.":
                    ignore_this_symbol = True
                    break
                else:
                    report.trade_system_error(f"API Request Failed for leverage_bracket. Retrying in 3 sec. -> {e}",debug)
                    sleep(1)
        #____________________________________________________________________________________________________
        if ignore_this_symbol == False:

            # Lv1 or Lv2. You have to adjust if you become rich.
            leverage_bracket_Lv2_notionalFloor = float(leverage_bracket[0]["brackets"][1]["notionalFloor"])
            leverage_bracket_Lv2_notionalCap   = float(leverage_bracket[0]["brackets"][1]["notionalCap"])

            # Bracket Lv.1 Notional has to be lower than Lv.2 notionalFloor.
            if leverage_bracket_Lv2_notionalFloor > position_symbol_notional:
                initialLeverage = int(leverage_bracket[0]["brackets"][0]["initialLeverage"])
            # Bracket Lv.2 Notional has to be lower than Lv.2 notionalCap.
            elif leverage_bracket_Lv2_notionalFloor < position_symbol_notional and position_symbol_notional < leverage_bracket_Lv2_notionalCap:
                initialLeverage = int(leverage_bracket[0]["brackets"][1]["initialLeverage"])
            # Over Bracket Lv.2 more than Lv.2 notionalCap. Update This system to adopt over Lv.2 bracket.
            else:
                initialLeverage = 5

                initialLeverage_message = "message from Daiki. Congrats! You're too rich. Fix Leverage bracket system because you are over leverage_bracket Lv2."
                report.trade_system_log(initialLeverage_message, debug)
                report.trade_system_error(initialLeverage_message, debug)

            # SET Max Leverage on the taregt symbol ----------------------------------------

            for i in range(5):
                try:
                    exchangeClient.futures_change_leverage(symbol=symbol, leverage=initialLeverage)
                    break
                except Exception as e:
                    report.trade_system_error(f"API Request Failed for change_leverage. Retrying in a sec. return -> {e}", debug)
                    sleep(1)

            # Hedge Mode Setting _____________________________________________________________
            try:
                if is_hedge_mode["dualSidePosition"] == False:
                    exchangeClient.futures_change_position_mode(dualSidePosition = True)
                    report.trade_system_log("Hedge Mode changed to True", debug)
                elif is_hedge_mode["dualSidePosition"] == False:
                    report.trade_system_log("Hedge Mode is True", debug)
            except Exception as e: 
                report.trade_system_error(f"Something wrong with HedgeMode setting process. reason -> {e}", debug)

            # Last order of this session ________________________________________________________
            try:
                last_session = exchangeClient.futures_get_order(symbol = symbol, origClientOrderId = sessionID)

                last_session_side           = last_session["side"]
                last_session_positionSide   = last_session["positionSide"]
                last_session_orderType      = last_session["type"]
                last_session_clientOrderId  = last_session["clientOrderId"]
                last_session_status         = last_session["status"]
                last_session_amount         = float(last_session["origQty"])
                last_session_timeUTC        = last_session["time"]
                unixTimeNowUTC              = last_session["updateTime"]

                # Pending open Order Timer. /1000 means ignore micro-seconds.
                pending_minutes = round(((unixTimeNowUTC - last_session_timeUTC)/1000)/60,1)

                # 反対売買が完了していれば、手仕舞い済み
                # If you order from website, it will fucked up. Because there is no crientId(Long or Short).

                operated = last_session_status == "EXPIRED" or last_session_status == "CANCELED"

                closed_LONG = last_session_side == "SELL" and \
                            "Long" in last_session_clientOrderId and \
                            last_session_status == "FILLED" or operated == True
                                        
                closed_SHORT = last_session_side == "BUY" and \
                            "Short" in last_session_clientOrderId and \
                            last_session_status == "FILLED" or operated == True

                session_KILLED  = "KILL" in last_session_clientOrderId
                session_STOPPED = "STOP" in last_session_clientOrderId

                if closed_LONG or closed_SHORT or session_KILLED or session_STOPPED:
                    session_position_exists = False
                else:
                    session_position_exists = True

            # No History on this session
            except Exception as e:
                last_session                = None
                last_session_side           = None
                last_session_positionSide   = None
                last_session_orderType      = None
                last_session_clientOrderId  = None
                last_session_status         = None
                last_session_amount         = 0
                last_session_timeUTC        = None
                unixTimeNowUTC              = None
                session_position_exists     = False
                closed_LONG                 = None
                closed_SHORT                = None
                session_KILLED              = None
                session_STOPPED             = None
                pending_minutes             = 0
                operated                    = False

            # openOrder on this sessionID ________________________________________________
            try:
                # All of open Orders of target symbol.
                openOrder_list = exchangeClient.futures_get_open_orders(symbol = symbol)
                # Find current session open order.
                open_session = list(filter(lambda item : item['clientOrderId'] == sessionID, openOrder_list))
                # original amount - executed amount = pending amount
                pending_amount = float(open_session[0]["origQty"]) - float(open_session[0]["executedQty"])
                pending_positionSide = open_session[0]["positionSide"]

            # No open order on this session.
            except Exception as e:
                openOrder_list       = None
                open_session         = None
                pending_amount       = None
                pending_positionSide = None

            # CONDITION ###########################################################################
            #______________________________
            # ENTRY 
            # セッションが生きている
            # 反対売買により、前回エントリーの手仕舞いが完了している。
            ENTRY_condition = \
                entryLogic == True and \
                session_phase == True and \
                session_position_exists == False and \
                current_leverage < 20 and \
                operated == False
            #______________________________
            # EXIT 
            # 最新のオーダーが約定済 
            # 最新のオーダーが反対売買ではない
            # つまり、未手仕舞いのセッション注文が市場に存在している。
            EXIT_condition = \
                exitLogic == True and \
                last_session_status == "FILLED" and \
                session_position_exists == True
            #______________________________
            # Replace Pending Order
            # Too long Pending -> Cancel, session Dead and NO Position -> Cancel
            RESET_condition = \
                pending_minutes > 10 and \
                last_session_status == "NEW"
            #______________________________
            # Buying too much. Have to cancel open-order.
            STOP_condition = \
                open_session != None and \
                session_position_exists == False and \
                current_leverage > 20 # x20 should be ok...
            #______________________________
            # session Dead and Position Exists. 
            # Wait for Exit order and become NO-position. JUST DO NOTHING
            WAIT_condition = \
                session_phase == False and \
                session_position_exists == True and\
                open_session == None
            #______________________________
            # session Dead and NO Position -> DEAD (反対取引が完了済)
            # open Order を削除せよ
            KILL_condition = \
                session_phase == False and \
                session_position_exists == False and \
                open_session != None
            #______________________________  
            # HOLDING
            IGNORE_ENTRY_condition = \
                entryLogic == True and \
                session_phase == True and \
                session_position_exists == True and \
                operated == False
            #______________________________  
            # HOLDING
            ALREADY_IN_POSITION_condition = \
                session_phase == True and \
                session_position_exists == True and \
                operated == False
            #______________________________
            # session Dead and NO Position -> DEAD (反対取引が完了済)
            # open Order を削除せよ
            DEAD_condition = \
                session_phase == False and \
                session_position_exists == False and \
                open_session == None
            # ENTER Long Position by MARKET_ORDER WITH Client Order ID.
            # To use postOnly, timeInForce = TIME_IN_FORCE_GTX. GTX means "Good Till Crossing".
            # Do not use OR to stop infinite loop.

            session_dead = False

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # TRADING

            if ENTRY_condition or EXIT_condition or RESET_condition:
                OrderFailed_Count = 0

                while True:
                    for i in range(5):
                        try:
                            orderbook = exchangeClient.futures_orderbook_ticker(symbol = symbol)
                            break
                        except Exception as e:
                            report.trade_system_error(f"API Request Failed for orderbook. Retrying in a sec. return -> {e}", debug)
                            sleep(1)

                    ask = float(orderbook["askPrice"])
                    bid = float(orderbook["bidPrice"])

                    for i in range(5):
                        try:
                            info = exchangeClient.futures_exchange_info()
                            break
                        except Exception as e:
                            report.trade_system_error(f"API Request Failed for orderbook. Retrying in 3 sec. return -> {e}", debug)
                            sleep(1)

                    total_symbols = info['symbols']

                    for i in range(len(total_symbols)):
                        pair = total_symbols[i]['pair']
                        if pair == symbol:
                            pricePrecision = int(info['symbols'][i]['pricePrecision'])
                            quantityPrecision = int(info['symbols'][i]['quantityPrecision'])

                    # ------------------------------------------------------------------------------------------

                    if ENTRY_condition:
                        #report.ORDER(f"TRYING TO ENTRY... {sessionID}.", debug = debug)

                        if "L_" in sessionID:
                            ORDER_SIDE     = SIDE_BUY
                            ORDER_POSITION = "LONG"
                            ORDER_PRICE    = bid
                            ORDER_AMOUNT   = round(balance_freeUSDT / ORDER_PRICE, quantityPrecision)
                        elif "S_" in sessionID:
                            ORDER_SIDE     = SIDE_SELL
                            ORDER_POSITION = "SHORT"
                            ORDER_PRICE    = ask
                            ORDER_AMOUNT   = round(balance_freeUSDT / ORDER_PRICE, quantityPrecision)

                    # ------------------------------------------------------------------------------------------

                    if EXIT_condition:  
                        #report.ORDER(f"EXITING... {sessionID}.", debug = debug)

                        if "L_" in sessionID:
                            ORDER_SIDE     = SIDE_SELL
                            ORDER_POSITION = "LONG"
                            ORDER_PRICE    = ask
                            ORDER_AMOUNT   = last_session_amount
                        elif "S_" in sessionID:
                            ORDER_SIDE     = SIDE_BUY
                            ORDER_POSITION = "SHORT"
                            ORDER_PRICE    = bid
                            ORDER_AMOUNT   = last_session_amount

                    # ------------------------------------------------------------------------------------------

                    if RESET_condition:
                        #report.ORDER(f"RESETING(REPLACE)... {sessionID}.", debug = debug)

                        if last_session_side == "BUY":
                            ORDER_SIDE     = SIDE_BUY
                            ORDER_POSITION = pending_positionSide
                            ORDER_PRICE    = bid
                            ORDER_AMOUNT   = pending_amount
                        elif last_session_side == "SELL":
                            ORDER_SIDE     = SIDE_SELL
                            ORDER_POSITION = pending_positionSide
                            ORDER_PRICE    = ask
                            ORDER_AMOUNT   = pending_amount

                        # Cancel pending open order.
                        order_message = exchangeClient.futures_cancel_order(\
                                        symbol            = symbol,\
                                        origClientOrderId = sessionID,\
                                        clientOrderId     = sessionID)
                        string_order_message = str(order_message).replace(",","\n").replace("{","").replace("}","")
                        
                        report.ORDER(f"Canceled open-Order to RESET(REPLACE). Pending time was {pending_minutes} min.", sessionID, string_order_message, debug)

                    #_____________________________________________________________________________
                    # Order

                    try:
                        order_message = exchangeClient.futures_create_order(
                                        symbol        = symbol,
                                        side          = ORDER_SIDE,
                                        positionSide  = ORDER_POSITION,
                                        type          = ORDER_TYPE_LIMIT,
                                        timeInForce   = TIME_IN_FORCE_GTX,
                                        quantity      = ORDER_AMOUNT,
                                        postOnly      = True,
                                        price         = ORDER_PRICE,
                                        newClientOrderId = sessionID)
                        string_order_message = str(order_message).replace(",","\n").replace("{","").replace("}","")

                        last_session = exchangeClient.futures_get_order(symbol = symbol, origClientOrderId = sessionID)
                        last_session_timeInForce = last_session["timeInForce"]
                        last_session_status = last_session["status"]

                        # POST-ONLY was rejected...
                        if last_session_timeInForce == "GTX" and last_session_status == "EXPIRED":
                            OrderFailed_Count += 1
                            report.trade_system_log(f"OrderFailed_Count -> {OrderFailed_Count} time. Retry. Status -> {last_session_status}", debug)
                            sleep(1)

                            if OrderFailed_Count == 3:
                                report.trade_system_error(f"Too many retry POST-ONLY. Trying LIMIT order. Status -> {last_session_status} @{sessionID}", debug)
                                break
                        else:
                            report.ORDER("POST-ONLY order success!", sessionID, string_order_message, debug)
                            break

                    except Exception as e:

                        OrderFailed_Count += 1
                        report.trade_system_log(f"You might have a open-Position already... @{sessionID}? error -> {e}", debug)
                        sleep(3)

                        if OrderFailed_Count == 3:
                            report.trade_system_log(f"Breaking Order Retrying. Tried {OrderFailed_Count} time. @{sessionID}? error -> {e}", debug)

                            try:
                                report.trade_system_log("Giving Up on Post-Only, Ordering by Good Till Cancel(Normal LIMIT Order).", debug)

                                order_message = exchangeClient.futures_create_order(
                                                symbol        = symbol,
                                                side          = ORDER_SIDE,
                                                type          = ORDER_TYPE_LIMIT,
                                                timeInForce   = TIME_IN_FORCE_GTC,  
                                                quantity      = ORDER_AMOUNT,
                                                postOnly      = False,
                                                price         = ORDER_PRICE,
                                                newClientOrderId = sessionID)
                                string_order_message = str(order_message).replace(",","\n").replace("{","").replace("}","")

                                report.ORDER("LIMIT order success!", sessionID, string_order_message, debug)

                            except Exception as e:
                                report.trade_system_log(f"Couldn't place a order. You might have a open-Position. @{sessionID}? error -> {e}", debug)

                            break
            #____________________________________________________________

            elif WAIT_condition:
                report.trade_system_log(f"WAITING... {sessionID}.", debug)
            #____________________________________________________________

            elif KILL_condition:
                try:
                    order_message = exchangeClient.futures_cancel_order(
                                    symbol = symbol,
                                    origClientOrderId = sessionID,
                                    clientOrderId = sessionID)
                    string_order_message = str(order_message).replace(",","\n").replace("{","").replace("}","")

                    report.ORDER(f"KILLED... {sessionID}. Pending time was {pending_minutes} min", sessionID, string_order_message, debug)
                    session_dead = True
                except Exception as e:
                    report.trade_system_error(f"[KILL] Couldn't Cancel @{sessionID}. error-> {e}", debug)
            #____________________________________________________________

            elif STOP_condition:
                try:
                    order_message = exchangeClient.futures_cancel_order(
                                    symbol = symbol,
                                    origClientOrderId = sessionID,
                                    clientOrderId = f"{sessionID}_STOP")
                    string_order_message = str(order_message).replace(",","\n").replace("{","").replace("}","")

                    report.ORDER(f"STOP(OVER BOUGHT)... {sessionID} Pending time was {pending_minutes} min.", sessionID, string_order_message, debug)
                except Exception as e:
                    report.trade_system_error(f"ERROR when [OverBUY->STOP] Couldn't Cancel @{sessionID}. error-> {e}", debug)
            #____________________________________________________________

            elif DEAD_condition:
                print(f"DEAD... {sessionID}.")
                session_dead = True 
            #____________________________________________________________

            elif IGNORE_ENTRY_condition:
                print(f"IgnoreENTRY...  {sessionID} (ALREDY in POSITION)")
            #____________________________________________________________

            elif ALREADY_IN_POSITION_condition:
                print(f"InPOSITION... {sessionID} (Holding Position)")
            #____________________________________________________________

            else:
                print(f"SKIP... {sessionID}")
            #____________________________________________________________

            if ENTRY_condition == False or EXIT_condition == False or RESET_condition == False:
                ORDER_SIDE      = None
                ORDER_POSITION  = None
                ORDER_PRICE     = None
                ORDER_AMOUNT    = None
            #__________________________________________________________________

            if __name__ == "__main__":
                print(f"symbol          = {symbol}")
                print(f"sessionID       = {sessionID}")
                print(f"session_alive   = {session_phase}")
                print()
                print(f"entryLogic     = {entryLogic}")
                print(f"exitLogic      = {exitLogic}")
                print()
                print(f"Hedge Mode      = {is_hedge_mode}")
                print()
                print(f"position_symbol_notional = {position_symbol_notional}")
                print(f"initialLeverage = {initialLeverage}")
                print()
                print(f"last_session                = {last_session}")
                print(f"last_session_side           = {last_session_side}")
                print(f"last_session_positionSide   = {last_session_positionSide}")
                print(f"last_session_orderType      = {last_session_orderType}")
                print(f"last_session_clientOrderId  = {last_session_clientOrderId}")
                print(f"last_session_status         = {last_session_status}")
                print(f"last_session_timeUTC        = {last_session_timeUTC}")
                print(f"last_session_amount         = {last_session_amount}")
                print(f"unixTimeNowUTC              = {unixTimeNowUTC}")
                print()
                print(f"pending_minutes = {pending_minutes}")
                print()
                print(f"closed_LONG     = {closed_LONG}")
                print(f"closed_SHORT    = {closed_SHORT}")
                print(f"session_KILLED  = {session_KILLED}")
                print(f"session_STOPPED = {session_STOPPED}")
                print()
                print(f"session_position_exists = {session_position_exists}")
                print()
                print(f"openOrder_list       = {openOrder_list}")
                print(f"open_session         = {open_session}")
                print(f"pending_amount       = {pending_amount}")
                print(f"pending_positionSide = {pending_positionSide}")
                print()
                print(f"balance_totalUSDT = {balance_totalUSDT}")
                print(f"balance_freeUSDT  = {balance_freeUSDT}")
                print()
                print(f"current_leverage  = {current_leverage}")
                print()
                # Check Condition
                # Entry condition
                print(f"entryLogic = {entryLogic}")
                print(f"session_alive = {session_phase}")
                print(f"session_position_exists = {session_position_exists}")
                print()
                # Exit condition
                print(f"exitLogic = {exitLogic}")
                print(f"last_session_status = {last_session_status}")
                print(f"last_session_clientOrderId = {last_session_clientOrderId}")
                print(f"session_position_exists = {session_position_exists}")
                print()
                # ReOrder condition
                print(f"pending_minutes = {pending_minutes}")
                print(f"last_session_status  = {last_session_status}")
                print()
                # WAIT-KILL / KILL / DEAD condition
                print(f"session_alive           = {session_phase}")
                print(f"session_position_exists = {session_position_exists}")
                print(f"open_session            = {open_session}")
                print()
                print(f"ENTRY_condition = {ENTRY_condition}")
                print(f"EXIT_condition   = {EXIT_condition}")
                print(f"RESET_condition = {RESET_condition}")
                print(f"WAIT_condition  = {WAIT_condition}")
                print(f"STOP_condition  = {STOP_condition}")
                print(f"KILL_condition  = {KILL_condition}")
                print(f"DEAD_condition  = {DEAD_condition}")
                print()
                print(f"ORDER_SIDE      = {ORDER_SIDE}")
                print(f"ORDER_POSITION  = {ORDER_POSITION}")
                print(f"ORDER_PRICE     = {ORDER_PRICE}")
                print(f"ORDER_AMOUNT    = {ORDER_AMOUNT}")

            return session_dead
        
    except Exception as e:
        print(f"ERROR... {sessionID}. reason -> {e}")

    else:
        # symbol is closed.

        session_dead = True 

        print(f"ERROR... symbol is closed. {sessionID}. I returned -> session_dead = True")

        return session_dead


#___________________________________________________________________


if __name__ == "__main__":

    symbol = "BTCUSDT"

    import inquirer
    import setup

    phase_questions = [inquirer.List('phase', message="Which phase?", choices=[True, False],),]
    phase_answers   = inquirer.prompt(phase_questions)
    session_phase   = phase_answers["phase"]

    entry_questions = [inquirer.List('entry', message="entry?", choices=["Entry", "Exit"],),]
    entry_answers   = inquirer.prompt(entry_questions)
    logic     = entry_answers["entry"]

    if logic == "Entry":
        entryLogic = True  
        exitLogic  = False

    if logic == "Exit":
        entryLogic = False 
        exitLogic  = True

    sessionInfo = setup.run()

    session = sessionInfo[2]

    from binance.client import Client

    exchangeClient = Client(pw.test_binance_api_key, pw.test_binance_api_secret, testnet = True)

    run(exchangeClient, symbol, session, session_phase, entryLogic, exitLogic, debug=True)
