import pygame as pg
import math
from constants import *
from arrow import Arrow
import engine as e


class Bow:
    def __init__(self):
        img = pg.image.load("assets/images/weapons/bow.png")
        self.original_image = e.scale_image(img, WEAPON_SCALE)
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()

    def shoot(self, x, y, arrows):
        arrow = Arrow(self.angle, x, y)
        arrows.add(arrow)

    def update(self, player, enemies):
        self.rect.center = player.rect.center
        pos = pg.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)  # -ve, Y increase down screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

    def display(self, screen):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        rect = ((self.rect.centerx - int(self.image.get_width() / 2)),
                self.rect.centery - int(self.image.get_height() / 3))
        screen.blit(self.image, rect)
