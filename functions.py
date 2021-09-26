
import datetime
import time

def Start_algo_check():
    market_open = int(3) * 60 + int(43)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Waiting for 9.13 AM , CURRENT TIME:{}".format(datetime.datetime.now()))



    while timenow < market_open:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Algorithm Started, CURRENT TIME:{}".format(datetime.datetime.now()))

    return True
def market_open_check():
    market_open = int(3) * 60 + int(45)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Waiting for 9.15 AM , CURRENT TIME:{}".format(datetime.datetime.now()))



    while timenow < market_open:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Market is Open!!, Started Placing Order, CURRENT TIME:{}".format(datetime.datetime.now()))

    return True
def market_open_screen():
    market_open = int(3) * 60 + int(45)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Waiting for 9.15 AM , CURRENT TIME:{}".format(datetime.datetime.now()))



    while timenow < market_open:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Market is Open!!, Started Screening, CURRENT TIME:{}".format(datetime.datetime.now()))

    return True


def place_order_check():
    market_open = int(3) * 60 + int(46)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Waiting for 9.16 AM , CURRENT TIME:{}".format(datetime.datetime.now()))



    while timenow < market_open:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print("Intraday will be starting after 5 second!!!!!!!, CURRENT TIME:{}".format(datetime.datetime.now()))

