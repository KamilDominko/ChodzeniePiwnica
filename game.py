import pygame as pg
from constants import *
from player import Player
from enemy import Enemy
from bow import Bow
from sprite_handler import SpriteHandler
from user_interface import UserInterface
from item import Item

pg.init()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player(self, 200, 300)
        self.running = True
        self.clock = pg.time.Clock()

        self.sprite_handler = SpriteHandler()
        self.interface = UserInterface(self.player)

        self.sprite_handler.player = self.player
        self.sprite_handler.enemies.add(Enemy(self, 'skeleton', 500, 500))
        self.sprite_handler.items.add(Item(600, 400, 1))
        self.sprite_handler.items.add(Item(700, 400, 0))

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
            self.sprite_handler.player.input(event)

    def _update(self):
        self.sprite_handler.update()

    def _update_screen(self):
        self.screen.fill(BG)
        self.sprite_handler.display(self.screen)
        self.interface.display(self.screen)
        # Odśwież okno.
        pg.display.update()

    def start(self):
        while self.running:
            self._check_events()
            self._update()
            self._update_screen()
            self.clock.tick(FPS)
