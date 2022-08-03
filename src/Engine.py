import cv2
import Common
from BrowserWrapper import OpenBrowserAndStoreCustomLabyrinth

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Color = namedtuple('Color', ['B', 'G', 'R'])

def GetProcessedLabyrinthImage() -> cv2.Mat | None:
    print('Reading stored labyrinth')
    labyrinth: cv2.Mat | None = cv2.imread(Common.LABYRINTH_PATH, cv2.IMREAD_GRAYSCALE)

    if labyrinth is None:
        print('Labyrinth image not found')
        return None

    _, threshold = cv2.threshold(labyrinth, 150, 255, cv2.THRESH_BINARY)
    binary_labyrinth = cv2.bitwise_and(labyrinth, labyrinth, mask=threshold)
    labyrinth = cv2.cvtColor(binary_labyrinth, cv2.COLOR_GRAY2RGB)
    
    cv2.imshow('Labyrinth', labyrinth)
    cv2.waitKey()

    return labyrinth

def GetStartPoint(labyrinth: cv2.Mat) -> Point:
    # Find leftmost vertical wall
    row = 30
    col = 0
    while tuple(labyrinth[row, col]) != Common.COLOR_BLACK:
        labyrinth[row, col] = [0, 255, 0]
        if col % 5 == 0:
            cv2.imshow('Looking for line', labyrinth)
            cv2.waitKey()

        col += 1

    print(row, col, 'Found black tile')

    while tuple(labyrinth[row, col]) == Common.COLOR_BLACK:
        labyrinth[row, col] = [0, 255, 0]
        if row % 5 == 0:
            cv2.imshow('Looking for line', labyrinth)
            cv2.waitKey()

        row -= 1

    row += 1

    print(row, col, 'Found last black tile')

    while tuple(labyrinth[row, col]) != Common.COLOR_WHITE:
        labyrinth[row, col] = [0, 255, 0]
        if col % 5 == 0:
            cv2.imshow('Looking for line', labyrinth)
            cv2.waitKey()

        col += 1

    print(row, col, 'Found entrance')
        

    return Point(col, row)

def DrawRectangle(img: cv2.Mat, start_point: Point, width: int, height: int, color: Color):
    for col in range(width):
        for row in range(height):
            img[start_point.y + row][start_point.x + col] = list(color)

    cv2.imshow('DrawRectangle', img)
    cv2.waitKey()

def PlayGame(make_new_labyrinth: bool):
    if make_new_labyrinth:
        if not OpenBrowserAndStoreCustomLabyrinth(Common.NUM_ROWS, Common.NUM_COLUMNS, Common.LABYRINTH_PATH):
            print('Failed to store custom labyrinth')

    labyrinth = GetProcessedLabyrinthImage()
    start_point = GetStartPoint(labyrinth)

    labyrinth_height, labyrinth_width, _ = labyrinth.shape

    block_height = int(labyrinth_height / Common.NUM_ROWS * 0.80)
    block_width = int(labyrinth_width / Common.NUM_COLUMNS * 0.80)

    print(labyrinth_height, labyrinth_width)
    print(block_height, block_width)

    DrawRectangle(labyrinth, start_point, block_height, block_width, Color(0, 0, 255))


    

if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    PlayGame(True)