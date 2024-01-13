import pygame as pg
import csv
from constants import *
import engine as e
from item import Item
from enemy import Enemy


class Word:
    def __init__(self, sprite_handler):
        self.sprite_handler = sprite_handler
        self.map_tiles = []
        self.tile_images = self._load_tile_images()
        self.obstacle_tiles = []
        self.exit_tile = None

    def create_epmty_world_data(self):
        world_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)
        return world_data

    def load_level_from_file(self, world_data, level):
        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        return world_data

    def _load_tile_images(self):
        tile_list = []
        for i in range(TILE_TYPES):
            tile_image = pg.image.load(
                f"assets/images/tiles/{i}.png").convert_alpha()
            tile_image = e.scale_image(tile_image, SCALE)
            tile_list.append(tile_image)
        return tile_list

    def process_data(self, data):
        self.level_lenght = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = self.tile_images[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                if tile == 7:  # ściana
                    self.sprite_handler.obstacles.append(tile_data)
                    # self.obstacle_tiles.append(tile_data)
                elif tile == 8:  # drabina
                    self.exit_tile = tile_data
                elif tile == 9:  # moneta
                    coin = Item(image_x, image_y, 0)
                    self.sprite_handler.items.add(coin)
                    tile_data[0] = self.tile_images[0]
                    tile_data[1] = tile_data[0].get_rect(
                        center=(image_x, image_y))
                elif tile == 10:  # mikstura życia
                    potion = Item(image_x, image_y, 1)
                    self.sprite_handler.items.add(potion)
                    tile_data[0] = self.tile_images[0]
                elif tile == 11:  # gracz
                    self.sprite_handler.player.rect.center = (image_x, image_y)
                    tile_data[0] = self.tile_images[0]
                    tile_data[1] = tile_data[0].get_rect(
                        center=(image_x, image_y))
                elif tile == 12:
                    enemy = Enemy("imp", image_x, image_y)
                    self.sprite_handler.enemies.add(enemy)
                    tile_data[0] = self.tile_images[0]
                elif tile == 13:
                    enemy = Enemy("skeleton", image_x, image_y)
                    self.sprite_handler.enemies.add(enemy)
                    tile_data[0] = self.tile_images[0]
                elif tile == 14:
                    enemy = Enemy("goblin", image_x, image_y)
                    self.sprite_handler.enemies.add(enemy)
                    tile_data[0] = self.tile_images[0]
                elif tile == 15:
                    enemy = Enemy("muddy", image_x, image_y)
                    self.sprite_handler.enemies.add(enemy)
                    tile_data[0] = self.tile_images[0]
                elif tile == 16:
                    enemy = Enemy("tiny_zombie", image_x, image_y)
                    self.sprite_handler.enemies.add(enemy)
                    tile_data[0] = self.tile_images[0]
                elif tile == 17:
                    enemy = Enemy("big_demon", image_x, image_y)
                    self.sprite_handler.enemies.add(enemy)
                    tile_data[0] = self.tile_images[0]
                    tile_data[1] = tile_data[0].get_rect(
                        center=(image_x, image_y))

                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def display(self, screen, offset):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1].topleft - offset)
