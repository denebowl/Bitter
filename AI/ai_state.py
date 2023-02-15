from datetime import datetime
from typing import List

from AI.ai_dto import CandleDto


def getBeforeState(candles):
    candles = candles[:50]

    state = []
    for candle in candles:
        # datetime_utc = datetime.strptime(candle.candle_date_time_utc, '%Y-%m-%dT%H:%M:%S')
        datetime_kst = datetime.strptime(candle.candle_date_time_kst, '%Y-%m-%dT%H:%M:%S')
        weekday = datetime_kst.weekday()

        state.append(
            [
                candle.timestamp,
                # datetime_utc,  # 세계 시각
                datetime_kst,  # 한국 시각
                weekday,
                candle.opening_price,  # 시가
                candle.high_price,  # 고가
                candle.low_price,  # 저가
                candle.trade_price,  # 종가
                candle.candle_acc_trade_price,  # 누적 거래금액
                candle.candle_acc_trade_volume,  # 누적 거래량
            ]
        )
    return state


def renderNP():
    return 1
