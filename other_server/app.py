import alpaca_trade_api as tradeapi
import numpy as np
import time
from datetime import datetime
from alpaca_trade_api.rest import REST, TimeFrame
import matplotlib.pyplot as plt
import requests
import queue


from flask import Flask, render_template, request
app = Flask(__name__)

def getChange(stock):
    api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL) # For real trading, don't enter a base_url


    symb = stock
    pos_held = False
    total_profit = 0
    profit_array = queue.Queue()
    # Add five zeros to the queue
    for _ in range(10):
        profit_array.put(0)
    start_price = 0
    count = 0
    hours = 15
    while True:
        print("")
        print("Checking Price")
        market_data = api.get_bars(symb, timeframe = TimeFrame.Minute, limit=5, start=f"2024-03-08T14:{str(10 + count)}:00Z", end=f"2024-03-08T14:{str(15 + count)}:00Z") # Get one bar object for each of the past 5 minutes
        close_list = [] # This array will store all the closing prices from the last 5 minutes
        for bar in market_data:
            close_list.append(bar.c) # bar.c is the closing price of that bar's time interval

        close_list = np.array(close_list, dtype=np.float64) # Convert to numpy array
        ma = np.mean(close_list)
        last_price = close_list[4] # Most recent closing price

        print("Moving Average: " + str(ma))
        print("Last Price: " + str(last_price))


        
        if ma + 0.1 > last_price and not pos_held: # If MA is more than 10cents under price, and we haven't already bought
            print("Buy")
            # api.submit_order(
            #     symbol=symb,
            #     qty=1,
            #     side='buy',
            #     type='market',
            #     time_in_force='gtc'
            # )
            start_price = last_price # we would want to change this to reflect actual, bought price since prices fluctuate and we need to find buyer

            pos_held = True
            # if bought, may need to halt function running until buy goes through
        elif ma - 0.1 < last_price and pos_held: # If MA is more than 10cents above price, and we already bought
            print("Sell")
            # api.submit_order(
            #     symbol=symb,
            #     qty=1,
            #     side='sell',
            #     type='market',
            #     time_in_force='gtc'
            # )
            #update profit
            total_profit += last_price - start_price
            total_profit =  float("{:.2f}".format(total_profit))
            pos_held = False
        count += 1
        print(f"Total profit: {total_profit}")
        profit_array.put(total_profit)
        profit_array.get()
        if count == 44:
            break     
        profit_list = list(profit_array.queue)   
        request = {
            "name": "Armaan",
            "URL": "doesn't matter",
            "Profit": ','.join(str(_) for _ in profit_list)
            # [3,4,5,6]
            #"3,4,5,6"
        }

        response = requests.get(url = "ipAddressHere", json=request)
        time.sleep(5)   



if __name__ == '__main__':
    balance = getChange("SPY")
    app.run(host="0.0.0.0", port=34002)

