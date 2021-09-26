from alice_blue import *

import pandas as pd

import time, datetime

from dateutil import relativedelta

import csv

from dateutil.relativedelta import relativedelta, TH

import math

import place_order

import functions

import sys

#path = '/home/abhishek/Freelance/anuj/'
path = '/home/ubuntu/Algorithm'
Input = pd.read_csv(f'{path}/input.csv',header=None)



if int((Input.loc[Input[0] == 'Start_Stop' ])[1]) == 0:

    sys.exit("Algorithm Stopped")

    exit()



if functions.Start_algo_check():

   pass





#User Credentials 

username ='393673'

password ='abhi@123'

api_secret ='9d6C2Iu8BHMKK6ntXE0W56AJLpbe1XqQr7GYHlGMbi9SUOCMpZcav3oICLZmAIxc'

api_id ='voz5NA1EEg'

code = 'AA'



#Access Token Generation

    

try:

    access_token=open(f'{path}/access_token.txt','r').read().strip()

    alice = AliceBlue(username=username, password=password, access_token=access_token, master_contracts_to_download=['NSE','NFO'])

except:        

    access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=code,  api_secret=api_secret,app_id = api_id)

    with open('./access_token.txt','w') as wr1:

        wr=csv.writer(wr1)

        wr.writerow([access_token])

    print("Access Token Generated")

    alice = AliceBlue(username='username', password='password', access_token=access_token, master_contracts_to_download=['NFO','NSE'])




#Read Input

Limit_1m = int((Input.loc[Input[0] == 'Qty_1m_trade' ])[1])

Limit_Intraday = int((Input.loc[Input[0] == 'Qty_Intraday' ])[1])



Equity_Multiplier = float((Input.loc[Input[0] == 'Equity_Multiplier'])[1])

Option_Multiplier = float((Input.loc[Input[0] == 'Option_Multiplier'])[1])

Margin = float((Input.loc[Input[0] == 'Margin' ])[1])



trade_1m = int((Input.loc[Input[0] == '1m_trade' ])[1])

Intraday = int((Input.loc[Input[0] == 'Intraday'])[1])



Equity_1m = int((Input.loc[Input[0] == '1m_Equity'])[1])

Option_1m = int((Input.loc[Input[0] == '1m_Option'])[1])

Intraday_Equity = int((Input.loc[Input[0] == 'Intraday_Equity'])[1])

Intraday_Option = int((Input.loc[Input[0] == 'Intraday_Option'])[1])



Strike_price = float((Input.loc[Input[0] == 'Strike'])[1])

Target = float((Input.loc[Input[0] == 'Target'])[1])

Stoploss = float((Input.loc[Input[0] == 'Stoploss'])[1])

Re_enter = float((Input.loc[Input[0] == 'Re_enter'])[1])


#-------------------------------------------Balance-------------------------

balance = alice.get_balance()

balance =float(balance['data']['cash_positions'][0]['net'])

print("------------------------Balance:-------------------------",balance)


if trade_1m == 1:

    if Equity_1m == 1 and Option_1m == 1:
    
        Equity_balance_1m = balance*Equity_Multiplier*Margin
        
        Option_balance_1m = balance*Option_Multiplier
    else:
        Equity_balance_1m = balance*Margin

        Option_balance_1m = 0
print(f"1m_trade balance E:{Equity_balance_1m} O:{Option_balance_1m}")

if Intraday == 1:
    if Intraday_Equity == 1 and Intraday_Option == 1:
    
        Intraday_Equity_balance = balance*Equity_Multiplier*Margin
        
        Intraday_Option_balance = balance*Option_Multiplier
    else:
        
        Intraday_Equity_balance = balance*Margin

        Intraday_Option_balance = 0
print(f"Intraday balance E:{Intraday_Equity_balance} O:{Intraday_Option_balance}")



#-------------------------------Option Expiry Date-------------------------------------

todayte = datetime.datetime.today()

cmon = todayte.month



t = todayte + relativedelta(weekday=TH(0))

if t.month > cmon:

    todayte = todayte + relativedelta(weekday=TH(0))

    cmon = t.month

for i in range(1, 6):

    t = todayte + relativedelta(weekday=TH(i))

    if t.month != cmon:

        # since t is exceeded we need last one  which we can get by subtracting -2 since it is already a Thursday.

        t = t + relativedelta(weekday=TH(-2))

        break



t = t.date()





history = {}

long_1m, short_1m = [],[]



#Checking for screening

if functions.market_open_screen():

    pass

