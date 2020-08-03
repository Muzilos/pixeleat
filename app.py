import pygame
from time import sleep
from random import randint

pygame.init()
RADIUS = 50
DIAMETER = 2 * RADIUS
WIDTH, HEIGHT = 500, 500
WHITE = (255,255,255)
BLUE = (20, 20, 200)
DELAY = 10

class Pixel:
    def __init__(self, x, y, radius, color, facing):
        self.coord = (x, y)
        self.radius = radius
        self.color = color
        self.facing = facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, self.coord, self.radius)

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
        print(self.color)

class App:
    def __init__(self):
        pygame.display.set_caption("PixelEater")
        self.window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        self.running = True
        self.pixels = []
    def run(self):
        # Top pixel
        top_x, top_y = 0, RADIUS
        top_color = Color(rgb=WHITE)
        top_facing = 'RIGHT'
        # Bottom pixel
        bot_x, bot_y = WIDTH, HEIGHT - RADIUS
        bot_color = Color(rgb=BLUE)
        bot_facing = 'LEFT'
        while self.running:
            pygame.time.delay(DELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()
            
            top_x, top_y, top_color, top_facing = self.run_pixel(top_x, top_y, top_color, top_facing)
            bot_x, bot_y, bot_color, bot_facing = self.run_pixel(bot_x, bot_y, bot_color, bot_facing)
    def run_pixel(self, x, y, color, direction):
        pixel = Pixel(x, y, RADIUS, color.color, facing=direction)
        pixel.draw(self.window)
        hit, direction = self.check_hit_change_direction(x, y, WIDTH, HEIGHT - RADIUS, direction)
        if hit:
            print('HIT {}'.format(direction))
            color.randomize()
        if pixel.facing == 'LEFT':
            x , y = self.move_backwards(x, y)
        else:
            x , y = self.move_forwards(x, y)

        return x, y, color, direction
    def move_forwards(self, x, y, x_max=WIDTH, y_max=HEIGHT):
        if x < x_max:
            x, y = x + RADIUS // 4, y
        else:
            x, y = 0, y + RADIUS // 4
        return x, y
    def move_backwards(self, x, y, x_max=WIDTH, y_max=HEIGHT):
        if x > 0:
            x, y = x - RADIUS // 4, y
        else:
            x, y = WIDTH, y - RADIUS // 4
        return x, y
    def check_hit_change_direction(self, x, y, hit_x, hit_y, cur_direction):
        if (x >= hit_x) and (y >= hit_y):
            return True, 'LEFT'
        elif (x <= 0) and (y <= RADIUS):
            return True, 'RIGHT'
        else:
            return False, cur_direction

if __name__ == "__main__":
    app = App()
    app.run()
    pygame.display.quit()