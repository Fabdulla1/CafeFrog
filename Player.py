import pygame as py

class Player(py.sprite.Sprite):
    def __init__(self, image, screen):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.mask = py.mask.from_surface(self.image)

        # Initialize player's position
        self.dx = self.screen.get_width() // 2
        self.dy = self.screen.get_height() // 2
        self.rect.x = self.dx
        self.rect.y = self.dy

        # Idle animations
        self.idleDown = self.get_image(0, 0)
        self.idleUp = self.get_image(0, 1)
        self.idleRight = self.get_image(0, 2)
        self.idleLeft = self.get_image(0, 3)

        # Walking animations
        self.moveDown = [self.get_image(x, 4) for x in range(6)]
        self.moveUp = [self.get_image(x, 5) for x in range(6)]
        self.moveRight = [self.get_image(x, 6) for x in range(6)]
        self.moveLeft = [self.get_image(x, 7) for x in range(6)]

        self.animation_frames = self.moveDown
        self.current_frame = self.idleDown  # Start with idle down animation
        self.last_update = py.time.get_ticks()
        self.frame = 0

    def get_image(self, frameX, frameY):
        width, height, scale = 64, 64, 2
        image = py.Surface((width, height), py.SRCALPHA)
        image.blit(self.image, (0, 0), (frameX * width, frameY * height, width, height))
        image = py.transform.scale(image, (width * scale, height * scale))
        #mask and rect must be updated anytime new image is created. This ensures consistency across all images.
        self.rect = image.get_rect()
        self.mask = py.mask.from_surface(image)
        return image

    def move(self, keyArr, obstacles):
        now = py.time.get_ticks()
        moving = False
        x, y = 0, 0  # Movement deltas

        # Check each direction and attempt to move, update facing direction regardless of movement
        if keyArr[py.K_w]:
            if self.canMove(0, -4, obstacles):
                y -= 4
                moving = True
            self.animation_frames = self.moveUp

        if keyArr[py.K_s]:
            if self.canMove(0, 4, obstacles):
                y += 4
                moving = True
            self.animation_frames = self.moveDown

        if keyArr[py.K_a]:
            if self.canMove(-4, 0, obstacles):
                x -= 4
                moving = True
            self.animation_frames = self.moveLeft

        if keyArr[py.K_d]:
            if self.canMove(4, 0, obstacles):
                x += 4
                moving = True
            self.animation_frames = self.moveRight

        # Update position if movement is allowed
        self.dx += x
        self.dy += y
        self.rect.x = self.dx
        self.rect.y = self.dy

        # Update the animation based on movement
        if moving:
            if now - self.last_update > 100:  # Update every 100ms
                self.last_update = now
                self.frame = (self.frame + 1) % len(self.animation_frames)
                self.current_frame = self.animation_frames[self.frame]
        else:
            # Set to idle animation based on last direction, and reset frame index
            self.set_idle_animation()
            self.frame = 0

        # Draw the current frame at the new position
        self.screen.blit(self.current_frame, self.rect)
    
    def set_idle_animation(self):
        # Set idle animation based on last movement animation
        if self.animation_frames == self.moveDown:
            self.current_frame = self.idleDown
        elif self.animation_frames == self.moveUp:
            self.current_frame = self.idleUp
        elif self.animation_frames == self.moveRight:
            self.current_frame = self.idleRight
        elif self.animation_frames == self.moveLeft:
            self.current_frame = self.idleLeft

    def draw(self, camera_offset_x, camera_offset_y):
        # Calculate the position with the camera offset
        screen_x = self.dx + camera_offset_x
        screen_y = self.dy + camera_offset_y

        # Draw the current frame of animation at the new position
        self.screen.blit(self.current_frame, (screen_x, screen_y))
    def canMove(self, dx, dy, obstacles):
        # Temporarily adjust the player's rect for the hypothetical next position
        original_position = self.rect.topleft
        self.rect.x += dx
        self.rect.y += dy
        
        # Check for collisions at the new position
        for obstacle in obstacles:
            collided_sprites = py.sprite.spritecollide(self, obstacle, False, py.sprite.collide_mask)
            if collided_sprites:
                return False

        # Reset the player's rect to its original position
        self.rect.topleft = original_position
        
        return True