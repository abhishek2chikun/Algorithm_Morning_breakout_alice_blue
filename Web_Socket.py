import json
from alice_blue import *
import pandas as pd
import time
import place_order
import datetime

#path = '/home/abhishek/Freelance/anuj/new'
path = '/home/ubuntu/new'

alice = place_order.login()


nifty_50 = pd.read_csv(f'{path}/ind_nifty50list.csv')
instrument_list = list(nifty_50.Symbol)




socket_opened = False
live_data = {}

nifty_50 = pd.read_csv(f'{path}/ind_nifty50list.csv')


def event_handler_quote_update(message):

    live_data[message['instrument'].symbol] = {"Open": message['open'],

                                            "High": message["high"],

                                            "Low": message["low"],

                                            "LTP": message["ltp"],

                                            "Close": message["close"],

                                            }



def open_callback():

    global socket_opened

    socket_opened = True



alice.start_websocket(subscribe_callback=event_handler_quote_update,

                    socket_open_callback=open_callback,

                    run_in_background=True)



while not socket_opened:

    print("Connecting to WebSocket...")

    time.sleep(1)

    pass



alice.subscribe([alice.get_instrument_by_symbol("NSE", i) for i in instrument_list], LiveFeedType.MARKET_DATA)





while len(live_data.keys()) != len(instrument_list):

    continue



print("Connected to web socket....")
colums = ['Open', 'High', 'Low', 'LTP', 'Close']
df_8 = pd.DataFrame(columns=colums)

i = 0
def Start_websocket():
    market_open = int(3) * 60 + int(38)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Waiting for 9.08 AM , CURRENT TIME:{}".format(datetime.datetime.now()))



    while timenow < market_open:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Algorithm Started, CURRENT TIME:{}".format(datetime.datetime.now()))

    return True

if Start_websocket():
    json_object = json.dumps(live_data, indent = 4)
    with open("/home/ubuntu/new/Data_9_8.json", "w") as outfile:
        outfile.write(json_object)

#time.sleep(60*5)

while True:
    json_object = json.dumps(live_data, indent = 4)
    with open("/home/ubuntu/new/Data_live.json", "w") as outfile:
        outfile.write(json_object)
    time.sleep(1)
    print("Saved at:",datetime.datetime.now())


# while i<50:
#     for symbol, values in live_data.items():

#         df_8.loc[i] = values
#     i+=1
# df_8.index = instrument_list
# df_8.to_csv('Data_9_8.csv')
# print("-------------Data saved for 9_8")

# #time.sleep(60*6)

# df = pd.DataFrame(columns=colums)

# while True:
#     i=0
#     df = pd.DataFrame(columns=colums)
#     for symbol, values in live_data.items():

#         df.loc[i] = values
#         i+=1
#     df.index = instrument_list
#     df.to_csv('Data_live.csv')
#     print("Saved")
#     time.sleep(1)
    
