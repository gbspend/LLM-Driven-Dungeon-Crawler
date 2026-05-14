import pygame

class Spritesheet():
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        # Black color key, properly renders transparent images
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        return sprite
    
    def get_sprite_pair(self, x, y, w, h):
        return self.get_sprite(x,y-32,w,h),self.get_sprite(x,y,w,h)
    
    def get_sprite_rc(self,r,c,w,h):
        return self.get_sprite(c*w,r*h,w,h)