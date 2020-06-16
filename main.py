from __future__ import annotations
import arcade

from factories import SCREEN_WIDTH, SCREEN_HEIGHT
from myGame import MyGame
from states import MenuClosed


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, MenuClosed())
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
