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
import datetime
from tenacity import retry, stop_after_attempt, retry_if_exception_type


# exchanges  conn

# crypto symbol
okxCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT',
                 'ETH/BTC','XRP/BTC','ADA/BTC','SOL/BTC','TRX/BTC','DOGE/BTC']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def okxCandleSticks(db, okx, cryptolists, timeStart, time_interval):
    # okx = ccxt.okx({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # okx.load_markets()

    # timeStart = okx.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if okx.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (okx.rateLimit / 1000)      # time.sleep wants seconds
            reslists = okx.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, okx.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def okxCryptoInfo(db, okx, cryptolists):
    # okx = ccxt.okx({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # okx.load_markets()

    if okx.has['fetchTickers']:
        time.sleep (okx.rateLimit / 1000)      # time.sleep wants seconds
        reslists = okx.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, okx, cryptolists)
        okxHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def okxHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def okxCandleHotRank(db, okx, cryptolists, timeStart, time_interval):
    # okx = ccxt.okx({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # okx.load_markets()

    # timeStart = okx.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if okx.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (okx.rateLimit / 1000)      # time.sleep wants seconds
            reslists = okx.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeRank(reslists, okx.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandRanking, data) 

if __name__ == '__main__':
    demo = sql.dbconn()
    okx = ccxt.okx({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    okx.load_markets()
    # okxCandleSticks(demo, okx, okxCryptoList)
    # okxCryptoInfo(demo, okx, okxCryptoList)

    startArray = conf.dateArray1
    startT = conf.startTimeSatmp
    endT = conf.endTimeSatmp
    t = startT
    while t < endT:
        okxCandleHotRank(demo, okx, okxCryptoList, t, '1m')
        startArray = startArray + datetime.timedelta(hours = 1)
        t = int(startArray.timestamp() * 1000)
        print('okx' + "finish insert lists...")
    demo.dbClose()