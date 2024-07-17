

# # authentication and connection details

import alpaca_trade_api as tradeapi
import numpy as np
import time
from datetime import datetime
from alpaca_trade_api.rest import REST, TimeFrame
import matplotlib.pyplot as plt



api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL) # For real trading, don't enter a base_url


symb = "SPY"
pos_held = False
total_profit = 0
proft_array = []
start_price = 0
count = 0
hours = 14
while True:
    print("")
    print("Checking Price")
    market_data = api.get_bars(symb, timeframe = TimeFrame.Minute, limit=5, start=f"2024-03-08T14:{str(30 + count)}:00Z", end=f"2024-03-08T14:{str(35 + count)}:00Z") # Get one bar object for each of the past 5 minutes
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
        total_profit += (last_price - start_price)  
        pos_held = False
    count += 1
    print(f"Total profit: {total_profit}")
    proft_array.append(total_profit)
    if count == 10:
        break
    time.sleep(5)   
# Plotting the total profit
plt.figure(figsize=(12, 6))
plt.plot(proft_array, label='Total Profit', color='blue')
plt.title('Total Profit Over Time')
plt.xlabel('Iteration')
plt.ylabel('Total Profit ($)')
plt.ylim(min(proft_array) - 0.5, max(proft_array) + 0.5)
plt.legend()
plt.grid(True)
plt.pause(1) 
plt.show()

