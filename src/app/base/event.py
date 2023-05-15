# Cleaner way to solve cyclic imports (applies only when cyclic imports are caused by typing)
# Source:
# https://stackoverflow.com/questions/744373/what-happens-when-using-mutual-or-circular-cyclic-imports/67673741#67673741
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.app.base.context import AbstractGameContext


from abc import ABC, abstractmethod

import tcod

from src.app.util.direction import Direction


class AbstractEventHandler(ABC):

    @abstractmethod
    def handle_event(self, *args, **kwargs) -> None:
        ...


class ExitEventHandler(AbstractEventHandler):

    def handle_event(self, event: tcod.event.Event):
        if isinstance(event, tcod.event.Quit):
            raise SystemExit()


class PlayerMovementEventHandler(AbstractEventHandler):

    def handle_event(self, event: tcod.event.Event, game_context: AbstractGameContext):
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

            tile_at_target_position = game_context.game_map.get_tile_at_coordinates(target_x, target_y)
            if tile_at_target_position is not None and tile_at_target_position.walkable:
                game_context.player.move(*direction)
