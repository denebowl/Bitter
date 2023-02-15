class CandleDto:
    def __init__(self, **kwargs):
        self.market = kwargs['market']
        self.candle_date_time_utc = kwargs['candle_date_time_utc']
        self.candle_date_time_kst = kwargs['candle_date_time_kst']
        self.opening_price = kwargs['opening_price']
        self.high_price = kwargs['high_price']
        self.low_price = kwargs['low_price']
        self.trade_price = kwargs['trade_price']
        self.timestamp = kwargs['timestamp']
        self.candle_acc_trade_price = kwargs['candle_acc_trade_price']
        self.candle_acc_trade_volume = kwargs['candle_acc_trade_volume']
        self.unit = kwargs['unit']
