import pygame, csv, os
from spritesheet import Spritesheet
from consts import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.start_x, self.start_y = 0, 0
        self.load_tiles(filename,spritesheet)
        # width of entire game map and height of entire game map
        #self.map_surface = pygame.Surface((self.map_w, self.map_h))
        #self.map_surface.set_colorkey((0,0,0))

    def draw_map(self, surface):
        surface.blit(self.map_surface, (self.start_x, self.start_y))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename, spritesheet):
        # CURRENTLY ONLY PROPERLY STORING FIRST ROW OF TILES
        self.tiles = []
        self.max_x = 0
        self.max_y = 0
        map = self.read_csv(filename)
        x, y, = 0, 0
        # WIP collision tile list
        # Currently includes all standard wall tiles
        collision_list = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 78]
        for row in map:
            x = 0
            for tile in row:
                # Changing tile ID from string to int
                tile = int(tile)
                # Checking row
                #multiplier = int(tile/10)
                # picking out x and y coordinates of tile on tileset
                tile_x = (tile % 10) * TILE_SIZE
                tile_y = (int(tile / 10)) * TILE_SIZE
                # designating the tile's location on screen
                screen_x = x * TILE_SIZE
                screen_y = y * TILE_SIZE
                if screen_x > self.max_x:
                    self.max_x = screen_x
                if screen_y > self.max_y:
                    self.max_y = screen_y
                # for index in collision, if tile == index, prevent movement (unimplemented)
                collision = tile in collision_list
                # tuple of sprite, x coordinate, y coordinate, and whether the sprite has collision
                new_tile = (spritesheet.get_sprite(tile_x, tile_y, TILE_SIZE, TILE_SIZE), screen_x, screen_y, collision)
                self.tiles.append(new_tile)
                # next tile in current row
                x += 1
            # next row
            y += 1
        self.max_x += TILE_SIZE
        self.max_y += TILE_SIZE
    
    def get_tiles(self):
        return self.tiles, self.max_x, self.max_y

    # Check 7:00 of tilemap tutorial for alternate load_tiles function
