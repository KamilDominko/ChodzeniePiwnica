import pygame as pg
import math
import os

import engine as e
from constants import *
from bow import Bow


class Player:
    def __init__(self, game, x, y):
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.flip = False  # Domyślnie sprite skierowany jest w PRAWO

        self.speed = 5
        self.bow = Bow()

        self.animation_index = 0
        self.animation_counter = pg.time.get_ticks()
        self.animations = e.load_animations("assets/images/characters", "elf")
        self.action = "idle"
        self.image = self.animations[self.action][self.animation_index]
        self.rect = self.image.get_rect(center=(x, y))

    def _load_animations(self, name):
        """Tworzy, a następnie zwraca słownik z nazwami animacji jako klucze i
        tablice obrazów animacji jako wartości."""
        _animation_types = ["idle", "run"]
        animations = {}
        for type in _animation_types:
            animations[type] = []
            _path = f"assets/images/characters/{name}/{type}"
            for i in range(len(os.listdir(_path))):
                img = pg.image.load(f"{_path}/{i}.png").convert_alpha()
                width = img.get_width()
                height = img.get_height()
                img = pg.transform.scale(img, (width * SCALE, height * SCALE))
                animations[type].append(img)
        return animations

    def _update_animation(self):
        _animation_cooldown = 120
        self.image = self.animations[self.action][self.animation_index]
        # sprawdź, czy sprite nie powinien zostać przekręcony w LEWO
        if self.flip:
            self.image = pg.transform.flip(self.image, self.flip, False)
        if pg.time.get_ticks() - self.animation_counter > _animation_cooldown:
            self.animation_index += 1
            self.animation_counter = pg.time.get_ticks()
        if self.animation_index >= len(self.animations[self.action]):
            self.animation_index = 0

    def input(self, event):
        """Funkcja sprawdza input z klawiatury i myszy dla gracza."""
        if event.type == pg.KEYDOWN:  # Wciśnięcie klawiszy klawiatury
            if event.key == pg.K_w:
                self.move_up = True
            if event.key == pg.K_s:
                self.move_down = True
            if event.key == pg.K_a:
                self.move_left = True
            if event.key == pg.K_d:
                self.move_right = True
        if event.type == pg.KEYUP:  # Zwolnienie klawiszy klawiatury
            if event.key == pg.K_w:
                self.move_up = False
            if event.key == pg.K_s:
                self.move_down = False
            if event.key == pg.K_a:
                self.move_left = False
            if event.key == pg.K_d:
                self.move_right = False
        if event.type == pg.MOUSEBUTTONDOWN:  # Wciśnięcie klawiszy myszki
            if event.button == 1:  # Lewy Przycisk Myszy LPM
                self.bow.shoot(self.rect.centerx,
                               self.rect.centery + self.rect.height // 4)
            if event.button == 3:  # Prawy Przycisk Myszy PPM
                pass
        if event.type == pg.MOUSEBUTTONUP:  # Zwolnienie klawiszy myszki
            if event.button == 1:  # LPM
                pass
            if event.button == 3:  # PPM
                pass

    def _move(self):
        dx, dy = 0, 0
        if self.move_up:
            dy += -self.speed
        if self.move_down:
            dy += self.speed
        if self.move_left:
            dx += -self.speed
        if self.move_right:
            dx += self.speed
        # zmień akcje z idle na run, jeżeli gracz się porusza
        if dx != 0 or dy != 0:
            self.action = "run"
        else:
            self.action = "idle"
        # przekręć gracza, jeżeli idzie w LEWO
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False
        # oblicz prędkość gracza, jeżeli porusza się w dwóch kierunkach naraz
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)
        # aktualizuj pozycje gracza
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self._move()
        self._update_animation()
        self.bow.update(self)

    def display(self, screen):
        screen.blit(self.image, self.rect)
        self.bow.display(screen)
        pg.draw.rect(screen, RED, self.rect, 1)
