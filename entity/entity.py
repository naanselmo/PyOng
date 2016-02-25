import pygame

from abc import ABCMeta, abstractmethod

from pygame.rect import Rect


class Entity:
    """docstring for Entity"""
    __metaclass__ = ABCMeta

    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height
        self.bounds = Rect(position.x, position.y, width, height)

    @abstractmethod
    def update(self, delta):
        pass

    @abstractmethod
    def render(self, canvas):
        pass

    def update_bounds(self):
        self.bounds.x = self.position.x
        self.bounds.y = self.position.y

    def get_bounds(self):
        return self.bounds
