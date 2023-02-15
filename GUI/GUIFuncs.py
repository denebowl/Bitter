import datetime
from threading import Timer
from typing import List

import winsound

from GUI.warning_dialog import WarningDialog


def cutRange(min_value, max_value, value):
    return max(min(value, max_value), min_value)


lastSoundTime: datetime.datetime = datetime.datetime.now()
listWarningText: List[str] = []
warningDialog = None


def updateWarning():
    def deleteWarning():
        del listWarningText[0]

    from mainWindow import warningBoundary, tradeVolumeBoundary
    from Singleton.GlobalData import cryptos

    global lastSoundTime
    if (datetime.datetime.now() - lastSoundTime).seconds < 1.5:
        return

    for crypto in cryptos.values():
        warningText = None

        rates = [0.0]
        if crypto.tradeAnalysis.rate_prev is not None:
            rates.append(crypto.tradeAnalysis.rate_prev)
        if crypto.tradeAnalysis.rate_5s is not None:
            rates.append(crypto.tradeAnalysis.rate_5s)
        if crypto.tradeAnalysis.rate_15s is not None:
            rates.append(crypto.tradeAnalysis.rate_15s)
        if crypto.tradeAnalysis.rate_30s is not None:
            rates.append(crypto.tradeAnalysis.rate_30s)
        if crypto.tradeAnalysis.rate_1m is not None:
            rates.append(crypto.tradeAnalysis.rate_1m)

        minRate = min(rates)
        maxRate = max(rates)
        isUp = maxRate > warningBoundary and abs(maxRate) > abs(minRate)
        isDown = minRate < -warningBoundary and abs(maxRate) < abs(minRate)

        if crypto.tradeAnalysis.trade_price_3s > tradeVolumeBoundary:
            winsound.PlaySound('Resources/up.wav', winsound.SND_ASYNC | winsound.SND_NOWAIT)
            lastSoundTime = datetime.datetime.now()
            warningText = str.format('{0} 거래금액({1:.1f}만)', crypto.name, crypto.tradeAnalysis.trade_price_3s)

        elif isUp:
            winsound.PlaySound('Resources/up.wav', winsound.SND_ASYNC | winsound.SND_NOWAIT)
            lastSoundTime = datetime.datetime.now()
            warningText = str.format('{0} 상승({1:.1f}%)', crypto.name, maxRate)

        elif isDown:
            winsound.PlaySound('Resources/down.wav', winsound.SND_ASYNC | winsound.SND_NOWAIT)
            lastSoundTime = datetime.datetime.now()
            warningText = str.format('{0} 하락({1:.1f}%)', crypto.name, minRate)

        if warningText is not None:
            listWarningText.append(warningText)
            Timer(10, deleteWarning).start()

            global warningDialog
            if isUp:
                warningDialog = WarningDialog(warningText, 'red')
            else:
                warningDialog = WarningDialog(warningText, 'blue')
            warningDialog.show()
