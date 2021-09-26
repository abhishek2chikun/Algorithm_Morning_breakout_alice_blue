import place_order
import functions
import datetime
import time
import json
import pandas as pd

def fun_1m(alice,t,Equity_1m,Option_1m,Limit_1m,Stoploss_1m,Equity_balance_1m):
    history = {}

    long_1m, short_1m = [],[]
    with open('/home/ubuntu/new/Data_live.json', 'r') as openfile:
  
    # Reading from json file
        live_data = json.load(openfile)
    print(live_data)
    for symbol, values in live_data.items():

        try:

            history[symbol]

        except:

            history[symbol] ={'Open': values['Open'], 'High': values['High'], 'Low': values['Low'], 'LTP': values['LTP'], 'Close': values['Close'],'Traded':False}

        #print(symbol,history[symbol])

        

        #1MinGame

        if len(long_1m) <= Limit_1m-1:

            if values['LTP'] < 10000 and values['LTP'] > 300 and values['Open'] > values['Close'] and values['Open'] == values['Low'] and not history[symbol]['Traded']:

                # print("Buy :", symbol, f" at {values['LTP']} and Time {datetime.datetime.now().time()}")

                history[symbol]['Traded'] = True

                long_1m.append(symbol)

            

        if len(short_1m) <= Limit_1m-1:

            if values['LTP'] < 10000 and values['LTP'] > 300 and values['Open'] < values['Close'] and values['Open'] == values['High'] and not history[symbol]['Traded']:

        

                # print("Sell :", symbol, f" at {values['LTP']} and Time {datetime.datetime.now().time()}")

                history[symbol]['Traded'] = True    

                short_1m.append(symbol)





    print(f"1 min Trade--- Stock to long {long_1m} and Stock to short {short_1m} ")  

    

    

    

    long_strike_list_1m = [round(history[long_1m[i]]['Open'],1) for i in range(len(long_1m))]

    short_strike_list_1m = [round(history[short_1m[i]]['Open'],1) for i in range(len(short_1m))]

    

    long_Stop_list_1m = [round(history[long_1m[i]]['LTP']-history[long_1m[i]]['LTP']*Stoploss_1m*0.01,1) for i in range(len(long_1m))]

    short_Stop_list_1m = [round(history[short_1m[i]]['LTP']*Stoploss_1m*0.01+history[short_1m[i]]['LTP'],1) for i in range(len(short_1m))]

    
    
    #1m Qty

    Long_qty_1m,Short_qty_1m = place_order.quantity(long_strike_list_1m,short_strike_list_1m,Equity_balance_1m)    


    #1m

    option_1m_long_symbol,option_1m_long_symbol_str,option_1m_short_symbol,option_1m_short_symbol_str = place_order.find_option(alice,t,history,long_1m,short_1m)

    

    if functions.market_open_check():

        
        
        #Placing order for 1m Equity 

        if Equity_1m == 1:

            response_equity_buy = place_order.equity_1m_order(alice,long_1m,Long_qty_1m,'B')

            

            response_equity_sell = place_order.equity_1m_order(alice,short_1m,Short_qty_1m,'S')

                            

            

            print("-------- 1min Equity has been placed successfully--------")



        #Placing order for 1m Option

        if Option_1m == 1:

            

            response_option_long = place_order.option_order(t,alice,option_1m_long_symbol,'B',True)

            response_option_short = place_order.option_order(t,alice,option_1m_short_symbol,'B',False)

        

            print("-------- 1min Option has been placed successfully--------")

        

        Data = {}

        orderplacetime = int(3) * 60 + int(45)*60 + int(50)
        
        timenow = (datetime.datetime.now().hour * 60 + (datetime.datetime.now().minute*60) + datetime.datetime.now().second)

        print("Waiting for 9.15:50 AM , CURRENT TIME:{}".format(datetime.datetime.now()))
        time.sleep(1)
        Open_trade_symbol = place_order.open_trade(alice)
        if len(Open_trade_symbol) == 0:
            time.sleep(1)
            print("Sleep")
            Open_trade_symbol = place_order.open_trade(alice)
            if len(Open_trade_symbol) == 0:
                time.sleep(1)
                Open_trade_symbol = place_order.open_trade(alice)
                print("Sleep")
        print("Open Trade:",Open_trade_symbol)
        while timenow < orderplacetime:
            print(timenow,orderplacetime)
            try:
                with open('Data_live.json', 'r') as openfile:
    
                    live_data = json.load(openfile)
                    #print("read 1m")
            except:
                pass
                #print("Skip")
            for symbol, values in live_data.items():

                

                

                try:

                    Data[symbol]['ltp'] = round(values['LTP'],1)

                except:

        

                    Data[symbol] ={'ltp':round(values['LTP'],1),'Traded-stoploss':False}

          

               #For Long
                n_long = len(long_1m)
                i = 0
                while i < n_long:
                    
                    if symbol == long_1m[i] and symbol in Open_trade_symbol:

                        #print(symbol,round(Data[symbol]['ltp'],1))

                        #Exiting Stoploss Option

                        if round(Data[symbol]['ltp'],1) <= long_Stop_list_1m[i] and not Data[symbol]['Traded-stoploss']:

                            if Option_1m == 1 and option_1m_long_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_1m_long_symbol[i]],'S',True)

                            if Equity_1m == 1:

                                response_equity_buy = place_order.equity_1m_order(alice,[long_1m[i]],[Long_qty_1m[i]],'S')

                            

                            Data[symbol]['Traded-stoploss'] = True

                            long_1m.pop(i)

                            option_1m_long_symbol.pop(i)

                            i-=1
                            n_long-=1
                            print(f"Long:::::Stoploss Hit on:  {symbol}")
                    i+=1

                #For Short
                n_short = len(short_1m)
                i=0
                while i < n_short:

                    if symbol == short_1m[i] and symbol in Open_trade_symbol:

                        #Exiting Stoploss Option
                        #print(symbol,round(Data[symbol]['ltp'],1))
                        if round(Data[symbol]['ltp'],1) >= short_Stop_list_1m[i] and not Data[symbol]['Traded-stoploss']:

                            if Option_1m == 1 and option_1m_short_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_1m_short_symbol[i]],'S',True)

                            if Equity_1m == 1:

                                response_equity_buy = place_order.equity_1m_order(alice,[short_1m[i]],[Short_qty_1m[i]],'B')

                            

                            Data[symbol]['Traded-stoploss'] = True

                            option_1m_short_symbol.pop(i)
                            short_1m.pop(i)
                            n_short-=1
                            i-=1

                            print(f"Short:::::Stoploss Hit on:  {symbol}")

                          

                        #print("Checking on Short Trades")
                    i+=1
            time.sleep(0.9)

            timenow = (datetime.datetime.now().hour * 60 + (datetime.datetime.now().minute*60) + datetime.datetime.now().second)


        

                        

        #Closing order for 1m Equity 
        Open_trade_symbol = place_order.open_trade(alice)
        print("Closing Trade")
        
        if Equity_1m == 1:

            for i in range(len(long_1m)):

                if long_1m[i] in Open_trade_symbol:

                    response_equity_buy = place_order.equity_1m_order(alice,[long_1m[i]],[Long_qty_1m[i]],'S')

            for i in range(len(short_1m)):

                if short_1m[i] in Open_trade_symbol:


                    response_equity_sell = place_order.equity_1m_order(alice,[short_1m[i]],[Short_qty_1m[i]],'B')

        

            print("-------- Position Close for 1min Equity successfully--------")

    

        if Option_1m == 1:

            #Closing order for 1m Option

            for i in range(len(option_1m_long_symbol)):
                
                if option_1m_long_symbol_str[i] in Open_trade_symbol:

                    response_option_long = place_order.option_order(t,alice,[option_1m_long_symbol[i]],'S',True)
	
            for i in range(len(option_1m_short_symbol)):

                if option_1m_short_symbol_str[i] in Open_trade_symbol:

                    response_option_short = place_order.option_order(t,alice,[option_1m_short_symbol[i]],'S',False)

    

            print("-------- Position Close for 1min Option successfully --------")
