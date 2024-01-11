import pygame as pg


class SpriteHandler:
    def __init__(self, offset):
        self.player = None
        self.offset = offset
        self.enemies = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.text = pg.sprite.Group()

    def update(self):
        self.player.update(self.offset)
        self.enemies.update()
        self.arrows.update(self.enemies, self.text)
        self.items.update(self.player)
        self.text.update()

    def display(self, screen):
        # player
        self.player.display(screen, self.offset)
        # enemies
        for enemy in self.enemies:
            enemy.display(screen, self.offset)
        # strzały
        if self.arrows:
            for arrow in self.arrows:
                arrow.display(screen, self.offset)
        # items
        # self.items.draw(screen)
        for item in self.items:
            item.display(screen, self.offset)
        # text
        # self.text.draw(screen)
        for text in self.text:
            text.display(screen, self.offset)
