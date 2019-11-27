import pygame
from datetime import datetime
from datetime import timedelta

from init import *

dir_key = {
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right'
}

s_x = scr_w // block // 2
s_y = scr_h // block // 2
s_pos = [(s_x, s_y), (s_x, s_y + 1), (s_x, s_y + 2), (s_x, s_y + 3)]


class EarthWorm:

    def __init__(self):
        self.pos = s_pos
        self.dir = 'up'
        self.c = gray

    def draw(self, s):
        for p in self.pos:
            draw_block(s, self.c, p)

    def go(self):
        h_pos = self.pos[0]
        x, y = h_pos

        if self.dir == 'up':
            self.pos = [(x, y - 1)] + self.pos[:-1]


class GameItem:

    def __init__(self, p=(5,5)):
        self.pos = p
        self.c = blue

    def draw(self, s):
        draw_block(s, self.c, self.pos)


class Game:

    def __init__(self):
        self.worm = EarthWorm()
        self.item = GameItem()
        self.w = scr_w // block
        self.h = scr_h // block

    def draw(self, s):
        self.worm.draw(s)
        self.item.draw(s)

    def go(self):
        self.worm.go()

        if self.worm.pos[0] == self.item.pos:
            self.worm.next()
            self.new_item()


def draw_bg(s):
    bg = pygame.Rect((0, 0), (scr_w, scr_h))
    pygame.draw.rect(s, white, bg)


def draw_block(s, c, p):
    b = pygame.Rect((p[0] * block, p[1] * block), (block, block))
    pygame.draw.rect(s, c, b)


pygame.init()
scr = pygame.display.set_mode((scr_w, scr_h))

draw_bg(scr)

pygame.display.update()

game = Game()

v = timedelta(seconds=0.5)
t = datetime.now()

while True:
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            exit()

    if v < datetime.now() - t:
        game.go()
        t = datetime.now()

    draw_bg(scr)
    game.draw(scr)
    pygame.display.update()
