import sys
# import pyautogui
from stockfish import Stockfish

from chess import *
from master_window import MasterWindow

from PyQt5.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self.main_window = MasterWindow()
        self.main_window.hide()

if __name__ == '__main__':
    app = App(sys.argv)
    
    sys.exit(app.exec_())
