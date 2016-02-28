class Player(object):
    """docstring for Player"""
    def __init__(self, input_handler, controls, pad, lives):
        super(Player, self).__init__()
        self.input = input_handler
        self.controls = controls
        self.pad = pad
        self.lives = lives

    def add_listeners(self):
        for key in self.controls:
            self.input.add_listener(self.controls[key])

    def update(self, delta):
        if self.input.key_down(self.controls['up']):
            self.pad.move_up(delta)
        elif self.input.key_down(self.controls['down']):
            self.pad.move_down(delta)
        else:
            self.pad.stop_movement(delta)

        if self.input.key_down(self.controls['dash']):
            self.pad.stop_movement(delta)
            self.pad.dash(delta)

        self.pad.update(delta)

    def render(self, canvas):
        self.pad.render(canvas)

    def remove_listeners(self):
        for key in self.controls:
            self.input.remove_listener(self.controls[key])