#------------------- Open position Symbol--------------------
Open_trade_symbol = []
def open_trade():
    open_trades = alice.get_daywise_positions()['data']['positions'] 
    #open_trades = x['data']['positions'] 
    open_trades_symbol = []
    for i in open_trades:
        open_trades_symbol.append(i['trading_symbol'].split('-')[0])
    return open_trades_symbol
                    



#-------------------------------1 MINUTE TRADE -------------------------------





if trade_1m == 1:



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

    

    long_Stop_list_1m = [round(history[long_1m[i]]['Open']-history[long_1m[i]]['Open']*Stoploss*0.01,1) for i in range(len(long_1m))]

    short_Stop_list_1m = [round(history[short_1m[i]]['Open']*Stoploss*0.01+history[short_1m[i]]['Open'],1) for i in range(len(short_1m))]

    

    #1m Qty

    Long_qty_1m,Short_qty_1m = quantity(long_strike_list_1m,short_strike_list_1m,Equity_balance_1m)    

    

    

    #1m

    option_1m_long_symbol,option_1m_long_symbol_str,option_1m_short_symbol,option_1m_short_symbol_str = place_order.find_option(alice,t,history,long_1m,short_1m)



    if functions.market_open_check():

        
        time.sleep(3)
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

        orderplacetime = int(3) * 60 + int(46)

        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)

        print("Waiting for 9.16 AM , CURRENT TIME:{}".format(datetime.datetime.now()))

        Open_trade_symbol = open_trade()

        while timenow < orderplacetime:

            

            for symbol, values in live_data.items():

                

                

                try:

                    Data[symbol]['ltp'] = round(values['LTP'],1)

                except:

        

                    Data[symbol] ={'ltp':round(values['LTP'],1),'Traded-stoploss':False}

          

               #For Long

                for i in range(len(long_1m)):

                    

                    if symbol == long_1m[i] and symbol in Open_trade_symbol:

    

                        #Exiting Stoploss Option

                        if round(Data[symbol]['ltp'],1) == round((long_strike_list_1m[i]-long_Stop_list_1m[i]),1) and not Data[symbol]['Traded-stoploss']:

                            if Option_1m == 1 and option_1m_long_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_1m_long_symbol[i]],'S',True)

                            if Equity_1m == 1:

                                response_equity_buy = place_order.equity_1m_order(alice,long_1m,Long_qty_1m,'S')

                            

                            Data[symbol]['Traded-stoploss'] = True

                            #long_1m.pop(i)

                            #option_1m_long_symbol.pop(i)

                            print(f"Long:::::Stoploss Hit on:  {symbol}")

                            

                #For Short

                for i in range(len(short_1m)):

                    

                    if symbol == short_1m[i] and symbol in Open_trade_symbol:

                        #Exiting Stoploss Option

                        if round(Data[symbol]['ltp'],1) == round((short_strike_list_1m[i]+short_strike_list_1m[i]),1) and not Data[symbol]['Traded-stoploss']:

                            if Option_1m == 1 and option_1m_short_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_1m_short_symbol[i]],'S',True)

                            if Equity_1m == 1:

                                response_equity_buy = place_order.equity_1m_order(alice,long_1m,Long_qty_1m,'B')

                            

                            Data[symbol]['Traded-stoploss'] = True

                            

                            

                            print(f"Long:::::Stoploss Hit on:  {symbol}")

                          

                        #print("Checking on Short Trades")

            time.sleep(0.5)

            timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)

        

                        

    #Closing order for 1m Equity 

    
    time.sleep(5)
    if Equity_1m == 1:

        for i in range(len(long_1m)):

            if long_1m[i] in Open_trade_symbol:

                response_equity_buy = place_order.equity_1m_order(alice,[long_1m],[Long_qty_1m],'S')

        for i in range(len(short_1m)):

            if short_1m[i] in Open_trade_symbol:


                response_equity_sell = place_order.equity_1m_order(alice,[short_1m],[Short_qty_1m[i]],'B')

        

        print("-------- Position Close for 1min Equity successfully--------")

    

    if Option_1m == 1:

        #Closing order for 1m Option

        for i in range(len(option_1m_long)):

            if option_1m_long[i] in Open_trade_symbol:

                response_option_long = place_order.option_order(t,alice,[option_1m_long_symbol[i]],'S',True)
	
        for i in range(len(option_1m_short)):

            if option_1m_short[i] in Open_trade_symbol:

                response_option_short = place_order.option_order(t,alice,[option_1m_short_symbol[i]],'S',False)

    

        print("-------- Position Close for 1min Option successfully --------")

else:

    print("----------------1m Trade is disable-------------------")

    

time.sleep(5)  

#-------------------------INTRADAY----------------------------  

    

    

