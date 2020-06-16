from abc import abstractmethod, ABC

import arcade

from factories import ConcreteFactory, TONGUE_SPEED, TEXTURE_LEFT, TEXTURE_RIGHT, TEXTURE_DOWN, TEXTURE_UP, \
    MOVEMENT_SPEED
from myGame import MyGame


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
