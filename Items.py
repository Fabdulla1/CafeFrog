import pygame as py

class Items(py.sprite.Sprite):
    def __init__(self, screen, image, name, description, x, y):
        super().__init__()
        self.image = py.image.load(image)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.description = description
        self.name = name
        self.mask = py.mask.from_surface(self.image)
        self.withPlayer = False

    def draw(self, camX, camY):
        x = self.rect.x + camX
        y = self.rect.y + camY
        self.screen.blit(self.image, (x, y))
    
