import place_order
import datetime
import json
import time
def fun_Intraday(alice,t,Intraday_Equity,Intraday_Option,Limit_Intraday, Strike_price,Target,Stoploss,Trailing_Stoploss,Re_enter,Intraday_Equity_balance,Intraday_Option_balance):    
    to_long_symbol, to_short_symbol, history = [], [], {}
    
    try:
        with open('/home/ubuntu/new/Data_live.json', 'r') as openfile:
    
            live_data = json.load(openfile)
    except:
        print("pass")
    with open('/home/ubuntu/new/Data_9_8.json', 'r') as openfile:
  

        data_9_8 = json.load(openfile)
    
    history_9_8 = {}

    for symbol, values in data_9_8.items():
        history_9_8[symbol] ={'Open': values['Open'], 'High': values['High'], 'Low': values['Low'], 'LTP': values['LTP'], 'Close': values['Close'],'Traded':False}
    
    
    
    for symbol, values in live_data.items():
        try:

            history[symbol]

        except:

            history[symbol] ={'Open': values['Open'], 'High': values['High'], 'Low': values['Low'], 'LTP': values['LTP'], 'Close': values['Close'],'Traded':False}

        #print(symbol,history[symbol])





        #Intraday To-long 

        if len(to_long_symbol) <= Limit_Intraday-1:

            

            #values['Open'] == values['Low'] and

            if values['LTP'] < 10000 and values['LTP'] > 500 and  round(values['Open'],1) == round(values['Low'],1) and not history[symbol]['Traded']:

                # print("Buy :", symbol, f" at {values['LTP']} and Time {datetime.datetime.now().time()}")

                history[symbol]['Traded'] = True

                to_long_symbol.append(symbol)

        

        #Intraday To-Short

        if len(to_short_symbol) < Limit_Intraday:

            

            #values['Open'] == values['High'] and

            if values['LTP'] < 10000 and values['LTP'] > 500 and round(values['Open'],1) == round(values['High'],1) and not history[symbol]['Traded']:

        

                # print("Sell :", symbol, f" at {values['LTP']} and Time {datetime.datetime.now().time()}")

                history[symbol]['Traded'] = True    

                to_short_symbol.append(symbol)  





    print(f"Intraday Trade----Stock to long {to_long_symbol} and Stock to short {to_short_symbol} ")

    long_ltp_list = [round(history_9_8[to_long_symbol[i]]['Open'],1) for i in range(len(to_long_symbol))]

    short_ltp_list = [round(history_9_8[to_short_symbol[i]]['Open'],1) for i in range(len(to_short_symbol))]

    l_long_strike_list = [round(history_9_8[to_long_symbol[i]]['Open']*(Strike_price-0.05)*0.01+history_9_8[to_long_symbol[i]]['Open'],1) for i in range(len(to_long_symbol))]

    l_short_strike_list = [round(history_9_8[to_short_symbol[i]]['Open']-history_9_8[to_short_symbol[i]]['Open']*(Strike_price-0.05)*0.01,1) for i in range(len(to_short_symbol))]
    

    long_strike_list = [round(history_9_8[to_long_symbol[i]]['Open']*Strike_price*0.01+history_9_8[to_long_symbol[i]]['Open'],1) for i in range(len(to_long_symbol))]

    short_strike_list = [round(history_9_8[to_short_symbol[i]]['Open']-history_9_8[to_short_symbol[i]]['Open']*Strike_price*0.01,1) for i in range(len(to_short_symbol))]

    for symbol, values in live_data.items():

        history[symbol] ={'Open': values['Open'], 'High': values['High'], 'Low': values['Low'], 'LTP': values['LTP'], 'Close': values['Close'],'Traded':False}

    print("Updated")

    long_squareoff_list = [round(history[to_long_symbol[i]]['LTP']*Target*0.01,1) for i in range(len(to_long_symbol))]

    short_squareoff_list = [round(history[to_short_symbol[i]]['LTP']*Target*0.01,1) for i in range(len(to_short_symbol))]

    long_stoploss_list = [round(history[to_long_symbol[i]]['LTP']*Stoploss*0.01,1) for i in range(len(to_long_symbol))]

    short_stoploss_list = [round(history[to_short_symbol[i]]['LTP']*Stoploss*0.01,1) for i in range(len(to_short_symbol))]

    long_re_enter_list = [round(history[to_long_symbol[i]]['LTP']*Re_enter*0.01,1) for i in range(len(to_long_symbol))]

    short_re_enter_list = [round(history[to_short_symbol[i]]['LTP']*Re_enter*0.01,1) for i in range(len(to_short_symbol))]


    print("Long Data:",long_strike_list,long_squareoff_list,long_stoploss_list,long_re_enter_list)
    print("Short Data:",short_strike_list,short_squareoff_list,short_stoploss_list,short_re_enter_list)
    Long_qty_Intraday,Short_qty_Intraday = place_order.quantity(long_strike_list,short_strike_list,Intraday_Equity_balance)

        

    option_long_symbol,option_long_symbol_str,option_short_symbol,option_short_symbol_str= place_order.find_option(alice,t,history,to_long_symbol,to_short_symbol)





    #Placing order for Equity 

    if Intraday_Equity == 1:

        response_equity_buy = place_order.equity_order(alice,to_long_symbol,long_strike_list,long_stoploss_list,long_squareoff_list,Long_qty_Intraday,'B')

        

        response_equity_sell = place_order.equity_order(alice,to_short_symbol,short_strike_list,short_stoploss_list,short_stoploss_list,Short_qty_Intraday,'S')

        

        print("--------Order for Intraday Equity has been placed successfully--------")

            





    #Placing order for Option

    if Intraday_Option == 1:

        response_option_long = place_order.option_order(t,alice,option_long_symbol,'B',True)

        response_option_short = place_order.option_order(t,alice,option_short_symbol,'B',False)

        print("--------Order for Intraday Option has been placed successfully--------")

            

    Open_trade_symbol = place_order.open_trade(alice)

    def long_trail_stop_loss(entry,close):

        initalSL = round(entry - (entry*Trailing_Stoploss*0.01),2)

        trail = round(entry*Trailing_Stoploss*0.01,2)

        forwardMove = round(entry*Trailing_Stoploss*0.01,2)

        print('Entry: ', entry,'SL : ',initalSL )

        SL = initalSL

        diff =  round((close - entry ) , 2) 

        point = int(diff/forwardMove)  if diff > 0 else 0 

        SLmove = point*trail

        if  SL >= close:

            print("SL hit ")

            return "Hit"

            

        elif SL - initalSL < SLmove:

            SL  = initalSL+ SLmove  #ORDER UPDATE HERE

            print("SL updated")

        else:

            print("No change")

        

        

        return SL



    def short_trail_stop_loss(entry,close):

        initalSL = round(entry + (entry*Trailing_Stoploss*0.01))

        trail = round(entry*Trailing_Stoploss*0.01,2)

        forwardMove = round(entry*Trailing_Stoploss*0.01,2)

        SL = initalSL

        print('Entry: ', entry,'SL : ',initalSL )

        diff = round((entry - close) , 2)

        point = int(diff/forwardMove)  if diff > 0 else 0 

        SLmove = point*trail

        

        if initalSL - SL < SLmove:

            SL  = initalSL- SLmove #SL ORDER UPDATE HERE

            print("SL updated")

        elif  SL <= close:

            print("SL hit ")

            #return "Hit"

        else: 

            print("No change")

        

        

        return SL







    Data = {}



    SL_long = []

    SL_short = []

    market_close = int(10) * 60 + int(00)
    timenow =0
    while True:
        try:
            with open('/home/ubuntu/new/Data_live.json', 'r') as openfile:
    
                live_data = json.load(openfile)
                #print("read")
        except:
            pass
        for symbol, values in live_data.items():

            

            

            try:

                Data[symbol]['ltp'] = round(values['LTP'],1)

            except:



                Data[symbol] ={'ltp':round(values['LTP'],1),'Traded-stoploss':False,'Traded-strike':False,'Traded-reenter':False,'Trade-completed':False}

        

            #For Long

            for i in range(len(to_long_symbol)):

                

                if symbol == to_long_symbol[i] and symbol in Open_trade_symbol:

                    #print("Checking on Long Trades")

                    #Stoploss Re-enter 

                    if round(Data[symbol]['ltp'],1) >= round((l_long_strike_list[i]),1) and round(Data[symbol]['ltp'],1) <= round((long_strike_list[i]),1) and Data[symbol]['Traded-stoploss']  and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'B',True)

                        if Intraday_Equity == 1:

                            place_order.equity_order(alice,[to_long_symbol[i]],[long_strike_list[i]],[long_stoploss_list[i]],[long_squareoff_list[i]],[Long_qty_Intraday[i]*2],'B')

                        Data[symbol]['Traded-stoploss'] = False

                        print(f"Long:::::Stoploss Re-entering trade on {symbol},,time:{timenow}")

                        

    # =============================================================================

    #                     #Target Re-enter 

    #                     if Data[symbol]['ltp'] == (long_ltp_list[i]) and Data[symbol]['Traded-strike'] :

    #                         if Intraday_Option == 1:

    #                             place_order.option_order(t,alice,[option_long_symbol[i]],'B',True)

    #                         if Intraday_Equity == 1:

    #                             place_order.equity_order(alice,[to_long_symbol[i]],[long_strike_list[i]],[long_stoploss_list[i]],[long_squareoff_list[i]],'B')

    #                         Data[symbol]['Traded-strike'] = False

    #                         print(f"Long:::::Target Re-entering trade on {symbol}")

    #                     

    # =============================================================================

                    #Exiting Stoploss Option

                    elif round(Data[symbol]['ltp'],1) <= round((long_ltp_list[i]-long_stoploss_list[i]),1) and not Data[symbol]['Traded-stoploss'] and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'S',True)

                        Data[symbol]['Traded-stoploss'] = True

                        print(f"Long:::::Stoploss Hit on:  {symbol},,time:{timenow}")

                        

                    #Exiting Traget Option

                    elif round(Data[symbol]['ltp'],1) >= round((long_squareoff_list[i]+long_ltp_list[i]),1) and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'S',True)

                        Data[symbol]['Traded-strike'] = True

                        print(f"Long:::::Target of {Target}% Achieved on:  {symbol},,time:{timenow}")

                    

                    #Re-Enter with trailing stop loss for Equity and Option

                    elif round(Data[symbol]['ltp'],1) >= round((long_ltp_list[i]+long_re_enter_list[i]),1) and not Data[symbol]['Traded-reenter'] and Data[symbol]['Traded-strike']:

                        if Intraday_Equity == 1:

                        

                            place_order.equity_re_enter_order(alice,[to_long_symbol[i]],[Long_qty_Intraday[i]],'B')

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'B',True)    

                        

                        Data[symbol]['Traded-reenter'] = True

                        

                        print(f"Long:::::Rentering Trade with Trailing on Symbol:{symbol},,time:{timenow}")

                    elif Data[symbol]['Traded-reenter'] and not Data[symbol]['Trade-completed']:

                        

                        SL = long_trail_stop_loss(round(long_ltp_list[i]+long_re_enter_list[i],1),Data[symbol]['ltp'])

                        

                        if SL == "Hit":

                            if Intraday_Equity == 1:

                                place_order.equity_re_enter_order(alice,[to_long_symbol[i]],[Long_qty_Intraday[i]],'S')

                            if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_long_symbol[i]],'S',True)    

                            #to_long_symbol.pop(i)
                            Data[symbol]['Trade-completed'] = True

                            print(f"Long:::::Trailing Stoploss Hit on Symbol:{symbol},,time:{timenow}")

            

            #For Short

            for i in range(len(to_short_symbol)):

                

                if symbol == to_short_symbol[i] and symbol in Open_trade_symbol:

                        

                    #print("Checking on Short Trades")

                    #Stoploss Re-enter 

                    if round(Data[symbol]['ltp'],1) >= round((short_strike_list[i]),1) and round(Data[symbol]['ltp'],1) <= round((l_short_strike_list[i]),1) and Data[symbol]['Traded-stoploss'] and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'B',False)

                        if Intraday_Equity == 1:

                            place_order.equity_order(alice,[to_short_symbol[i]],[short_strike_list[i]],[short_stoploss_list[i]],[short_squareoff_list[i]],[Short_qty_Intraday[i]*2],'S')

                        Data[symbol]['Traded-stoploss'] = False

                        print(f"Short:::::Stoploss Re-entering trade on {symbol},time:{timenow}")

                        

    # =============================================================================

    #                     if Data[symbol]['ltp'] == (short_ltp_list[i]) and Data[symbol]['Traded-strike']:

    #                         if Intraday_Option == 1:

    #                             place_order.option_order(t,alice,[option_short_symbol[i]],'B',False)

    #                         if Intraday_Equity == 1:

    #                             place_order.equity_order(alice,[to_short_symbol[i]],[short_strike_list[i]],[short_stoploss_list[i]],[short_squareoff_list[i]],'S')

    #                         Data[symbol]['Traded-strike'] = False

    #                         print(f"Short:::::Target Re-entering trade on {symbol}")

    #                     

    # =============================================================================



                    #Exiting Stoploss Option

                    elif round(Data[symbol]['ltp'],1) >= round((short_ltp_list[i]+short_stoploss_list[i]),1) and not Data[symbol]['Traded-stoploss'] and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'S',False)

                        Data[symbol]['Traded-stoploss'] = True

                        print(f"Short:::::Stoploss Hit on:  {symbol},time:{timenow}")

                        

                    #Exiting Traget Option

                    elif round(Data[symbol]['ltp'],1) <= round((short_squareoff_list[i]-short_ltp_list[i]),1) and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'S',False)

                        Data[symbol]['Traded-strike'] = True

                        print(f"Short:::::Target of {Target}% Achieved on:  {symbol},time:{timenow}")

                    

                    #Enter with trailing stop loss Equity

                    elif round(Data[symbol]['ltp'],1) <= round((short_ltp_list[i]-short_re_enter_list[i]),1) and not Data[symbol]['Traded-reenter'] and Data[symbol]['Traded-strike']:

                        

                        if Intraday_Equity == 1:

                            place_order.equity_re_enter_order(alice,[to_short_symbol[i]],[Short_qty_Intraday[i]*2],'S')

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'B',False)    

                        Data[symbol]['Traded-reenter'] = True

                        print(f"Short:::::Rentering Trade with Trailing on Symbol:{symbol},time:{timenow}")

                    

                    elif Data[symbol]['Traded-reenter'] and not Data[symbol]['Trade-completed']:

                        

                        SL = short_trail_stop_loss(round(short_ltp_list[i]-short_re_enter_list[i],1),Data[symbol]['ltp'])

                        

                        if SL == "Hit":

                            if Intraday_Equity == 1:

                                place_order.equity_re_enter_order(alice,[to_short_symbol[i]],[Short_qty_Intraday[i]],'B')

                            if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_short_symbol[i]],'S',False)    

                            Data[symbol]['Trade-completed'] = True

                            print(f"Short:::::Trailing Stoploss Hit on Symbol:{symbol},,time:{timenow}")

        time.sleep(0.9)



        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)

    # =============================================================================

        if timenow > market_close:

            print("Market is Closed")

            break

    # =============================================================================
