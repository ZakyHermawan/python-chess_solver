from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from numpy.core.numeric import full

from ui_screenshot import Ui_MainWindow
from screenshot_window import ScreenshotWindow

import cv2
from chess import find_board, template_detection, reverse_fen, state_to_fen

class MasterWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.ss_window = ScreenshotWindow()

        self.ss_window.pushButton.clicked.connect(self.screenshot_wrapper)

        self.ss_window.show()

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
    

    def screenshot_wrapper(self):
        board_image = self.take_screenshot()
        found_board = self.board_detection(board_image)

        found_board, state = self.detect_pieces(found_board)

        cv2.imshow('found', found_board)

        full_fen = self.get_full_fen(state)

        print(full_fen)

        
        
    def take_screenshot(self):
        board_image = cv2.imread('assets/puzzles/blek.png')
        return board_image


    # memotong gambar, sehingg yang diambbil papan caturnya saja
    def board_detection(self, board_image):

        is_found, found_board, board_height, board_width = find_board(board_image)

        return found_board

        found_board, self.state = self.detect_pieces(board_image)
        
        cv2.imshow('match', found_board)
        if self.who_to_play == 'b':
            self.state = reverse_fen(self.state)

        self.fen = self.get_fen(self.state)

        self.full_fen = "{} {} - - 0 1".format(self.fen, self.who_to_play)


        for i in self.state:
            print(i)

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

        return full_fen


    def get_fen(self, state):
        fen = state_to_fen(state)

        return fen




