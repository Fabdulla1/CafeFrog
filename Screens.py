import pygame as py
from Customers import Customers
from Player import Player
from Inventory import Inventory
from Map import Map as world
import random
from Items import Items
from DialogueClassifier import DialogueClassifier

class Screens:
    @staticmethod
    def mainMenu():
        pass

    def spawnCustomers(self, probability, customersGroup, screen):
        roll = random.randint(1, 100)
        names = ["BIRD", "CAT", "FOX", "RACCOON"]
        def random_name():
            return random.choice(names)
        if roll <= probability:
            customersGroup.add(Customers(f"Assets/Customers/{random_name()}SPRITESHEET.png", screen))
   
    def cafeScreen(self):
        run = True
        screen = py.display.set_mode((1280, 720))
        tmClass = world("Assets/Map/CafeMap.tmx")
        cafe = tmClass.returnTM() #tilemap class
        screen_width, screen_height = 1280, 720  # Assume these are your screen dimensions
        map_width = cafe.tilewidth * cafe.width  # Total width of the map in pixels
        map_height = cafe.tileheight * cafe.height  # Total height of the map in pixels
        player = Player(image="Assets/Player/playerSprite.png", screen=screen)
        customerChatBot = DialogueClassifier()
        clock = py.time.Clock()
        FPS = 200
        spawn_timer = 0
        spawn_interval = 1000
        
        
        playerGroup = py.sprite.Group()
        customersGroup = py.sprite.Group()

        playerGroup.add(player)

        inventory = Inventory(screen)
        customer_prob = 50 #probability for spawning customers.
        #initialize all sprite groups. AKA list of all entities/objects for cafe
        drink = Items(image="Assets/Drinks/Beaver Brew.png", name="Beaver Brew", description="A luscious drink that's rich and bound to give you creativity", x=503, y=394, screen=screen)
        floor = py.sprite.Group()
        chairs = py.sprite.Group()
        tables = py.sprite.Group()
        tableLegs = py.sprite.Group()
        items = py.sprite.Group()
        items.add(drink)
        #Initialize cafe objects
        tmClass.initializeCafeObjects(cafe, floor, chairs, tables, tableLegs)
        inventory_open = False  # A flag to check if inventory is open

        # Define camera starting position
        camera_x, camera_y = 0, 0

        # Define screen boundaries for camera movement
        camera_dead_zone = {'left': 1280 // 4, 'right': 1280 // 4, 'top': 720 // 4, 'bottom': 720 // 4}
        py.font.init()
        #Temp function for mouse position. Helps with notifying location.
        def render_text(text, position, font_size=20, color=(255, 255, 255)):
            font = py.font.Font()  # Use Pygame's default font
            text_surface = font.render(text, True, color)  # True for anti-aliased text
            screen.blit(text_surface, position)

        while run:
            screen.fill((0, 0, 0))  # Clear the screen
            
            dt = clock.tick(FPS)

            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_i:
                        Screens.inventoryMenu(screen, inventory)
                    elif event.key == py.K_ESCAPE:
                        run = False
            
            keyArr = py.key.get_pressed()
            player.move(keyArr, [tables]) # This updates the player's position and frame of animation
            spawn_timer += dt  # Increment spawn timer by delta time
            if spawn_timer >= spawn_interval:
                spawn_timer %= spawn_interval  # Reset timer with remainder to stay accurate
                self.spawnCustomers(customer_prob, customersGroup, screen)
            for customer in customersGroup.sprites():
                customersGroup.remove(customer)
                customer.pathfinding(obstacles=[tables, playerGroup, customersGroup])
                customersGroup.add(customer)
            
            # Calculate player's position on the screen (without camera offset)
            player_screen_pos_x = player.dx + camera_x
            player_screen_pos_y = player.dy + camera_y

            # Adjust camera_x and camera_y based on player's position and the dead zone
            if player_screen_pos_x < camera_dead_zone['left']:
                camera_x += camera_dead_zone['left'] - player_screen_pos_x
            elif player_screen_pos_x > camera_dead_zone['right']:
                camera_x -= player_screen_pos_x - camera_dead_zone['right']

            if player_screen_pos_y < camera_dead_zone['top']:
                camera_y += camera_dead_zone['top'] - player_screen_pos_y
            elif player_screen_pos_y > camera_dead_zone['bottom']:
                camera_y -= player_screen_pos_y - camera_dead_zone['bottom']
            camera_x = min(0, max(-(map_width - screen_width), camera_x))  # Max camera_x is 0, min is -(mapWidth - screenWidth)
            camera_y = min(0, max(-(map_height - screen_height), camera_y))  # Max camera_y is 0, min is -(mapHeight - screenHeight)

            tmClass.drawCafe(screen=screen, camera_x=camera_x, camera_y=camera_y, floorGroup=floor, chairGroup=chairs, tableGroup=tables, tableLegs=tableLegs) # Draw the cafe with camera offset

            #Draw drinks
            for drink in items.sprites():
                drink.draw(camera_x, camera_y)
                if py.sprite.collide_mask(drink, player):
                    items.remove(drink)
                    drink = None
            # Draw the player and Customers with camera offset
            for customer in customersGroup.sprites():
                customer.draw(camera_x, camera_y)
                customer.updateDialog(player.rect)
            player.draw(camera_x, camera_y)

            #Helps with pixel locations with mouse
            mouse_x, mouse_y = py.mouse.get_pos()
            render_text(f"Mouse: {mouse_x}, {mouse_y}", (10, 10))
            py.display.update()
            clock.tick(60)

    def inventoryMenu(screen, inventory):
        # Clear the screen to show the pause menu
        screen.fill((0, 0, 0))  # Filling the screen with black or another color
        inventory.open()  # Display the inventory

        # Pause Menu loop
        paused = True
        while paused:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_i:
                        paused = False  # Close the pause menu
                    elif event.key == py.K_ESCAPE:
                        Screens.pauseMenu()
            inventory.draw_buttons()
            py.display.flip()
                        
            # Update only the necessary parts or wait to reduce CPU usage
            py.time.wait(100)

        # Clear the pause menu/inventory screen (optional, depending on desired behavior)
        inventory.close()  # Optionally close the inventory visually if needed
        screen.fill((0, 0, 0))  # Optionally clear the screen
    
    def pauseMenu(self, screen):
        #clear the screen for rendering
        screen.fill((0, 0, 0))


screens = Screens()
screens.cafeScreen()
