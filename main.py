import random

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SPRITE_SCALING_BUG = 0.1
SPRITE_SCALING_FROG = 0.3
BUG_COUNT = 5
MOVEMENT_SPEED = 4

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

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
            self.frog_sprite = arcade.Sprite("images/frog.png",
                                             SPRITE_SCALING_FROG)
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

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
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
        """Вызывается, когда пользователь отпускает клавишу"""

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