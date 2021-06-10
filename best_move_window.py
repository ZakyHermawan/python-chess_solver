from PyQt5.QtWidgets import QMainWindow
from ui_best_move import Ui_Form

class BestMoveWindow(Ui_Form, QMainWindow):
    def __init__(self):
        Ui_Form.__init__(self)
        QMainWindow.__init__(self)

        self.setupUi(self)