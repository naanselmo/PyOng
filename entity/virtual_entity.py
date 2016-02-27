from entity import Entity


class VirtualEntity(Entity):
    def update(self, delta):
        self.position += self.velocity * delta
        self.update_bounds()
        
    def render(self, canvas):
        pass
