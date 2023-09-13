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
bitfinexCryptoList = ['BTC/USDT','ETH/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def bitfinexCandleSticks(db, bitfinex, cryptolists, timeStart, time_interval):
    # bitfinex = ccxt.bitfinex({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bitfinex.load_markets()

    # timeStart = bitfinex.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if bitfinex.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (bitfinex.rateLimit / 1000 * 2)      # time.sleep wants seconds
            reslists = bitfinex.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, bitfinex.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def bitfinexCryptoInfo(db, bitfinex, cryptolists):
    # bitfinex = ccxt.bitfinex({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bitfinex.load_markets()

    if bitfinex.has['fetchTickers']:
        time.sleep (bitfinex.rateLimit / 1000)      # time.sleep wants seconds
        reslists = bitfinex.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, bitfinex, cryptolists)
        bitfinexHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def bitfinexHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    #  bitstamp = ccxt.bitstamp({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # bitstamp.load_markets()
    # bitfinexCandleSticks(demo, bitfinex, bitfinexCryptoList)
    # bitfinexCryptoInfo(demo, bitfinex, bitfinexCryptoList)
    demo.dbClose()

