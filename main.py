from __future__ import annotations
from typing import Optional


import math
import random

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SPRITE_SCALING_BUG = 0.1
SPRITE_SCALING_FLOWER = 0.1
SPRITE_SCALING_FROG = 0.3
SPRITE_SCALING_TONGUE = 0.08

BUG_COUNT = 10
FLOWER_COUNT = 8

MOVEMENT_SPEED = 2
TONGUE_SPEED = 5

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3

class SingletonMeta(type):
    """
    В Python класс Одиночка можно реализовать по-разному. Возможные способы
    включают себя базовый класс, декоратор, метакласс. Мы воспользуемся
    метаклассом, поскольку он лучше всего подходит для этой цели.
    """

    _instance: Optional[Singleton] = None

    def __call__(self) -> Singleton:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Frog(arcade.Sprite, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()

        self.textures = []
        texture = arcade.load_texture("images/frog2.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/frog1.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/frog3.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/frog4.png")
        self.textures.append(texture)

        self.scale = SPRITE_SCALING_FROG

        self.center_x = 500
        self.center_y = 400

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




class Bug(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        texture = arcade.load_texture("images/bug.png")
        self.textures.append(texture)

        self.scale = SPRITE_SCALING_BUG

        self.set_texture(TEXTURE_LEFT)

        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)

class Flower(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        texture = arcade.load_texture("images/flower.png")
        self.textures.append(texture)

        self.scale = SPRITE_SCALING_FLOWER

        self.set_texture(TEXTURE_LEFT)

        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)



class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.bug_list = None
        self.tongue_list = None
        self.flower_list = None
        self.frog_list = None
        self.score_text = None
        arcade.set_background_color(arcade.color.FRENCH_BEIGE)

    def setup(self):
        # Настроить игру здесь
            """ Настроить игру и инициализировать переменные. """

            # Создать список спрайтов
            self.frog_list = arcade.SpriteList()
            self.bug_list = arcade.SpriteList()
            self.tongue_list = arcade.SpriteList()
            self.flower_list = arcade.SpriteList()
            self.obstacle_list = arcade.SpriteList()

            self.score = 0

            self.frog_sprite = Frog()
            self.frog_list.append(self.frog_sprite)

            # Создать монетки
            for i in range(BUG_COUNT):
                bug = Bug()
                self.bug_list.append(bug)
                self.obstacle_list.append(bug)

            for i in range(FLOWER_COUNT):
                flower = Flower()
                self.flower_list.append(flower)
                self.obstacle_list.append(flower)

            self.physics_engine = arcade.PhysicsEngineSimple(self.frog_sprite, self.obstacle_list)

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.frog_list.draw()
        self.bug_list.draw()
        self.flower_list.draw()
        self.tongue_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_press(self, x, y, button, modifiers):

        # Create a bullet
        tongue = arcade.Sprite("images/tongue.png", SPRITE_SCALING_TONGUE)

        # Position the bullet at the player's current location
        if self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_LEFT]:
            start_x = self.frog_sprite.center_x-50
            start_y = self.frog_sprite.center_y
        elif self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_RIGHT]:
            start_x = self.frog_sprite.center_x+50
            start_y = self.frog_sprite.center_y
        elif self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_UP]:
            start_x = self.frog_sprite.center_x
            start_y = self.frog_sprite.center_y-50
        else:
            start_x = self.frog_sprite.center_x
            start_y = self.frog_sprite.center_y+50
        tongue.center_x = start_x
        tongue.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        tongue.angle = math.degrees(angle)
        print(f"Bullet angle: {tongue.angle:.2f}")

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        tongue.change_x = math.cos(angle) * TONGUE_SPEED
        tongue.change_y = math.sin(angle) * TONGUE_SPEED

        # Add the bullet to the appropriate lists
        self.tongue_list.append(tongue)

    def on_update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        self.frog_list.update()
        self.bug_list.update()
        self.physics_engine.update()
        # Call update on all sprites
        self.tongue_list.update()

        # Loop through each bullet
        for tongue in self.tongue_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(tongue, self.bug_list)
            dont_hit_list = arcade.check_for_collision_with_list(tongue, self.flower_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                tongue.remove_from_sprite_lists()

            if len(dont_hit_list) > 0:
                self.close()

            # For every coin we hit, add to the score and remove the coin
            for bug in hit_list:
                bug.remove_from_sprite_lists()
                self.score += 1
            if self.score == BUG_COUNT:
                self.close()

            # If the bullet flies off-screen, remove it.
            if tongue.bottom > self.width/2 or tongue.top < 0 or tongue.right < 0 or tongue.left > self.width/2:
                tongue.remove_from_sprite_lists()



    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.frog_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.frog_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.frog_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.frog_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.frog_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.frog_sprite.change_x = 0




def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()