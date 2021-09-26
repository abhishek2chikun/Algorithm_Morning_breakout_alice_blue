from alice_blue import *
import csv


path = '/home/abhishek/Freelance/anuj/new'
path = '/home/ubuntu/new'


def equity_order(alice, Stock_symbol_list,Price_list,Stoploss_list,Target_list,qty,Type):
    if Type == 'B':
        order_type = TransactionType.Buy
    else:
        order_type = TransactionType.Sell

    response_list = {}
    for i in range(len(Stock_symbol_list)):
        stock_name = alice.get_instrument_by_symbol("NSE", Stock_symbol_list[i])
        response = alice.place_order(transaction_type = order_type,
                         instrument = stock_name,
                         quantity = qty[i],
                         order_type = OrderType.Limit,
                         product_type = ProductType.BracketOrder,
                         price = Price_list[i],
                         trigger_price = None,
                         stop_loss = Stoploss_list[i],
                         square_off = Target_list[i],
                         trailing_sl = None,
                         is_amo = False)
        print("Order placed for:",response)

        response_list[stock_name] = response
    return response_list

def equity_1m_order(alice, Stock_symbol_list,qty,Type):
    if Type == 'B':
        order_type = TransactionType.Buy
    else:
        order_type = TransactionType.Sell

    response_list = {}
    for i in range(len(Stock_symbol_list)):
        stock_name = alice.get_instrument_by_symbol("NSE", Stock_symbol_list[i])
        response = alice.place_order(transaction_type = order_type,
                         instrument = stock_name,
                         quantity = qty[i],
                         order_type = OrderType.Market,
                         product_type = ProductType.Intraday,
                         price = 0.0,
                         trigger_price = None,
                         stop_loss = None,
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False)
        print("Order placed for:",response)

        response_list[stock_name] = response  
    return response_list


def equity_re_enter_order(alice, Stock_symbol_list,qty,Type):
    if Type == 'B':
        order_type = TransactionType.Buy
    else:
        order_type = TransactionType.Sell

    response_list = {}
    for i in range(len(Stock_symbol_list)):
        stock_name = alice.get_instrument_by_symbol("NSE", Stock_symbol_list[i])
        response = alice.place_order(transaction_type = order_type,
                         instrument = stock_name,
                         quantity = qty[i],
                         order_type = OrderType.Market,
                         product_type = ProductType.Intraday,
                         price = 0.0,
                         trigger_price = None,
                         stop_loss = None,
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False)
        print("Order placed for:",response)

        response_list[stock_name] = response
    return response_list

def option_order(t,alice, Stock_symbol_list,Type,flage):
    if Type == 'B':
        order_type = TransactionType.Buy
    else:
        order_type = TransactionType.Sell

    response_list = {}
    for i in range(len(Stock_symbol_list)):
        
        stock_name  = alice.get_instrument_for_fno(symbol = Stock_symbol_list[i][1], expiry_date=t, is_fut=False, strike=Stock_symbol_list[i][0], is_CE = flage)
        qty = int(stock_name.lot_size)
        response = alice.place_order(transaction_type = order_type,
                         instrument = stock_name,
                         quantity = qty,
                         order_type = OrderType.Limit,
                         product_type = ProductType.Delivery,
                         price = 0.0,
                         trigger_price = None,
                         stop_loss = None,
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False)
        print("Order placed for:",stock_name)

        response_list[stock_name] = response

    return response_list


#---------Find Option Symbol-----------
def find_option(alice,t,history,to_long_symbol,to_short_symbol):
    count_flag = []
    import pandas as pd
    for i in range(2):
        if i == 0:
            option_list = to_long_symbol
            option_long_symbol = []
            option_long_str =[]
        else:
            count_flag = []
            option_short_symbol = []
            option_short_str = []
            option_list = to_short_symbol
        for n,j in enumerate(option_list):
            option_instruments = alice.search_instruments('NFO',j)
            df = pd.DataFrame(option_instruments)
            df = df.loc[df.expiry == t]
            temp =list(df.symbol)
            
            
            x= round(history[option_list[n]]['Open'])
           
            for k in range(1,len(str(x))):
                mul = pow(10,k)
                if i == 0:
                    x=x-x%mul 
                else:
                    x=x+(pow(10,k)-x%mul)
                instruments=df[df.symbol.str.startswith(f"{j} {(t.strftime('%B')[:3]).upper()} {x}")]
                #print(instruments)
                if(len(instruments)) == 2:
                    Year =  instruments.iloc[0].expiry.year
                    count_flag.append(True)
                    if i ==0:
                        option_long_symbol.append([x,j])
                        option_long_str.append(instruments.iloc[0]['symbol'])
                    else:
                        option_short_symbol.append([x,j])
                        option_short_str.append(instruments.iloc[1]['symbol'])
                    break
                
        if sum(count_flag) == len(option_list):
            print("Done!!")
            
        else:
            print("Something Went Wrong!!")

    option_long_str_new ,option_short_str_new= [], []
    for j in range(2):
        if j == 0:
            option_str = option_long_str
        else:
            option_str = option_short_str
        for i in option_str:
            x = i.split(' ')
            if j == 0:
                option_long_str_new.append(x[0]+str(Year)[-2:]+x[1]+str(int(float(x[2])))+x[3])
            else:
                option_short_str_new.append(x[0]+str(Year)[-2:]+x[1]+str(int(float(x[2])))+x[3])
    return (option_long_symbol,option_long_str_new,option_short_symbol,option_short_str_new)



