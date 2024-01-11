import pygame as pg
import engine as e
from constants import *


class UserInterface:
    def __init__(self, player):
        self.player = player
        self.font = pg.font.Font("assets/fonts/AtariClassic.ttf", 60)
        self._load_images()

        self.panel_rect = pg.Rect(0, 0, SCREEN_WIDTH, self.height)

    def _load_images(self):
        self.hearth_full = e.scale_image(pg.image.load(
            "assets/images/items/heart_full.png").convert_alpha(), HEARTH_SCALE)
        self.hearth_half = e.scale_image(pg.image.load(
            "assets/images/items/heart_half.png").convert_alpha(), HEARTH_SCALE)
        self.hearth_empty = e.scale_image(pg.image.load(
            "assets/images/items/heart_empty.png").convert_alpha(),
                                          HEARTH_SCALE)
        self.width = self.hearth_full.get_width()
        self.height = self.hearth_full.get_height()
        self.coin = e.scale_image(pg.image.load(
            "assets/images/items/coin_f0.png").convert_alpha(), 7)

    def _draw_panel(self, screen):
        pg.draw.rect(screen, PANEL, self.panel_rect)
        pg.draw.line(screen, WHITE, (0, self.height),
                     (SCREEN_WIDTH, self.height), 3)

    def _draw_hearths(self, screen):
        half = False
        for i in range(8):
            if self.player.health >= ((i + 1) * 2):
                screen.blit(self.hearth_full, (i * self.width, 0))
            elif self.player.health % 2 > 0 and not half:
                screen.blit(self.hearth_half, (i * self.width, 0))
                half = True
            else:
                screen.blit(self.hearth_empty, (i * self.width, 0))

    def _draw_score(self, screen):
        img = self.font.render(f"X{self.player.score}", True, BLACK)
        img_rect = img.get_rect(right=SCREEN_WIDTH,
                                centery=self.panel_rect.centery)
        screen.blit(img, img_rect)
        coin_rect = self.coin.get_rect(right=img_rect.left,
                                       centery=self.panel_rect.centery)
        screen.blit(self.coin, coin_rect)

    def display(self, screen):
        self._draw_panel(screen)
        self._draw_hearths(screen)
        self._draw_score(screen)
