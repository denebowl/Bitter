from threading import Timer, Thread
from time import sleep

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QInputDialog, QLineEdit, QListWidget, QTextEdit

from AI.ai_manager import AIManager
from DTO.crypto import Crypto
from DTO.trade import Trade
from GUI.GUIFuncs import updateWarning, listWarningText

from Singleton import GlobalData

upDownBoundary = 0.0
warningBoundary = 3.0
tradeVolumeBoundary = 100000.0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        for crypto in GlobalData.cryptos.values():
            crypto.receiver.setCallback(self.onReceived)

        # UI
        self.root_widget = QWidget()
        self.root_widget_grid = QGridLayout()
        from GUI.table_widget import QBitterTableWidget
        self.tableWidget = QBitterTableWidget()
        self.lineEdit_monitoringRate = QLineEdit()
        self.lineEdit_warningRate = QLineEdit()
        self.lineEdit_tradeVolume = QLineEdit()

        self.textEditWarning = QTextEdit()
        self.setupUI()

        self.timerUpdateUI = QTimer()
        self.timerUpdateUI.setInterval(0.3)
        self.timerUpdateUI.timeout.connect(self.timerTaskUpdateUI)
        self.timerUpdateUI.start()

        self.aiManager = AIManager()
        self.aiManager.start()

        self.timerParseUserInput = None

    def onReceived(self, crypto: Crypto, trade: Trade):
        return

    def timerTaskUpdateUI(self):
        self.updateUI()
        updateWarning()

    ###############

    def setupUI(self):
        self.setWindowTitle('Bitter')
        self.setGeometry(0, 0, 1900, 1100)
        self.setCentralWidget(self.root_widget)
        self.root_widget.setLayout(self.root_widget_grid)

        # 메인 위젯 1
        self.root_widget_grid.addWidget(self.tableWidget, 0, 0, 10, 10)

        # 메인 위젯 2
        label_monitoringRate = QLabel('색상출력')
        self.root_widget_grid.addWidget(label_monitoringRate, 0, 10)
        self.lineEdit_monitoringRate.setFixedWidth(50)
        self.lineEdit_monitoringRate.setFixedHeight(25)
        self.lineEdit_monitoringRate.setText(str(upDownBoundary))
        self.lineEdit_monitoringRate.textChanged.connect(self.onUserInputChanged)
        self.root_widget_grid.addWidget(self.lineEdit_monitoringRate, 1, 10)

        label_warningRate = QLabel('급등락')
        self.root_widget_grid.addWidget(label_warningRate, 0, 11)
        self.lineEdit_warningRate.setFixedWidth(50)
        self.lineEdit_warningRate.setFixedHeight(25)
        self.lineEdit_warningRate.setText(str(warningBoundary))
        self.lineEdit_warningRate.textChanged.connect(self.onUserInputChanged)
        self.root_widget_grid.addWidget(self.lineEdit_warningRate, 1, 11)

        label_warningTradePrice = QLabel('거래량')
        self.root_widget_grid.addWidget(label_warningTradePrice, 0, 12)
        self.lineEdit_tradeVolume.setFixedWidth(50)
        self.lineEdit_tradeVolume.setFixedHeight(25)
        self.lineEdit_tradeVolume.setText(str(tradeVolumeBoundary))
        self.lineEdit_tradeVolume.textChanged.connect(self.onUserInputChanged)
        self.root_widget_grid.addWidget(self.lineEdit_tradeVolume, 1, 12)

        addButton = QPushButton('코인 추가', self)
        addButton.setFixedWidth(80)
        addButton.setFixedHeight(25)
        addButton.clicked.connect(self.onAddButtonClicked)
        self.root_widget_grid.addWidget(addButton, 3, 10)

        removeButton = QPushButton('코인 삭제', self)
        removeButton.setFixedWidth(80)
        removeButton.setFixedHeight(25)
        removeButton.clicked.connect(self.onRemoveButtonClicked)
        self.root_widget_grid.addWidget(removeButton, 3, 11)

        font = self.textEditWarning.font()
        font.bold()
        font.setPointSize(15)
        self.textEditWarning.setFont(font)
        self.root_widget_grid.addWidget(self.textEditWarning, 4, 10, 1, 4)

        # myTextbox = QLineEdit(w)

    def updateUI(self):
        self.tableWidget.updateUI()

        warningText = ''
        for text in listWarningText:
            warningText += text + '\n'
        self.textEditWarning.setText(warningText)

    ###############

    def onAddButtonClicked(self):
        text, ok = QInputDialog.getText(self, '코인 추가', '이름 또는 코드')
        if not ok:
            return
        text = text.upper()
        for cryptoInfo in GlobalData.coinList.values():
            if text == cryptoInfo.code or text == cryptoInfo.localName:
                GlobalData.addCrypto(cryptoInfo)  # 해당 기능 삭제
                GlobalData.cryptos[cryptoInfo.code].receiver.setCallback(self.onReceived)
                break

    def onRemoveButtonClicked(self):
        text, ok = QInputDialog.getText(self, '코인 삭제', '이름 또는 코드')
        if not ok:
            return
        text = text.upper()
        for crypto in GlobalData.cryptos.values():
            if text == crypto.code or text == crypto.name:
                GlobalData.removeCrypto(crypto)  # 해당 기능 삭제
                break

    def onUserInputChanged(self):
        if self.timerParseUserInput is not None:
            self.timerParseUserInput.cancel()

        self.timerParseUserInput = Timer(0.5, self.ParseUserInput)
        self.timerParseUserInput.daemon = True
        self.timerParseUserInput.start()

    def ParseUserInput(self):
        global upDownBoundary, warningBoundary, tradeVolumeBoundary
        try:
            tmpUpDown = max(0.0, float(self.lineEdit_monitoringRate.text()))
            upDownBoundary = tmpUpDown
            self.lineEdit_monitoringRate.setText(str(upDownBoundary))

            tmpWarning = max(0.3, float(self.lineEdit_warningRate.text()))
            warningBoundary = tmpWarning
            self.lineEdit_warningRate.setText(str(warningBoundary))

            tmpTradeVolume = max(1000.0, float(self.lineEdit_tradeVolume.text()))
            tradeVolumeBoundary = tmpTradeVolume
            self.lineEdit_tradeVolume.setText(str(tradeVolumeBoundary))
        except ValueError:
            pass
        finally:
            self.timerParseUserInput = None
