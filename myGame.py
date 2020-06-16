import os

import arcade

from buttons import CloseButton, LoadButton, SaveButton, MenuButton
from factories import ConcreteFactory, FLOWER_COUNT, BUG_COUNT
from objects import Frog, Flower, Bug
from states import State, MenuOpened, MenuClosed


class MyGame(arcade.Window):
    _save_point = None

    def __init__(self, width, height, state: State) -> None:
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

    def setup(self):
        self.frog_list = arcade.SpriteList()
        self.bug_list = arcade.SpriteList()
        self.tongue_list = arcade.SpriteList()
        self.flower_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()

        self.score = 0

        self.frog_sprite = ConcreteFactory.create_frog()
        self.frog_list.append(self.frog_sprite)

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
        self.tongue_list.update()

        for tongue in self.tongue_list:

            hit_list = arcade.check_for_collision_with_list(tongue, self.bug_list)
            dont_hit_list = arcade.check_for_collision_with_list(tongue, self.flower_list)

            if len(hit_list) > 0:
                tongue.remove_from_sprite_lists()

            if len(dont_hit_list) > 0:
                self.close()

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