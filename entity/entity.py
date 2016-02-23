import pygame

from abc import ABCMeta, abstractmethod


class Entity(pygame.Rect):
    """docstring for Entity"""
    __metaclass__ = ABCMeta

    def __init__(self, coords, bounds, velocity):
        super(Entity, self).__init__(coords.x, coords.y, bounds.x, bounds.y)
        self.velocity = velocity

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def update(self, delta):
        pass
