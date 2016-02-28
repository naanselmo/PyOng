import pygame

from abc import ABCMeta, abstractmethod

from pygame.rect import Rect
from core.game_math import Vector2


class Entity:
    """docstring for Entity"""
    __metaclass__ = ABCMeta

    def __init__(self, position, velocity, width, height):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.width = width
        self.height = height
        self.bounds = Rect(self.position.x, self.position.y, width, height)

    @abstractmethod
    def update(self, delta):
        pass

    @abstractmethod
    def render(self, canvas):
        pass

    def update_bounds(self):
        self.bounds.x = self.position.x
        self.bounds.y = self.position.y
        self.bounds.width = self.width
        self.bounds.height = self.height

    def get_bounds(self):
        return self.bounds
