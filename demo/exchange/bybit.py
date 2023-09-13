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
bybitCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def bybitCandleSticks(db, bybit, cryptolists, timeStart, time_interval):
    # bybit = ccxt.bybit({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bybit.load_markets()

    # timeStart = bybit.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if bybit.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (bybit.rateLimit / 1000)      # time.sleep wants seconds
            reslists = bybit.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, bybit.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def bybitCryptoInfo(db, bybit, cryptolists):
    # bybit = ccxt.bybit({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bybit.load_markets()

    if bybit.has['fetchTickers']:
        time.sleep (bybit.rateLimit / 1000)      # time.sleep wants seconds
        reslists = bybit.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, bybit, cryptolists)
        bybitHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def bybitHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)
       

if __name__ == '__main__':
    demo = sql.dbconn()
    # bybit = ccxt.bybit({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bybit.load_markets()
    # bybitCandleSticks(demo, bybit, bybitCryptoList)
    # bybitCryptoInfo(demo, bybit, bybitCryptoList)
    demo.dbClose()





    