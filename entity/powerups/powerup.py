import pygame
import resources

from abc import ABCMeta, abstractmethod

from constants import *
from entity.entity import Entity

from random import randint


class PowerUp(Entity):
    """docstring for PowerUp"""
    __metaclass__ = ABCMeta

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(PowerUp, self).__init__(position, velocity, width, height)

    @abstractmethod
    def update(self, delta):
        pass

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def apply(self, state, ball):
        with state.game.rendering:
            pass

    @staticmethod
    def get_random_powerup(position):
        from entity.powerups.duplicate import Duplicate
        from entity.powerups.speed import Speed
        from entity.powerups.extend import Extend
        from entity.powerups.explosive import Explosive

        print "Creating powerup!"
        random = randint(0, 3)

        if random == 0:
            return Duplicate(position)
        if random == 1:
            return Speed(position)
        if random == 2:
            return Extend(position)
        if random == 3:
            return Explosive(position)
