import collections
import sys
from turtle import left
sys.setrecursionlimit(4000)

from typing import List, Set
from pygame import Rect
import cv2
import Common
from BrowserWrapper import OpenBrowserAndStoreCustomLabyrinth

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Color = namedtuple('Color', ['B', 'G', 'R'])

found_solution = False


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
    row = 30
    col = 0
    while tuple(labyrinth[row, col]) != Common.COLOR_BLACK:
        col += 1

    print(row, col, 'Found black tile')

    while tuple(labyrinth[row, col]) == Common.COLOR_BLACK:
        row -= 1

    row += 1

    print(row, col, 'Found last black tile')

    while tuple(labyrinth[row, col]) != Common.COLOR_WHITE:
        col += 1

    print(row, col, 'Found entrance')

    return Point(col, row)


def GetExitPoint(labyrinth: cv2.Mat) -> Point:
    row = 31
    col = 0
    while tuple(labyrinth[row, col]) != Common.COLOR_BLACK:
        col += 1

    print(row, col, 'Found black tile')

    while tuple(labyrinth[row, col]) == Common.COLOR_BLACK:
        row += 1

    row -= 1

    print(row, col, 'Found last black tile')

    while tuple(labyrinth[row, col]) != Common.COLOR_WHITE:
        col += 1

    print(row, col, 'Found exit')

    return Point(col, row)

def DrawRectangle(img: cv2.Mat, start_point: Point, width: int, height: int, color: Color, show_img: bool = True):
    for col in range(width):
        for row in range(height):
            img[start_point.y + row][start_point.x + col] = list(color)

    if show_img:
        cv2.imshow('DrawRectangle', img)
        cv2.waitKey(5)

def DoRectanglesCollide(first_point: Point, first_width: int, first_height: int, second_point: Point, second_width: int, second_height: int):
    # Too lazy to write it myself.
    first = Rect(first_point.x, first_point.y, first_width, first_height)
    second = Rect(second_point.x, second_point.y, second_width, second_height)

    return first.colliderect(second)

def IsRectangleTouchingAWall(labyrinth: cv2.Mat, point: Point, width: int, height: int):
    labyrinth_height, labyrinth_width, _ = labyrinth.shape

    if point.x < 0 or point.y < 0 or (point.x + width) >= labyrinth_width or (point.y + height) >= labyrinth_height:
        return True

    # If too slow, maybe check only the perimeter.
    for col in range(width):
        for row in range(height):
            if tuple(labyrinth[point.y + row][point.x + col]) == Common.COLOR_BLACK:
                return True

    return False

def MoveRectangle(labyrinth: cv2.Mat, point: Point, width: int, height: int, dx: int, dy: int) -> Point:
    labyrinth_height, labyrinth_width, _ = labyrinth.shape

    print(point, width, height, dx, dy, labyrinth_height, labyrinth_width)

    if point.x < 0 or \
       (point.x + dx < 0) or \
       point.y < 0 or \
       (point.y + dy) < 0 or \
       (point.x + width) >= labyrinth_width or \
       (point.x + width + dx) >= labyrinth_width or \
       (point.y + height) >= labyrinth_height or \
       (point.y + height + dy) >= labyrinth_height:
        print('Cannot move')
        return point

    DrawRectangle(labyrinth, point, width, height, Color(0, 0, 100), False)

    next_point = Point(point.x + dx, point.y + dy)

    DrawRectangle(labyrinth, next_point, width, height, Color(0, 0, 255))

    return next_point

def PointsAreEqual(first: Point, second: Point):
    return first.x == second.x and first.y == second.y

# DFS solution
def SolveRecursivelyDFS(original_labyrinth: cv2.Mat, labyrinth: cv2.Mat, start_point: Point, width: int, height: int, path: List[Point], depth: int, end_point: Point):
    global found_solution

    print(depth)
    if IsRectangleTouchingAWall(labyrinth, start_point, width, height) or found_solution:
        return

    if DoRectanglesCollide(start_point, width, height, end_point, width, height):
        print("Made it to the end", depth, path)
        found_solution = True
        return

    can_go_left = True
    for i in range(height):
        if tuple(labyrinth[start_point.y + i][start_point.x - 1]) != Common.COLOR_WHITE:
            can_go_left = False
            break

    if can_go_left:
        left_point = MoveRectangle(labyrinth, start_point, width, height, -1, 0)
        if PointsAreEqual(start_point, left_point):
            return
        left_path = path.copy()
        left_path.append(left_point)
        SolveRecursivelyDFS(original_labyrinth, labyrinth, left_point, width, height, left_path, depth + 1, end_point)

    can_go_up = True
    for i in range(width):
        if tuple(labyrinth[start_point.y - 1][start_point.x + i]) != Common.COLOR_WHITE:
            can_go_up = False
            break

    if can_go_up:
        up_point = MoveRectangle(labyrinth, start_point, width, height, 0, -1)
        if PointsAreEqual(start_point, up_point):
            return
        up_path = path.copy()
        up_path.append(up_point)
        SolveRecursivelyDFS(original_labyrinth, labyrinth, up_point, width, height, up_path, depth + 1, end_point)

    can_go_right = True
    for i in range(height):
        if tuple(labyrinth[start_point.y + i][start_point.x + width + 1]) != Common.COLOR_WHITE:
            can_go_right = False
            break

    if can_go_right:
        right_point = MoveRectangle(labyrinth, start_point, width, height, 1, 0)
        if PointsAreEqual(start_point, right_point):
            return
        right_path = path.copy()
        right_path.append(right_point)
        SolveRecursivelyDFS(original_labyrinth, labyrinth, right_point, width, height, right_path, depth + 1, end_point)

    can_go_down = True
    for i in range(height):
        if tuple(labyrinth[start_point.y + height + 1][start_point.x + i]) != Common.COLOR_WHITE:
            can_go_down = False
            break

    if can_go_down:
        down_point = MoveRectangle(labyrinth, start_point, width, height, 0, 1)
        if PointsAreEqual(start_point, down_point):
            return
        down_path = path.copy()
        down_path.append(down_point)
        SolveRecursivelyDFS(original_labyrinth, labyrinth, down_point, width, height, down_path, depth + 1, end_point)

