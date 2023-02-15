import time
from datetime import datetime, timedelta
from typing import List

identifier = -1


class Trade:

    def __init__(self, dictionaryData):
        global identifier
        identifier = (identifier + 1) if (identifier < 9) else 0

        # 기본키로 시스템 타임 사용함.
        # -------------------------------------------------------------------------------
        self.timestamp = dictionaryData['trade_timestamp']  # 실제 거래 타임
        # self.timestamp = str.format('{0}{1}', round(time.time() * 1000), identifier) #시스템 타임
        self.datetime = datetime.fromtimestamp(self.timestamp / 1000)

        # -------------------------------------------------------------------------------
        self.code = dictionaryData['code']
        self.opening_price = dictionaryData['opening_price']
        self.high_price = dictionaryData['high_price']
        self.low_price = dictionaryData['low_price']
        self.trade_price = dictionaryData['trade_price']
        self.prev_closing_price = dictionaryData['prev_closing_price']
        self.acc_trade_price = dictionaryData['acc_trade_price']
        self.change = dictionaryData['change']
        self.change_price = dictionaryData['change_price']
        self.signed_change_price = dictionaryData['signed_change_price']
        self.change_rate = dictionaryData['change_rate']
        self.signed_change_rate = dictionaryData['signed_change_rate']
        self.ask_bid = dictionaryData['ask_bid']
        self.trade_volume = dictionaryData['trade_volume']
        self.acc_trade_volume = dictionaryData['acc_trade_volume']
        # self.trade_date = dictionaryData['trade_date']
        # self.trade_time = dictionaryData['trade_time']
        self.acc_ask_volume = dictionaryData['acc_ask_volume']
        self.acc_bid_volume = dictionaryData['acc_bid_volume']
        self.highest_52_week_price = dictionaryData['highest_52_week_price']
        self.highest_52_week_date = dictionaryData['highest_52_week_date']
        self.lowest_52_week_price = dictionaryData['lowest_52_week_price']
        self.lowest_52_week_date = dictionaryData['lowest_52_week_date']
        #self.trade_status = dictionaryData['trade_status']
        self.market_state = dictionaryData['market_state']
        #self.market_state_for_ios = dictionaryData['market_state_for_ios']
        self.is_trading_suspended = dictionaryData['is_trading_suspended']
        self.delisting_date = dictionaryData['delisting_date']
        self.market_warning = dictionaryData['market_warning']
        self.timestamp = dictionaryData['timestamp']
        self.acc_trade_price_24h = dictionaryData['acc_trade_price_24h']
        self.acc_trade_volume_24h = dictionaryData['acc_trade_volume_24h']
        self.stream_type = dictionaryData['stream_type']

        # addon
        self.crypto_code = self.code.split('-')[1]
        self.trade_volume_price = round(self.trade_volume * self.trade_price / 10000, 1)


