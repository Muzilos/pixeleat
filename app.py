import pygame
from time import sleep
from random import randint

pygame.init()
RADIUS = 40
DIAMETER = 2 * RADIUS
WIDTH, HEIGHT = 400,600
WHITE = (255,255,255)
BLUE = (20, 20, 200)
DELAY = 5


class Pixel:
    def __init__(self, x, y, radius, color, facing):
        self.coord = (x, y)
        self.radius = radius
        self.color = color
        self.facing = facing
        self.displacement = RADIUS

    def draw(self, win):
        pygame.draw.circle(win, self.color.color, self.coord, self.radius)

    def move_forwards(self, x_max=WIDTH, y_max=HEIGHT):
        x, y = self.coord
        if x < x_max:
            x, y = x + self.displacement, y
        else:
            x, y = 0, y + self.displacement
        self.coord = (x, y)

    def move_backwards(self, x_max=WIDTH, y_max=HEIGHT):
        x, y = self.coord
        if x > 0:
            x, y = x - self.displacement, y
        else:
            x, y = WIDTH, y - self.displacement
        self.coord = (x, y)


class Color:
    def __init__(self, r=0, g=0, b=0, rgb=()):
        self.r = r
        self.g = g
        self.b = b
        if rgb:
            if len(rgb) >= 3:
                self.r, self.g, self.b = rgb[0:3] 
            else:
                raise Exception('RGB should have at least 3 values to unpack')
        self.color = [self.r, self.g, self.b]

    def randomize(self):
        for i in range(len(self.color)):
            primary_color = self.color[i]
            try:
                if primary_color >= 50:
                    primary_color = primary_color % randint(1, 255) 
                else: 
                    primary_color = randint((primary_color + 10) * 2, 255) - primary_color
            except ZeroDivisionError:
                primary_color = randint((primary_color + 10), 255) - primary_color
            self.color[i] = primary_color
        # print(self.color)

class App:
    def __init__(self):
        pygame.display.set_caption("PixelEater")
        self.window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        self.running = True
        self.top_pixels, self.bot_pixels = [], []

        # Top pixel
        self.top_color = Color(rgb=WHITE)
        self.top_pixel = Pixel(0, RADIUS, RADIUS, self.top_color, facing='RIGHT')
        # Bottom pixel
        self.bot_color = Color(rgb=BLUE)
        self.bot_pixel = Pixel(WIDTH, HEIGHT - RADIUS, RADIUS, self.bot_color, facing='LEFT')

    def run(self):
        while self.running:
            pygame.time.delay(DELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.run_pixel(self.top_pixel)
            self.run_pixel(self.bot_pixel)
            # print("{top}\t{bot}".format(top=(self.top_pixel.coord), \
            #     bot=(self.bot_pixel.coord)))
            pygame.display.update()

    def run_pixel(self, pixel):
        x, y = pixel.coord
        hit, direction = self.check_hit_change_direction(pixel, WIDTH, HEIGHT - (RADIUS/2))
        if hit:
            pixel.facing = direction
            pixel.color.randomize()
        else:
            if pixel.facing == 'LEFT':
                pixel.move_backwards()
            else:
                pixel.move_forwards()

        pixel.draw(self.window)
        return pixel.color, direction

    def check_hit_change_direction(self, pixel, hit_x, hit_y):
        cur_direction = pixel.facing
        x, y = pixel.coord
        if (x >= hit_x) and (y >= hit_y):
            pixel.move_backwards()
            return True, 'LEFT'
        elif (x <= (0 + RADIUS//2)) and (y <= RADIUS//2):
            pixel.move_forwards()
            return True, 'RIGHT'
        else:
            return False, cur_direction

if __name__ == "__main__":
    app = App()
    app.run()
    pygame.display.quit()