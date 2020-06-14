from __future__ import annotations

from time import sleep
from typing import Optional
from abc import ABC, abstractmethod
import os

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
TONGUE_SPEED = 0.00001

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3


class AbstractFactory(arcade.Sprite):

    @abstractmethod
    def create_actor(self) -> Actor:
        pass

    @abstractmethod
    def create_aim(self) -> Aim:
        pass

    @abstractmethod
    def create_obstacle(self) -> Obstacle:
        pass

    @abstractmethod
    def create_weapon(self) -> Weapon:
        pass


class ConcreteFactory(AbstractFactory):

    @staticmethod
    def create_frog() -> Frog:
        obj = Frog()
        obj.textures = []
        texture = arcade.load_texture("images/frog2.png")
        obj.textures.append(texture)
        texture = arcade.load_texture("images/frog1.png")
        obj.textures.append(texture)
        texture = arcade.load_texture("images/frog3.png")
        obj.textures.append(texture)
        texture = arcade.load_texture("images/frog4.png")
        obj.textures.append(texture)

        obj.scale = SPRITE_SCALING_FROG

        obj.center_x = 500
        obj.center_y = 400

        obj.set_texture(TEXTURE_RIGHT)
        return obj

    @staticmethod
    def create_bug() -> Bug:
        obj = Bug()

        texture = arcade.load_texture("images/bug.png")
        obj.textures.append(texture)
        obj.set_texture(TEXTURE_LEFT)

        obj.scale = SPRITE_SCALING_BUG

        obj.center_x = random.randrange(SCREEN_WIDTH)
        obj.center_y = random.randrange(SCREEN_HEIGHT)
        return obj

    @staticmethod
    def create_flower() -> Flower:
        obj = Flower()

        texture = arcade.load_texture("images/flower.png")
        obj.textures.append(texture)
        obj.set_texture(TEXTURE_LEFT)

        obj.scale = SPRITE_SCALING_FLOWER

        obj.center_x = random.randrange(SCREEN_WIDTH)
        obj.center_y = random.randrange(SCREEN_HEIGHT)

        return obj

    @staticmethod
    def create_tongue() -> Tongue:
        obj = Tongue()
        obj.textures = []
        texture = arcade.load_texture("images/tongue2.png")
        obj.textures.append(texture)
        texture = arcade.load_texture("images/tongue1.png")
        obj.textures.append(texture)
        texture = arcade.load_texture("images/tongue3.png")
        obj.textures.append(texture)
        texture = arcade.load_texture("images/tongue4.png")
        obj.textures.append(texture)

        obj.scale = SPRITE_SCALING_TONGUE

        obj.center_x = 500
        obj.center_y = 400

        obj.set_texture(TEXTURE_RIGHT)
        return obj


class Actor(arcade.Sprite):

    @abstractmethod
    def useful_function_a(self) -> str:
        pass


class Frog(Actor):
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


class Aim(arcade.Sprite):
    """
    Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
    друг с другом, но правильное взаимодействие возможно только между продуктами
    одной и той же конкретной вариации.
    """

    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass


class Bug(Aim):
    def useful_function_b(self) -> str:
        return "The result of the product B1."


class Obstacle(arcade.Sprite):
    """
    Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
    друг с другом, но правильное взаимодействие возможно только между продуктами
    одной и той же конкретной вариации.
    """

    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass


class Flower(Obstacle):
    def useful_function_b(self) -> str:
        return "The result of the product B1."


class Weapon(arcade.Sprite):
    """
    Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
    друг с другом, но правильное взаимодействие возможно только между продуктами
    одной и той же конкретной вариации.
    """

    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass


class Tongue(Weapon):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

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


