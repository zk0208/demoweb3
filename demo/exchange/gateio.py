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
gateioCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def gateioCandleSticks(db, gateio, cryptolists, timeStart, time_interval):
    # gateio = ccxt.gateio({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # gateio.load_markets()

    # timeStart = gateio.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if gateio.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (gateio.rateLimit / 1000)      # time.sleep wants seconds
            reslists = gateio.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, gateio.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def gateioCryptoInfo(db, gateio, cryptolists):
    # gateio = ccxt.gateio({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # gateio.load_markets()

    if gateio.has['fetchTickers']:
        time.sleep (gateio.rateLimit / 1000)      # time.sleep wants seconds
        reslists = gateio.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, gateio, cryptolists)
        gateioHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def gateioHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    gateio = ccxt.gateio({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    gateio.load_markets()
    gateioCandleSticks(demo, gateio, gateioCryptoList)
    gateioCryptoInfo(demo, gateio, gateioCryptoList)
    demo.dbClose()

