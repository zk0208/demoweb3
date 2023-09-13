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
from tenacity import retry, stop_after_attempt, retry_if_exception_type

# crypto list


# crypto symbol
bitstampCryptoList = ['BTC/USDT','ETH/USDT','XRP/USDT','DOGE/USD','ADA/USD','SOL/USD']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def bitstampCandleSticks(db, bitstamp, cryptolists, timeStart, time_interval):
    # bitstamp = ccxt.bitstamp({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bitstamp.load_markets()

    # timeStart = bitstamp.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if bitstamp.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (bitstamp.rateLimit / 1000)      # time.sleep wants seconds
            reslists = bitstamp.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, bitstamp.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def bitstampCryptoInfo(db, bitstamp, cryptolists):
    # bitstamp = ccxt.bitstamp({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bitstamp.load_markets()

    if bitstamp.has['fetchTickers']:
        time.sleep (bitstamp.rateLimit / 1000)      # time.sleep wants seconds
        reslists = bitstamp.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, bitstamp, cryptolists)
        bitstampHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def bitstampHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    #  bitstamp = ccxt.bitstamp({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bitstamp.load_markets()
    # bitstampCandleSticks(demo, bitstamp, bitstampCryptoList)
    # bitstampCryptoInfo(demo, bitstamp, bitstampCryptoList)
    demo.dbClose()


