import pygame as pg
import math
import os

import engine as e
from constants import *
from bow import Bow


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.offset = game.offset
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.flip = False  # Domyślnie sprite skierowany jest w PRAWO

        self.speed = 5
        self.health = 16
        self.score = 0
        self.bow = Bow()

        self.last_hit = pg.time.get_ticks()

        self.animation_index = 0
        self.animation_counter = pg.time.get_ticks()
        self.animations = e.load_animations("assets/images/characters", "elf")
        self.action = "idle"
        self.image = self.animations[self.action][self.animation_index]

        self.rect = self.image.get_rect(center=(x, y), width=TILE_SIZE,
                                        height=TILE_SIZE)

    def _update_animation(self):
        """Aktualizuje obraz bytu oraz indeks animacji."""
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

    def _move(self, obstacles):
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
        # sprawdź kolizję z przeszkodami w poziomie
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        # sprawdź kolizję z przeszkodami w pionie
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

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
                               self.rect.centery + self.rect.height // 4,
                               self.game.sprite_handler.arrows, self.offset)
            if event.button == 3:  # Prawy Przycisk Myszy PPM
                pass
        if event.type == pg.MOUSEBUTTONUP:  # Zwolnienie klawiszy myszki
            if event.button == 1:  # LPM
                pass
            if event.button == 3:  # PPM
                pass

    def take_damage(self, damage):
        if pg.time.get_ticks() - self.last_hit > 500:
            self.last_hit = pg.time.get_ticks()
            self.health -= damage
            if self.health <= 0:
                self.health = 0

    def update(self, offset, obstacles):
        self._move(obstacles)
        self._update_animation()
        self.bow.update(self, offset)

    def display(self, screen, offset):
        # nie wiem kurwa co tu się stało, podzielić TILE_SIZE na 3 i działa
        rect = (self.rect.x, self.rect.y - self.image.get_rect().w +
                TILE_SIZE / 3)

        # rect = self.image.get_rect(center=(self.rect.centerx,
        #                                    self.rect.centery-self.image.get_rect().h//3))
        rect -= offset
        screen.blit(self.image, rect)

        # img_rect = self.image.get_rect(center=self.rect.center)
        # img_rect.topleft -= offset
        # pg.draw.rect(screen, BLACK, img_rect, 2)
        # screen.blit(self.image, img_rect.topleft)

        self.bow.display(screen, offset)
        # pg.draw.rect(screen, RED, self.rect, 1)

        # rect = pg.Rect(self.rect.x - offset.x, self.rect.y - offset.y,
        #                self.rect.w, self.rect.h)

        # rect = pg.Rect(self.rect.x - offset.x, self.rect.y - offset.y,
        #                self.rect.w, self.rect.h)
        # pg.draw.rect(screen, RED, rect, 1)
