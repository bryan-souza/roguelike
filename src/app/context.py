from abc import ABC, abstractmethod

import tcod
from loguru import logger

from src.app.actor import Actor
from src.app.event import ExitEventHandler, PlayerMovementEventHandler
from src.app.map import GameMap
from src.app.util.palette import Palette, Color


class AbstractGameContext(ABC):
    game_map: GameMap
    root_console: tcod.Console
    tcod_context: tcod.context.Context
    player: Actor

    @abstractmethod
    def start_game(self):
        ...

    @abstractmethod
    def _render_all(self):
        ...


class GameContext(AbstractGameContext):

    def __init__(
        self,
        game_map: GameMap,
        root_console: tcod.Console,
        tcod_context: tcod.context.Context,
        player: Actor
    ):
        self.game_map = game_map
        self.root_console = root_console
        self.tcod_context = tcod_context
        self.player = player

    def start_game(self):
        exit_event_handler = ExitEventHandler()
        player_movement_event_handler = PlayerMovementEventHandler()
        logger.debug(f'Registered event handlers: {[exit_event_handler, player_movement_event_handler]}')

        while True:
            self._render_all()

            for event in tcod.event.wait():
                self.tcod_context.convert_event(event)
                logger.debug(f'Received event: {event}')

                exit_event_handler.handle_event(event)
                player_movement_event_handler.handle_event(event, self)

    def _render_all(self):
        self.root_console.clear()
        self.game_map.compute_fov(self.player)

        for tile in self.game_map.tiles:
            if tile.visible:
                self.root_console.print(tile.x, tile.y, tile.char, tile.color, Palette.BACKGROUND)

                actor_in_tile = self.game_map.get_actor_at_coordinates(tile.x, tile.y)
                objects_in_tile = self.game_map.get_objects_at_coordinates(tile.x, tile.y)

                objects_to_be_rendered = objects_in_tile
                if actor_in_tile:
                    objects_to_be_rendered = [actor_in_tile, *objects_in_tile]

                objects_ordered_by_render_order = sorted(objects_to_be_rendered, key=lambda o: o.render_order.value)
                for obj in objects_ordered_by_render_order:
                    self.root_console.print(obj.x, obj.y, obj.char, obj.color, Palette.BACKGROUND)
            elif tile.explored:
                self.root_console.print(tile.x, tile.y, tile.char, Color.DARK_GRAY, Palette.BACKGROUND)

        self.tcod_context.present(self.root_console)
