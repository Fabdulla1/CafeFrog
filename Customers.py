import pygame as py
import random
    
class Customers(py.sprite.Sprite):
    def __init__(self, image, screen):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.mask = py.mask.from_surface(self.image)
        self.frame_width = 32
        self.frame_height = 32
        self.scale = 2
        self.dx = 0
        self.dy = self.screen.get_height() // 2
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.idleDown = self.get_image(0, 0)
        self.idleRight = self.get_image(1, 0)
        self.idleUp = self.get_image(2, 0)
        self.idleLeft = self.get_image(3, 0)
        self.moveDown = [self.get_image(x, row) for row in range(1, 3) for x in range(4)]
        self.moveLeft = [self.get_image(x, row) for row in range(3, 5) for x in range(4)]
        self.moveRight = [self.get_image(x, row) for row in range(5, 7) for x in range(4)]
        self.moveUp = [self.get_image(x, row) for row in range(7, 9) for x in range(4)]
        self.animation_frames = self.moveDown
        self.current_frame = self.idleDown
        self.last_update = py.time.get_ticks()
        self.frame = 0
        self.font = py.font.Font(None, 24)
        self.dialog_box = None
        self.prompt_visible = False
        self.dialog_visible = False
        
        # Checks for customer's activity
        self.paid = False
        self.togo = False
        #Customer's target location upon entrance. Takes them straight to the cash register.
        self.targetX = (self.screen.get_width() // 2) + 70
        self.targetY = self.screen.get_height() // 2

        self.status = 'In Line'

    def get_image(self, frameX, frameY):
        image = py.Surface((self.frame_width, self.frame_height), py.SRCALPHA)
        image.blit(self.image, (0, 0), (frameX * self.frame_width, frameY * self.frame_height, self.frame_width, self.frame_height))
        image = py.transform.scale(image, (self.frame_width * self.scale, self.frame_height * self.scale))
        self.rect = image.get_rect()
        self.mask = py.mask.from_surface(image)
        return image
    
    #TODO: 
    def determineNextLocation(self):
        #variables to use: self.targetX, self.targetY, self.paid, self.togo
        if self.paid:
            self.targetX = 700
            self.targetY = 40
            self.status = 'Paid'
    
    def pathfinding(self, obstacles):
        now = py.time.get_ticks()
        moving = False
        self.determineNextLocation()

        
        if abs(self.dx - self.targetX) <= 10 and abs(self.dy - self.targetY) <= 10:
            self.set_idle_animation()
            self.status = 'Ordering'
            return

        directions = {
            'right': (4, 0, self.moveRight),
            'left': (-4, 0, self.moveLeft),
            'up': (0, -4, self.moveUp),
            'down': (0, 4, self.moveDown),
        }

        f_values = {
            direction: self.gCalc(self.dx, self.dy, self.dx + dx, self.dy + dy) + self.hCalc(self.dx + dx, self.dy + dy, self.targetX, self.targetY)
            for direction, (dx, dy, _) in directions.items()
        }

        #Quick sorting
        sorted_f_values = sorted(f_values.items(), key=lambda item: item[1])
        sorted_f_values_dict = dict(sorted_f_values)

        direction = min(f_values, key=f_values.get)
        dx, dy, self.animation_frames = directions[direction]

        if self.canMove(dx, dy, obstacles):
            moving = True
            self.dx += dx
            self.dy += dy
        else:
            if self.status == 'In Line':
                self.set_idle_animation()
            else:
                for path in directions.keys():
                    if path != direction:
                        if self.canMove(directions[path][0], directions[path][1], obstacles):
                            moving = True
                            self.dx += directions[path][0]
                            self.dy += directions[path][1]


        self.update_animation(now, moving)

    def set_idle_animation(self):
        if self.animation_frames in [self.moveDown, self.moveRight, self.moveUp, self.moveLeft]:
            if self.animation_frames == self.moveDown:
                self.current_frame = self.idleDown
            elif self.animation_frames == self.moveUp:
                self.current_frame = self.idleUp
            elif self.animation_frames == self.moveRight:
                self.current_frame = self.idleRight
            elif self.animation_frames == self.moveLeft:
                self.current_frame = self.idleLeft

    def update_animation(self, now, moving):
        if moving:
            if now - self.last_update > 100:
                self.last_update = now
                self.frame = (self.frame + 1) % len(self.animation_frames)
                self.current_frame = self.animation_frames[self.frame]
        else:
            self.set_idle_animation()
            self.frame = 0

        self.rect.x = self.dx
        self.rect.y = self.dy
        self.mask = py.mask.from_surface(self.current_frame)
        self.screen.blit(self.current_frame, self.rect)

    def hCalc(self, x, y, tgtX, tgtY):
        return abs(x - tgtX) + abs(y - tgtY)

    def gCalc(self, thetaX, thetaY, x, y):
        return abs(thetaX - x) + abs(thetaY - y)

    def draw(self, camera_offset_x, camera_offset_y):
        screen_x = self.dx + camera_offset_x
        screen_y = self.dy + camera_offset_y
        self.screen.blit(self.current_frame, (screen_x, screen_y))

    def canMove(self, dx, dy, obstacles):
        original_position = self.rect.topleft
        self.rect.x += dx
        self.rect.y += dy
        for obstacle in obstacles:
            if py.sprite.spritecollide(self, obstacle, False, py.sprite.collide_mask):
                self.rect.topleft = original_position
                return False
        self.rect.topleft = original_position
        return True
    
    def check_proximity(self, player_rect):
        """Check if the player is close enough to trigger the interaction prompt."""
        distance = self.rect.colliderect(player_rect.inflate(50, 50))  # Inflate the player rect for proximity checking
        if distance:
            self.prompt_visible = True
            return True
        else:
            self.prompt_visible = False
            self.dialog_visible = False  # Hide dialog if player moves away
            return False

    def draw_prompt(self):
        """Draw the 'Press E to talk' prompt above the customer."""
        if self.prompt_visible and not self.dialog_visible:
            text_surface = self.font.render("Press E to talk", True, (255, 255, 255))
            x = self.rect.centerx - text_surface.get_width() / 2
            y = self.rect.top - 30
            self.screen.blit(text_surface, (x, y))


    

    
