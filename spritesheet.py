import pygame
from consts import TILE_SIZE

class Spritesheet:
    def __init__(self, filename, w=TILE_SIZE, h=TILE_SIZE):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.w = w
        self.h = h

    def get_sprite(self, x, y):
        sprite = pygame.Surface((self.w, self.h))
        # Black color key, properly renders transparent images
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0), (x, y, self.w, self.h))
        return sprite
    
    def get_sprite_pair(self, x, y):
        return self.get_sprite(x,y-32),self.get_sprite(x,y)
    
    def get_sprite_rc(self,r,c):
        return self.get_sprite(c*self.w,r*self.h)