from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from numpy.core.numeric import full

from ui_screenshot import Ui_MainWindow
from screenshot_window import ScreenshotWindow
from best_move_window import BestMoveWindow

import cv2
from stockfish import Stockfish

from chess import find_board, template_detection, reverse_fen, state_to_fen

class MasterWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.ss_window = ScreenshotWindow()

        self.ss_window.pushButton.clicked.connect(self.screenshot_wrapper)
        self.ss_window.closeEvent = self.destroyAllWindow
        self.screenshot_taken = False

        self.ss_window.show()

        self.best_move_window = None

        # initiate member variables

        self.templates_path = [
            'assets/white_pawn.png',
            'assets/black_pawn.png',
            'assets/white_knight.png',
            'assets/black_knight.png',
            'assets/white_bishop.png',
            'assets/black_bishop.png',
            'assets/white_rook.png',
            'assets/black_rook.png',
            'assets/white_queen.png',
            'assets/black_queen.png',
            'assets/white_king.png',
            'assets/black_king.png'
        ]

        self.box_colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (100, 0, 0),
            (0, 100, 0),
            (0, 0, 100),
            (100, 100, 0),
            (100, 0, 100),
            (0, 100, 100),
            (100, 100, 255),
            (100, 255, 100),
            (255, 100, 100),
        ]

        self.notation = [
            'P',
            'p',
            'N',
            'n',
            'B',
            'b',
            'R',
            'r',
            'Q',
            'q',
            'K',
            'k'
        ]

        self.global_threshold = 0.7

        self.state = [ ["" for _ in range(8)] for _ in range(8) ]

        self.who_to_play = 'b'

        self.found_board = []

        self.fen = ''

        self.full_fen = ''


    def destroyAllWindow(self, event):
        self.ss_window.close()

        if self.screenshot_taken:
            self.best_move_window.close()


    def screenshot_wrapper(self):
        self.screenshot_taken = True

        board_image = self.take_screenshot()
        found_board = self.board_detection(board_image)

        found_board, state = self.detect_pieces(found_board)

        cv2.imshow('found', found_board)

        full_fen = self.get_full_fen(state)
        self.full_fen = full_fen

        print(full_fen)
        print(state)

        self.best_move_window = BestMoveWindow()
        self.best_move_window.pushButton.clicked.connect(self.best_move_wrapper)
        self.best_move_window.textBrowser.setFontPointSize(12)
        self.best_move_window.show()


    def best_move_wrapper(self):
        self.get_best_move(self.full_fen)


    def get_best_move(self, full_fen):
        stockfish = Stockfish('stockfish_13_win_x64/stockfish_13_win_x64.exe')

        stockfish.set_depth(15)
        stockfish.set_fen_position(full_fen)

        move = stockfish.get_best_move()
        print('Best move:', move)

        self.best_move_window.textBrowser.append(move)


    def take_screenshot(self):
        board_image = cv2.imread('assets/puzzles/blek.png')
        return board_image


    # memotong gambar, sehingg yang diambbil papan caturnya saja
    def board_detection(self, board_image):

        is_found, found_board, board_height, board_width = find_board(board_image)

        return found_board

    def detect_pieces(self, board_image):
        
        for path, color, code in zip(self.templates_path, self.box_colors, self.notation):
            template = cv2.imread(path, 0)
    
            board_image, self.state = template_detection(board_image, template, self.global_threshold, color, code, self.state)

        return board_image, self.state


    def get_full_fen(self, state):
        if self.who_to_play == 'b':
            state = reverse_fen(state)

        fen = self.get_fen(state)

        full_fen = "{} {} - - 0 1".format(fen, self.who_to_play)
        for i in state:
            print(i)
        return full_fen


    def get_fen(self, state):
        fen = state_to_fen(state)

        return fen




