import pygame
import resources

from abc import ABCMeta, abstractmethod

from constants import *
from entity.entity import Entity
from core.game_math import Vector2


class PowerUp(Entity):
    """docstring for Entity"""
    __metaclass__ = ABCMeta

    def __init__(self, position, velocity, width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(PowerUp, self).__init__(position, velocity, width, height)

    @abstractmethod
    def update(self, delta):
        pass

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def apply(self, state):
        pass
