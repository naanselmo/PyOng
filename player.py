class Player(object):
    """docstring for Player"""
    def __init__(self, input_handler, controls, entity):
        super(Player, self).__init__()
        self.input = input_handler
        self.controls = controls
        self.entity = entity

    def add_listeners(self):
        for key in self.controls:
            self.input.add_listener(self.controls[key])

    def remove_listeners(self):
        for key in self.controls:
            self.input.remove_listener(self.controls[key])

    def update(self, delta):
        if self.input.key_down(self.controls['up']):
            self.entity.move_up(delta)
        elif self.input.key_down(self.controls['down']):
            self.entity.move_down(delta)
        elif self.input.key_down(self.controls['dash']):
            self.entity.dash(delta)

        self.entity.update(delta)

    def render(self, canvas):
        self.entity.render(canvas)
