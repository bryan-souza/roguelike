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

            object_at_target_position = game_context.game_map.get_object_in_position(target_x, target_y)
            if object_at_target_position is None:
                game_context.player.move(*direction)
            else:
                if isinstance(object_at_target_position, Tile) and object_at_target_position.walkable:
                    game_context.player.move(*direction)
