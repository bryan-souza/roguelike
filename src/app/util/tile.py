from typing import Tuple, Optional

from src.app.base.object import GameObject
from src.app.util.palette import Palette
from src.app.util.render import RenderOrder


class Tile(GameObject):
    visible: bool
    explored: bool


class Wall(Tile):

    def __init__(
            self,
            x: int,
            y: int,
            char: Optional[str] = None,
            color: Optional[Tuple[int, int, int]] = None
    ):
        if char is None:
            char = '#'
        if color is None:
            color = Palette.FOREGROUND

        render_order = RenderOrder.TILE
        transparent = False
        walkable = False

        super().__init__(x, y, char, color, render_order, transparent, walkable)
        self.visible = False
        self.explored = False

    def __str__(self):
        return f'<Wall(x={self.x}, y={self.y}, transparent={self.transparent}, walkable={self.walkable}, visible={self.visible}, explored={self.explored})>'


class Floor(Tile):

    def __init__(
            self,
            x: int,
            y: int,
            char: Optional[str] = None,
            color: Optional[Tuple[int, int, int]] = None,
    ):
        if char is None:
            char = '.'
        if color is None:
            color = Palette.FOREGROUND

        render_order = RenderOrder.TILE
        transparent = True
        walkable = True

        super().__init__(x, y, char, color, render_order, transparent, walkable)
        self.visible = False
        self.explored = False

    def __str__(self):
        return f'<Floor(x={self.x}, y={self.y}, transparent={self.transparent}, walkable={self.walkable}, visible={self.visible}, explored={self.explored})>'
