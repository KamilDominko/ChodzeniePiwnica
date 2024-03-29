import random

import pygame as pg
import math
from constants import *
import engine as e
from damage_text import DamageText


class Arrow(pg.sprite.Sprite):
    image = e.scale_image(
        pg.image.load("assets/images/weapons/arrow.png"), WEAPON_SCALE)

    def __init__(self, angle, x, y, offset):
        super().__init__()
        self.offset = offset
        self.image = pg.transform.rotate(Arrow.image, angle - 90)
        self.rect = self.image.get_rect(center=(x, y))
        self.x, self.y = x, y
        self.dx, self.dy = self._set_dx_dy(self.offset)

    def _set_dx_dy(self, offset):
        mosX, mosY = pg.mouse.get_pos() + offset
        _angle = math.atan2(mosY - self.y, mosX - self.x)
        dx = math.cos(_angle) * ARROW_SPEED
        dy = math.sin(_angle) * ARROW_SPEED
        return dx, dy

    def _move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))

    def _collide_screen_borders(self):
        """Sprawdza, czy strzała wyszła poza okno gry, jeżeli tak,
        to ją kasuje"""
        # _rect = self.rect.copy()
        # _rect.topleft -= self.offset
        # if (_rect.right < 0 or _rect.left > SCREEN_WIDTH or
        #         _rect.bottom < 0 or _rect.top > SCREEN_HEIGHT):
        #     self.kill()

        # if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
        #         self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
        #     self.kill()
        if ((self.rect.right - self.offset.x < 0) or
                (self.rect.left - self.offset.x > SCREEN_WIDTH) or
                (self.rect.bottom - self.offset.y < 0) or
                (self.rect.top - self.offset.y > SCREEN_HEIGHT)):
            self.kill()

    def _collide_enemies(self, enemies, text):
        """Sprawdza, czy strzała trafiła wroga. Jeżeli tak, zadaje obrażenia."""
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect):
                damage = random.randint(5, 15)
                enemy.take_damage(damage)
                x = enemy.rect.centerx
                y = enemy.rect.top
                text.add(DamageText(x, y, damage, RED))
                self.kill()

    def update(self, enemies, text):
        self._move()
        self._collide_screen_borders()
        self._collide_enemies(enemies, text)

    def display(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
        # pg.draw.rect(screen, RED, self.rect, 1)
