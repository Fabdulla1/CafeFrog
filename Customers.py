import pygame as py
import random
import numpy as np
from sklearn.naive_bayes import MultinomialNB

class DialogueClassifier:
    def __init__(self):
        self.model = MultinomialNB()
        # Dummy train (here we just pretend as if we are training)
        self.train()

    def train(self):
        # Dummy feature vectors and labels (for demonstration)
        X = np.array([[1,1], [2,0], [0,1], [1,0], [0,1], [1,1]])  # Simplified feature vectors
        y = np.array(['greeting', 'farewell', 'complaint', 'greeting', 'complaint', 'farewell'])  # Labels
        self.model.fit(X, y)

    def classify(self, features):
        # Dummy predict (we simulate a feature input)
        return self.model.predict(np.array([features]))[0]

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
        self.dialogue_classifier = DialogueClassifier()
        self.dialog = {
            'greeting': ["Hey there!", "How are you?", "Working hard or hardly working? XD"],
            'inquiry': ["What do you have for sale today?", "What's the special today?", ""],
            'complaint': ["I'm really sad about this.", "Can I speak to the manager"],
            'farewell': ["Goodbye, have a great day!", "See you next time!", "Thanks for the coffee!"]
        }
        self.dialog_box = None
        self.prompt_visible = False
        self.dialog_visible = False

    def get_image(self, frameX, frameY):
        image = py.Surface((self.frame_width, self.frame_height), py.SRCALPHA)
        image.blit(self.image, (0, 0), (frameX * self.frame_width, frameY * self.frame_height, self.frame_width, self.frame_height))
        image = py.transform.scale(image, (self.frame_width * self.scale, self.frame_height * self.scale))
        self.rect = image.get_rect()
        self.mask = py.mask.from_surface(image)
        return image
    
    def pathfinding(self, target, obstacles):
        now = py.time.get_ticks()
        moving = False

        if abs(self.dx - target[0]) <= 4 and abs(self.dy - target[1]) <= 4:
            self.set_idle_animation()
            return

        directions = {
            'right': (4, 0, self.moveRight),
            'left': (-4, 0, self.moveLeft),
            'up': (0, -4, self.moveUp),
            'down': (0, 4, self.moveDown),
        }

        f_values = {
            direction: self.gCalc(self.dx, self.dy, self.dx + dx, self.dy + dy) + self.hCalc(self.dx + dx, self.dy + dy, target[0], target[1])
            for direction, (dx, dy, _) in directions.items()
        }

        direction = min(f_values, key=f_values.get)
        dx, dy, self.animation_frames = directions[direction]

        if self.canMove(dx, dy, obstacles):
            moving = True
            self.dx += dx
            self.dy += dy
        else:
            self.set_idle_animation()

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
        self.draw_prompt()
        if self.dialog_visible:
            self.draw_dialog()

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_e and self.prompt_visible:
                    self.handle_interaction(event)
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
        else:
            self.prompt_visible = False
            self.dialog_visible = False  # Hide dialog if player moves away

    def draw_prompt(self):
        """Draw the 'Press E to talk' prompt above the customer."""
        if self.prompt_visible and not self.dialog_visible:
            text_surface = self.font.render("Press E to talk", True, (255, 255, 255))
            x = self.rect.centerx - text_surface.get_width() / 2
            y = self.rect.top - 30
            self.screen.blit(text_surface, (x, y))

    def handle_interaction(self, event):
        self.dialog_visible = not self.dialog_visible
        if self.dialog_visible:
            features = [random.randint(0, 2), random.randint(0, 2)]  # Dummy features
            dialogue_type = self.dialogue_classifier.classify(features)
            self.current_dialog = random.choice(self.dialog[self.dialogue_classifier.classify(features)])
        else:
            self.current_dialog = None

    def toggle_dialog(self):
        """Toggle the visibility of the dialog box."""
        self.dialog_visible = not self.dialog_visible

    def draw_dialog(self):
        if self.dialog_visible:
            dialog_box = self.font.render(self.current_dialog, True, (255, 255, 255))
            x = (self.screen.get_width() - dialog_box.get_width()) // 2
            y = self.screen.get_height() - dialog_box.get_height() - 20
            self.screen.blit(dialog_box, (x, y))

    def updateDialog(self, player_rect):
        """Call this method every frame, passing in the player's rect."""
        self.check_proximity(player_rect)

    
