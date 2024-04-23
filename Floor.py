import pygame as py

class Floor(py.sprite.Sprite):

    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
    def updatePosition(self, x, y):
        self.rect.x += x
        self.rect.y += y