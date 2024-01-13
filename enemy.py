import pygame as pg
import math
import os
from constants import *
import engine as e


class Enemy(pg.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.flip = False  # Domyślnie sprite skierowany jest w PRAWO

        self.speed = 3
        self.health = 100
        self.damage = 1

        self.last_hit = pg.time.get_ticks()

        self.animation_index = 0
        self.animation_counter = pg.time.get_ticks()
        self.animations = e.load_animations("assets/images/characters", name)
        self.action = "idle"
        self.image = self.animations[self.action][self.animation_index]
        self.rect = self.image.get_rect(center=(x, y))

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
        # zmień akcje z idle na run, jeżeli się porusza
        if dx != 0 or dy != 0:
            self.action = "run"
        else:
            self.action = "idle"
        # przekręć sprite, jeżeli idzie w LEWO
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False
        # dostosowanie prędkości do ruchu po przekątnej
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)
        # aktualizuj pozycje
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

    def _ai(self, player, obstacles):
        clipped_line = ()
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        # sprawdź, czy gracz jest w zasięgu wzroku
        line_of_sight = ((self.rect.centerx, self.rect.centery),
                         (player.rect.centerx, player.rect.centery))
        for obstacle in obstacles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        x = (self.rect.centerx - player.rect.centerx) ** 2
        y = (self.rect.centery - player.rect.centery) ** 2
        dist = math.sqrt(x + y)
        if not clipped_line and dist > self.rect.w // 2:
            if self.rect.centerx > player.rect.centerx:
                self.move_left = True
            if self.rect.centerx < player.rect.centerx:
                self.move_right = True
            if self.rect.centery > player.rect.centery:
                self.move_up = True
            if self.rect.centery < player.rect.centery:
                self.move_down = True
        # zaatakuj gracza
        if dist <= self.rect.w:
            player.take_damage(self.damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.kill()

    def update(self, obstacles, player):
        self._ai(player, obstacles)
        self._move(obstacles)
        self._update_animation()

    def display(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
        # pg.draw.rect(screen, RED, self.rect, 1)
