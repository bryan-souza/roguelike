from typing import Tuple

from src.app.object import GameObject


class Tile(GameObject):
    visible: bool
    walkable: bool


class Wall(Tile):

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        super().__init__(x, y, char, color)
        self.visible = True
        self.walkable = False


class Floor(Tile):

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        super().__init__(x, y, char, color)
        self.visible = True
        self.walkable = True
