class Camera:
    def __init__(self):
        self.offset = [0, 0]


    def update_offset(self):
        """Funkcja aktualizuje wartość przesunięcia kamery, która mówi jak
        bardzo wszystko ma być przesunięte podczas wyświetlania na ekranie,
        aby gracz był ciągle na środku ekranu."""
        self.offset.x = self.program.player.rect.centerx - \
                        self.screenHalfWidth
        self.offset.y = self.program.player.rect.centery - \
                        self.screenHalfHeight

    def camera_draw(self, image, topleft):
        _offset = topleft - self.offset
        self.screen.blit(image, _offset)

    def give_mouse(self):
        x, y = pygame.mouse.get_pos()
        x += self.offset[0]
        y += self.offset[1]
        return x, y