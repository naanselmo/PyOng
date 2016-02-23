class Player(object):
    """docstring for Player"""
    def __init__(self, input_handler, controls, entity):
        super(Player, self).__init__()
        self.input = input_handler
        self.controls = controls
        self.entity = entity

    def add_listeners(self):
        for key in self.controls:
            self.input.add_listener(key)

    def remove_listeners(self):
        for key in self.controls:
            self.input.add_listener(key)

    def update(self):
        if self.input.key_clicked(self.controls['up']):
            self.entity.move_up()
        elif self.input.key_clicked(self.controls['down']):
            self.entity.move_down()
        elif self.input.key_clicked(self.controls['dash']):
            self.entity.dash()

        self.entity.update()

    def render(self, canvas):
        self.entity.render(canvas)
