import sys
import pyautogui
from stockfish import Stockfish

from chess import *
from ss_window import ScreenshotWindow

from PyQt5.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self.main_window = ScreenshotWindow()
        self.main_window.show()


templates_path = [
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

notation = [
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

box_colors = [
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


state = [ ["" for _ in range(8)] for _ in range(8) ]

global_threshold = 0.7

if __name__ == '__main__':
    app = App(sys.argv)
    
    sys.exit(app.exec_())

board = cv2.imread('assets/puzzles/blek.png')
is_found, found_board, board_height, board_width = find_board(board)

# detect chess pieces
for path, color, code in zip(templates_path, box_colors, notation):
    template = cv2.imread(path, 0)
    
    found_board, state = template_detection(found_board, template, global_threshold, color, code, state)

cv2.imshow('found_board', found_board)

who_to_play = 'b'

if who_to_play == 'b':
    state = reverse_fen(state)

fen = state_to_fen(state)

full_fen = "{} {} - - 0 1".format(fen, who_to_play)


print('Fen notation:', full_fen)
for i in state:
    print(i)

# load stockfish engine
stockfish = Stockfish('stockfish_13_win_x64/stockfish_13_win_x64.exe')

stockfish.set_depth(15)
stockfish.set_fen_position(full_fen)

move = stockfish.get_best_move()
print('Best move:', move)

cv2.waitKey(0)
