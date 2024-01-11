import pygame as pg
import engine as e
from constants import *


class Item(pg.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type  # 0:coin. 1:health potion
        self.animation_list = self._load_images(item_type)
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    # def _load_both_images(self):
    #     coin_images = []
    #     potion_images = []
    #     # moneta
    #     for i in range(4):
    #         img = e.scale_image(
    #             pg.image.load(f"assets/images/items/coin_f{i}.png"), ITEM_SCALE)
    #         coin_images.append(img)
    #     # mikstura
    #     img = e.scale_image(pg.image.load("assets/images/items/potion_red.png"),
    #                         ITEM_SCALE)
    #     potion_images.append(img)

    def _load_images(self, item_type):
        aniamtion_list = []
        if item_type == 0:  # coin
            for i in range(4):
                img = pg.image.load(f"assets/images/items/coin_f{i}.png")
                img = e.scale_image(img, ITEM_SCALE)
                aniamtion_list.append(img)
        elif item_type == 1:  # health potion
            img = pg.image.load("assets/images/items/potion_red.png")
            img = e.scale_image(img, POTION_SCALE)
            aniamtion_list.append(img)
        return aniamtion_list

    def _update_animation(self):
        self.image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > 150:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def _collision(self, player):
        if self.rect.colliderect(player):
            if self.item_type == 0: # moneta
                player.score += 1
                self.kill()
            elif self.item_type == 1: # mikstura życia
                if player.health < 16:
                    player.health += 1
                    self.kill()


    def update(self, player):
        self._update_animation()
        self._collision(player)


    def display(self, screen):
        pg.draw.rect(screen, RED, self.rect, 1)