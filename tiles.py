import pygame, csv, os, random
from spritesheet import Spritesheet
from consts import *

class Object:
    def __init__(self,anims,x,y):
        self.anims = anims
        self.pos = (x,y)
        self.f = 0
        self.reset_t()
    
    def reset_t(self):
        self.t = random.randint(5,9)
    
    def update(self):
        self.t -= 1
        if self.t <= 0:
            self.reset_t()
            self.f = random.randint(0,len(self.anims)-1)
    
    def draw(self, screen):
        rad = 18+self.f
        side = rad*2 + 1
        light = pygame.Surface((side,side),pygame.SRCALPHA)
        l_rect = light.get_rect()
        pygame.draw.circle(light,(255,213,105),l_rect.center,rad)
        light.set_alpha(32)
        x,y = self.pos
        l_rect.center = x + TILE_SIZE//2, y+6
        screen.blit(light,l_rect.topleft)
        screen.blit(self.anims[self.f],self.pos)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

def read_csv(filename):
    grid = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            grid.append(list(row))
    return grid

#turns sequential numbering of tileset tiles into their x,y position
def seq2XY(i):
    x = (i % 10) * TILE_SIZE
    y = (int(i / 10)) * TILE_SIZE
    return x,y

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
    
    def update(self):
        for o in self.objs:
            o.update()
    
    def draw(self,screen):
        screen.blit(self.bg,(0,0))
        for o in self.objs:
            o.draw(screen)
        screen.blit(self.roof,(0,0))

    def load_tiles(self, filename, spritesheet):
        # CURRENTLY ONLY PROPERLY STORING FIRST ROW OF TILES
        self.tiles = []
        decos = []
        self.objs = []
        self.max_x = 0
        self.max_y = 0
        grid = read_csv(filename)
        objs = read_csv("objs2.csv")
        fire = Spritesheet("fire.png")
        obj_anims = {}
        obj_anims["T"] = [fire.get_sprite_rc(3,c,TILE_SIZE,TILE_SIZE) for c in range(4)]
        obj_anims["C"] = [fire.get_sprite_rc(1,c,TILE_SIZE,TILE_SIZE) for c in range(1,4)]
        x, y, = 0, 0
        # WIP collision tile list
        # Currently includes all standard wall tiles
        collision_list = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 78]
        for r in range(len(grid)):
            row = grid[r]
            x = 0
            for c in range(len(row)):
                tile = row[c]
                # Changing tile ID from string to int
                tile = int(tile)
                # Checking row
                #multiplier = int(tile/10)
                # picking out x and y coordinates of tile on tileset
                tile_x,tile_y = seq2XY(tile)
                # designating the tile's location on screen
                screen_x = x * TILE_SIZE
                screen_y = y * TILE_SIZE
                if screen_x > self.max_x:
                    self.max_x = screen_x
                if screen_y > self.max_y:
                    self.max_y = screen_y
                # for index in collision, if tile == index, prevent movement (unimplemented)
                collision = tile in collision_list
                
                #check for object
                if r < len(objs) and c < len(objs[r]) and objs[r][c]:
                    entry = objs[r][c]
                    try:
                        i = int(entry)
                        decos.append((i,screen_x,screen_y))
                    except ValueError:
                        #non-numeric obj entry means animated object
                        collision = True
                        self.objs.append(Object(obj_anims[entry],screen_x,screen_y))
                
                # tuple of sprite, x coordinate, y coordinate, and whether the sprite has collision
                new_tile = (spritesheet.get_sprite(tile_x, tile_y, TILE_SIZE, TILE_SIZE), screen_x, screen_y, collision)
                self.tiles.append(new_tile)
                # next tile in current row
                x += 1
            # next row
            y += 1
        self.max_x += TILE_SIZE
        self.max_y += TILE_SIZE
        
        roof_color = (33,17,23)
        self.bg = pygame.Surface((self.max_x, self.max_y))
        self.bg.fill(roof_color)
        
        for tile in self.tiles:
            self.bg.blit(tile[0], (tile[1], tile[2]))
        for i,x,y in decos:
            tile_x,tile_y = seq2XY(i)
            surf = spritesheet.get_sprite(tile_x, tile_y, TILE_SIZE, TILE_SIZE)
            self.bg.blit(surf,(x,y))
        #just for fun :)
        carpet_surf = pygame.image.load("carpet2.png").convert_alpha()
        carpet_surf.set_alpha(150)
        self.bg.blit(carpet_surf,(160-16-(16*3),160+(16*3)+8))
            
        roof_mask = pygame.mask.from_threshold(self.bg, roof_color,(1, 1, 1, 255))
        self.roof = roof_mask.to_surface(setcolor=roof_color,unsetcolor=None)
    
    def get_tiles(self):
        return self.tiles, self.max_x, self.max_y

