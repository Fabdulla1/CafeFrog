import pygame as py

class items(py.sprite.Sprite):
    def __init__(self, image, name, description, height, width, x, y, path):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width
        self.description = description
        self.name = name
        self.mask = py.mask.from_surface(self.image)
