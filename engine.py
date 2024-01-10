import pygame as pg

import os
from constants import *


def scale_image(image, scale):
    """Skaluje obraz-image przez podaną wartość-scale"""
    width = image.get_width() * scale
    height = image.get_height() * scale
    return pg.transform.scale(image, (width, height))


def load_animations(path, name, animation_types=("idle", "run")):
    """Pobiera ścieżkę-path do folderu, w którym znajduje się folder-name,
    w którym z kolei znajdują się foldery-animation_types.
    Tworzy i zwraca słownik z nazwami-animation_types jako klucze
    i tablicami zawierającymi obrazy poszczególnego animation_types jako
    wartości."""
    animations = {}
    for type in animation_types:
        animations[type] = []
        _path = f"{path}/{name}/{type}"
        for i in range(len(os.listdir(_path))):
            img = pg.image.load(f"{_path}/{i}.png").convert_alpha()
            width = img.get_width()
            height = img.get_height()
            img = pg.transform.scale(img, (width * SCALE, height * SCALE))
            animations[type].append(img)
    return animations
