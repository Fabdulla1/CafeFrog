import pygame as py

class Inventory(py.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.is_open = False
        self.load_animations()
        self.current_page = 0
        self.button_scale_factor = 1.0
        self.load_buttons()
        self.button_left_rect = self.button_left.get_rect(topleft=(160, 640))
        self.button_right_rect = self.button_right.get_rect(topleft=(1040, 640))
        self.items = []
        # Load other necessary UI elements or inventory items here.
    def load_buttons(self):
        # Load and scale buttons
        left_button_img = py.image.load("Assets/Book/leftArrowButton.png").convert_alpha()
        right_button_img = py.image.load("Assets/Book/rightArrowButton.png").convert_alpha()
        self.button_left = self.scale_image(left_button_img, self.button_scale_factor)
        self.button_right = self.scale_image(right_button_img, self.button_scale_factor)

    def load_animations(self):
        scale_factor = 1.5  # Example scale factor, adjust as needed
        # Adjust the loading and scaling of images
        self.animations = {
            'open': [self.scale_image(py.image.load(f'Assets/Book/Open/{i}.png').convert_alpha(), scale_factor) for i in range(1, 7)],
            'close': [self.scale_image(py.image.load(f'Assets/Book/Close/{i}.png').convert_alpha(), scale_factor) for i in range(1, 7)],
            'flip_left': [self.scale_image(py.image.load(f'Assets/Book/Left/{i}.png').convert_alpha(), scale_factor) for i in range(1, 9)],
            'flip_right': [self.scale_image(py.image.load(f'Assets/Book/Right/{i}.png').convert_alpha(), scale_factor) for i in range(1, 9)]
        }
    def scale_image(self, image, scale_factor):
        # Scale the image by the given factor
        width = int(image.get_width() * scale_factor)
        height = int(image.get_height() * scale_factor)
        return py.transform.scale(image, (width, height))

    def play_animation(self, animation_key):
        book_frame = self.animations[animation_key][0]  # Just for reference to get scaled size
        book_pos_x = (self.screen.get_width() - book_frame.get_width()) // 2
        book_pos_y = (self.screen.get_height() - book_frame.get_height()) // 2

        for frame in self.animations[animation_key]:
            self.screen.fill((0, 0, 0))
            self.screen.blit(frame, (book_pos_x, book_pos_y))
            # Draw the buttons within the loop before the display update
            py.display.flip()
            py.time.wait(100)
    
        if self.current_page > 0: 
            self.screen.blit(self.button_left, (160, 640))
        self.screen.blit(self.button_right, (1040, 640))
        py.display.flip()

    def draw_buttons(self):
        # Check for mouse hover and draw buttons with or without hover effect
        mouse_pos = py.mouse.get_pos()
        
        if self.button_left_rect.collidepoint(mouse_pos) and self.current_page > 0:
            self.button_left_hover = self.apply_hover_effect(self.button_left)
            self.screen.blit(self.button_left_hover, self.button_left_rect.topleft)
        elif self.current_page > 0:
            self.screen.blit(self.button_left, self.button_left_rect.topleft)
        
        if self.button_right_rect.collidepoint(mouse_pos):
            self.button_right_hover = self.apply_hover_effect(self.button_right)
            self.screen.blit(self.button_right_hover, self.button_right_rect.topleft)
        else:
            self.screen.blit(self.button_right, self.button_right_rect.topleft)
        mouse_pos = py.mouse.get_pos()
        mouse_click = py.mouse.get_pressed()
        
        if self.button_left_rect.collidepoint(mouse_pos) and self.current_page > 0:
            self.button_left_hover = self.apply_hover_effect(self.button_left)
            self.screen.blit(self.button_left_hover, self.button_left_rect.topleft)
            if mouse_click[0]:  # If left mouse button is clicked
                self.flip_page('right')
        elif self.current_page > 0:
            self.screen.blit(self.button_left, self.button_left_rect.topleft)
        
        if self.button_right_rect.collidepoint(mouse_pos):
            self.button_right_hover = self.apply_hover_effect(self.button_right)
            self.screen.blit(self.button_right_hover, self.button_right_rect.topleft)
            if mouse_click[0]:  # If left mouse button is clicked
                self.flip_page('left')
        else:
            self.screen.blit(self.button_right, self.button_right_rect.topleft)
    
    def apply_hover_effect(self, image):
        # Create a 'brighter' version of the image for the hover effect
        # This example simply creates a slightly transparent white overlay.
        # Adjust the alpha for the desired brightness effect.
        hover_image = image.copy()
        overlay = py.Surface(hover_image.get_size(), py.SRCALPHA)
        overlay.fill((255, 255, 255, 50))  # Adjust the alpha for brightness
        hover_image.blit(overlay, (0, 0), special_flags=py.BLEND_RGBA_ADD)
        return hover_image
    
    def open(self):
        if not self.is_open:
            self.play_animation('open')
            self.is_open = True
            # After opening animation, draw the first page or inventory items here.
            self.pageOne()

    def close(self):
        if self.is_open:
            self.play_animation('close')
            self.is_open = False
            # Additional cleanup or transition can be handled here.

    def flip_page(self, direction):
        # This could be simplified to just 'left' or 'right'
        if direction == 'left':
            self.current_page += 1
            self.play_animation('flip_left')
            # Update the current_page and items shown as necessary.
        elif direction == 'right':
            self.current_page -= 1
            self.play_animation('flip_right')
            if self.current_page == 0:
                self.pageOne()
            # Update the current_page and items shown as necessary.
                
    def addToInventory(self, item):
        self.items.append(item)

    def pageOne(self):
        inventorySlots, index = [], 0
        for i in range(200, 500, 42):
            for j in range(250, 600, 42):
                inventorySlots.append(self.scale_image(py.image.load("Assets/Book/emptyBox.png").convert_alpha(), 1.0))
                self.screen.blit(inventorySlots[index], (i, j))
                if index < len(self.items) and index > -1:
                    self.screen.blit(self.items[index])
    def pageTwo(self):
        pass