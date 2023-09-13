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
coinbaseCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def coinbaseCandleSticks(db, coinbase, cryptolists, timeStart, time_interval):
    # coinbase = ccxt.coinbase({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # coinbase.load_markets()

    # timeStart = coinbase.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if coinbase.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (coinbase.rateLimit / 1000)      # time.sleep wants seconds
            reslists = coinbase.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, coinbase.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def coinbaseCryptoInfo(db, coinbase, cryptolists):
    # coinbase = ccxt.coinbase({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # coinbase.load_markets()

    if coinbase.has['fetchTickers']:
        time.sleep (coinbase.rateLimit / 1000)      # time.sleep wants seconds
        reslists = coinbase.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, coinbase, cryptolists)
        coinbaseHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def coinbaseHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    coinbase = ccxt.coinbase({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    coinbase.load_markets()
    coinbaseCandleSticks(demo, coinbase, coinbaseCryptoList)
    coinbaseCryptoInfo(demo, coinbase, coinbaseCryptoList)
    demo.dbClose()
