import pygame


class InputHandler:
    def __init__(self):
        self.quit = False
        self.escape = Key()
        self.up = Key()
        self.down = Key()
        self.right = Key()
        self.left = Key()
        self.w = Key()
        self.s = Key()
        self.d = Key()
        self.a = Key()
        self.keys = [self.up, self.down, self.right, self.left,
                     self.w, self.s, self.d, self.a]

    def init(self):
        pass

    def update(self):
        for key in self.keys:
            key.update()

    def catch_events(self):
        for event in pygame.event.get():
            # Catch main events
            self.quit = event.type == pygame.QUIT

            # Catch keyboard events
            pressed = None
            if event.type == pygame.KEYDOWN:
                pressed = True
            if event.type == pygame.KEYUP:
                pressed = False
            if pressed is not None:
                self.toggle(event, pressed)

    def toggle(self, event, pressed):
        if event.key == pygame.K_ESCAPE:
            self.escape.toggle(pressed)

        elif event.key == pygame.K_UP:
            self.up.toggle(pressed)
        elif event.key == pygame.K_DOWN:
            self.down.toggle(pressed)
        elif event.key == pygame.K_RIGHT:
            self.right.toggle(pressed)
        elif event.key == pygame.K_LEFT:
            self.left.toggle(pressed)

        elif event.key == pygame.K_w:
            self.w.toggle(pressed)
        elif event.key == pygame.K_s:
            self.s.toggle(pressed)
        elif event.key == pygame.K_d:
            self.d.toggle(pressed)
        elif event.key == pygame.K_a:
            self.a.toggle(pressed)


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
