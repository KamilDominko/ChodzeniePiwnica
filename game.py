import pygame as pg
from constants import *
from player import Player
from enemy import Enemy
from bow import Bow

pg.init()


class Game:
    def __init__(self):
        self.running = True
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.player = Player(self, 200, 300)
        self.enemy = Enemy(self, 'skeleton', 500, 500)

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_SPACE:
                    self.enemy.action = "run"
            self.player.input(event)

    def _update(self):
        self.player.update()
        self.enemy.update()

    def _update_screen(self):
        self.screen.fill(BLACK)
        self.player.display(self.screen)
        self.enemy.display(self.screen)
        pg.display.update()

    def start(self):
        while self.running:
            self._check_events()
            self._update()
            self._update_screen()
            self.clock.tick(FPS)
