import ccxt
import os
import sys
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # print(DIR_BASE)
sys.path.append(DIR_BASE) 
import ccxtAPI.config as cof
import datetime
import time

datastr = '2023-07-24 00:00:00'
dateArray = datetime.datetime.strptime(datastr, '%Y-%m-%d %H:%M:%S')
date = int(dateArray.timestamp() * 1000)
print(date)

a = datetime.datetime.fromtimestamp(date / 1000) + datetime.timedelta(hours=1)
print(a)

file = open('./text.txt','a+')



# binance = ccxt.binance()    #
# binance= ccxt.binance({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# binance.load_markets()
# symbols = binance.symbols
# file.write('binance : ' + str(symbols))

# coinbase = ccxt.coinbase() # 需要APIKEY
# coinbase= ccxt.coinbase({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# coinbase.load_markets()
# symbols = coinbase.symbols
# file.write('coinbase : ' + str(symbols))

# kraken= ccxt.kraken({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# kraken.load_markets()
# symbols = kraken.symbols
# file.write(str(symbols))

# bybit= ccxt.bybit({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# bybit.load_markets()
# symbols = bybit.symbols
# file.write('bybit : ' + str(symbols))

# kucoin = ccxt.kucoin()      #
# kucoin= ccxt.kucoin({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# kucoin.load_markets()
# symbols = kucoin.symbols
# file.write('kucoin : ' + str(symbols))

okx = ccxt.okx()            #
okx= ccxt.okx({
    'proxies' : cof.proxy,
    'enableRateLimit' : True,
    'timeout' : 30000,
})      #
okx.load_markets()
symbols = okx.symbols
file.write('okx : ' + str(symbols))
okx.fetch_ohlcv()

# bitstamp = ccxt.bitstamp()  
# bitstamp= ccxt.bitstamp({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# bitstamp.load_markets()
# symbols = bitstamp.symbols
# file.write('bitstamp : ' + str(symbols))

# bitfinex = ccxt.bitfinex()
# bitfinex= ccxt.bitfinex({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# bitfinex.load_markets()
# symbols = bitfinex.symbols
# file.write('bitfinex : ' + str(symbols))

# gateio = ccxt.gateio()      #
# gateio= ccxt.gateio({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# gateio.load_markets()
# symbols = gateio.symbols
# file.write('gateio : ' + str(symbols))

# huobi = ccxt.huobi()        #
# huobi= ccxt.huobi({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# huobi.load_markets()
# symbols = huobi.symbols
# file.write('huobi : ' + str(symbols))

# gemini = ccxt.gemini() 
# gemini= ccxt.gemini({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# gemini.load_markets()
# symbols = gemini.symbols
# file.write('gemini : ' + str(symbols))

# gemini = ccxt.gemini() 
# okx= ccxt.okx({
#     'proxies' : cof.proxy,
#     'enableRateLimit' : True,
#     'timeout' : 30000,
# })      #
# okx.load_markets()
# symbols = okx.symbols
# file.write('okx : ' + str(symbols))