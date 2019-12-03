import ccxt
import time
from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt

def get_latest_candles():
    """Returns the hourly candles data from the last 720 hours"""
    exchange = ccxt.kraken({'enableRateLimit': True})
    # Fetch hourly OHLCV (Open High Low Close Volume) data from last 720 hours (30 days)
    price_history = exchange.fetch_ohlcv ('BTC/USD', '1h')
    time.sleep(exchange.rateLimit / 1000)
    price_history = np.array(price_history)
    # Sort by the timestamp (first column) in case of errors
    price_history = price_history[price_history[:,0].argsort()]
    return price_history[:,1:]



price_history = get_latest_candles()


plt.plot(price_history[:,1])
plt.show()