if Intraday == 1:

    

    to_long_symbol, to_short_symbol = [], []

    for symbol, values in live_data.items():

        try:

            history[symbol]

        except:

            history[symbol] ={'Open': values['Open'], 'High': values['High'], 'Low': values['Low'], 'LTP': values['LTP'], 'Close': values['Close'],'Traded':False}

        #print(symbol,history[symbol])

    

    

        #Intraday To-long 

        if len(to_long_symbol) <= Limit_Intraday-1:

            

            #values['Open'] == values['Low'] and

            if values['LTP'] > 300 and  round(values['Open'],1) == round(values['Low'],1) and not history[symbol]['Traded']:

                # print("Buy :", symbol, f" at {values['LTP']} and Time {datetime.datetime.now().time()}")

                history[symbol]['Traded'] = True

                to_long_symbol.append(symbol)

        

        #Intraday To-Short

        if len(to_short_symbol) < Limit_Intraday:

            

            #values['Open'] == values['High'] and

            if values['LTP'] > 300 and round(values['Open'],1) == round(values['High'],1) and not history[symbol]['Traded']:

        

                # print("Sell :", symbol, f" at {values['LTP']} and Time {datetime.datetime.now().time()}")

                history[symbol]['Traded'] = True    

                to_short_symbol.append(symbol)  

    

    

    print(f"Intraday Trade----Stock to long {to_long_symbol} and Stock to short {to_short_symbol} ")

    long_ltp_list = [round(history[to_long_symbol[i]]['Open'],1) for i in range(len(to_long_symbol))]

    short_ltp_list = [round(history[to_short_symbol[i]]['Open'],1) for i in range(len(to_short_symbol))]

    long_strike_list = [round(history[to_long_symbol[i]]['Open']*Strike_price*0.01+history[to_long_symbol[i]]['Open'],1) for i in range(len(to_long_symbol))]

    short_strike_list = [round(history[to_short_symbol[i]]['Open']-history[to_short_symbol[i]]['Open']*Strike_price*0.01,1) for i in range(len(to_short_symbol))]

    long_squareoff_list = [round(history[to_long_symbol[i]]['Open']*Target*0.01,1) for i in range(len(to_long_symbol))]

    short_squareoff_list = [round(history[to_short_symbol[i]]['Open']*Target*0.01,1) for i in range(len(to_short_symbol))]

    long_stoploss_list = [round(history[to_long_symbol[i]]['Open']*Stoploss*0.01,1) for i in range(len(to_long_symbol))]

    short_stoploss_list = [round(history[to_short_symbol[i]]['Open']*Stoploss*0.01,1) for i in range(len(to_short_symbol))]

    long_re_enter_list = [round(history[to_long_symbol[i]]['Open']*Re_enter*0.01,1) for i in range(len(to_long_symbol))]

    short_re_enter_list = [round(history[to_short_symbol[i]]['Open']*Re_enter*0.01,1) for i in range(len(to_short_symbol))]



    Long_qty_Intraday,Short_qty_Intraday = quantity(long_strike_list,short_strike_list,Intraday_Equity_balance)

       

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

         

    Open_trade_symbol = open_trade()

    def long_trail_stop_loss(entry,close):

        initalSL = round(entry - (entry*0.2*0.01),2)

        trail = round(entry*0.2*0.01,2)

        forwardMove = round(entry*0.2*0.01,2)

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

        initalSL = round(entry + (entry*0.2*0.01))

        trail = round(entry*0.2*0.01,2)

        forwardMove = round(entry*0.2*0.01,2)

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

    while True:

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

                    if round(Data[symbol]['ltp'],1) == round((long_ltp_list[i]),1) and Data[symbol]['Traded-stoploss']  and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'B',True)

                        if Intraday_Equity == 1:

                            place_order.equity_order(alice,[to_long_symbol[i]],[long_strike_list[i]],[long_stoploss_list[i]],[long_squareoff_list[i]],[Long_qty_Intraday[i]*2],'B')

                        Data[symbol]['Traded-stoploss'] = False

                        print(f"Long:::::Stoploss Re-entering trade on {symbol}")

                        

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

                    elif round(Data[symbol]['ltp'],1) == round((long_ltp_list[i]-long_stoploss_list[i]),1) and not Data[symbol]['Traded-stoploss'] and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'S',True)

                        Data[symbol]['Traded-stoploss'] = True

                        print(f"Long:::::Stoploss Hit on:  {symbol}")

                        

                    #Exiting Traget Option

                    elif round(Data[symbol]['ltp'],1) == round((long_squareoff_list[i]+long_ltp_list[i]),1) and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'S',True)

                        Data[symbol]['Traded-strike'] = True

                        print(f"Long:::::Target of {Target}% Achieved on:  {symbol}")

                    

                    #Re-Enter with trailing stop loss for Equity and Option

                    elif round(Data[symbol]['ltp'],1) == round((long_ltp_list[i]+long_re_enter_list[i]),1) and not Data[symbol]['Traded-reenter'] and Data[symbol]['Traded-strike']:

                        if Intraday_Equity == 1:

                        

                            place_order.equity_re_enter_order(alice,[to_long_symbol[i]],[Long_qty_Intraday[i]],'B')

                        if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_long_symbol[i]],'B',True)    

                        

                        Data[symbol]['Traded-reenter'] = True

                        

                        print(f"Long:::::Rentering Trade with Trailing on Symbol:{symbol}")

                    elif Data[symbol]['Traded-reenter'] and not Data[symbol]['Trade-completed']:

                        

                        SL = long_trail_stop_loss(round(long_ltp_list[i]+long_re_enter_list[i],1),Data[symbol]['ltp'])

                        

                        if SL == "Hit":

                            if Intraday_Equity == 1:

                                place_order.equity_re_enter_order(alice,[to_long_symbol[i]],[Long_qty_Intraday[i]],'S')

                            if Intraday_Option == 1 and option_long_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_long_symbol[i]],'S',True)    

                            #to_long_symbol.pop(i)
                            Data[symbol]['Trade-completed'] = True

                            print(f"Long:::::Trailing Stoploss Hit on Symbol:{symbol}")

            

            #For Short

            for i in range(len(to_short_symbol)):

                

                if symbol == to_short_symbol[i] and symbol in Open_trade_symbol:

                      

                    #print("Checking on Short Trades")

                    #Stoploss Re-enter 

                    if round(Data[symbol]['ltp'],1) == round((short_ltp_list[i]),1) and Data[symbol]['Traded-stoploss'] and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'B',False)

                        if Intraday_Equity == 1:

                            place_order.equity_order(alice,[to_short_symbol[i]],[short_strike_list[i]],[short_stoploss_list[i]],[short_squareoff_list[i]],[Short_qty_Intraday[i]*2],'S')

                        Data[symbol]['Traded-stoploss'] = False

                        print(f"Short:::::Stoploss Re-entering trade on {symbol}")

                        

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

                    elif round(Data[symbol]['ltp'],1) == round((short_ltp_list[i]+short_stoploss_list[i]),1) and not Data[symbol]['Traded-stoploss'] and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'S',False)

                        Data[symbol]['Traded-stoploss'] = True

                        print(f"Short:::::Stoploss Hit on:  {symbol}")

                        

                    #Exiting Traget Option

                    elif round(Data[symbol]['ltp'],1) == round((short_squareoff_list[i]-short_ltp_list[i]),1) and not Data[symbol]['Traded-strike']:

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'S',False)

                        Data[symbol]['Traded-strike'] = True

                        print(f"Short:::::Target of {Target}% Achieved on:  {symbol}")

                    

                    #Enter with trailing stop loss Equity

                    elif round(Data[symbol]['ltp'],1) == round((short_ltp_list[i]-short_re_enter_list[i]),1) and not Data[symbol]['Traded-reenter'] and Data[symbol]['Traded-strike']:

                        

                        if Intraday_Equity == 1:

                            place_order.equity_re_enter_order(alice,[to_short_symbol[i]],[Short_qty_Intraday[i]*2],'S')

                        if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                            place_order.option_order(t,alice,[option_short_symbol[i]],'B',False)    

                        Data[symbol]['Traded-reenter'] = True

                        print(f"Short:::::Rentering Trade with Trailing on Symbol:{symbol}")

                    

                    elif Data[symbol]['Traded-reenter'] and not Data[symbol]['Trade-completed']:

                        

                        SL = short_trail_stop_loss(round(short_ltp_list[i]-short_re_enter_list[i],1),Data[symbol]['ltp'])

                        

                        if SL == "Hit":

                            if Intraday_Equity == 1:

                                place_order.equity_re_enter_order(alice,[to_short_symbol[i]],[Short_qty_Intraday[i]],'B')

                            if Intraday_Option == 1 and option_short_symbol_str[i] in Open_trade_symbol:

                                place_order.option_order(t,alice,[option_short_symbol[i]],'S',False)    

                            Data[symbol]['Trade-completed'] = True

                            print(f"Short:::::Trailing Stoploss Hit on Symbol:{symbol}")

        time.sleep(0.5)

    

        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)

# =============================================================================

        if timenow > market_close:

            print("Market is Closed")

            break

# =============================================================================

else:

    print("---Intraday is Disable---")


