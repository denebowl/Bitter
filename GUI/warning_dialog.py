from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout
from qasync import QtCore


class WarningDialog(QDialog):
    def __init__(self, text: str, backgroundColor: str):
        super().__init__()

        self.setWindowTitle('급등락 경고')
        self.resize(800, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        labelMain = QLabel(text)
        labelMain.setStyleSheet(str.format("background-color : {0}; color : white;", backgroundColor))
        font = labelMain.font()
        font.setPointSize(40)
        labelMain.setFont(font)

        # 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(labelMain)
        self.setLayout(layout)

        QtCore.QTimer.singleShot(3000, self.close)

