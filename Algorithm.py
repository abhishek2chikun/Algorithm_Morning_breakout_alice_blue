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

import Fun_Intraday,Fun_1m

#path = '/home/abhishek/Freelance/anuj/new'
path = '/home/ubuntu/new'

Input = pd.read_csv(f'{path}/input.csv',header=None)



if int((Input.loc[Input[0] == 'Start_Stop' ])[1]) == 0:

    sys.exit("Algorithm Stopped")

    exit()



if functions.Start_algo_check():

   pass




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
Stoploss_1m = float((Input.loc[Input[0] == 'Stoploss_1m'])[1])
Trailing_Stoploss = float((Input.loc[Input[0] == 'Trailing_SL'])[1])
Re_enter = float((Input.loc[Input[0] == 'Re_enter'])[1])


alice = place_order.login()


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

#Checking for screening

if functions.market_open_screen():

    pass





#-------------------------------1 MINUTE TRADE -------------------------------



if trade_1m == 1:

    Fun_1m.fun_1m(alice,t,Equity_1m,Option_1m,Limit_1m,Stoploss_1m,Equity_balance_1m)

else:

    print("----------1m Trade is disable------------")

if functions.place_order_check():
    pass

time.sleep(5)  


#-------------------------INTRADAY----------------------------  

if Intraday == 1:

    

    Fun_Intraday.fun_Intraday(alice,t ,Intraday_Equity,Intraday_Option,Limit_Intraday, Strike_price,Target,Stoploss,Trailing_Stoploss,Re_enter,Intraday_Equity_balance,Intraday_Option_balance)

else:

    print("---Intraday is Disable---")