class MenuButton(arcade.gui.TextButton):
    def __init__(self, dialoguebox, x, y, width=110, height=50, text="Menu", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if not self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox.active = True


class CloseButton(arcade.gui.TextButton):
    def __init__(self, dialoguebox, x, y, width=110, height=50, text="Close", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed and self.dialoguebox.active:
            self.pressed = False
            self.dialoguebox.active = False

class SaveButton(arcade.gui.TextButton):
    def __init__(self, dialoguebox, x, y, width=110, height=50, text="Save", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False





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
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.theme = None

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

        self.frog_sprite = ConcreteFactory.create_frog()
        self.frog_list.append(self.frog_sprite)

        # Создать монетки
        for i in range(BUG_COUNT):
            bug = ConcreteFactory.create_bug()
            self.bug_list.append(bug)
            self.obstacle_list.append(bug)

        for i in range(FLOWER_COUNT):
            flower = ConcreteFactory.create_flower()
            self.flower_list.append(flower)
            self.obstacle_list.append(flower)

        self.physics_engine = arcade.PhysicsEngineSimple(self.frog_sprite, self.obstacle_list)

        self.set_theme()
        self.add_dialogue_box()
        self.add_text()
        self.add_button()

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
        super().on_draw()

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

            if self.dialogue_box_list[0].active:
                return

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.frog_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.frog_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.frog_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.frog_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.tongue_sprite = ConcreteFactory.create_tongue()
            self.tongue_list.append(self.tongue_sprite)
            if self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_LEFT]:
                start_x = self.frog_sprite.center_x - 60
                start_y = self.frog_sprite.center_y - 5
            elif self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_RIGHT]:
                start_x = self.frog_sprite.center_x + 60
                start_y = self.frog_sprite.center_y + 5
            elif self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_UP]:
                start_x = self.frog_sprite.center_x + 5
                start_y = self.frog_sprite.center_y - 60
            else:
                start_x = self.frog_sprite.center_x - 5
                start_y = self.frog_sprite.center_y + 60
            self.tongue_sprite.center_x = start_x
            self.tongue_sprite.center_y = start_y
            if self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_LEFT]:
                self.tongue_sprite.change_x = -TONGUE_SPEED
            elif self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_RIGHT]:
                self.tongue_sprite.change_x = TONGUE_SPEED
            elif self.frog_sprite.texture == self.frog_sprite.textures[TEXTURE_DOWN]:
                self.tongue_sprite.change_y = TONGUE_SPEED
            else:
                self.tongue_sprite.change_y = -TONGUE_SPEED

    def on_key_release(self, key, modifiers):
        flag = True
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.frog_sprite.change_y = 0
            flag = True
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.frog_sprite.change_x = 0
            flag = False
        if key == arcade.key.SPACE and flag is True:
            self.tongue_sprite.change_x = 0
            self.tongue_sprite.remove_from_sprite_lists()
        elif key == arcade.key.SPACE and flag is False:
            self.tongue_sprite.change_y = 0
            self.tongue_sprite.remove_from_sprite_lists()

    def add_dialogue_box(self):
        color = (220, 228, 255)
        dialoguebox = arcade.gui.DialogueBox(self.half_width, self.half_height, self.half_width * 1.1,
                                             self.half_height * 1.5, color, self.theme)
        close_button = CloseButton(dialoguebox, self.half_width, self.half_height - (self.half_height / 2) + 40,
                                   theme=self.theme)
        save_button = SaveButton(dialoguebox, self.half_width, self.half_height - (self.half_height / 2) + 100,
                                   theme=self.theme)
        dialoguebox.button_list.append(close_button)
        dialoguebox.button_list.append(save_button)
        message = "Hello I am a Dialogue Box."
        dialoguebox.text_list.append(
            arcade.gui.TextBox(message, self.half_width, self.half_height, self.theme.font_color))
        self.dialogue_box_list.append(dialoguebox)

    def add_text(self):
        message = "Press this button to activate the Dialogue Box"
        self.text_list.append(arcade.gui.TextBox(message, self.half_width - 50, self.half_height))

    def add_button(self):
        show_button = MenuButton(self.dialogue_box_list[0], 60, self.height - 30, theme=self.theme)
        self.button_list.append(show_button)

    def set_dialogue_box_texture(self):
        dialogue_box = ":resources:gui_themes/Fantasy/DialogueBox/DialogueBox.png"
        self.theme.add_dialogue_box_texture(dialogue_box)

    def set_button_texture(self):
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def set_theme(self):
        self.theme = arcade.gui.Theme()
        self.set_dialogue_box_texture()
        self.set_button_texture()
        self.theme.set_font(24, arcade.color.WHITE)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
