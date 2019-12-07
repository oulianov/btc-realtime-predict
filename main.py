import ccxt
import time
from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
from pylab import rcParams

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


rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(price_history[:,1], model='additive', freq=24)
fig = decomposition.plot()

plt.show()

import itertools

p = range(0, 2)
pdq = list(itertools.product(p, p, p))
seasonal_pdq = list(itertools.product(p, p, p, p, p, p))

smallest_aic = 10E99
best_res = None
best_param = None

for param in pdq:
	for param_seasonal in pdq:
		model_param = param + (param_seasonal,)
		model = sm.tsa.statespace.SARIMAX(price_history[:,1], trend='c', order=model_param)
		res = model.fit(disp=False)
		if res.aic < smallest_aic:
			print(res.aic)
			smallest_aic = res.aic
			best_res = res
			best_param = model_param


mod = sm.tsa.statespace.SARIMAX(price_history[:,2], trend='c', order=(1, 1, (1, 1, 1)))
res = mod.fit(disp=False)
print(res.summary())

res.forecast(100)
res.aic
price_history[:,2]
