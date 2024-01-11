import pygame as pg


class SpriteHandler:
    def __init__(self):
        self.player = None
        self.enemies = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.text = pg.sprite.Group()

    def update(self):
        # player
        self.player.update(self.enemies)
        # enemies
        self.enemies.update()
        # arrows
        self.arrows.update(self.enemies, self.text)
        # text
        self.text.update()

    def display(self, screen):
        # player
        self.player.display(screen)
        # enemies
        for enemy in self.enemies:
            enemy.display(screen)
        # strzały
        if self.arrows:
            for arrow in self.arrows:
                arrow.display(screen)
        # text
        self.text.draw(screen)
