import ccxt
import os
import sys
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # print(DIR_BASE)
sys.path.append(DIR_BASE) 
import sql
import util
import pandas as pd
import time
import datetime

# proxies setting

proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

#   start time & time interval
datastr1 = '2023-08-20 00:00:00'
datastr2 = '2023-09-01 00:00:00'
dateArray1 = datetime.datetime.strptime(datastr1, '%Y-%m-%d %H:%M:%S')
# dateArray1 = dateArray1 + datetime.timedelta(hours=1)
dateArray2 = datetime.datetime.strptime(datastr2, '%Y-%m-%d %H:%M:%S')
startTimeSatmp = int(dateArray1.timestamp() * 1000)
endTimeSatmp = int(dateArray2.timestamp() * 1000)

# print(startTimeSatmp)

# a = datetime.datetime.fromtimestamp(startTimeSatmp / 1000) 
# print(a)

# timeInterval = '1m'

# exchanges  conn

"""
    binance = ccxt.binance()    #
    coinbase = ccxt.coinbase() 
    kraken = ccxt.kraken()      #
    bybit = ccxt.bybit()        #
    kucoin = ccxt.kucoin()      #
    okx = ccxt.okx()            #
    bitstamp = ccxt.bitstamp()  
    bitfinex = ccxt.bitfinex()
    gateio = ccxt.gateio()      #
    huobi = ccxt.huobi()        #
    gemini = ccxt.gemini()
"""

exchangelist = ['binance', 'coinbase', 'kraken', 'bybit', 'kucoin', 'okx', 'bitstamp', 'bitfinex', 'gate', 'huobi']

# crypto symbol
cryptoList = ['BTC/USDT','ETH/BTC','BNB/BTC','XRP/BTC','DOGE/BTC','ADA/BTC','SOL/BTC','TRX/BTC']

# if __name__ == '__main__' :
#     demo = sql.dbconn()
#     for exchangeID in exchangelist[2:-1] :
#         exchangeClass = getattr(ccxt, exchangeID)
#         exchange = exchangeClass({
#             'proxies' : proxy,
#             'enableRateLimit' : True,
#             'timeout' : 30000,
#         })
#         exchange = ccxt.okx()
#         exchange.load_markets()
#         timeStart = exchange.milliseconds() - 3600 * 10000 # five minutes before
#         time_interval = '1m'
#         if exchange.has['fetchOHLCV']:
#             for i, crypto in enumerate(cryptoList) :
#                 time.sleep (exchange.rateLimit / 1000)      # time.sleep wants seconds
#                 reslists = exchange.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 2)
#                 data = util.dataListChangeCandle(reslists, exchange, crypto, time_interval)
#                 res = demo.insertDB(sql.sqlCommandCandle, data)
            