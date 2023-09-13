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

# exchanges  conn

# crypto symbol
kucoinCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def kucoinCandleSticks(db, kucoin, cryptolists, timeStart, time_interval):
    # kucoin = ccxt.kucoin({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # kucoin.load_markets()

    # timeStart = kucoin.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if kucoin.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (kucoin.rateLimit / 1000)      # time.sleep wants seconds
            reslists = kucoin.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, kucoin.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def kucoinCryptoInfo(db, kucoin, cryptolists):
    # kucoin = ccxt.kucoin({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # kucoin.load_markets()

    if kucoin.has['fetchTickers']:
        time.sleep (kucoin.rateLimit / 1000)      # time.sleep wants seconds
        reslists = kucoin.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, kucoin, cryptolists)
        kucoinHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def kucoinHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    kucoin = ccxt.kucoin({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    kucoin.load_markets()
    kucoinCandleSticks(demo, kucoin, kucoinCryptoList)
    kucoinCryptoInfo(demo, kucoin, kucoinCryptoList)
    demo.dbClose()


