from src.app.object import MovableObject

from typing import Tuple

from src.app.render import RenderOrder


class Actor(MovableObject):
    max_hp: int
    hp: int

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int], max_hp: int, hp: int):
        render_order = RenderOrder.ACTOR
        transparent = False
        walkable = False

        super().__init__(x, y, char, color, render_order, transparent, walkable)
        self.max_hp = max_hp
        self.hp = hp
