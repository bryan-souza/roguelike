from __future__ import annotations

import itertools
import random
from abc import ABC, abstractmethod
from typing import List

import numpy as np
import tcod
from loguru import logger

from src.app.base.actor import Actor
from src.app.base.object import GameObject
from src.app.util.tile import Floor, Wall, Tile


class AbstractGameMap(ABC):
    _tiles: List[List[Tile]]
    _objects: List[GameObject]
    _actors: List[Actor]

    @property
    @abstractmethod
    def tiles(self):
        ...

    @property
    @abstractmethod
    def objects(self):
        ...

    @property
    @abstractmethod
    def actors(self):
        ...

    @abstractmethod
    def get_tile_at_coordinates(self, x: int, y: int) -> Tile:
        ...

    @abstractmethod
    def place_objects(self, objects: List[GameObject]) -> None:
        ...

    @abstractmethod
    def get_objects_at_coordinates(self, x: int, y: int) -> List[GameObject]:
        ...

    @abstractmethod
    def remove_object(self, obj: GameObject) -> None:
        ...

    @abstractmethod
    def place_actors(self, actors: List[Actor]) -> None:
        ...

    @abstractmethod
    def get_actor_at_coordinates(self, x: int, y: int) -> Actor | None:
        ...

    @abstractmethod
    def remove_actor(self, actor: Actor) -> None:
        ...

    @abstractmethod
    def compute_fov(self, player: Actor) -> None:
        ...


class AbstractMapBuilder(ABC):
    _tiles: List[List[Tile]]

    @abstractmethod
    def generate_map(self) -> AbstractGameMap:
        ...

    @abstractmethod
    def _create_room(self, room: tcod.bsp.BSP) -> None:
        ...

    @abstractmethod
    def _connect_rooms(self, parent_node: tcod.bsp.BSP) -> None:
        ...

    @staticmethod
    @abstractmethod
    def _get_door_coordinates(parent_node: tcod.bsp.BSP) -> tuple[int, int]:
        ...

    @abstractmethod
    def _is_door_obstructed(self, door_x: int, door_y: int) -> bool:
        ...


class GameMap(AbstractGameMap):
    def __init__(self, tiles: List[List[Tile]]):
        self._tiles = tiles
        self._objects = []
        self._actors = []

    @property
    def tiles(self):
        logger.debug(self._tiles[:10])
        return list(itertools.chain.from_iterable(self._tiles))

    @property
    def objects(self):
        return self._objects

    @property
    def actors(self):
        return self._actors

    def get_tile_at_coordinates(self, x: int, y: int) -> Tile:
        return self._tiles[x][y]

    def place_objects(self, objects: List[GameObject]) -> None:
        self._objects.extend(objects)
        logger.debug(f'Placed objects: {objects}')

    def get_objects_at_coordinates(self, x: int, y: int) -> List[GameObject]:
        object_list = []

        for obj in self._objects:
            if obj.x == x and obj.y == y:
                object_list.append(obj)

        logger.debug(f'Found objects at coordinates {x}, {y}: {object_list}')
        return object_list

    def remove_object(self, obj: GameObject) -> None:
        self._objects.remove(obj)
        logger.debug(f'Removed object: {obj}')

    def place_actors(self, actors: List[Actor]) -> None:
        self._actors.extend(actors)
        logger.debug(f'Placed actors: {actors}')

    def get_actor_at_coordinates(self, x: int, y: int) -> Actor | None:
        for actor in self._actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def remove_actor(self, actor: Actor) -> None:
        self._actors.remove(actor)

    def compute_fov(self, player: Actor) -> None:
        transparent_tiles = np.array([[tile.transparent for tile in row] for row in self._tiles])
        visible = tcod.map.compute_fov(transparent_tiles, (player.x, player.y), radius=5)

        map_width, map_height = transparent_tiles.shape
        for x, y in itertools.product(range(map_width), range(map_height)):
            self._tiles[x][y].visible = False

            if visible[x, y]:
                self._tiles[x][y].visible = True
                self._tiles[x][y].explored = True


class GameMapBuilder(AbstractMapBuilder):

    def __init__(self, map_width: int, map_height: int):
        self.map_width = map_width
        self.map_height = map_height
        self._tiles = [[Tile(x, y, '.') for y in range(map_height)] for x in range(map_width)]

    def generate_map(self) -> AbstractGameMap:
        bsp = tcod.bsp.BSP(0, 0, self.map_width - 1, self.map_height - 1)
        bsp.split_recursive(5, 8, 8, 1.0, 1.0)

        for node in bsp.inverted_level_order():
            if node.children:
                self._connect_rooms(node)
                logger.debug(f'Connected rooms: {node.children}')
                continue

            self._create_room(node)
            logger.debug(f'Created room: {node}')

        return GameMap(self._tiles)

    def _create_room(self, room: tcod.bsp.BSP) -> None:
        for x in range(room.x, (room.x + room.width) + 1):
            for y in range(room.y, (room.y + room.height) + 1):
                if x == room.x or x == room.x + room.width or y == room.y or y == room.y + room.height:
                    self._tiles[x][y] = Wall(x, y)
                    continue

                self._tiles[x][y] = Floor(x, y)

    def _connect_rooms(self, parent_node: tcod.bsp.BSP) -> None:
        while True:
            door_x, door_y = self._get_door_coordinates(parent_node)
            if not self._is_door_obstructed(door_x, door_y):
                self._tiles[door_x][door_y] = Floor(door_x, door_y)
                break

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
        top_tile = self._tiles[door_x][door_y + 1]
        bottom_tile = self._tiles[door_x][door_y - 1]
        right_tile = self._tiles[door_x + 1][door_y]
        left_tile = self._tiles[door_x - 1][door_y]

        if (top_tile.walkable and bottom_tile.walkable) or (right_tile.walkable and left_tile.walkable):
            return False

        return True
