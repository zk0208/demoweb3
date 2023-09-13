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
huobiCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT']

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def huobiCandleSticks(db, huobi, cryptolists, timeStart, time_interval):
    # huobi = ccxt.huobi({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # huobi.load_markets()

    # timeStart = huobi.milliseconds() - 3600 * 10000 # five minutes before
    # time_interval = '1m'

    if huobi.has['fetchOHLCV']:
        for i, crypto in enumerate(cryptolists) :
            time.sleep (huobi.rateLimit / 1000)      # time.sleep wants seconds
            reslists = huobi.fetch_ohlcv(crypto, timeframe= time_interval, since= timeStart, limit = 60)
            data = util.dataListChangeCandle(reslists, huobi.name, crypto, time_interval)
            db.insertDB(sql.sqlCommandCandle, data)

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def huobiCryptoInfo(db, huobi, cryptolists):
    # huobi = ccxt.huobi({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # huobi.load_markets()

    if huobi.has['fetchTickers']:
        time.sleep (huobi.rateLimit / 1000)      # time.sleep wants seconds
        reslists = huobi.fetch_tickers(cryptolists)
        data, ranking = util.dataListChangeCrypto(reslists, huobi, cryptolists)
        huobiHotRanking(db, ranking)
        db.insertDB(sql.sqlCommandCrypto, data)

def huobiHotRanking(db, list):
    db.insertDB(sql.sqlCommandRanking, list)

if __name__ == '__main__':
    demo = sql.dbconn()
    huobi = ccxt.huobi({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    huobi.load_markets()
    huobiCandleSticks(demo, huobi, huobiCryptoList)
    huobiCryptoInfo(demo, huobi, huobiCryptoList)
    demo.dbClose()




'''
huobi :
'''