import os
import sys
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(DIR_BASE)
sys.path.append(DIR_BASE) 
import sql
import time
import ccxt


# crypto symbol
okxCryptoList = ['BTC/USDT','ETH/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','SOL/USDT','TRX/USDT',
                 'ETH/BTC','XRP/BTC','ADA/BTC','SOL/BTC','TRX/BTC','DOGE/BTC']
if __name__ == '__main__':
    demo = sql.dbconn()
    okx = ccxt.okx({
        # 'apiKey': 'YOUR_API_KEY',
        # 'secret': 'YOUR_SECRET',
        'enableRateLimit' : True,
        'timeout' : 30000,
        }) 
    okx.load_markets()

    # k line data
    if okx.has['fetchOHLCV']:
        timeStart = okx.milliseconds() - 3600 * 10000   # five minutes before
        for i, crypto in enumerate(okxCryptoList) :
            time.sleep (okx.rateLimit / 1000)
            klists = okx.fetch_ohlcv(crypto, timeframe= '1m', since= timeStart, limit = 60)

    # price data
    if okx.has['fetchTickers']:
        time.sleep (okx.rateLimit / 1000)      # time.sleep wants seconds
        pricelists = okx.fetch_tickers(okxCryptoList)
    
    # insert to db
    demo.insertDB(sql.sqlCommandCandle, klists)

    demo.dbClose()

