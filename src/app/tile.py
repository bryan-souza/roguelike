from typing import Tuple, Optional

from src.app.object import GameObject
from src.app.palette import Palette
from src.app.render import RenderOrder


class Tile(GameObject):
    visible: bool
    walkable: bool


class Wall(Tile):

    def __init__(
            self,
            x: int,
            y: int,
            char: Optional[str] = None,
            color: Optional[Tuple[int, int, int]] = None,
            render_order: Optional[RenderOrder] = None
    ):
        if char is None:
            char = '#'
        if color is None:
            color = Palette.FOREGROUND
        if render_order is None:
            render_order = RenderOrder.TILE

        super().__init__(x, y, char, color, render_order)
        self.visible = True
        self.walkable = False

    def __str__(self):
        return f'<Wall(x={self.x}, y={self.y},  char={self.char}, color={self.color}, render_order={self.render_order})>'


class Floor(Tile):

    def __init__(
            self,
            x: int,
            y: int,
            char: Optional[str] = None,
            color: Optional[Tuple[int, int, int]] = None,
            render_order: Optional[RenderOrder] = None
    ):
        if char is None:
            char = '.'
        if color is None:
            color = Palette.FOREGROUND
        if render_order is None:
            render_order = RenderOrder.TILE

        super().__init__(x, y, char, color, render_order)
        self.visible = True
        self.walkable = True

    def __str__(self):
        return f'<Floor(x={self.x}, y={self.y},  char={self.char}, color={self.color}, render_order={self.render_order})>'
