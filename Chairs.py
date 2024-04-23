import pygame as py

class Chairs(py.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def location(self):
        return (self.x, self.y)
    def updatePosition(self, dx, dy):
        self.rect.x = dx
        self.rect.y = dy
        