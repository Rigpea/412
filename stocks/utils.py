import alpaca_trade_api as tradeapi
import pandas as pd
from django.conf import settings
from .models import TradeLog


def fetch_stock_data(symbol, start_date, end_date):
    """
    Fetch historical stock data from Alpaca using the IEX feed.
    """
    api = tradeapi.REST(
        settings.ALPACA_API_KEY,
        settings.ALPACA_SECRET_KEY,
        settings.ALPACA_BASE_URL,
        api_version="v2"
    )

    barset = api.get_bars(
        symbol=symbol,
        timeframe="1Day",
        start=start_date,
        end=end_date,
        feed="iex" 
    )
    data = barset.df
    data['symbol'] = symbol
    return data
def moving_average_strategy(data):
    """
    Decide whether to buy, sell, or hold based on moving average crossover strategy.
    """
    data['SMA_20'] = data['close'].rolling(window=20).mean() 
    data['SMA_50'] = data['close'].rolling(window=50).mean()  


    data['signal'] = 0
    data.loc[data['SMA_20'] > data['SMA_50'], 'signal'] = 1 
    data.loc[data['SMA_20'] < data['SMA_50'], 'signal'] = -1  
    return data

def execute_trade(api, stock_symbol, action, amount):
    """
    Perform a buy or sell action using Alpaca's API.
    Log the trade in the database.
    """
    try:
        if action == "buy":
            order = api.submit_order(
                symbol=stock_symbol,
                qty=amount,
                side="buy",
                type="market",
                time_in_force="gtc"
            )
        elif action == "sell":
            order = api.submit_order(
                symbol=stock_symbol,
                qty=amount,
                side="sell",
                type="market",
                time_in_force="gtc"
            )
        # Log the trade
        TradeLog.objects.create(
            stock_symbol=stock_symbol,
            action=action,
            quantity=amount,
            order_id=order.id,
            status=order.status
        )
    except Exception as e:
        print(f"Error executing {action} order for {stock_symbol}: {e}")