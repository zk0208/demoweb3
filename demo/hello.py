import http.client
import json
import pymysql


conn = http.client.HTTPSConnection("api.coinbase.com")
payload = ''
headers = {
  'Content-Type': 'application/json'
}
conn.request("GET", "/api/v3/brokerage/products/XRP-USDC", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

print("hello python")

# coding=utf-8

import time
import okx.MarketData as MarketData
import MySQLdb

connection = MySQLdb.connect(
    host="gateway01.us-west-2.prod.aws.tidbcloud.com",
    port=4000,
    user="4D3vpXsNRNzveru.root",
    password="RUphmFj41kDATFSi",
    database="",
    ssl_mode="VERIFY_IDENTITY",
    ssl={
      "ca": "/etc/ssl/cert.pem"
      }
    )

def run_sql(conn, sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()
    pass


def get_datetime_by_timestamp(timestamp):
    time_array = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

def insert_one_row_to_db(exchange,instid, timestamp, open_price, close_price, high_price, low_price):
    sql = "insert ignore into web3_exchange_data.index_candlesticks (exchange, instid, time, open_price, close_price, high_price, low_price) values "
    sql = sql + '(\"'+exchange+'\",\"'+instid+'\",\"'+timestamp+ '\",'+open_price+','+close_price+','+high_price+','+low_price+');'
    print(sql)
    return run_sql(connection, sql)


api_key = "e8a5e0db-bbbd-4d6a-aa05-cfcdfd4ed1dd"
secret_key = "87116A76A8ADD36BEEA9FF2ACC1FE2A1"
passphrase = "okx123A"

flag = "0"
exchange = "okx"
instId="BTC-USD"

marketDataAPI =  MarketData.MarketAPI(flag=flag)

result = marketDataAPI.get_index_candlesticks(
    instId=instId
)

for item in result['data']:
    if len(item) != 6:
        continue
    timestamp = item[0]
    open_price = item[1]
    high_price = item[2]
    low_price = item[3]
    close_price = item[4]
    confirmed = item[5]
    insert_one_row_to_db(exchange, instId, get_datetime_by_timestamp(int(timestamp)/1000), open_price, close_price, high_price, low_price)
    #print(item)
