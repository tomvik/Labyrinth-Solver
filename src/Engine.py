from pygame import Rect
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


def GetExitPoint(labyrinth: cv2.Mat) -> Point:
    # Find leftmost vertical wall
    row = 31
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

        row += 1

    row -= 1

    print(row, col, 'Found last black tile')

    while tuple(labyrinth[row, col]) != Common.COLOR_WHITE:
        labyrinth[row, col] = [0, 255, 0]
        if col % 5 == 0:
            cv2.imshow('Looking for line', labyrinth)
            cv2.waitKey()

        col += 1

    print(row, col, 'Found exit')

    return Point(col, row)

def DrawRectangle(img: cv2.Mat, start_point: Point, width: int, height: int, color: Color):
    for col in range(width):
        for row in range(height):
            img[start_point.y + row][start_point.x + col] = list(color)

    cv2.imshow('DrawRectangle', img)
    cv2.waitKey()

def DoRectanglesCollide(first_point: Point, first_width: int, first_height: int, second_point: Point, second_width: int, second_height: int):
    # Too lazy to write it myself.
    first = Rect(first_point.x, first_point.y, first_width, first_height)
    second = Rect(second_point.x, second_point.y, second_width, second_height)

    return first.colliderect(second)

def IsRectangleTouchingAWall(labyrinth: cv2.Mat, point: Point, width: int, height: int):
    labyrinth_height, labyrinth_width, _ = labyrinth.shape

    if point.x < 0 or point.y < 0 or (point.x + width) >= labyrinth_width or (point.y + height) >= labyrinth_height:
        return True

    for col in range(width):
        for row in range(height):
            if tuple(labyrinth[point.y + row][point.x + col]) == Common.COLOR_BLACK:
                return True

    return False


def PlayGame(make_new_labyrinth: bool):
    if make_new_labyrinth:
        if not OpenBrowserAndStoreCustomLabyrinth(Common.NUM_ROWS, Common.NUM_COLUMNS, Common.LABYRINTH_PATH):
            print('Failed to store custom labyrinth')

    labyrinth = GetProcessedLabyrinthImage()
    original_labyrinth = labyrinth.copy()
    start_point = GetStartPoint(labyrinth)
    exit_point = GetExitPoint(labyrinth)

    labyrinth_height, labyrinth_width, _ = labyrinth.shape

    block_height = int(labyrinth_height / Common.NUM_ROWS * 0.60)
    block_width = int(labyrinth_width / Common.NUM_COLUMNS * 0.60)

    print(labyrinth_height, labyrinth_width)
    print(block_height, block_width)

    start_point = Point(start_point.x + 1, start_point.y + 1)
    exit_point = Point(exit_point.x, exit_point.y - block_height)


    DrawRectangle(labyrinth, start_point, block_height, block_width, Color(0, 0, 255))
    DrawRectangle(labyrinth, exit_point, block_height, block_width, Color(0, 0, 255))

    if DoRectanglesCollide(start_point, block_width, block_height, exit_point, block_width, block_height):
        print('Collision afar')
    if DoRectanglesCollide(start_point, block_width, block_height, start_point, block_width, block_height):
        print('Collision close')

    if IsRectangleTouchingAWall(original_labyrinth, start_point, block_width, block_height):
        print('Touching a wall')


    

if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    PlayGame(False)