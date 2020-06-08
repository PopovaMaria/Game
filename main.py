import random

import arcade
import os

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SPRITE_SCALING_BUG = 0.1
SPRITE_SCALING_FROG = 0.3
BUG_COUNT = 5
MOVEMENT_SPEED = 4

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3

class Frog(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture("images/frog2.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/frog1.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/frog3.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/frog4.png")
        self.textures.append(texture)


        self.scale = SPRITE_SCALING_FROG

        # By default, face right.
        self.set_texture(TEXTURE_RIGHT)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]
        elif self.change_y > 0:
            self.texture = self.textures[TEXTURE_DOWN]
        elif self.change_y < 0:
            self.texture = self.textures[TEXTURE_UP]

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        # Variables that will hold sprite lists
        self.bug_list = None

        # Set up the player info
        self.frog_list = None
        arcade.set_background_color(arcade.color.FRENCH_BEIGE)

    def setup(self):
        # Настроить игру здесь
            """ Настроить игру и инициализировать переменные. """

            # Создать список спрайтов
            self.frog_list = arcade.SpriteList()
            self.bug_list = arcade.SpriteList()

            # Счет
            self.score = 0

            # Задать игрока и
            # Его изображение из kenney.nl
            self.frog_sprite = Frog()
            self.frog_sprite.center_x = 500  # Стартовая позиция
            self.frog_sprite.center_y = 400
            self.frog_list.append(self.frog_sprite)

            # Создать монетки
            for i in range(BUG_COUNT):
                # Создать инстанс монеток
                # и их изображение из kenney.nl
                bug = arcade.Sprite("images/bug.png", SPRITE_SCALING_BUG)

                # Задать положение монеток
                bug.center_x = random.randrange(SCREEN_WIDTH)
                bug.center_y = random.randrange(SCREEN_HEIGHT)

                # Добавить монетку к списку
                self.bug_list.append(bug)

            self.physics_engine = arcade.PhysicsEngineSimple(self.frog_sprite, self.bug_list)

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.frog_list.draw()
        self.bug_list.draw()

    def on_update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        self.frog_list.update()
        self.bug_list.update()
        self.physics_engine.update()



    def on_key_press(self, key, modifiers):
        """Вызывается при нажатии пользователем клавиши"""

        if key == arcade.key.UP:
            self.frog_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.frog_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.frog_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.frog_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.frog_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.frog_sprite.change_x = 0






def main():
    # bug = arcade.Sprite("images/bug.png", SPRITE_SCALING_BUG)
    # frog = arcade.Sprite("images/frog.png", SPRITE_SCALING_FROG)
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()