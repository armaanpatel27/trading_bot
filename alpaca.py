import alpaca_trade_api as tradeapi
import threading
class Wallet:
    def __init__(self):

       
        self.api = tradeapi.REST(key_id= self.PUB_KEY, secret_key=self.SEC_KEY, base_url=self.BASE_URL) # For real trading, don't enter a base_url

    def buy(stock_name, quantity):
    # Buy a stock

        self.api.submit_order(
            symbol=str(stock_name), # Replace with the ticker of the stock you want to buy
            qty=int(quantity),
            side='buy',
            type='market', 
            time_in_force='gtc' # Good 'til cancelled
        )
        return f"Bought {quantity} {stock_name}"

        

