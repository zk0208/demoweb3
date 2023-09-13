import ccxt
import os
import sys
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(DIR_BASE)
sys.path.append(DIR_BASE) 
import ccxtAPI.config as conf
import sql
import util
import time
import  urllib3
from tenacity import retry, stop_after_attempt, retry_if_exception_type

# exchanges  conn

# crypto symbol
krakenCryptoList = ['BTC/USDT','ETH/BTC','XRP/BTC','DOGE/BTC','ADA/BTC','SOL/BTC','TRX/BTC']


@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def krakenCandleSticks(db, kraken, cryptolists, timeStart, time_interval):
    # kraken = ccxt.kraken({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # kraken.load_markets()

    # timeStart = kraken.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if kraken.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (kraken.rateLimit / 1000)      # time.sleep wants seconds
            reslists = kraken.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, kraken.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def krakenCryptoInfo(db, kraken, cryptolists):
    # kraken = ccxt.kraken({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # kraken.load_markets()

    if kraken.has['fetchTickers']:
        time.sleep (kraken.rateLimit / 1000)      # time.sleep wants seconds
        reslists = kraken.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, kraken, cryptolists)
        krakenHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def krakenHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    kraken = ccxt.kraken({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    kraken.load_markets()
    krakenCandleSticks(demo, kraken, krakenCryptoList)
    krakenCryptoInfo(demo, kraken, krakenCryptoList)
    demo.dbClose()
