from PyQt5.QtWidgets import QWidget, QMainWindow
from ui_screenshot import Ui_MainWindow

class ScreenshotWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)

        self.setupUi(self)
