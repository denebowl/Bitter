import datetime
import json
import random
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal
from websocket._app import WebSocketApp

from DTO.crypto import Crypto
from DTO.trade import Trade
from Singleton import GlobalData

nextRequestTime = datetime.datetime.now()
indexer = 0


class UpbitReceiver(QThread):
    onReceiveSignal = pyqtSignal(Crypto, Trade)

    def __init__(self, cryptoCode: str):
        super().__init__()

        # update 간격 조절
        self.delayReceive = 0.5  # 메시지 수신하는 딜레이
        self.updateTime = datetime.datetime.now()

        self.cryptoCode = cryptoCode
        self.requestCode = '[{"ticket":"test"},{"type":"ticker","codes":["KRW-' + cryptoCode + '"]}]'
        self.webSocket = self.createWebsocket()

    def run(self):
        while True:
            global nextRequestTime
            while datetime.datetime.now() < nextRequestTime:
                sleep(0.1)
                # waiting...
            nextRequestTime = datetime.datetime.now() + datetime.timedelta(seconds=1)

            self.webSocket.run_forever()
            print(self.cryptoCode + ' run task finished and try to run again.')

    def stop(self):
        self.webSocket.close()

    # websocket
    def createWebsocket(self):
        websocket = WebSocketApp(
            url="wss://api.upbit.com/websocket/v1",
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws: self.on_close(ws),
            on_open=lambda ws: self.on_open(ws, self.requestCode))
        return websocket

    def on_open(self, ws, request):
        self.webSocket.send(request)
        global indexer
        indexer += 1
        print('on_open with ' + self.cryptoCode + '(' + str(indexer) + ')')

    def on_message(self, ws, msg):
        from DTO.trade import Trade

        timeDelta = datetime.datetime.now() - self.updateTime
        if timeDelta.total_seconds() < self.delayReceive:  # 메시지 수신 딜레이
            return

        msg = json.loads(msg.decode('utf-8'))
        tradeData = Trade(msg)

        crypto = GlobalData.cryptos[self.cryptoCode]
        crypto.addTradeData(tradeData)
        crypto.tradeAnalysis.update(crypto.trades)

        #GlobalData.mysqlDatabase.addUploadData(tradeData)

        self.onReceiveSignal.emit(GlobalData.cryptos[self.cryptoCode], tradeData)
        self.updateTime = datetime.datetime.now()
        # print('on_message')

    def on_error(self, ws, msg):
        self.stop()
        print(self.cryptoCode + ' socket on_error. ' + msg)

    def on_close(self, ):
        global indexer
        indexer -= 1
        self.stop()
        print(self.cryptoCode + ' socket on_close')

    def setCallback(self, onReceived):
        self.onReceiveSignal.connect(onReceived)


# static
def downloadCandleDate(unit: int, marketCode: str, count: int, toDate: str = None):
    if toDate is None:
        startTime = datetime.datetime(2020, 1, 1, 00, 00).timestamp()
        endTime = datetime.datetime.now().timestamp()
        toDate = random.uniform(startTime, endTime)
        toDate = datetime.datetime.fromtimestamp(toDate)
        toDate = toDate.strftime('%Y-%m-%dT%H:%M:%SZ')

    import requests
    url = "https://api.upbit.com/v1/candles/minutes/" + str(unit)
    querystring = {"to": toDate, "market": marketCode, "count": count}
    response = requests.request("GET", url, params=querystring)
    jsonData = response.json()
    return jsonData
