from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import List

from src.app.object import GameObject

import tcod

from src.app.tile import Floor, Wall, Tile


class AbstractMap(ABC):
    _objects: List[GameObject]

    @property
    @abstractmethod
    def objects(self):
        ...

    @abstractmethod
    def place_objects(self, objects: List[GameObject]) -> None:
        ...

    @abstractmethod
    def remove_object_at_position(self, target_x: int, target_y: int) -> None:
        ...

    @abstractmethod
    def generate_map(self, map_width: int, map_height: int) -> None:
        ...

    @abstractmethod
    def _create_room(self, room: tcod.bsp.BSP) -> None:
        ...

    @abstractmethod
    def _connect_rooms(self, parent_node: tcod.bsp.BSP) -> None:
        ...

    @abstractmethod
    def get_object_in_position(self, target_x: int, target_y: int) -> GameObject | None:
        ...


class Map(AbstractMap):

    def __init__(self):
        self._objects = []

    @property
    def objects(self):
        return self._objects

    def place_objects(self, objects: List[GameObject]) -> None:
        self._objects.extend(objects)

    def remove_object_at_position(self, target_x: int, target_y: int) -> None:
        obj = self.get_object_in_position(target_x, target_y)
        if obj:
            self._objects.remove(obj)

    def get_object_in_position(self, target_x: int, target_y: int) -> GameObject | None:
        # TODO: Optimize object search
        for obj in self._objects:
            if (obj.x == target_x) and (obj.y == target_y):
                return obj

        return None

    def generate_map(self, map_width: int, map_height: int) -> None:
        bsp = tcod.bsp.BSP(0, 0, map_width - 1, map_height - 1)
        bsp.split_recursive(5, 8, 8, 1.0, 1.0)

        for node in bsp.inverted_level_order():
            if node.children:
                self._connect_rooms(node)
                continue

            self._create_room(node)

    def _connect_rooms(self, parent_node: tcod.bsp.BSP) -> None:
        while True:
            door_x, door_y = self._get_door_coordinates(parent_node)
            if not self._is_door_obstructed(door_x, door_y):
                self._objects.append(Floor(door_x, door_y))
                break

    def _create_room(self, room: tcod.bsp.BSP) -> None:
        for x in range(room.x, (room.x + room.width) + 1):
            for y in range(room.y, (room.y + room.height) + 1):
                if x == room.x or x == room.x + room.width or y == room.y or y == room.y + room.height:
                    self._objects.append(Wall(x, y))
                    continue

                self._objects.append(Floor(x, y))

    @staticmethod
    def _get_door_coordinates(parent_node: tcod.bsp.BSP) -> tuple[int, int]:
        if parent_node.horizontal:
            door_x = random.randint(parent_node.x + 1, (parent_node.x + parent_node.width) - 1)
            door_y = parent_node.position
        else:
            door_x = parent_node.position
            door_y = random.randint(parent_node.y + 1, (parent_node.y + parent_node.height) - 1)

        return door_x, door_y

    def _is_door_obstructed(self, door_x: int, door_y: int) -> bool:
        top_tile = self._get_tile_at_coordinates(door_x, door_y + 1)
        right_tile = self._get_tile_at_coordinates(door_x + 1, door_y)
        bottom_tile = self._get_tile_at_coordinates(door_x, door_y - 1)
        left_tile = self._get_tile_at_coordinates(door_x - 1, door_y)

        if (top_tile.walkable and bottom_tile.walkable) or (right_tile.walkable and left_tile.walkable):
            return False

        return True

    def _get_tile_at_coordinates(self, x: int, y: int) -> Tile:
        for obj in self.objects:
            if isinstance(obj, Tile) and (obj.x == x) and (obj.y == y):
                return obj

        return Floor(x, y)
