import pygame


class InputHandler:
    def __init__(self):
        self.quit = False
        self.keys = {}

    def init(self):
        pass

    def update(self):
        for key in self.keys:
            self.keys[key].update()

    def catch_events(self):
        for event in pygame.event.get():
            # Catch main events
            self.quit = (event.type == pygame.QUIT)

            # Catch keyboard event
            if event.type == pygame.KEYDOWN:
                self.toggle(event, True)

            elif event.type == pygame.KEYUP:
                self.toggle(event, False)

    def toggle(self, event, pressed):
        key = self.keys.get(event.key)
        if key is not None:
            key.toggle(pressed)

    def add_listener(self, key):
        if key not in self.keys:
            self.keys[key] = Key()

    def remove_listener(self, key):
        if key in self.keys:
            del self.keys[key]

    def key_down(self, key):
        return self.keys[key].down

    def key_clicked(self, key):
        return self.keys[key].clicked

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
