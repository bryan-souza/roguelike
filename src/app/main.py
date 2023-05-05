import tcod

from src.app.character import Character
from src.app.direction import Direction
from src.app.palette import Color
from src.app.tile import Wall


def main():
    tileset = tcod.tileset.load_tilesheet("../../assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    console = tcod.Console(80, 50, order='F')
    player = Character(0, 0, '@', Color.WHITE, 100, 100)
    objects = [
        Wall(10, 20, '#', Color.WHITE),
        player
    ]

    with tcod.context.new(columns=console.width, rows=console.height, tileset=tileset) as context:
        while True:
            console.clear()

            for obj in objects:
                console.print(obj.x, obj.y, obj.char, obj.color)

            context.present(console)

            for event in tcod.event.wait():
                context.convert_event(event)

                # Player movement
                # TODO: Move this to a separate class
                if isinstance(event, tcod.event.KeyDown):
                    print(event)

                    if event.sym == tcod.event.KeySym.LEFT:
                        player.move(*Direction.LEFT)
                    elif event.sym == tcod.event.KeySym.RIGHT:
                        player.move(*Direction.RIGHT)
                    elif event.sym == tcod.event.KeySym.UP:
                        player.move(*Direction.UP)
                    elif event.sym == tcod.event.KeySym.DOWN:
                        player.move(*Direction.DOWN)

                    print(player.x, player.y)

                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()


if __name__ == "__main__":
    main()
