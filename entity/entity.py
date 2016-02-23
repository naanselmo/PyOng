import pygame

from abc import ABCMeta, abstractmethod


class Entity(pygame.Rect):
    """docstring for Entity"""
    __metaclass__ = ABCMeta

    def __init__(self, game, coords, dimensions, velocity):
        super(Entity, self).__init__(coords['x'], coords['y'], dimensions['x'], dimensions['y'])
        self.velocity = velocity
        self.game = game

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def update(self, delta):
        pass
