import random
from abc import abstractmethod

import arcade

from objects import Tongue, Weapon, Obstacle, Aim, Actor, Flower, Frog

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
