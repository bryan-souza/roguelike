import tcod

from src.app.character import Character
from src.app.context import GameContext
from src.app.map import Map
from src.app.palette import Color


def main():
    tileset = tcod.tileset.load_tilesheet("../../assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    console = tcod.Console(80, 50, order='F')
    player = Character(1, 1, '@', Color.WHITE, 100, 100)
    objects = [
        player
    ]

    game_map = Map()
    game_map.generate_map(console.width, console.height)
    game_map.place_objects(objects)

    with tcod.context.new(columns=console.width, rows=console.height, tileset=tileset) as context:
        game_context = GameContext(game_map, console, context, player)
        game_context.start_game()


if __name__ == "__main__":
    main()
