from abc import ABC, abstractmethod

import tcod

from src.app.direction import Direction
from src.app.tile import Tile


class AbstractEventHandler(ABC):

    @abstractmethod
    def handle_event(self, *args, **kwargs):
        ...


class ExitEventHandler(AbstractEventHandler):

    def handle_event(self, event: tcod.event.Event):
        if isinstance(event, tcod.event.Quit):
            raise SystemExit()


class PlayerMovementEventHandler(AbstractEventHandler):

    def handle_event(self, event: tcod.event.Event, game_context):
        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.KeySym.LEFT:
                direction = Direction.LEFT
            elif event.sym == tcod.event.KeySym.RIGHT:
                direction = Direction.RIGHT
            elif event.sym == tcod.event.KeySym.UP:
                direction = Direction.UP
            elif event.sym == tcod.event.KeySym.DOWN:
                direction = Direction.DOWN
            else:
                return

            target_x = game_context.player.x + direction[0]
            target_y = game_context.player.y + direction[1]

            objects_at_target_position = game_context.game_map.get_objects_at_coordinates(target_x, target_y)
            if objects_at_target_position is not None:
                for obj in objects_at_target_position:
                    if isinstance(obj, Tile) and obj.walkable:
                        game_context.player.move(*direction)
