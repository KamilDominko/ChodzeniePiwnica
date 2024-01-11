import pygame as pg
import csv
from constants import *
import engine as e


class Word:
    def __init__(self):
        self.map_tiles = []
        self.tile_images = self._load_tile_images()

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
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def display(self, screen, offset):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1].topleft-offset)