class TradeAnalysis:
    def __init__(self):
        self.price_prev = None
        self.rate_prev = None
        self.price_1s = None
        self.rate_1s = None
        self.price_3s = None
        self.rate_3s = None
        self.price_5s = None
        self.rate_5s = None
        self.price_15s = None
        self.rate_15s = None
        self.price_30s = None
        self.rate_30s = None
        self.price_1m = None
        self.rate_1m = None
        self.price_3m = None
        self.rate_3m = None
        self.price_5m = None
        self.rate_5m = None
        self.price_15m = None
        self.rate_15m = None
        self.price_30m = None
        self.rate_30m = None
        self.price_1h = None
        self.rate_1h = None
        self.price_4h = None
        self.rate_4h = None
        self.price_1d = None
        self.rate_1d = None

        self.trade_price_3s = 0
        self.trade_price_5s = 0

    def reset(self):
        self.price_prev = None
        self.rate_prev = None
        self.price_1s = None
        self.rate_1s = None
        self.price_3s = None
        self.rate_3s = None
        self.price_5s = None
        self.rate_5s = None
        self.price_15s = None
        self.rate_15s = None
        self.price_30s = None
        self.rate_30s = None
        self.price_1m = None
        self.rate_1m = None
        self.price_3m = None
        self.rate_3m = None
        self.price_5m = None
        self.rate_5m = None
        self.price_15m = None
        self.rate_15m = None
        self.price_30m = None
        self.rate_30m = None
        self.price_1h = None
        self.rate_1h = None
        self.price_4h = None
        self.rate_4h = None
        self.price_1d = None
        self.rate_1d = None

        self.trade_price_3s = 0
        self.trade_price_5s = 0

    def update(self, trades: List[Trade]):
        self.reset()

        if len(trades) < 2:
            return 0

        nowPrice = trades[0].trade_price
        oldPrice = trades[1].trade_price
        self.price_prev = nowPrice - oldPrice
        self.rate_prev = self.price_prev / oldPrice * 100

        for trade in trades:
            deltaTimeSec = (trades[0].datetime - trade.datetime).seconds
            if self.price_1s is None and deltaTimeSec >= 1:
                self.price_1s = nowPrice - trade.trade_price
                self.rate_1s = (self.price_1s / trade.trade_price) * 100
            if self.price_3s is None and deltaTimeSec >= 3:
                self.price_3s = nowPrice - trade.trade_price
                self.rate_3s = (self.price_3s / trade.trade_price) * 100
            if self.price_5s is None and deltaTimeSec >= 5:
                self.price_5s = nowPrice - trade.trade_price
                self.rate_5s = (self.price_5s / trade.trade_price) * 100
            if self.price_15s is None and deltaTimeSec >= 15:
                self.price_15s = nowPrice - trade.trade_price
                self.rate_15s = (self.price_15s / trade.trade_price) * 100
            if self.price_30s is None and deltaTimeSec >= 30:
                self.price_30s = nowPrice - trade.trade_price
                self.rate_30s = (self.price_30s / trade.trade_price) * 100
            if self.price_1m is None and deltaTimeSec >= 60:
                self.price_1m = nowPrice - trade.trade_price
                self.rate_1m = (self.price_1m / trade.trade_price) * 100
            if self.price_3m is None and deltaTimeSec >= 180:
                self.price_3m = nowPrice - trade.trade_price
                self.rate_3m = (self.price_3m / trade.trade_price) * 100
            if self.price_5m is None and deltaTimeSec >= 300:
                self.price_5m = nowPrice - trade.trade_price
                self.rate_5m = (self.price_5m / trade.trade_price) * 100
            if self.price_15m is None and deltaTimeSec >= 900:
                self.price_15m = nowPrice - trade.trade_price
                self.rate_15m = (self.price_15m / trade.trade_price) * 100
            if self.price_30m is None and deltaTimeSec >= 1800:
                self.price_30m = nowPrice - trade.trade_price
                self.rate_30m = (self.price_30m / trade.trade_price) * 100
            if self.price_1h is None and deltaTimeSec >= 3600:
                self.price_1h = nowPrice - trade.trade_price
                self.rate_1h = (self.price_1h / trade.trade_price) * 100
            if self.price_4h is None and deltaTimeSec >= 14400:
                self.price_4h = nowPrice - trade.trade_price
                self.rate_4h = (self.price_4h / trade.trade_price) * 100
            if self.price_1d is None and deltaTimeSec >= 86400:
                self.price_1d = nowPrice - trade.trade_price
                self.rate_1d = (self.price_1d / trade.trade_price) * 100

            if deltaTimeSec <= 3:
                self.trade_price_3s += trades[0].trade_volume_price
            if deltaTimeSec <= 5:
                self.trade_price_5s += trades[0].trade_volume_price

        self.trade_price_3s = round(self.trade_price_3s)
        self.trade_price_5s = round(self.trade_price_5s)
