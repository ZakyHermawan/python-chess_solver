import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

def template_detection(image, template, threshold, bgr_color):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_height, template_width = template.shape
    match_result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    
    # mmr structure
    # 0,0 coordinate is at the very top left
    # [min_value, max_value, (min_col_location, min_row_location), (max_col_location, max_col_locaion)]

    mmr = cv2.minMaxLoc(match_result)

    rects = []

    (j_coordinates, i_coordinates) = np.where(match_result >= threshold)

    for (i, j) in zip(i_coordinates, j_coordinates):
        rects.append((i, j, i+template_width, j+template_height))

    pick = non_max_suppression(np.array(rects))

    for (start_col, start_row, end_col, end_row) in pick:
        cv2.rectangle(image, (start_col, start_row), (end_col, end_row), bgr_color, 2)

    return image

# will probably need for denoising
def gaussian_blur_rectangle(image, kernel_size, start_coordinate, end_coordinate):
    kernel_height, kernel_width = kernel_size
    startX, startY = start_coordinate
    endX, endY = end_coordinate
    
    blurred_image = cv2.GaussianBlur(image, (kernel_height, kernel_width), 0)

    mask = np.zeros((height, width, 3), dtype=np.uint8)
    mask = cv2.rectangle(mask, (startX, startY), (endX, endY), (255, 255, 255), -1)

    image = np.where(mask!=np.array([255, 255, 255]), image, blurred_image)

    return image

def find_board(image):
    kernelH = np.array([[-1, 1]])
    kernelV = np.array([[-1],[1]])

    #Récupération des lignes horizontales :
    lignesHorizontales = np.absolute(cv2.filter2D(image.astype('float'),-1,kernelV))
    ret,thresh1 = cv2.threshold(lignesHorizontales,30,255,cv2.THRESH_BINARY)
    
    kernelSmall = np.ones((1,3), np.uint8)
    kernelBig = np.ones((1,50), np.uint8)

    #Remove holes:
    imgH1 = cv2.dilate(thresh1, kernelSmall, iterations=1)
    imgH2 = cv2.erode(imgH1, kernelSmall, iterations=1)
    
    #Remove small lines
    imgH3 = cv2.erode(imgH2, kernelBig, iterations=1)
    imgH4 = cv2.dilate(imgH3, kernelBig, iterations=1)

    linesStarts = cv2.filter2D(imgH4,-1,kernelH)
    linesEnds = cv2.filter2D(imgH4,-1,-kernelH)

    lines = linesStarts.sum(axis=0)/255
    lineStart = 0
    nbLineStart = 0
    for idx, val in enumerate(lines):
        if val > 6:
            nbLineStart += 1
            lineStart = idx

    lines = linesEnds.sum(axis=0)/255
    lineEnd = 0
    nbLineEnd = 0
    for idx, val in enumerate(lines):
        if val > 6:
            nbLineEnd += 1
            lineEnd = idx        

    #Récupération des lignes verticales:
    lignesVerticales = np.absolute(cv2.filter2D(image.astype('float'),-1,kernelH))
    ret,thresh1 = cv2.threshold(lignesVerticales,30,255,cv2.THRESH_BINARY)
    
    kernelSmall = np.ones((3,1), np.uint8)
    kernelBig = np.ones((50,1), np.uint8)
    
    #Remove holes:
    imgV1 = cv2.dilate(thresh1, kernelSmall, iterations=1)
    imgV2 = cv2.erode(imgV1, kernelSmall, iterations=1)
    
    #Remove small lines
    imgV3 = cv2.erode(imgV2, kernelBig, iterations=1)
    imgV4 = cv2.dilate(imgV3, kernelBig, iterations=1)

    columnStarts = cv2.filter2D(imgV4,-1,kernelV)
    columnEnds = cv2.filter2D(imgV4,-1,-kernelV)

    column = columnStarts.sum(axis=1)/255
    columnStart = 0
    nbColumnStart = 0
    for idx, val in enumerate(column):
        if val > 6:
            columnStart = idx
            nbColumnStart += 1
            
    column = columnEnds.sum(axis=1)/255
    columnEnd = 0
    nbColumnEnd = 0
    for idx, val in enumerate(column):
        if val > 6:
            columnEnd = idx
            nbColumnEnd += 1


    found_board = False
    if (nbLineStart == 1) and (nbLineEnd == 1) and (nbColumnStart == 1) and (nbColumnEnd == 1) :
        print("We found a board")
        if abs((columnEnd - columnStart) - (lineEnd - lineStart)) > 3:
            print ("However, the board is not a square")
        else:
            print(columnStart,columnEnd,lineStart,lineEnd)
            if (columnEnd - columnStart) % 8 == 1:
                columnEnd -= 1
            if (columnEnd - columnStart) % 8 == 7:
                columnEnd += 1
            if (lineEnd - lineStart) % 8 == 1:
                lineStart += 1
            if (lineEnd - lineStart) % 8 == 7:
                lineStart -= 1
            print(columnStart,columnEnd,lineStart,lineEnd)

            found_board = True
    else:
        print("We did not found the borders of the board")

    if found_board:
        print("Found chessboard sized:" , (columnEnd-columnStart),(lineEnd-lineStart)," row (begin, end):",columnStart,columnEnd," column (begin, end): ",lineStart,lineEnd)
        dim = (400, 400 ) # perform the actual resizing of the chessboard
        print(lineStart,lineEnd,columnStart,columnEnd)
        resizedChessBoard = cv2.resize(image[columnStart:columnEnd, lineStart:lineEnd], dim, interpolation = cv2.INTER_AREA)
        return True, resizedChessBoard, lineStart, columnStart, lineEnd, columnEnd

    return False, image, 0, 0, 0, 0 , image


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

image = cv2.imread('assets/sample_board2.png')

global_threshold = 0.8


# piesces detection
for path, color in zip(templates_path, box_colors):
    template = cv2.imread(path, 0)
    image = template_detection(image, template, global_threshold, color)

board = cv2.imread('assets/board.png')

grey_image = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)

arr = find_board(grey_image)
print('\n'*3)
img, lineStart, columnStart, lineEnd, columnEnd = arr[1], arr[2], arr[3], arr[4], arr[5]

cv2.line(img, (columnStart, lineStart), (lineEnd, columnEnd), (0, 0, 255), 2)

cv2.imshow('sdd', arr[1])

cv2.imshow('yahalo', image)
p = [1, 2, 3, 6]
for i, j in enumerate(p):
    print(i, j)

tinggi = board.shape[0]
lebar = board.shape[1]
strr = 'asdadd'
repr(strr)
print(repr(strr))
cv2.imshow('actual', board[0:tinggi-140, 0:lebar])
cv2.waitKey(0)

kernelH = np.array([[-1,1]])
kernelV = np.array([[-1],[1]])
print(kernelH, kernelV)
