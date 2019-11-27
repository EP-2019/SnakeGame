import pygame
import random
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


class ItemException(Exception):
    pass


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
        elif self.dir == 'down':
            self.pos = [(x, y + 1)] + self.pos[:-1]
        elif self.dir == 'left':
            self.pos = [(x - 1, y)] + self.pos[:-1]
        elif self.dir == 'right':
            self.pos = [(x + 1, y)] + self.pos[:-1]

    def turn(self, d):
        self.dir = d

    def next(self):
        t_pos = self.pos[-1]
        x, y = t_pos

        if self.dir == 'up':
            self.pos.append((x, y - 1))
        elif self.dir == 'down':
            self.pos.append((x, y + 1))
        elif self.dir == 'left':
            self.pos.append((x - 1, y))
        elif self.dir == 'right':
            self.pos.append((x + 1, y))


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

        if self.worm.pos[0] in self.worm.pos[1:]:
            raise ItemException()

        if self.worm.pos[0] == self.item.pos:
            self.worm.next()
            self.new_item()

    def new_item(self):
        nx = random.randint(0, self.w - 1)
        ny = random.randint(0, self.h - 1)
        self.item = GameItem((nx, ny))

        for p in self.worm.pos:
            if self.item.pos == p:
                self.new_item()
                break


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

v = timedelta(seconds=0.2)
t = datetime.now()

while True:
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key in dir_key:
                game.worm.turn(dir_key[e.key])

    if v < datetime.now() - t:
        try:
            game.go()
        except ItemException:
            quit()

        t = datetime.now()

    draw_bg(scr)
    game.draw(scr)
    pygame.display.update()
