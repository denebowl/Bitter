from typing import List

from DTO.trade import Trade


def isInTimeSeconds(current, prev, seconds):
    return (current.datetime - prev.datetime).seconds <= seconds


def getTicksInSeconds(tradeData: List[Trade], timeRange):
    start = tradeData[0]
    ticks = 0
    for td in tradeData:
        if isInTimeSeconds(start, td, timeRange):
            ticks += 1
    return ticks


def getUpDownPrice(before: Trade, after: Trade):
    return after.trade_price - before.trade_price


def getUpDownTickInSeconds(tradeData: List[Trade], timeRange):
    current = tradeData[0]

    increaseTick = 0
    for i in range(len(tradeData) - 1):
        prev = tradeData[i]
        # 시간 기준
        if not isInTimeSeconds(current, prev, timeRange):
            break

        # 상승/하락 틱 감지
        prevOfPrev = tradeData[i + 1]
        if prev.trade_price - prevOfPrev.trade_price > 0:
            increaseTick += 1
        elif prev.trade_price - prevOfPrev.trade_price < 0:
            increaseTick -= 1

    return increaseTick
