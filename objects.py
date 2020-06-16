from abc import abstractmethod

import arcade

from factories import TEXTURE_LEFT, ConcreteFactory, TEXTURE_RIGHT, TEXTURE_DOWN, TEXTURE_UP, SCREEN_WIDTH, \
    SCREEN_HEIGHT


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

    @abstractmethod
    def useful_function_b(self) -> None:
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