from abc import ABC, abstractmethod

import tcod
from loguru import logger

from src.app.character import Character
from src.app.event import ExitEventHandler, PlayerMovementEventHandler
from src.app.map import AbstractMap
from src.app.palette import Palette


class AbstractGameContext(ABC):
    game_map: AbstractMap
    root_console: tcod.Console
    tcod_context: tcod.context.Context
    player: Character

    @abstractmethod
    def start_game(self):
        ...


class GameContext(AbstractGameContext):

    def __init__(self, game_map: AbstractMap, root_console: tcod.Console, tcod_context: tcod.context.Context,
                 player: Character):
        self.game_map = game_map
        self.root_console = root_console
        self.tcod_context = tcod_context
        self.player = player

    def start_game(self):
        exit_event_handler = ExitEventHandler()
        player_movement_event_handler = PlayerMovementEventHandler()
        logger.debug(f'Registered event handlers: {[exit_event_handler, player_movement_event_handler]}')

        while True:
            self.root_console.clear()

            objects_ordered_by_render_order = sorted(self.game_map.objects, key=lambda o: o.render_order.value)
            for obj in objects_ordered_by_render_order:
                self.root_console.print(obj.x, obj.y, obj.char, obj.color, Palette.BACKGROUND)

            self.tcod_context.present(self.root_console)

            for event in tcod.event.wait():
                self.tcod_context.convert_event(event)
                logger.debug(f'Received event: {event}')

                exit_event_handler.handle_event(event)
                player_movement_event_handler.handle_event(event, self)
