from enum import Enum, auto

WIDTH = 900
HEIGHT = 500


class Color:
    # Basic
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Application specific
    GOBLIN_GREEN = (0, 138, 5)
    GOBLIN_PURPLE = (211, 46, 255)


class Position(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    MIDDLE = 4

    @staticmethod
    def center(x, y, width, height, obj_width, obj_height):
        return x + (width - obj_width) // 2, y + (height - obj_height) // 2

    @staticmethod
    def center_x(x, width, obj_width):
        return x + (width - obj_width) // 2

    @staticmethod
    def center_y(y, height, obj_height):
        return y + (height - obj_height) // 2


class ScreenType(Enum):
    TITLE = auto
    GAME = auto
    SHOP = auto
    GUI = auto


class Rotate(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
