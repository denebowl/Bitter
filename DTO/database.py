import datetime
from threading import Thread
from time import sleep
from typing import Dict

import cymysql
from cymysql import OperationalError

from DTO.crypto import Crypto
from DTO.trade import Trade
from Singleton import GlobalData


class MysqlDatabase:
    def __init__(self):
        self.uploadDelay = 1
        self.updateTime = datetime.datetime.now()
        self.nextUploadData: Dict[str, Trade] = {}

        try:
            self.dbConn = cymysql.connect(host='192.168.10.100', user='bitter', passwd='6@ZybieSJg]8Z7^5u4y(',
                                          db='bitter',
                                          charset='utf8')
            print("DB Connected.")
        except OperationalError:
            print("DB Connection Failed.")
            return
        self.dbCursor = self.dbConn.cursor()

        # 테이블이 없는 경우를 대비해서 생성
        for crypto in GlobalData.cryptos.values():
            self.createTableIfNeeds(crypto)
        self.dbConn.commit()

        # Upload TimerTask
        thread = Thread(target=self.InsertDB)
        thread.daemon = True
        thread.start()

    def createTableIfNeeds(self, crypto: Crypto):
        tableName = ('trade_' + crypto.code).lower()
        sql = 'CREATE TABLE IF NOT EXISTS`' \
              + tableName + \
              '` (' \
              '`timestamp` bigint NOT NULL,' \
              '`datetime` DATETIME DEFAULT NULL,' \
              '`opening_price` double DEFAULT NULL,' \
              '`high_price` double DEFAULT NULL,' \
              '`low_price` double DEFAULT NULL,' \
              '`trade_price` double DEFAULT NULL,' \
              '`prev_closing_price` double DEFAULT NULL,' \
              '`acc_trade_price` double DEFAULT NULL,' \
              '`change` varchar(8) DEFAULT NULL,' \
              '`change_price` double DEFAULT NULL,' \
              '`signed_change_price` double DEFAULT NULL,' \
              '`change_rate` double DEFAULT NULL,' \
              '`signed_change_rate` double DEFAULT NULL,' \
              '`ask_bid` varchar(8) DEFAULT NULL,' \
              '`trade_volume` double DEFAULT NULL,' \
              '`acc_trade_volume` double DEFAULT NULL,' \
              '`acc_ask_volume` double DEFAULT NULL,' \
              '`acc_bid_volume` double DEFAULT NULL,' \
              '`highest_52_week_price` double DEFAULT NULL,' \
              '`highest_52_week_date` varchar(10) DEFAULT NULL,' \
              '`lowest_52_week_price` double DEFAULT NULL,' \
              '`lowest_52_week_date` varchar(10) DEFAULT NULL,' \
              '`trade_status` varchar(99) DEFAULT NULL,' \
              '`market_state` varchar(99) DEFAULT NULL,' \
              '`market_state_for_ios` varchar(99) DEFAULT NULL,' \
              '`is_trading_suspended` tinyint DEFAULT NULL,' \
              '`delisting_date` varchar(10) DEFAULT NULL,' \
              '`market_warning` varchar(99) DEFAULT NULL,' \
              '`acc_trade_price_24h` double DEFAULT NULL,' \
              '`acc_trade_volume_24h` double DEFAULT NULL,' \
              '`stream_type` varchar(99) DEFAULT NULL,' \
              'PRIMARY KEY (`timestamp`)' \
              ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'
        self.dbCursor.execute(sql)

    def addUploadData(self, tradeData: Trade):
        # nextUploadData.Clear() 이 후 처음 들어오는 데이터만 저장함.
        if tradeData.crypto_code not in self.nextUploadData:
            self.nextUploadData[tradeData.crypto_code] = tradeData

    def InsertSQL(self, tradeData: Trade):
        tableName = ('trade_' + tradeData.crypto_code).lower()
        # sql = 'insert into ' + tableName \
        sql = 'REPLACE into ' + tableName \
              + '(' \
                '`timestamp`, ' \
                '`datetime`, ' \
                '`opening_price`, ' \
                '`high_price`, ' \
                '`low_price`, ' \
                '`trade_price`, ' \
                '`prev_closing_price`, ' \
                '`acc_trade_price`, ' \
                '`change`, ' \
                '`change_price`, ' \
                '`signed_change_price`, ' \
                '`change_rate`, ' \
                '`signed_change_rate`, ' \
                '`ask_bid`, ' \
                '`trade_volume`, ' \
                '`acc_trade_volume`, ' \
                '`acc_ask_volume`, ' \
                '`acc_bid_volume`, ' \
                '`highest_52_week_price`, ' \
                '`highest_52_week_date`, ' \
                '`lowest_52_week_price`, ' \
                '`lowest_52_week_date`, ' \
                '`trade_status`, ' \
                '`market_state`, ' \
                '`market_state_for_ios`, ' \
                '`is_trading_suspended`, ' \
                '`delisting_date`, ' \
                '`market_warning`, ' \
                '`acc_trade_price_24h`, ' \
                '`acc_trade_volume_24h`, ' \
                '`stream_type`' \
                ')' \
                ' values (' \
              + '"' + str(tradeData.timestamp) + '",' \
              + '"' + str(tradeData.datetime) + '", ' \
              + '"' + str(tradeData.opening_price) + '", ' \
              + '"' + str(tradeData.high_price) + '", ' \
              + '"' + str(tradeData.low_price) + '", ' \
              + '"' + str(tradeData.trade_price) + '", ' \
              + '"' + str(tradeData.prev_closing_price) + '", ' \
              + '"' + str(tradeData.acc_trade_price) + '", ' \
              + '"' + str(tradeData.change) + '", ' \
              + '"' + str(tradeData.change_price) + '", ' \
              + '"' + str(tradeData.signed_change_price) + '", ' \
              + '"' + str(tradeData.change_rate) + '", ' \
              + '"' + str(tradeData.signed_change_rate) + '", ' \
              + '"' + str(tradeData.ask_bid) + '", ' \
              + '"' + str(tradeData.trade_volume) + '", ' \
              + '"' + str(tradeData.acc_trade_volume) + '", ' \
              + '"' + str(tradeData.acc_ask_volume) + '", ' \
              + '"' + str(tradeData.acc_bid_volume) + '", ' \
              + '"' + str(tradeData.highest_52_week_price) + '", ' \
              + '"' + str(tradeData.highest_52_week_date) + '", ' \
              + '"' + str(tradeData.lowest_52_week_price) + '", ' \
              + '"' + str(tradeData.lowest_52_week_date) + '", ' \
              + '"' + str(tradeData.trade_status) + '", ' \
              + '"' + str(tradeData.market_state) + '", ' \
              + '"' + str(tradeData.market_state_for_ios) + '", ' \
              + '"' + str(1 if tradeData.is_trading_suspended else 0) + '", ' \
              + '"' + str(tradeData.delisting_date) + '", ' \
              + '"' + str(tradeData.market_warning) + '", ' \
              + '"' + str(tradeData.acc_trade_price_24h) + '", ' \
              + '"' + str(tradeData.acc_trade_volume_24h) + '", ' \
              + '"' + str(tradeData.stream_type) + '")'
        self.dbCursor.execute(sql)

    def InsertDB(self):
        while True:
            if len(self.nextUploadData) > 0:
                tempDuplication = self.nextUploadData.copy()
                uploaded = 0
                for key, item in tempDuplication.items():
                    self.InsertSQL(item)
                    uploaded += 1
                self.dbConn.commit()
                print('Database upload cryptos trading data.', uploaded)
            self.nextUploadData.clear()
            sleep(30)  # Database 업로드 간격
