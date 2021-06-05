from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow

class ScreenshotWindow(QMainWindow):    
    def __init__(self):
        super().__init__()
        uic.loadUi('screenshot.ui', self)

        self.pushButton.clicked.connect(self.take_screenshot)


    def take_screenshot(self):
        print("screenshot telah diambil")
