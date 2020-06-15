from __future__ import annotations

from time import sleep
from typing import Optional
from abc import ABC, abstractmethod
import os
import datetime
import json
import math
import random
from datetime import datetime
from random import sample
from string import ascii_letters, digits

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


class MyGame(arcade.Window):
    _save_point = None

    def __init__(self, width, height, state: State) -> None:
        # self._save_point = savePoint
        self.transition_to(state)
        super().__init__(width, height)
        self.caretaker = None
        self.bug_list = None
        self.tongue_list = None
        self.flower_list = None
        self.frog_list = None
        self.score = None
        arcade.set_background_color(arcade.color.FRENCH_BEIGE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.theme = None

    def get_photoshot(self):
        return {
            'frogs': [item.get_photoshot() for item in self.frog_list],
            'bugs': [item.get_photoshot() for item in self.bug_list],
            'flowers': [item.get_photoshot() for item in self.flower_list],
            'score': self.score
        }

    def restore(self, state) -> None:
        """
        Восстанавливает состояние Создателя из объекта снимка.
        """
        self.frog_list = arcade.SpriteList()
        self.bug_list = arcade.SpriteList()
        self.flower_list = arcade.SpriteList()

        self.frog_list.extend([Frog.from_photoshot(item) for item in state['frogs']])
        self.bug_list.extend([Bug.from_photoshot(item) for item in state['bugs']])
        self.flower_list.extend([Flower.from_photoshot(item) for item in state['flowers']])

        self.score = state['score']

        self.frog_sprite = self.frog_list[0]


        self.obstacle_list = arcade.SpriteList()
        self.obstacle_list.extend(self.bug_list)
        self.obstacle_list.extend(self.flower_list)
        self.physics_engine = arcade.PhysicsEngineSimple(self.frog_sprite, self.obstacle_list)

    def setup(self, caretaker):
        # Настроить игру здесь
        """ Настроить игру и инициализировать переменные. """
        self.caretaker = caretaker
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

    def transition_to(self, state: State):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def on_key_press(self, key, modifiers):
        self._state.on_key_press(self, key, modifiers)

    def on_key_release(self, key, modifiers):
        self._state.on_key_release(self, key, modifiers)

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

        if self.dialogue_box_list[0].active and type(self._state).__name__ == 'MenuClosed':
            self.transition_to(MenuOpened())
        elif self.dialogue_box_list[0].active is not True and type(self._state).__name__ == 'MenuOpened':
            self.transition_to(MenuClosed())

    def add_dialogue_box(self):
        color = (220, 228, 255)
        dialoguebox = arcade.gui.DialogueBox(self.half_width, self.half_height, self.half_width * 1.1,
                                             self.half_height * 1.5, color, self.theme)
        close_button = CloseButton(dialoguebox, self.half_width, self.half_height - (self.half_height / 2) + 40,
                                   theme=self.theme)
        save_button = SaveButton(self, dialoguebox, self.half_width, self.half_height - (self.half_height / 2) + 100,
                                 theme=self.theme)
        load_button = LoadButton(self, dialoguebox, self.half_width, self.half_height - (self.half_height / 2) + 160,
                                 theme=self.theme)
        dialoguebox.button_list.append(close_button)
        dialoguebox.button_list.append(save_button)
        dialoguebox.button_list.append(load_button)
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


class State(ABC):

    @property
    def context(self) -> MyGame:
        return self._context

    @context.setter
    def context(self, context: MyGame) -> None:
        self._context = context

    @abstractmethod
    def on_key_press(self, game, key, modifiers) -> None:
        pass

    @abstractmethod
    def on_key_release(self, game, key, modifires) -> None:
        pass


# class Memento(ABC):
#     """
#     Интерфейс Снимка предоставляет способ извлечения метаданных снимка, таких
#     как дата создания или название. Однако он не раскрывает состояние Создателя.
#     """
#
#     @abstractmethod
#     def get_bug_list(self) -> arcade.sprite_list:
#         pass
#
#     @abstractmethod
#     def get_frog_list(self) -> arcade.sprite_list:
#         pass
#
#     @abstractmethod
#     def get_flower_list(self) -> arcade.sprite_list:
#         pass
#
#     @abstractmethod
#     def get_score(self) -> int:
#         pass
#
#     @abstractmethod
#     def get_obstacle_list(self) -> arcade.sprite_list:
#         pass


# class ConcreteMemento(Memento):
#     def __init__(self, frog_list, bug_list, flower_list, score, obstacle_list) -> None:
#         self.frog_list = frog_list
#         self.bug_list = bug_list
#         self.flower_list = flower_list
#         self.score = score
#         self.obstacle_list = obstacle_list
#
#     def get_frog_list(self) -> arcade.sprite_list:
#         return self.frog_list
#
#     def get_bug_list(self) -> arcade.sprite_list:
#         return self.bug_list
#
#     def get_flower_list(self) -> arcade.sprite_list:
#         return self.flower_list
#
#     def get_score(self) -> int:
#         return self.score
#
#     def get_obstacle_list(self) -> arcade.sprite_list:
#         return self.obstacle_list

class Caretaker():
    """
    Опекун не зависит от класса Конкретного Снимка. Таким образом, он не имеет
    доступа к состоянию создателя, хранящемуся внутри снимка. Он работает со
    всеми снимками через базовый интерфейс Снимка.
    """

    def __init__(self, mygame: MyGame) -> None:
        self._mementos = []
        self._originator = mygame

    def backup(self) -> None:
        print("\nCaretaker: Saving Originator's state...")
        self._mementos.append(self._originator.save())

    def undo(self) -> None:

        if not len(self._mementos):
            return
        memento = self._mementos.pop()

        print("\nUndo func")
        print(f"Caretaker: Restoring state to: {memento.get_score()}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    # def show_history(self) -> None:
    #     print("Caretaker: Here's the list of mementos:")
    #     for memento in self._mementos:
    #         print(memento.())


class MenuClosed(State):
    def on_key_press(self, game, key, modifiers) -> None:
        if key == arcade.key.UP:
            game.frog_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            game.frog_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            game.frog_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            game.frog_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            game.tongue_sprite = ConcreteFactory.create_tongue()
            game.tongue_list.append(game.tongue_sprite)
            if game.frog_sprite.texture == game.frog_sprite.textures[TEXTURE_LEFT]:
                start_x = game.frog_sprite.center_x - 60
                start_y = game.frog_sprite.center_y - 5
            elif game.frog_sprite.texture == game.frog_sprite.textures[TEXTURE_RIGHT]:
                start_x = game.frog_sprite.center_x + 60
                start_y = game.frog_sprite.center_y + 5
            elif game.frog_sprite.texture == game.frog_sprite.textures[TEXTURE_UP]:
                start_x = game.frog_sprite.center_x + 5
                start_y = game.frog_sprite.center_y - 60
            else:
                start_x = game.frog_sprite.center_x - 5
                start_y = game.frog_sprite.center_y + 60
            game.tongue_sprite.center_x = start_x
            game.tongue_sprite.center_y = start_y
            if game.frog_sprite.texture == game.frog_sprite.textures[TEXTURE_LEFT]:
                game.tongue_sprite.change_x = -TONGUE_SPEED
            elif game.frog_sprite.texture == game.frog_sprite.textures[TEXTURE_RIGHT]:
                game.tongue_sprite.change_x = TONGUE_SPEED
            elif game.frog_sprite.texture == game.frog_sprite.textures[TEXTURE_DOWN]:
                game.tongue_sprite.change_y = TONGUE_SPEED
            else:
                game.tongue_sprite.change_y = -TONGUE_SPEED

    def on_key_release(self, game, key, modifiers) -> None:
        flag = True
        if key == arcade.key.UP or key == arcade.key.DOWN:
            game.frog_sprite.change_y = 0
            flag = True
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            game.frog_sprite.change_x = 0
            flag = False
        if key == arcade.key.SPACE and flag is True:
            game.tongue_sprite.change_x = 0
            game.tongue_sprite.remove_from_sprite_lists()
        elif key == arcade.key.SPACE and flag is False:
            game.tongue_sprite.change_y = 0
            game.tongue_sprite.remove_from_sprite_lists()


class MenuOpened(State):
    def on_key_press(self, game, key, modifiers) -> None:
        pass

    def on_key_release(self, game, key, modifiers) -> None:
        pass


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

    def get_photoshot(self):
        return {
            'center_x': self.center_x,
            'center_y': self.center_y
        }

    def set_photoshot(self, photoshot):
        for k, v in photoshot.items():
            setattr(self, k, v)

    @classmethod
    def from_photoshot(cls, photoshot):
        obj = ConcreteFactory.create_frog()
        obj.set_photoshot(photoshot)
        return obj



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

    def get_photoshot(self):
        return {
            'center_x': self.center_x,
            'center_y': self.center_y
        }

    def set_photoshot(self, photoshot):
        for k, v in photoshot.items():
            setattr(self, k, v)

    @classmethod
    def from_photoshot(cls, photoshot):
        obj = ConcreteFactory.create_bug()
        obj.set_photoshot(photoshot)
        return obj


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
    def get_photoshot(self):
        return {
            'center_x': self.center_x,
            'center_y': self.center_y
        }

    def set_photoshot(self, photoshot):
        for k, v in photoshot.items():
            setattr(self, k, v)

    @classmethod
    def from_photoshot(cls, photoshot):
        obj = ConcreteFactory.create_flower()
        obj.set_photoshot(photoshot)
        return obj


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
    def __init__(self, game, dialoguebox, x, y, width=110, height=50, text="Save", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox
        self.game = game

    def on_press(self):
        if self.dialoguebox.active:
            #now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            with open(f'data.json', 'w') as stream:
                json.dump(self.game.get_photoshot(), stream)
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False


class LoadButton(arcade.gui.TextButton):
    def __init__(self, game, dialoguebox, x, y, width=110, height=50, text="Load", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox
        self.game = game

    def on_press(self):
        if self.dialoguebox.active:
            with open(f'data.json') as stream:
                snapshot = json.load(stream)
                self.game.restore(snapshot)
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, MenuClosed())
    caretaker = Caretaker(game)
    game.setup(caretaker)
    arcade.run()


if __name__ == "__main__":
    main()