def SolveLabyrinthBFS(original_labyrinth: cv2.Mat, labyrinth: cv2.Mat, start_point: Point, width: int, height: int, end_point: Point):
    global found_solution

    visited_points: Set[Point] = set()
    next_points = collections.deque([start_point])

    visited_points.add(start_point)

    while next_points:
        print(next_points)
        print(visited_points)
        current_point = next_points.popleft()
        print(current_point)

        if DoRectanglesCollide(current_point, width, height, end_point, width, height):
            print('Finished')
            found_solution = True
            break

        left_point = Point(current_point.x - 1, current_point.y)
        if left_point not in visited_points and not IsRectangleTouchingAWall(labyrinth, left_point, width, height):
            next_points.append(left_point)
            visited_points.add(left_point)
            MoveRectangle(labyrinth, current_point, width, height, -1, 0)

        right_point = Point(current_point.x + 1, current_point.y)
        if right_point not in visited_points and not IsRectangleTouchingAWall(labyrinth, right_point, width, height):
            next_points.append(right_point)
            visited_points.add(right_point)
            MoveRectangle(labyrinth, current_point, width, height, 1, 0)

        up_point = Point(current_point.x, current_point.y - 1)
        if up_point not in visited_points and not IsRectangleTouchingAWall(labyrinth, up_point, width, height):
            next_points.append(up_point)
            visited_points.add(up_point)
            MoveRectangle(labyrinth, current_point, width, height, 0, -1)

        down_point = Point(current_point.x, current_point.y - 1)
        if down_point not in visited_points and not IsRectangleTouchingAWall(labyrinth, down_point, width, height):
            next_points.append(down_point)
            visited_points.add(down_point)
            MoveRectangle(labyrinth, current_point, width, height, 0, 1)


def SolveLabyrinth(original_labyrinth: cv2.Mat, labyrinth: cv2.Mat, start_point: Point, width: int, height: int, end_point: Point):

    path: List[Point] = list()
    path.append(start_point)
    depth = 0

    # SolveRecursivelyDFS(original_labyrinth, labyrinth, start_point, width, height, path, depth, end_point)
    SolveLabyrinthBFS(original_labyrinth, labyrinth, start_point, width, height, end_point)



def PlayGame(make_new_labyrinth: bool):
    if make_new_labyrinth:
        if not OpenBrowserAndStoreCustomLabyrinth(Common.NUM_ROWS, Common.NUM_COLUMNS, Common.LABYRINTH_PATH):
            print('Failed to store custom labyrinth')

    labyrinth = GetProcessedLabyrinthImage()
    original_labyrinth = labyrinth.copy()
    start_point = GetStartPoint(labyrinth)
    exit_point = GetExitPoint(labyrinth)

    labyrinth_height, labyrinth_width, _ = labyrinth.shape

    block_height = int(labyrinth_height / Common.NUM_ROWS * 0.30)
    block_width = int(labyrinth_width / Common.NUM_COLUMNS * 0.30)

    print(labyrinth_height, labyrinth_width)
    print(block_height, block_width)

    start_point = Point(start_point.x + 1, start_point.y + 2)
    exit_point = Point(exit_point.x, exit_point.y - block_height)


    DrawRectangle(labyrinth, start_point, block_height, block_width, Color(0, 0, 255))
    # DrawRectangle(labyrinth, exit_point, block_height, block_width, Color(0, 255, 0))

    if DoRectanglesCollide(start_point, block_width, block_height, exit_point, block_width, block_height):
        print('Collision afar')
    if DoRectanglesCollide(start_point, block_width, block_height, start_point, block_width, block_height):
        print('Collision close')

    if IsRectangleTouchingAWall(original_labyrinth, start_point, block_width, block_height):
        print('Touching a wall')

    SolveLabyrinth(original_labyrinth, labyrinth, start_point, block_width, block_height, exit_point)


    

if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    PlayGame(False)