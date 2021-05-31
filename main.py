import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

def template_detection(image, template, threshold, bgr_color):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_height, template_width = template.shape
    match_result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)

    mmr = cv2.minMaxLoc(match_result)

    rects = []

    (j_coordinates, i_coordinates) = np.where(match_result >= threshold)

    for (i, j) in zip(i_coordinates, j_coordinates):
        rects.append((i, j, i+template_width, j+template_height))

    pick = non_max_suppression(np.array(rects))

    for (start_col, start_row, end_col, end_row) in pick:
        cv2.rectangle(image, (start_col, start_row), (end_col, end_row), bgr_color, 2)

        # kembalikan koordinat
        

    return image

def find_board(original_image):
    kernelH = np.array([[-1, 1]])
    kernelV = np.array([[-1],[1]])

    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Filter horizontal lines :
    horizontal_lines = np.absolute(cv2.filter2D(image.astype('float'),-1,kernelV))
    
    ret,thresh1 = cv2.threshold(horizontal_lines,30,255,cv2.THRESH_BINARY)
    
    kernelSmall = np.ones((1,3), np.uint8)
    kernelBig = np.ones((1,50), np.uint8)

    # Remove holes:
    imgH1 = cv2.dilate(thresh1, kernelSmall, iterations=1)
    imgH2 = cv2.erode(imgH1, kernelSmall, iterations=1)
    
    # Remove small lines
    imgH3 = cv2.erode(imgH2, kernelBig, iterations=1)
    imgH4 = cv2.dilate(imgH3, kernelBig, iterations=1)

    column_starts = cv2.filter2D(imgH4,-1,kernelH)
    column_ends = cv2.filter2D(imgH4,-1,-kernelH)

    columns = column_starts.sum(axis=0)/255
    column_start = 0
    nbColumn_start = 0
    for idx, val in enumerate(columns):
        if val > 6:
            nbColumn_start += 1
            column_start = idx

    columns = column_ends.sum(axis=0)/255
    column_end = 0
    nbColumn_end = 0
    for idx, val in enumerate(columns):
        if val > 6:
            nbColumn_end += 1
            column_end = idx        

    # Filter vertical lines:
    vertical_lines = np.absolute(cv2.filter2D(image.astype('float'),-1,kernelH))
    ret,thresh1 = cv2.threshold(vertical_lines,30,255,cv2.THRESH_BINARY)
    
    kernelSmall = np.ones((3,1), np.uint8)
    kernelBig = np.ones((50,1), np.uint8)
    
    # Remove holes:
    imgV1 = cv2.dilate(thresh1, kernelSmall, iterations=1)
    imgV2 = cv2.erode(imgV1, kernelSmall, iterations=1)
    
    # Remove small lines
    imgV3 = cv2.erode(imgV2, kernelBig, iterations=1)
    imgV4 = cv2.dilate(imgV3, kernelBig, iterations=1)

    row_starts = cv2.filter2D(imgV4,-1,kernelV)
    row_ends = cv2.filter2D(imgV4,-1,-kernelV)

    row = row_starts.sum(axis=1)/255
    row_start = 0
    nbRow_start = 0
    for idx, val in enumerate(row):
        if val > 6:
            row_start = idx
            nbRow_start += 1
            
    row = row_ends.sum(axis=1)/255
    row_end = 0
    nbRow_end = 0
    for idx, val in enumerate(row):
        if val > 6:
            row_end = idx
            nbRow_end += 1


    found_board = False
    if (nbColumn_start == 1) and (nbColumn_end == 1) and (nbRow_start == 1) and (nbRow_end == 1) :
        print("We found a board")
        if abs((row_end - row_start) - (column_end - column_start)) > 3:
            print ("However, the board is not a square")
        else:
            if (row_end - row_start) % 8 == 1:
                row_end -= 1
            if (row_end - row_start) % 8 == 7:
                row_end += 1
            if (column_end - column_start) % 8 == 1:
                column_start += 1
            if (column_end - column_start) % 8 == 7:
                column_start -= 1
            found_board = True
    else:
        print("We did not found the borders of the board")

    if found_board:
        height = row_end-row_start
        width = column_end-column_start
        print("Found chessboard sized:" , (height),(width)," row (begin, end):",row_start,row_end," column (begin, end): ",column_start,column_end)
        resizedChessBoard = original_image[row_start:row_end, column_start:column_end]

        return True, resizedChessBoard, height, width

    return False, image, 0, 0

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

image = cv2.imread('assets/initial_board.png')

global_threshold = 0.65

board = cv2.imread('assets/board.png')
origin = board

is_found, found_board, height, width = find_board(board)


# pieces detection
for path, color in zip(templates_path, box_colors):
    template = cv2.imread(path, 0)
    found_board = template_detection(found_board, template, global_threshold, color)

cv2.imshow('found_board', found_board)

cv2.waitKey(0)
