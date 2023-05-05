from typing import Tuple

from src.app.palette import Color


class GameObject:
    x: int
    y: int
    char: str
    color: Tuple[int, int, int]

    def __init__(self, x: int, y: int, char: str, color=None):
        if color is None:
            color = Color.WHITE

        self.x = x
        self.y = y
        self.char = char
        self.color = color


class MovableObject(GameObject):

    def __init__(self, x: int, y: int, char: str, color=None):
        super().__init__(x, y, char, color)

    def move(self, target_x: int, target_y: int):
        self.x += target_x
        self.y += target_y