#----------------------------------------------Login--------------------------------

def login():

    #User Credentials 


    with open('/home/abhishek/Algo/cred.txt','r') as f:
        username=f.readline().split('=')[1]
        password=f.readline().split('=')[1]
        api_secret=f.readline().split('=')[1]
        api_id=f.readline().split('=')[1]
        key=f.readline().split('=')[1]


    #Access Token Generation

        

    try:

        access_token=open(f'{path}/access_token.txt','r').read().strip()

        alice = AliceBlue(username=username, password=password, access_token=access_token, master_contracts_to_download=['NSE','NFO'])

    except:        

        access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=key,  api_secret=api_secret,app_id = api_id)

        with open('./access_token.txt','w') as wr1:

            wr=csv.writer(wr1)

            wr.writerow([access_token])

        print("Access Token Generated")

        alice = AliceBlue(username='username', password='password', access_token=access_token, master_contracts_to_download=['NFO','NSE'])

    return alice

#----------------------------------------------Calculate Qty--------------------------------

def quantity(long,short,balance):

    qty_long,qty_short = [],[]

    try:

        per_share = balance/(len(long)+len(short))
        max_price = max(long+short)
        
        if max_price > per_share:
            per_share = balance/(len(long)+len(short) + 1)
        print(f"Balance:{balance} -----  Per Share Price:{per_share}")
    except:

        return (0,0)
    count = 0
    for x in range(2):

        if x == 0:

            t=long

        else:

            t=short
        
        
        for price in t:

            for i in range(10000):

                if price*i < per_share:

                    pass

                else:

                    if x == 0 :
                        if i==1:
                            qty_long.append(1)
                            count += price*1
                        elif price*i > per_share:
                            qty_long.append(i-1)
                            count += price*(i-1)
                        else:
                            qty_long.append(i)
                            count += price*i
                        #print(f"price:{price*i} qty:{i} Total:{count}")
                    elif x == 1:
                        if  i == 1:
                            qty_short.append(1)
                            count += price*1
                        elif price*i > per_share:
                            qty_short.append(i-1)
                            count += price*(i-1)
                        else:
                            qty_short.append(i)
                            count += price*i
                        #print(f"price:{price*i} qty:{i} Total:{count}")
                    break

            
    print("Total Amount will be Traded:",count)
    return (qty_long,qty_short) 



#------------------- Open position Symbol--------------------
Open_trade_symbol = []
def open_trade(alice):
    open_trades = alice.get_daywise_positions()['data']['positions'] 
    #open_trades = x['data']['positions'] 
    open_trades_symbol = []
    for i in open_trades:
        #print(i['trading_symbol'].split('-'))
        symbol = i['trading_symbol'].split('-')[:-1]
        sym=''
        for i in symbol:
            sym+=i
        #print(sym) 
        open_trades_symbol.append(sym)
    return open_trades_symbol
                    
'''option_1m_long_symbol_strike,option_1m_short_symbol_strike = [],[]
option_long_symbol_strike,option_short_symbol_strike = [],[]
def find_strike(option_short_symbol_strike,option_list):
    for i in option_list:
        x = str(i).split(' ')
        x = x[0]+str(t.day)+x[1]+str(t.year)[-2:]+str(x[2]).split('.')[0]+x[3]
        x= option_strike.loc[option_strike.symbol.str.startswith(x)]
        option_short_symbol_strike.append(x.strike/100)
find_strike(option_short_symbol_strike,option_short_symbol)    '''
