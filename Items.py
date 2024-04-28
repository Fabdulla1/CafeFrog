import pygame as py

class Items(py.sprite.Sprite):
    def __init__(self, screen, image, name, description, x, y):
        super().__init__()
        original_image = py.image.load(image)
        # Calculate new dimensions based on the scale factor
        width = int(original_image.get_width() * .5)
        height = int(original_image.get_height() * .5)
        # Scale the image
        self.image = py.transform.scale(original_image, (width, height))
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.withPlayer = False

    def draw(self, camX, camY):
        x = self.rect.x + camX
        y = self.rect.y + camY
        self.screen.blit(self.image, (x, y))
    
