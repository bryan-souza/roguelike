from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from src.app.object import GameObject


class AbstractMap(ABC):

    @property
    @abstractmethod
    def objects(self):
        ...

    @abstractmethod
    def get_object_in_position(self, target_x: int, target_y: int) -> GameObject | None:
        ...


class Map(AbstractMap):
    _objects: List[GameObject]

    def __init__(self, objects: List[GameObject]):
        self._objects = objects

    @property
    def objects(self):
        return self._objects

    def get_object_in_position(self, target_x: int, target_y: int) -> GameObject | None:
        # TODO: Optimize object search
        for obj in self.objects:
            if (obj.x == target_x) and (obj.y == target_y):
                return obj

            return None
