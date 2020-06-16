import json

import arcade


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
