import pygame as pg
import math
from constants import *


class Arrow:
    def __init__(self, image, angle, x, y):
        super().__init__()
        self.image = pg.transform.rotate(image, angle - 90)
        self.rect = self.image.get_rect(center=(x, y))
        self.x, self.y = x, y
        self.dx, self.dy = self._set_dx_dy()

    def _set_dx_dy(self):
        mosX, mosY = pg.mouse.get_pos()
        _angle = math.atan2(mosY - self.y, mosX - self.x)
        dx = math.cos(_angle) * ARROW_SPEED
        dy = math.sin(_angle) * ARROW_SPEED
        return dx, dy

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))

    def display(self, screen):
        screen.blit(self.image, self.rect)
        pg.draw.rect(screen, RED, self.rect, 1)
