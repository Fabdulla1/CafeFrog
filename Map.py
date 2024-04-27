import pygame as py
import pytmx as pyt
from pytmx.util_pygame import load_pygame
from Tables import Tables, TableLegs
from Chairs import Chairs
from Floor import Floor

class Map:
    def __init__(self, filename):
        self.tm = load_pygame(filename)
        self.initialized = False

    def returnTM(self): 
        return self.tm #Returns the entire tilemap
    
    #Draws the map, layer by layer. Does not consider different types.
    def initializeCafeObjects(self, tilemap, floorGroup, chairGroup, tableGroup, tableLegs):
        for layer in tilemap.visible_layers:
            if isinstance(layer, pyt.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tilemap.get_tile_image_by_gid(gid)
                    if tile:
                        # Scale the tile image based on the tile size specified in Tiled
                        tile_size = (tilemap.tilewidth, tilemap.tileheight)  # Assuming you want the original tile size
                        tile = py.transform.scale(tile, tile_size)
                        
                        # Convert tile positions (in tile units) to pixel positions sicne Tiled layer returns different units and pygame process in pixels.
                        pixel_x = x * tilemap.tilewidth
                        pixel_y = y * tilemap.tileheight
                        
                        floorGroup.add(Floor(tile, pixel_x, pixel_y, tilemap.tilewidth, tilemap.tileheight))

            elif isinstance(layer, pyt.TiledObjectGroup):
                for obj in layer:
                    if obj.gid:  
                        tile = tilemap.get_tile_image_by_gid(obj.gid)
                        if tile:
                            obj_width, obj_height = int(obj.width), int(obj.height)  # Ensure these are integers
                            tile = py.transform.scale(tile, (obj_width, obj_height))
                            if layer.name == "tables":
                                tableGroup.add(Tables(image=tile, x=int(obj.x), y=int(obj.y), width=obj_width, height=obj_height))
                            elif layer.name == "chairs":
                                chairGroup.add(Chairs(tile, int(obj.x), int(obj.y)))  # Ensure coordinates are integers
                            elif layer.name == "tableLegs":
                                tableLegs.add(TableLegs(tile, int(obj.x), int(obj.y)))
                                
        self.initialized = True

    def drawCafe(self, screen, chairGroup, tableGroup, floorGroup, camera_x, camera_y, tableLegs):
        # Draw floor tiles
        for sprite in floorGroup.sprites():
            screen.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))

        # Draw tables
        for sprite in tableGroup.sprites():
            screen.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))
            
        # Draw chairs
        for sprite in chairGroup.sprites():
            screen.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))

        # Draw table legs
        for sprite in tableLegs.sprites():
            screen.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))