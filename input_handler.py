import pygame


class InputHandler:
    def __init__(self):
        self.thread = None
        self.quit = False
        self.up = Key()
        self.down = Key()
        self.right = Key()
        self.left = Key()
        self.keys = [self.up, self.down, self.right, self.left]

    def update(self):
        for key in self.keys:
            key.update()

    def catch_events(self):
        for event in pygame.event.get():
            # Catch main events
            self.quit = event.type == pygame.QUIT

            # Catch keyboard event
            pressed = None
            if event.type == pygame.KEYDOWN: pressed = True
            if event.type == pygame.KEYUP: pressed = False
            if pressed != None:
                self.toggle(event, pressed)

    def toggle(self, event, pressed):
        if event.key == pygame.K_UP: self.up.toggle(pressed)


class Key:
    def __init__(self):
        self.presses = 0
        self.absorbs = 0
        self.down = False
        self.clicked = False

    def toggle(self, pressed):
        if pressed != self.down:
            self.down = pressed
        if pressed:
            self.presses += 1

    def update(self):
        if self.absorbs < self.presses:
            self.absorbs += 1
            self.clicked = True
        else:
            self.clicked = False
