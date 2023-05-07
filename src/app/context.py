from abc import ABC, abstractmethod

import tcod

from src.app.character import Character
from src.app.direction import Direction
from src.app.map import AbstractMap
from src.app.tile import Tile


class AbstractGameContext(ABC):

    @abstractmethod
    def start_game(self):
        ...


class GameContext(AbstractGameContext):
    game_map: AbstractMap
    root_console: tcod.Console
    tcod_context: tcod.context.Context
    player: Character

    def __init__(self, game_map: AbstractMap, root_console: tcod.Console, tcod_context: tcod.context.Context,
                 player: Character):
        self.game_map = game_map
        self.root_console = root_console
        self.tcod_context = tcod_context
        self.player = player

    def start_game(self):
        while True:
            self.root_console.clear()

            for obj in self.game_map.objects:
                self.root_console.print(obj.x, obj.y, obj.char, obj.color)

            self.tcod_context.present(self.root_console)

            for event in tcod.event.wait():
                self.tcod_context.convert_event(event)

                # Player movement
                # TODO: Move this to a separate class
                if isinstance(event, tcod.event.KeyDown):
                    print(event)

                    if event.sym == tcod.event.KeySym.LEFT:
                        direction = Direction.LEFT
                    elif event.sym == tcod.event.KeySym.RIGHT:
                        direction = Direction.RIGHT
                    elif event.sym == tcod.event.KeySym.UP:
                        direction = Direction.UP
                    elif event.sym == tcod.event.KeySym.DOWN:
                        direction = Direction.DOWN

                    if direction:
                        target_x = self.player.x + direction[0]
                        target_y = self.player.y + direction[1]

                        object_at_target_position = self.game_map.get_object_in_position(target_x, target_y)
                        if object_at_target_position is None:
                            self.player.move(*direction)
                        else:
                            if isinstance(object_at_target_position, Tile) and object_at_target_position.walkable:
                                self.player.move(*direction)

                        print(self.player.x, self.player.y)

                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
