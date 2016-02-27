import pygame
import math

from constants import *
from core.game_math import Vector2
from entity.ball import Ball
from entity.virtual_ball import VirtualBall
from game_state import GameState

from player import Player
from entity.pad import Pad
from entity.virtual_pad import VirtualPad

class MultiPlayerState(GameState):
    def __init__(self, game):
        super(MultiPlayerState, self).__init__(game)
        self.player1 = Player(game.input, PLAYER1, Pad(Vector2(GAME_WIDTH - PAD_DISTANCE - PAD_WIDTH, GAME_HEIGHT/2 - PAD_HEIGHT/2), dash_direction=PLAYER1_DASH), MULTIPLAYER_LIVES)
        self.player2 = Player(game.input, PLAYER2, Pad(Vector2(0 + PAD_DISTANCE, GAME_HEIGHT/2 - PAD_HEIGHT/2), dash_direction=PLAYER2_DASH), MULTIPLAYER_LIVES)
        self.balls = [Ball()]
        self.winner = None
        self.ball_hit_by_dash = False

    def show(self):
        pass

    def add_listeners(self):
        super(MultiPlayerState, self).add_listeners()
        self.player1.add_listeners()
        self.player2.add_listeners()

    def update(self, delta):
        # Check pads
        self.player1.update(delta)
        self.check_upper_bottom_boundaries(self.player1.pad)
        self.player2.update(delta)
        self.check_upper_bottom_boundaries(self.player2.pad)

        # Check balls
        for b in self.balls:
            b.update(delta)

            # Check each ball
            if self.check_upper_bottom_boundaries(b) or \
            self.check_ball_collision(delta, b, self.player1.pad) or \
            self.check_ball_collision(delta, b, self.player2.pad):
                pass

            # Check scoring
            if self.check_left_boundary(b, self.player1, self.player2) or \
            self.check_right_boundary(b, self.player1, self.player2):
                with self.game.rendering:
                    self.balls = [Ball()]
                    self.balls[0].update_bounds()
                    break

    def check_upper_bottom_boundaries(self, entity):
        # Check top boundary
        if entity.position.y < 0:
            entity.position.y *= -1
            entity.velocity.y *= -1
            return True

        # Check bottom boundary
        elif entity.position.y + entity.height > GAME_HEIGHT:
            entity.position.y -= (entity.position.y + entity.height - GAME_HEIGHT)*2
            entity.velocity.y *= -1
            return True

        return False

    def check_right_boundary(self, ball, player1, player2):
        if ball.position.x + ball.width >= GAME_WIDTH:
            player1.lives -= ball.damage
            print "Player 1 lost a life"
            if player1.lives <= 0:
                self.winner = player2
                print "Player 2 won"
            return True
        return False

    def check_left_boundary(self, ball, player1, player2):
        if ball.position.x <= 0:
            player2.lives -= ball.damage
            print "Player 2 lost a life"
            if player2.lives <= 0:
                self.winner = player1
                print "Player 1 won"
            return True
        return False

    def check_ball_collision(self, delta, ball, pad):
        # Maybe a collision should've happened but wasn't detected
        i = 0
        collision = False
        virtualball = VirtualBall(ball.position-delta*ball.velocity, width=ball.width, height=ball.height, velocity=ball.velocity)
        virtualpad = VirtualPad(pad.position-delta*pad.velocity, width=pad.width, height=pad.height, velocity=pad.velocity)
        while not(collision) and i < COLLISION_INTERPOLATION:
            virtualball.update(delta/COLLISION_INTERPOLATION)
            virtualpad.update(delta/COLLISION_INTERPOLATION)
            collision = virtualball.get_bounds().colliderect(virtualpad.get_bounds())
            i += 1

        # We were right!
        if collision:
            # Copy all of the virtual ball's variables
            self.calculate_collision(pad, virtualball)
            ball.position = virtualball.position
            ball.velocity = virtualball.velocity
            ball.update_bounds()

            if ball.velocity.x < BALL_SPEED_LIMIT:
                ball.velocity.x *= BALL_SPEED_MULTIPLIER
            else:
                ball.velocity.x /= BALL_SPEED_MULTIPLIER

            # Transfer a portion of the speed to the ball
            ball.velocity.y += BALL_SPEED_TRANSFER * pad.velocity.y
            ball.velocity.x += BALL_SPEED_TRANSFER_DASH * pad.velocity.x

            # Add dash charge to the pad
            if pad.charge < PAD_MAX_CHARGE:
                pad.charge += pad.charging_rate

        return collision

    def calculate_collision(self, entity, point):
        entity_angle = math.atan2(entity.height/2, entity.width/2)
        collision_angle = math.atan2(entity.bounds.centery - point.bounds.centery, point.bounds.centerx - entity.bounds.centerx) + entity_angle

        if collision_angle < 0:
            collision_angle += 2*math.pi

        if collision_angle < 2*entity_angle or (point.velocity.x < 0 and collision_angle < math.pi+2*entity_angle):
            point.position.x = entity.position.x + entity.width
            point.velocity.x *= -1
        elif collision_angle < math.pi:
            point.position.y = entity.position.y - point.height
            point.velocity.y *= -1
        elif collision_angle < math.pi+2*entity_angle or (point.velocity.x > 0 and collision_angle < 2*entity_angle):
            point.position.x = entity.position.x - point.width
            point.velocity.x *= -1
        elif collision_angle < 2*math.pi:
            point.position.y = entity.position.y + entity.height
            point.velocity.y *= -1

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        self.player1.render(canvas)
        self.player2.render(canvas)

        for b in self.balls:
            b.render(canvas)

    def remove_listeners(self):
        super(MultiPlayerState, self).remove_listeners()
        self.player1.remove_listeners()
        self.player2.remove_listeners()

    def dispose(self):
        pass
