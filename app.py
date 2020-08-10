import pygame
from time import sleep
from random import randint
from sound import Sound
from pixel import Pixel, Color
from consts import *

pygame.init()

class App:
    def __init__(self):
        pygame.display.set_caption("Visualizer")
        self.window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        self.running = True
        self.top_pixels, self.bot_pixels = [], []

        # Top pixel
        self.top_color = Color(rgb=WHITE)
        self.top_pixel = Pixel(0, RADIUS, RADIUS, self.top_color, facing='RIGHT', win=self.window)
        # Bottom pixel
        self.bot_color = Color(rgb=BLUE)
        self.bot_pixel = Pixel(WIDTH, HEIGHT - RADIUS, RADIUS, self.bot_color, facing='LEFT', win=self.window)

        self.sound = Sound()

    def run(self):
        self.scenario2()

    def scenario1(self):
        self.sound.open_stream()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            sound_bit = self.sound.update_stream()[0]
            if sound_bit.any():
                rad_mod, dis_mod = 100 * (sound_bit[-1])
            else:
                rad_mod, dis_mod = (1, 1)
            self.top_pixel.mod_radius(rad_mod)
            self.bot_pixel.mod_radius(rad_mod)
            self.run_pixel(self.top_pixel)
            self.run_pixel(self.bot_pixel)
            self.top_pixel.mod_displacement(dis_mod)
            self.bot_pixel.mod_displacement(dis_mod)
            
            pygame.display.update()
            pygame.time.delay(DELAY)

    def scenario2(self):
        self.sound.open_stream()
        rad_mod, dis_mod = (1, 1)
        center = (WIDTH // 2, HEIGHT // 2)
        top_coord, bot_coord = center, center
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            sound_bit = self.sound.update_stream()[0]
            if sound_bit.any():
                sound_block = sum(sound_bit)
                rad_mod, dis_mod = 10 * (sound_block)
                top_coord = (center[0] + int(rad_mod), center[1] + int(dis_mod))
                bot_coord = (center[0] - int(rad_mod), center[1] + int(dis_mod))

            if abs(rad_mod) >= RADIUS:
                self.top_pixel.coord = top_coord
                self.top_pixel.mod_radius(rad_mod/10)

                self.bot_pixel.coord = bot_coord
                self.bot_pixel.mod_radius(rad_mod/10)

            if abs(rad_mod) > (HEIGHT//5):
                self.bot_pixel.color.randomize()
                self.top_pixel.color.randomize()

            self.bot_pixel.draw()
            self.top_pixel.draw()
            
            pygame.display.update()
            pygame.time.delay(DELAY*4)

    def run_pixel(self, pixel):
        hit, direction = self.check_hit_change_direction(pixel, WIDTH, HEIGHT - (RADIUS/2))
        if hit:
            pixel.facing = direction
            pixel.color.randomize()
        else:
            if pixel.facing == 'LEFT':
                pixel.move_backwards()
            else:
                pixel.move_forwards()

        pixel.draw()
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