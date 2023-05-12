from typing import Tuple, Optional

from src.app.palette import Color
from src.app.render import RenderOrder


class GameObject:
    x: int
    y: int
    char: str
    color: Tuple[int, int, int]
    render_order: RenderOrder
    transparent: bool
    walkable: bool

    def __init__(
            self,
            x: int,
            y: int,
            char: str,
            color: Optional[Tuple[int, int, int]] = None,
            render_order: Optional[RenderOrder] = None,
            transparent: Optional[bool] = None,
            walkable: Optional[bool] = None
    ):
        if color is None:
            color = Color.WHITE

        if render_order is None:
            render_order = RenderOrder.TILE

        if transparent is None:
            transparent = False

        if walkable is None:
            walkable = False

        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.render_order = render_order
        self.transparent = transparent
        self.walkable = walkable

    def __str__(self):
        return f'<GameObject x={self.x} y={self.y} char={self.char} color={self.color} render_order={self.render_order}>'


class MovableObject(GameObject):

    def __init__(
            self,
            x: int,
            y: int,
            char: str,
            color: Optional[Tuple[int, int, int]] = None,
            render_order: Optional[RenderOrder] = None,
            transparent: Optional[bool] = None,
            walkable: Optional[bool] = None
    ):
        if color is None:
            color = Color.WHITE

        if render_order is None:
            render_order = RenderOrder.ACTOR

        if transparent is None:
            transparent = False

        if walkable is None:
            walkable = False

        super().__init__(x, y, char, color, render_order, transparent, walkable)

    def move(self, target_x: int, target_y: int):
        self.x += target_x
        self.y += target_y
