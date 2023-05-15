from abc import ABC, abstractmethod
from typing import Tuple

from src.app.base.object import GameObject
from src.app.util.render import RenderOrder


class AbstractActor(ABC, GameObject):
    max_hp: int
    hp: int

    @abstractmethod
    def move(self, target_x: int, target_y: int) -> None:
        ...


class Actor(AbstractActor):

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int], max_hp: int, hp: int):
        super().__init__(x, y, char, color, render_order=RenderOrder.ACTOR, transparent=False, walkable=False)
        self.max_hp = max_hp
        self.hp = hp

    def move(self, target_x: int, target_y: int) -> None:
        self.x += target_x
        self.y += target_y


