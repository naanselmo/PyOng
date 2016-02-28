import pygame
from pygame.rect import Rect

import resources

from constants import *
from entity import Entity
from core.game_math import Vector2


class Pad(Entity):
    def __init__(self, position, player = None, velocity = Vector2(0, 0), width = PAD_WIDTH, height = PAD_HEIGHT, speed = PAD_SPEED, dash_direction = 0, charge = PAD_INITIAL_CHARGE, charging_rate = PAD_CHARGING_RATE):
        super(Pad, self).__init__(position, velocity, width, height)
        self.owner = player
        self.speed = speed
        self.charge = charge
        self.charging_rate = charging_rate
        self.dash_direction = dash_direction
        self.dash_time = 250
        self.dash_returning = False
        self.invisible = False
        self.invisible_timer = 0
        self.stunned = False
        self.stunned_timer = 0

    def update(self, delta):
        if self.velocity.x != 0:
            self.position.x += self.velocity.x * delta
            if self.dash_returning:
                if self.dash_direction * (self.position.x - self.dashing_start_position) < 0:
                    self.velocity.x = 0
                    self.position.x = self.dashing_start_position

            else:
                self.dash_time -= delta
                if self.dash_time < 0:
                    self.dash_returning = True
                    self.velocity.x *= -1

        else:
            self.position.y += self.velocity.y * delta

        if self.height != PAD_HEIGHT:
            self.position.y -= POWERUP_SIZE_RESTITUTION_RATE * 0.00001 * delta * (PAD_HEIGHT - self.height) * 0.5
            self.height += POWERUP_SIZE_RESTITUTION_RATE * 0.00001 * delta * (PAD_HEIGHT - self.height)

        if self.invisible:
            self.invisible_timer -= delta
            if self.invisible_timer <= 0:
                self.invisible = False

        if self.stunned:
            self.stop_movement(delta)
            self.stunned_timer -= delta
            if self.stunned_timer <= 0:
                self.stunned = False

        self.update_bounds()

    def move_up(self, delta):
        if not self.stunned:
            self.velocity.y = self.speed * -1

    def move_down(self, delta):
        if not self.stunned:
            self.velocity.y = self.speed * 1

    def stop_movement(self, delta):
        self.velocity.y = 0

    def dash(self, delta):
        if not self.stunned and self.velocity.x == 0:
            self.velocity.x = self.dash_direction * self.charge * 0.01
            self.dashing_start_position = self.position.x
            self.dash_returning = False
            self.charge = 0
            self.dash_time = 250

    def render(self, canvas):
        if self.stunned:
            pygame.draw.rect(canvas, POWERUP_STUNNED_COLOR, self.get_bounds())
        elif self.invisible:
            pygame.draw.rect(canvas, POWERUP_INVISIBLE_COLOR, self.get_bounds())
        else:
            pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
