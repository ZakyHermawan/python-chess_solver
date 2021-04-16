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


cv2.imshow('yahalo', image)
cv2.waitKey(0)
