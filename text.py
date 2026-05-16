import pygame
from math import floor
from consts import *

#HELPERS

#converts string "msg" into list of strings with max width
def fit_line_in_width(msg, width, font, color=(255,255,255)):
    ret = []
    prev = ""
    for part in msg.split(" "):
        curr = (prev + " " + part) if prev else part
        curr_render = font.render(curr, True, color)
        if curr_render.get_size()[0] > width:
            ret.append(prev)
            prev = part
        else:
            prev = curr
    if prev:
        ret.append(prev)
    return ret

#surf is modified directly
#lines is list of separate lines of text
#   ^ NOT RESIZED, use fit_line_in_width first
#draws from top down; truncates lines that won't fit
def draw_text_on_surf(surf, lines, font, center=False, color=(255,255,255)):
    x_delta, y_delta = font.size("M")
    width = surf.get_width()
    height = surf.get_height()
    
    sub_h = min(height, len(lines) * y_delta)
    sub_surf = pygame.Surface((width, sub_h), flags=pygame.SRCALPHA)
    off_y = 0
    for s in lines:
        rendered_text = font.render(s, True, color)
        sub_surf.blit(rendered_text, (0,off_y))
        off_y += y_delta
        if off_y >= sub_h:
            break
    sub_x = sub_y = 0
    if center:
        sub_x = (surf.get_width() - sub_surf.get_width())//2
        sub_y = (surf.get_height() - sub_surf.get_height())//2
    surf.blit(sub_surf, (sub_x, sub_y))

class TextBox:
    def __init__(self, font, text_rect, text_color, bg_color, pos=None, center=False):
        self.clear()
        self.font = font
        self.x_delta, self.y_delta = font.size("M")
        self.center = center
        self.last_y = None #how far up the Surface the text ended up
        self.update_rect(text_rect)
        self.text_color = text_color
        self.bg_color = bg_color
        self.pos = pos

    def update_rect(self, text_rect):
        self.rect = text_rect
        self.size = text_rect.size
        self.surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        
    def clear(self):
        self.text = []
        self.changed = True
    
    def add(self, msg):
        self.changed = True
        self.text += fit_line_in_width(msg, self.size[0], self.font, self.text_color) + [" "]

    def resize_to_text(self):
        self.changed = True
        new_height = (len(self.text) * self.y_delta) + 1
        new_rect = pygame.Rect(0,0,self.size[0], new_height)
        self.update_rect(new_rect)
        
    def render(self, screen, force_pos = None):
        if self.changed:
            #re-render
            self.surface.fill(self.bg_color)
            text_y = self.size[1]
            text_y -= self.y_delta
            text_index = len(self.text) - 1
            while text_index >= 0:
                rendered_text = self.font.render(self.text[text_index], True, self.text_color)
                self.surface.blit(rendered_text, (0, text_y))
                text_y -= self.y_delta
                text_index -= 1
                if text_y <= 0:
                    break
            self.last_y = text_y
            self.changed = False
            if self.center and self.last_y > 0:
                surf_size = self.surface.get_size()
                temp = pygame.Surface(surf_size)
                temp.fill(self.bg_color)
                area = pygame.Rect(0,self.last_y,self.size[0],self.size[1]-self.last_y)
                t_rect = area.copy()
                t_rect.center = self.surface.get_rect().center
                temp.blit(self.surface,t_rect.topleft,area)
                self.surface = temp
        if force_pos:
            screen.blit(self.surface, force_pos)
        else:
            assert self.pos is not None, "no textbox pos given in init or render"
            screen.blit(self.surface, self.pos)
            
#title in string, entries is list of (name, desc) tuples
#returns two things:
#   1. rendered Surface (with given width and height)
#   2. ordered list of Rects corresponding to "entries" index
#       truncated to # of entries that fit on surf
def render_list(title, entries, width, height, inv_font, title_font):
    x_in = y_in = 10
    surf = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    title_surf = title_font.render(title, True, (255,255,255))
    surf.blit(title_surf, (x_in, y_in))
    y_off = title_surf.get_height() + y_in
    
    x_delta, y_delta = inv_font.size("M")
    rect_h = y_delta*3
    rect_w = width - (x_in*2)
    ret_rects = []
    for name, desc in entries:
        sub_surf = pygame.Surface((rect_w, rect_h), flags=pygame.SRCALPHA)
        text = fit_line_in_width(desc, rect_w, inv_font)
        lines = [name] + text
        draw_text_on_surf(sub_surf, lines, inv_font)
        top_left = (x_in, y_off)
        surf.blit(sub_surf, top_left)
        ret_rects.append(sub_surf.get_rect(topleft=top_left))
        y_off += rect_h
        if y_off >= height:
            break
        
    return surf, ret_rects

class Inventory:
    def __init__(self, screen_w, screen_h, font, title_font):
        self.font = font
        self.title_font = title_font
        s = 0.9
        box_w, box_h = floor(screen_w * s), floor(screen_h * s)
        self.surf = pygame.Surface((box_w, box_h))
        self.topleft = ((screen_w - box_w)//2, (screen_h - box_h)//2)
        self.sel_rect = None #rectangle to draw border around for current selection
        self.equip_rects = []
        self.item_rects = []
    
    #prepare static inv screen
    #   call once when game state switches to INV
    def prep(self, player):
        self.sel_rect = None
        self.surf.fill((0,0,0))
        surf_w = self.surf.get_width()
        surf_h = self.surf.get_height()
        border_rect = (0,0,surf_w-1,surf_h-1)
        pygame.draw.rect(self.surf, (255,255,255), border_rect, width=1)
        
        half_w = (surf_w-1)//2
        left_rect = (0,0,half_w,surf_h-1)
        pygame.draw.rect(self.surf, (255,255,255), left_rect, width=1)
        
        e_surf, self.equip_rects = render_list(
            "Equipment", player.weapons, half_w, surf_h, self.font, self.title_font)
        
        eq_rect = self.equip_rects[player.weapon_i]
        self.equip_rects[player.weapon_i] = None
        pygame.draw.rect(e_surf, (0,255,255), eq_rect, width=1)
        
        i_surf, self.item_rects = render_list(
            "Items", player.items, half_w, surf_h, self.font, self.title_font)
        #offset to right
        for r in self.item_rects:
            r.move_ip(half_w, 0)
        
        self.surf.blit(e_surf,(0,0))
        self.surf.blit(i_surf,(half_w,0))            
    
    #returns tuple:(bool, index)
    #   bool is True for equipment, False for item
    #   index is into player.weapons or player.items that mouse is over
    def update(self, raw_mouse):
        self.sel_rect = None
        #offset mouse from abs screen pos
        off_x, off_y = self.topleft
        mouse_pos = (raw_mouse[0] - off_x, raw_mouse[1] - off_y)
        found = False
        ret_i = None
        
        #check left (weapons)
        isWeap = True
        for i,r in enumerate(self.equip_rects):
            if r is not None and r.collidepoint(mouse_pos):
                found = True
                self.sel_rect = r.copy()
                ret_i = i
                break
        
        #check right (items) if necessary
        if not found:
            isWeap = False
            for i,r in enumerate(self.item_rects):
                if r.collidepoint(mouse_pos):
                    found = True
                    self.sel_rect = r.copy()
                    ret_i = i
                    break
        if found:
            #un-offset rect
            self.sel_rect.move_ip(off_x,off_y)
            return isWeap, ret_i
        else:
            return None, None
        
    def draw(self, screen):
        screen.blit(self.surf, self.topleft)
        if self.sel_rect:
            pygame.draw.rect(screen, (255,255,255), self.sel_rect, width=1)