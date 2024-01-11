import pygame as pg


class DamageText(pg.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        super().__init__()
        self.font = pg.font.Font("assets/fonts/AtariClassic.ttf", 20)
        self.image = self.font.render(str(damage), True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = pg.time.get_ticks()

    def update(self):
        self.rect.y -= 1
        if pg.time.get_ticks() - self.counter > 500:
            self.kill()

    def display(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
