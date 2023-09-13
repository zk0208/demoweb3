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
geminiCryptoList = ['BTC/USDT','ETH/USDT','XRP/USD','DOGE/USD','SOL/USD']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def geminiCandleSticks(db, gemini, cryptolists, timeStart, time_interval):
    # gemini = ccxt.gemini({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # gemini.load_markets()

    # timeStart = gemini.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if gemini.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (gemini.rateLimit / 1000)      # time.sleep wants seconds
            reslists = gemini.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, gemini.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def geminiCryptoInfo(db, gemini, cryptolists):
    # gemini = ccxt.gemini({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # gemini.load_markets()

    if gemini.has['fetchTickers']:
        time.sleep (gemini.rateLimit / 1000)      # time.sleep wants seconds
        reslists = gemini.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, gemini, cryptolists)
        geminiHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def geminiHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    gemini = ccxt.gemini({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    gemini.load_markets()
    geminiCandleSticks(demo, gemini, geminiCryptoList)
    geminiCryptoInfo(demo, gemini, geminiCryptoList)
    demo.dbClose()
