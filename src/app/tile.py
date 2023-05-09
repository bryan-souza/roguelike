from typing import Tuple, Optional

from src.app.object import GameObject
from src.app.palette import Palette


class Tile(GameObject):
    visible: bool
    walkable: bool


class Wall(Tile):

    def __init__(self, x: int, y: int, char: Optional[str] = None, color: Optional[Tuple[int, int, int]] = None):
        if char is None:
            char = '#'
        if color is None:
            color = Palette.FOREGROUND

        super().__init__(x, y, char, color)
        self.visible = True
        self.walkable = False


class Floor(Tile):

    def __init__(self, x: int, y: int, char: Optional[str] = None, color: Optional[Tuple[int, int, int]] = None):
        if char is None:
            char = '.'
        if color is None:
            color = Palette.FOREGROUND

        super().__init__(x, y, char, color)
        self.visible = True
        self.walkable = True
