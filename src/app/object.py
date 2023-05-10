from typing import Tuple, Optional

from src.app.palette import Color
from src.app.render import RenderOrder


class GameObject:
    x: int
    y: int
    char: str
    color: Tuple[int, int, int]
    render_order: RenderOrder

    def __init__(self, x: int, y: int, char: str, color: Optional[Tuple[int, int, int]] = None, render_order: Optional[RenderOrder] = None):
        if color is None:
            color = Color.WHITE

        if render_order is None:
            render_order = RenderOrder.TILE

        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.render_order = render_order

    def __str__(self):
        return f'<GameObject x={self.x} y={self.y} char={self.char} color={self.color} render_order={self.render_order}>'


class MovableObject(GameObject):

    def __init__(self, x: int, y: int, char: str, color: Optional[Tuple[int, int, int]] = None, render_order: Optional[RenderOrder] = None):
        if render_order is None:
            render_order = RenderOrder.ACTOR

        super().__init__(x, y, char, color, render_order)

    def move(self, target_x: int, target_y: int):
        self.x += target_x
        self.y += target_y
