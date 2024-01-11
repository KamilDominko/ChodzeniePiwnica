import pygame as pg
from constants import *
from player import Player
from enemy import Enemy
from bow import Bow
from sprite_handler import SpriteHandler
from user_interface import UserInterface
from item import Item
from world import Word

pg.init()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.clock = pg.time.Clock()

        self.offset = pg.math.Vector2()
        self.level = 1
        self.player = Player(self, 200, 300)
        self.world = Word()
        world_data = self.world.create_epmty_world_data()
        world_data = self.world.load_level_from_file(world_data, self.level)
        self.world.process_data(world_data)


        self.sprite_handler = SpriteHandler(self.offset)
        self.interface = UserInterface(self.player)

        self.sprite_handler.player = self.player
        self.sprite_handler.enemies.add(Enemy(self, 'skeleton', 500, 500))
        self.sprite_handler.items.add(Item(600, 400, 1))
        self.sprite_handler.items.add(Item(700, 400, 0))

    def _update_offset(self):
        self.offset.x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = self.player.rect.centery - SCREEN_HEIGHT // 2

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
        self._update_offset()

    def _update_screen(self):
        self.screen.fill(BG)
        self.world.display(self.screen, self.offset)
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
