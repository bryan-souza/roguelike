from src.app.object import MovableObject

from typing import Tuple


class Character(MovableObject):
    max_hp: int
    hp: int

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int], max_hp: int, hp: int):
        super().__init__(x, y, char, color)
        self.max_hp = max_hp
        self.hp = hp
