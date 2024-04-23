import pygame as py

class Tables(py.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width
        self.mask = py.mask.from_surface(self.image)
    def location(self):
        return (self.x, self.y)
    def updatePosition(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
class TableLegs(py.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = py.mask.from_surface(self.image)
    def location(self):
        return (self.x, self.y)
    def updatePosition(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy