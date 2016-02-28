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
    def get_random_powerup(position, multiplayer=True):

        print "Creating powerup!"
        if multiplayer:
            random = randint(0, 12)
        else:
            random = randint(0, 9)

        if random == 0:
            from entity.powerups.duplicate import Duplicate as Power
        if random == 1:
            from entity.powerups.speed import Speed as Power
        if random == 2:
            from entity.powerups.slow import Slow as Power
        if random == 3:
            from entity.powerups.extend import Extend as Power
        if random == 4:
            from entity.powerups.shrink import Shrink as Power
        if random == 5:
            from entity.powerups.invisible_ball import InvisibleBall as Power
        if random == 6:
            from entity.powerups.invisible_pad import InvisiblePad as Power
        if random == 7:
            from entity.powerups.spin import Spin as Power
        if random == 8:
            from entity.powerups.teleport import Teleport as Power
        if random == 9:
            from entity.powerups.stun import Stun as Power
        if random == 10:
            from entity.powerups.life import Life as Power
        if random == 11:
            from entity.powerups.charge import Charge as Power
        if random == 12:
            from entity.powerups.explosive import Explosive as Power

        return Power(position)
