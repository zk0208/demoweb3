import pymysql
import numpy as np
import pandas as pd

# sql connect & settings

class dbconn():
    def __init__(self) :
        self.sqlConnect = pymysql.connect(
            # host= '127.0.0.1',
            # user= 'root',
            # passwd= 'MySQL1234#',
            # port= 3306,
            # db= 'web3_exchange_data',
            # charset= 'utf8mb4'
            host="gateway01.us-west-2.prod.aws.tidbcloud.com",
            port=4000,
            user="4D3vpXsNRNzveru.root",
            password="RUphmFj41kDATFSi",
            database="web3_exchange_data",
            # ssl_mode="VERIFY_IDENTITY",
            ssl= {
                "ca": "/etc/ssl/cert.pem"
            }
            )
        self.cursor = self.sqlConnect.cursor()
    
    def insertDB(self, sql, datalist):
        try:
            if len(datalist) > 0 and isinstance(datalist[0], (tuple,list)) == False :
                self.cursor.execute(sql, datalist)
            else :
                self.cursor.executemany(sql, datalist)
        except:
            self.sqlConnect.rollback()
        else:
            self.sqlConnect.commit()
        # print("finish insert lists...")

    def dbClose(self):
        self.cursor.close()
        self.sqlConnect.close()
# 之前的数据可能存在问题，需要改一下
sqlCommandCandle = "INSERT INTO index_candlesticks \
(exchange,instid,time,open_price,high_price,low_price,close_price,time_interal) \
VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"

sqlCommandCrypto = "INSERT INTO crypto_info \
(exchange,instid,update_time,curr_price,base_volume) \
VALUES(%s,%s,%s,%s,%s);"

sqlCommandRanking = "INSERT INTO hot_ranking \
(instid,time,hot_score) \
VALUES(%s,%s,%s);"

if __name__ == '__main__':
    demo = dbconn()
    demo.insertDB(sqlCommandCandle,[('c','b','2020-09-08 12:09:23',1,2,3,4,'1m')])
    # demo.insertDB(sqlCommandCrypto,[('c','b','2020-09-08 12:09:23',1,2),('c','b','2020-09-08 12:09:25',1,4)])
    # demo.insertDB(sqlCommandRanking,[('c','2020-09-08 12:09:26',1),('d','2020-09-08 12:09:26',1)])
    demo.dbClose()