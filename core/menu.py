import pygame
import math

from pygame.rect import Rect


class MenuComponent:
    def __init__(self):
        self.active = True


class MenuSlider(MenuComponent):
    def __init__(self, minimum, value, maximum):
        MenuComponent.__init__(self)
        self.min = float(minimum)
        self.value = float(value)
        self.max = float(maximum)
        self.speed = (self.max - self.min) / 1000.0

        self.bar_width = None
        self.bar_height = None
        self.bar_color = None
        self.pointer_color = None

    def init(self, width, height, bar_color, pointer_color):
        self.bar_width = width
        self.bar_height = height
        self.bar_color = bar_color
        self.pointer_color = pointer_color

    def update(self, input_handler, delta):
        if not self.active:
            return

        # If active catch events
        if input_handler.key_down(pygame.K_RIGHT):
            if self.value < self.max:
                self.value += self.speed * delta
            else:
                self.value = self.max
        elif input_handler.key_down(pygame.K_LEFT):
            if self.value > self.min:
                self.value -= self.speed * delta
            else:
                self.value = self.min

    def render(self, canvas, center_x, y):
        # Draw the bar
        slider_rect = Rect(center_x - self.bar_width / 2, y, self.bar_width, self.bar_height)
        pygame.draw.rect(canvas, self.bar_color, slider_rect)

        # Constants change if active
        y_offset_constant = 0.28 if not self.active else 0.30
        pointer_width_constant = 3 / 4 if not self.active else 5 / 4

        y_offset = math.ceil(self.bar_height * y_offset_constant)
        pointer_width = self.bar_height * pointer_width_constant
        pointer_height = self.bar_height + y_offset * 2
        pointer_x = slider_rect.x + (self.value - self.min) / (self.max - self.min) * (self.bar_width - pointer_width)
        pointer_y = y - y_offset
        pointer_rect = Rect(pointer_x, pointer_y, pointer_width, pointer_height)
        pygame.draw.rect(canvas, self.pointer_color, pointer_rect)

    def reset(self):
        pass


class MenuOptions(MenuComponent):
    def __init__(self, options, on_click=None, on_change=None, reverse=False, rotative=True):
        MenuComponent.__init__(self)
        self.menu_options = options
        self.on_click = on_click
        self.on_change = on_change
        self.reverse = reverse
        self.rotative = rotative
        self.selected_option = 0
        self.menu_options_surfaces = []
        self.text_color = None

        self.reset()

    def init(self, font, font_size, antialias, color):
        font_renderer = pygame.font.Font(font, font_size)
        self.text_color = color
        self.menu_options_surfaces = [font_renderer.render(option, antialias, color) for option in self.menu_options]

    def update(self, input_handler):
        if not self.active:
            return

        # If active catch events
        delta = 1 if not self.reverse else -1
        options_length = len(self.menu_options)
        if input_handler.key_clicked(pygame.K_DOWN):
            old_option = self.selected_option
            if self.rotative:
                # If rotative, rotate it
                self.selected_option = (self.selected_option + delta) % options_length
            else:
                stop_bool = self.selected_option != (options_length - 1 if not self.reverse else 0)
                if stop_bool:
                    # Only change it if its not in the last option
                    self.selected_option += delta

            # Run the on change function
            if self.on_change is not None:
                self.on_change(old_option, self.selected_option)
        if input_handler.key_clicked(pygame.K_UP):
            old_option = self.selected_option
            if self.rotative:
                # If rotative, rotate it
                self.selected_option = (self.selected_option - delta) % options_length
            else:
                stop_bool = self.selected_option != (0 if not self.reverse else options_length - 1)
                if stop_bool:
                    # Only change it if its not in the first option
                    self.selected_option -= delta

            # Run the on change function
            if self.on_change is not None:
                self.on_change(old_option, self.selected_option)

        if input_handler.key_clicked(pygame.K_RETURN):
            # If pressed enter run the click function
            if self.on_click is not None:
                self.on_click(self.selected_option)

    def render(self, canvas, center_x, y):
        for i in range(len(self.menu_options_surfaces)):
            option_surface = self.menu_options_surfaces[i]
            surface_x = center_x - option_surface.get_width() / 2
            if not self.reverse:
                surface_y = y + i * option_surface.get_height() * 1.8
            else:
                surface_y = (y - option_surface.get_height()) - i * option_surface.get_height() * 1.8
            surface_width, surface_height = option_surface.get_size()
            canvas.blit(option_surface, (surface_x, surface_y))
            # Draw arrow
            if self.active and self.selected_option == i:
                arrow_width = arrow_height = surface_height / 1.6
                arrow_x = surface_x - arrow_height * 2
                arrow_y = surface_y + surface_height / 8
                points = self.arrow_points(arrow_x, arrow_y, arrow_width, arrow_height)
                pygame.draw.polygon(canvas, self.text_color, points)

    def arrow_points(self, x, y, width, height):
        return (x, y), (x, y + height), (x + width, y + (height / 2))

    def reset(self):
        self.selected_option = 0
