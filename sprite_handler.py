import pygame as pg


class SpriteHandler:
    def __init__(self):
        self.player = None
        self.enemies = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.text = pg.sprite.Group()

    def update(self):
        self.player.update(self.enemies)
        self.enemies.update()
        self.arrows.update(self.enemies, self.text)
        self.items.update(self.player)
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
        # items
        self.items.draw(screen)
        # for item in self.items:
        #     item.display(screen)
        # text
        self.text.draw(screen)
