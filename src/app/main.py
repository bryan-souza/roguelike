from pathlib import Path

import tcod
from loguru import logger

from src.app.actor import Actor
from src.app.context import GameContext
from src.app.map import GameMap, GameMapBuilder
from src.app.palette import Color


def main():
    tileset_path = Path('..', '..', 'assets', 'dejavu10x10_gs_tc.png').resolve().absolute()
    tileset = tcod.tileset.load_tilesheet(tileset_path, 32, 8, tcod.tileset.CHARMAP_TCOD)
    logger.debug(f'Loaded tileset from file {tileset_path}')

    console = tcod.Console(80, 50, order='F')
    player = Actor(1, 1, '@', Color.WHITE, 100, 100)
    actors = [
        player
    ]

    map_builder = GameMapBuilder(console.width, console.height)
    game_map = map_builder.generate_map()
    logger.debug('Map generated successfully')

    game_map.place_objects([])
    logger.debug('Objects placed successfully')

    game_map.place_actors(actors)
    logger.debug('Actors placed successfully')

    with tcod.context.new(columns=console.width, rows=console.height, tileset=tileset) as context:
        game_context = GameContext(game_map, console, context, player)
        game_context.start_game()


if __name__ == "__main__":
    main()
