import ctypes
import sys
from Singleton import GlobalData

from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

if __name__ == '__main__':
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # 모니터 슬립모드 오프

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # 모니터 슬립모드 다시 켬
