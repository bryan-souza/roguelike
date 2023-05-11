from __future__ import annotations

import itertools
import random
from abc import ABC, abstractmethod
from typing import List

import tcod
from loguru import logger

from src.app.object import GameObject
from src.app.tile import Floor, Wall, Tile


class AbstractMap(ABC):
    map_width: int
    map_height: int
    _tiles: List[List[Tile]]
    _objects: List[GameObject]

    @property
    @abstractmethod
    def objects(self):
        ...

    @property
    @abstractmethod
    def tiles(self):
        ...

    @abstractmethod
    def place_objects(self, objects: List[GameObject]) -> None:
        ...

    @abstractmethod
    def get_objects_at_coordinates(self, target_x: int, target_y: int) -> List[GameObject] | None:
        ...

    @abstractmethod
    def remove_object(self, obj: GameObject) -> None:
        ...

    @abstractmethod
    def get_tile_at_coordinates(self, x: int, y: int) -> Tile:
        ...

    @abstractmethod
    def generate_map(self) -> None:
        ...

    @abstractmethod
    def _create_room(self, room: tcod.bsp.BSP) -> None:
        ...

    @abstractmethod
    def _connect_rooms(self, parent_node: tcod.bsp.BSP) -> None:
        ...


class Map(AbstractMap):

    def __init__(self, map_width: int, map_height: int):
        self.map_width = map_width
        self.map_height = map_height
        self._objects = []
        self._tiles = [[Tile(x, y, '.') for y in range(map_height)] for x in range(map_width)]

    @property
    def objects(self):
        return self._objects

    @property
    def tiles(self):
        return itertools.chain(*self._tiles)

    def place_objects(self, objects: List[GameObject]) -> None:
        self._objects.extend(objects)
        logger.debug(f'Placed objects: {objects}')

    def remove_object(self, obj: GameObject) -> None:
        if isinstance(obj, GameObject):
            self._objects.remove(obj)
            logger.debug(f'Removed object: {obj}')

    def get_objects_at_coordinates(self, target_x: int, target_y: int) -> List[GameObject] | None:
        output = []
        for obj in self._objects:
            if obj.x == target_x and obj.y == target_y:
                output.append(obj)

        if not output:
            logger.debug(f'No objects found at coordinates: {target_x}, {target_y}')
            return None

        logger.debug(f'Objects found at coordinates: {target_x}, {target_y}: {output}')
        return output

    def get_tile_at_coordinates(self, x: int, y: int) -> Tile:
        return self._tiles[x][y]

    def generate_map(self) -> None:
        bsp = tcod.bsp.BSP(0, 0, self.map_width - 1, self.map_height - 1)
        bsp.split_recursive(5, 8, 8, 1.0, 1.0)

        for node in bsp.inverted_level_order():
            if node.children:
                self._connect_rooms(node)
                logger.debug(f'Connected rooms: {node.children}')
                continue

            self._create_room(node)
            logger.debug(f'Created room: {node}')

    def _connect_rooms(self, parent_node: tcod.bsp.BSP) -> None:
        while True:
            door_x, door_y = self._get_door_coordinates(parent_node)
            if not self._is_door_obstructed(door_x, door_y):
                self._tiles[door_x][door_y] = Floor(door_x, door_y)
                break

    def _create_room(self, room: tcod.bsp.BSP) -> None:
        for x in range(room.x, (room.x + room.width) + 1):
            for y in range(room.y, (room.y + room.height) + 1):
                if x == room.x or x == room.x + room.width or y == room.y or y == room.y + room.height:
                    self._tiles[x][y] = Wall(x, y)
                    continue

                self._tiles[x][y] = Floor(x, y)

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
        top_tile = self.get_tile_at_coordinates(door_x, door_y + 1)
        right_tile = self.get_tile_at_coordinates(door_x + 1, door_y)
        bottom_tile = self.get_tile_at_coordinates(door_x, door_y - 1)
        left_tile = self.get_tile_at_coordinates(door_x - 1, door_y)

        if (top_tile.walkable and bottom_tile.walkable) or (right_tile.walkable and left_tile.walkable):
            return False

        return True
