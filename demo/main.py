# coding=utf-8

import ccxt
import os
import sys
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(DIR_BASE)
sys.path.append(DIR_BASE) 
import ccxtAPI.config as conf
import exchange
from exchange import *
import sql
from tenacity import retry, stop_after_attempt, retry_if_exception_type
import datetime

exListNeedAPIKey = ['coinbase']
exList = [ 'okx']
# exList = ['binance', 'kraken', 'bybit', 'kucoin','okx', 'bitstamp','bitfinex','gateio',]

@retry(stop=stop_after_attempt(5), retry=retry_if_exception_type(ccxt.NetworkError), reraise=True)
def exconn(exchangeID):
    exClass = getattr(ccxt, exchangeID)
    ex = exClass({
        'proxies' : conf.proxy,
        'enableRateLimit' : True,
        'timeout' : 30000,
    })
    ex.load_markets()
    return ex

if __name__ == '__main__':
    demo = sql.dbconn()
    for exID in exList:
        try:
            ex = exconn(exID)
        except Exception as err:
            print('find error : {0}'.format(err))
        

        moudle = getattr(exchange, exID)
        cryptoList = getattr(moudle, exID+'CryptoList')
        candelInput = getattr(moudle, exID+'CandleSticks')
        # cryptoInput = getattr(moudle, exID+'CryptoInfo')

        # try:
        #     # candelInput(demo, ex, cryptoList)
        #     cryptoInput(demo, ex, cryptoList)
        #     print(exID + ' done!')
        # except Exception as err:
        #     print('find error : {0}'.format(err))
        #     print('retry fail!')
        #     continue

        startArray = conf.dateArray1
        startT = conf.startTimeSatmp
        endT = conf.endTimeSatmp
        t = startT
        while t < endT:
            candelInput(demo, ex, cryptoList, t, '1m')
            startArray = startArray + datetime.timedelta(hours = 1)
            t = int(startArray.timestamp() * 1000)
        print(exID + "finish insert lists...")
    demo.dbClose()

    # # binance
    # ex = ccxt.binance({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # binance.binanceCandleSticks(demo, ex, binance.binanceCryptoList)
    # binance.binanceCryptoInfo(demo, ex, binance.binanceCryptoList)
    # print("binance done!")

    # bitfinex
    # ex = ccxt.bitfinex({
    #     'proxies' : conf.proxy,                  
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # bitfinex.bitfinexCandleSticks(demo, ex, bitfinex.bitfinexCryptoList)
    # bitfinex.bitfinexCryptoInfo(demo, ex, bitfinex.bitfinexCryptoList)
    # print("bitfinex done!")

    # # bitstamp
    # ex = ccxt.bitstamp({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # bitstamp.bitstampCandleSticks(demo, ex, bitstamp.bitstampCryptoList)
    # bitstamp.bitstampCryptoInfo(demo, ex, bitstamp.bitstampCryptoList)
    # print("bitstamp done!")

    # # bybit
    # ex = ccxt.bybit({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # bybit.bybitCandleSticks(demo, ex, bybit.bybitCryptoList)
    # bybit.bybitCryptoInfo(demo, ex, bybit.bybitCryptoList)
    # print("bybit done!")

    # # gateio
    # ex = ccxt.gateio({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # gateio.gateioCandleSticks(demo, ex, gateio.gateioCryptoList)
    # gateio.gateioCryptoInfo(demo, ex, gateio.gateioCryptoList)
    # print("gateio done!")

    # # gemini
    # ex = ccxt.gemini({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # gemini.geminiCandleSticks(demo, ex, gemini.geminiCryptoList)
    # gemini.geminiCryptoInfo(demo, ex, gemini.geminiCryptoList)
    # print("gemini done!")

    # # huobi
    # ex = ccxt.huobi({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # huobi.huobiCandleSticks(demo, ex, huobi.huobiCryptoList)
    # huobi.huobiCryptoInfo(demo, ex, huobi.huobiCryptoList)
    # print("huobi done!")

    # # kraken
    # ex = ccxt.kraken({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # kraken.krakenCandleSticks(demo, ex, kraken.krakenCryptoList)
    # kraken.krakenCryptoInfo(demo, ex, kraken.krakenCryptoList)
    # print("kraken done!")

    # # kucoin
    # ex = ccxt.kucoin({
    #     'proxies' : conf.proxy,
    #     'enableRateLimit' : True,
    #     'timeout' : 30000,
    #     }) 
    # ex.load_markets()
    # kucoin.kucoinCandleSticks(demo, ex, kucoin.kucoinCryptoList)
    # kucoin.kucoinCryptoInfo(demo, ex, kucoin.kucoinCryptoList)
    # print("kucoin done!")