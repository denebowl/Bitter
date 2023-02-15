import copy
from typing import Dict, List

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from qasync import QtCore

from DTO.crypto import Crypto
from GUI.GUIFuncs import cutRange


class QBitterTableWidget(QTableWidget):

    def __init__(self):
        super().__init__()

        from Singleton.GlobalData import cryptos
        self.rows = len(cryptos)
        self.cols = 12
        self.tableItems: Dict[str, List[QBitterTableWidgetItem]] = {}

        self.setMaximumWidth(1800)
        font = self.font()
        font.setPointSize(15)
        self.setFont(font)
        self.autoScroll = True
        self.setSortingEnabled(True)

        # rows
        self.setRowCount(self.rows)
        for row in range(self.rows):
            self.setRowHeight(row, 30)

        # cols
        self.setColumnCount(self.cols)
        self.setColumnWidth(0, 240)
        self.setColumnWidth(1, 180)
        self.setColumnWidth(2, 120)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 100)
        self.setColumnWidth(5, 100)
        self.setColumnWidth(6, 100)
        self.setColumnWidth(7, 100)
        self.setColumnWidth(8, 100)
        self.setColumnWidth(9, 100)
        self.setColumnWidth(10, 10)
        self.setColumnWidth(11, 100)
        self.setHorizontalHeaderItem(0, QBitterTableWidgetItem("날짜시간"))
        self.setHorizontalHeaderItem(1, QBitterTableWidgetItem("화폐명"))
        self.setHorizontalHeaderItem(2, QBitterTableWidgetItem("코드"))
        self.setHorizontalHeaderItem(3, QBitterTableWidgetItem("가격"))
        self.setHorizontalHeaderItem(4, QBitterTableWidgetItem("직전"))
        self.setHorizontalHeaderItem(5, QBitterTableWidgetItem("5초간"))
        self.setHorizontalHeaderItem(6, QBitterTableWidgetItem("15초간"))
        self.setHorizontalHeaderItem(7, QBitterTableWidgetItem("30초간"))
        self.setHorizontalHeaderItem(8, QBitterTableWidgetItem("1분간"))
        self.setHorizontalHeaderItem(9, QBitterTableWidgetItem("5분간"))
        self.setHorizontalHeaderItem(10, QBitterTableWidgetItem("통합"))
        self.setHorizontalHeaderItem(11, QBitterTableWidgetItem("거래량"))
        # self.horizontalHeader().setFont(font)

        # init data
        for crypto in cryptos.values():
            rowData = []
            for col in range(0, self.cols):
                newItem = QBitterTableWidgetItem('')
                self.setItem(crypto.index, col, newItem)
                rowData.insert(col, newItem)
            rowData[1].setText(crypto.name)
            rowData[2].setText(crypto.code)
            self.tableItems[crypto.code] = rowData

    def updateUI(self):
        from Singleton import GlobalData
        import mainWindow

        self.setRowCount(len(GlobalData.cryptos))

        for crypto in GlobalData.cryptos.values():
            tradeData = crypto.trades
            if len(tradeData) <= 0:
                continue

            rowData = self.tableItems[crypto.code]
            current = tradeData[0]
            tradeAnalysis = copy.deepcopy(crypto.tradeAnalysis)

            rowData[0].setText(str(current.datetime))  # 날짜
            rowData[1].setText(str(crypto.name))  # 이름
            rowData[2].setText(str(crypto.code))  # 코드
            rowData[3].setText(str(current.trade_price))  # 가격

            # 직전
            minRate = 0
            maxRate = 0
            maxColorRate = 3  # 이 수치% 이상 올라가면 가장 진한 색으로 뜸
            colorWhite = QColor(255, 255, 255)
            if tradeAnalysis.price_prev is not None and tradeAnalysis.rate_prev is not None:
                text = str.format('{0}', round(tradeAnalysis.rate_prev, 2))
                color = colorWhite
                colorIntensity = cutRange(-255, 255, 255 / maxColorRate * tradeAnalysis.rate_prev)
                if tradeAnalysis.rate_prev > mainWindow.upDownBoundary:  # 횟수
                    color = QColor(255, 255 - colorIntensity, 255 - colorIntensity)
                elif tradeAnalysis.rate_prev < -mainWindow.upDownBoundary:
                    color = QColor(255 + colorIntensity, 255 + colorIntensity, 255)
                rowData[4].setBackground(color)
                rowData[4].setText(text)
                maxRate = max(maxRate, tradeAnalysis.rate_prev)
                minRate = min(minRate, tradeAnalysis.rate_prev)

            # 5초전
            if tradeAnalysis.price_5s is not None and tradeAnalysis.rate_5s is not None:
                text = str.format('{0}', round(tradeAnalysis.rate_5s, 2))
                color = colorWhite
                colorIntensity = cutRange(-255, 255, 255 / maxColorRate * tradeAnalysis.rate_5s)
                if tradeAnalysis.rate_5s > mainWindow.upDownBoundary:  # 횟수
                    color = QColor(255, 255 - colorIntensity, 255 - colorIntensity)
                elif tradeAnalysis.rate_5s < -mainWindow.upDownBoundary:
                    color = QColor(255 + colorIntensity, 255 + colorIntensity, 255)
                rowData[5].setBackground(color)
                rowData[5].setText(text)
                maxRate = max(maxRate, tradeAnalysis.rate_5s)
                minRate = min(minRate, tradeAnalysis.rate_5s)

            # 15초전
            if tradeAnalysis.price_15s is not None and tradeAnalysis.rate_15s is not None:
                text = str.format('{0}', round(tradeAnalysis.rate_15s, 2))
                color = colorWhite
                colorIntensity = cutRange(-255, 255, 255 / maxColorRate * tradeAnalysis.rate_15s)
                if tradeAnalysis.rate_15s > mainWindow.upDownBoundary:  # 횟수
                    color = QColor(255, 255 - colorIntensity, 255 - colorIntensity)
                elif tradeAnalysis.rate_15s < -mainWindow.upDownBoundary:
                    color = QColor(255 + colorIntensity, 255 + colorIntensity, 255)
                rowData[6].setBackground(color)
                rowData[6].setText(text)
                maxRate = max(maxRate, tradeAnalysis.rate_15s)
                minRate = min(minRate, tradeAnalysis.rate_15s)

            # 30초전
            if tradeAnalysis.price_30s is not None and tradeAnalysis.rate_30s is not None:
                text = str.format('{0}', round(tradeAnalysis.rate_30s, 2))
                color = colorWhite
                colorIntensity = cutRange(-255, 255, 255 / maxColorRate * tradeAnalysis.rate_30s)
                if tradeAnalysis.rate_30s > mainWindow.upDownBoundary:  # 횟수
                    color = QColor(255, 255 - colorIntensity, 255 - colorIntensity)
                elif tradeAnalysis.rate_30s < -mainWindow.upDownBoundary:
                    color = QColor(255 + colorIntensity, 255 + colorIntensity, 255)
                rowData[7].setBackground(color)
                rowData[7].setText(text)
                maxRate = max(maxRate, tradeAnalysis.rate_30s)
                minRate = min(minRate, tradeAnalysis.rate_30s)

            # 1분전
            if tradeAnalysis.price_1m is not None and tradeAnalysis.rate_1m is not None:
                text = str.format('{0}', round(tradeAnalysis.rate_1m, 2))
                color = colorWhite
                colorIntensity = cutRange(-255, 255, 255 / maxColorRate * tradeAnalysis.rate_1m)
                if tradeAnalysis.rate_1m > mainWindow.upDownBoundary:  # 횟수
                    color = QColor(255, 255 - colorIntensity, 255 - colorIntensity)
                elif tradeAnalysis.rate_1m < -mainWindow.upDownBoundary:
                    color = QColor(255 + colorIntensity, 255 + colorIntensity, 255)
                rowData[8].setBackground(color)
                rowData[8].setText(text)
                maxRate = max(maxRate, tradeAnalysis.rate_1m)
                minRate = min(minRate, tradeAnalysis.rate_1m)

            # 5분전
            if tradeAnalysis.price_5m is not None and tradeAnalysis.rate_5m is not None:
                text = str.format('{0}', round(tradeAnalysis.rate_5m, 2))
                color = colorWhite
                colorIntensity = cutRange(-255, 255, 255 / maxColorRate * tradeAnalysis.rate_5m)
                if tradeAnalysis.rate_5m > mainWindow.upDownBoundary:  # 횟수
                    color = QColor(255, 255 - colorIntensity, 255 - colorIntensity)
                elif tradeAnalysis.rate_5m < -mainWindow.upDownBoundary:
                    color = QColor(255 + colorIntensity, 255 + colorIntensity, 255)
                rowData[9].setBackground(color)
                rowData[9].setText(text)
                maxRate = max(maxRate, tradeAnalysis.rate_5m)
                minRate = min(minRate, tradeAnalysis.rate_5m)

            # 통합
            if abs(minRate) < abs(maxRate):  # 상승
                color = colorWhite
                if maxRate > mainWindow.upDownBoundary:
                    finalColorIntensity = cutRange(-255, 255, 255 / maxColorRate * maxRate)
                    color = QColor(255, 255 - finalColorIntensity, 255 - finalColorIntensity)
                rowData[0].setBackground(color)
                rowData[1].setBackground(color)
                rowData[2].setBackground(color)
                rowData[10].setBackground(color)
                rowData[10].setText(str(round(maxRate, 2)))
            else:  # 하강
                color = colorWhite
                if minRate < -mainWindow.upDownBoundary:
                    finalColorIntensity = cutRange(-255, 255, 255 / maxColorRate * minRate)
                    color = QColor(255 + finalColorIntensity, 255 + finalColorIntensity, 255)
                rowData[0].setBackground(color)
                rowData[1].setBackground(color)
                rowData[2].setBackground(color)
                rowData[10].setBackground(color)
                rowData[10].setText(str(round(minRate, 2)))

            maxTradeVolumePrice = 50000
            tradeVolumeColorIntensity = cutRange(-255, 255, 255 / maxTradeVolumePrice * tradeAnalysis.trade_price_3s)
            color = QColor(255 - tradeVolumeColorIntensity, 255, 255)
            rowData[11].setText(str.format('{0}', tradeAnalysis.trade_price_3s))  # 거래금액
            rowData[11].setBackground(color)


class QBitterTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            selfDataValue = float(self.data(QtCore.Qt.EditRole))
            otherDataValue = float(other.data(QtCore.Qt.EditRole))
            return selfDataValue < otherDataValue
        except ValueError:
            return QTableWidgetItem.__lt__(self, other)
