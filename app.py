import pygame
from time import sleep

pygame.init()
RADIUS = 6
WHITE = (255,255,255)
WIDTH, HEIGHT = 200, 100
pygame.display.set_caption("PixelEater")
win = pygame.display.set_mode(size=(WIDTH, HEIGHT))

class Pixel:
    def __init__(self, x, y, radius, color):
        self.coord = (x, y)
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.coord, self.radius)

def update_coords(x, y, x_max=WIDTH, y_max=HEIGHT):
    if x < x_max:
        x, y = x + 1, y
    else:
        x, y = 0, y + RADIUS * 2
    return x, y
    
if __name__ == "__main__":
    running = True
    pixels = []
    x, y = 0, RADIUS
    while running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        x , y = update_coords(x, y)
        pixel = Pixel(x, y, RADIUS, WHITE)
        pixel.draw(win)

    
    pygame.display.quit()