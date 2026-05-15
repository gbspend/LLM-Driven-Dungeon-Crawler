import pygame
import random
from consts import *

class Character():
    def __init__(self, name, description, max_hp, pos, sprites, dead_sprite):
        self.name = name
        self.description = description
        self.max_hp = max_hp
        self.hp = max_hp
        self.dead_sprite = dead_sprite
        self.dead = False
        
        self.last_hp = None #know when to update health panel below
        self.health_panel = None
        
        self.pos = pos
        self.face_right = True
        self.current_effects = []
        self.sprites = sprites
        self.i = 0
        self.t = BOB_TIME
        if self.sprites: #allows testing without sprites
            size = sprites[0].get_size()
            self.hi = pygame.Surface((size[0],size[1]-1))
            self.hi.fill((255,255,0))
        #move player up and down a little
        self.off = 0
        self.t = 15
        self.weapons = [
            ('Knife', 'A small dull knife.'),
            ('Longsword', 'A well-forged longsword.'),
            ('Dragon Slayer', 'A massive sword, magically empowered by slain dragons.'),
            ('Faithful', 'A longsword, blessed by the church. Especially powerful against the undead.')
        ]
        self.weapon_i = 1 #weapon index
        self.items = [
            ("Shimmering Potion", "A small flask of bright iridescent liquid."),
            ("Singed Scroll","A scroll covered in ancient runes; the edges are charred."),
            ("Evil Wand","A heavy black rod that pulses with malevolent intent."),
        ]
    
    def get_desc(self):
        desc = self.description + ", armed with " + self.weapons[self.weapon_i][1]
        if self.current_effects:
            desc = desc + (" with the current effects:",self.current_effects)
        return desc

    # player spawn location
    def spawn(self, tiles_list, collision_list):
        # looking for tiles without collision
        for tile in tiles_list:
            if tile[3] is False:
                collision_list.append(tile)
        spawn_index = random.randint(0, len(collision_list) - 1)
        spawn = (collision_list[spawn_index][1], collision_list[spawn_index][2])
        return spawn

    def move(self, dx, dy, pos, tiles, tile_size, enemies):
        # only take turn on successful movement
        turn = False
        # attack when moving into adjacent enemy
        attack = False
        dest = 0
        t_pos = (0, 0)
        flip_facing = False #don't update until below
        # direction check
        if dx == 1:
            dest = (pos[0] + tile_size, pos[1])
            if not self.face_right:
                flip_facing = True
        elif dx == -1:
            dest = (pos[0] - tile_size, pos[1])
            if self.face_right:
                flip_facing = True
        elif dy == 1:
            dest = (pos[0], pos[1] + tile_size)
        elif dy == -1:
            dest = (pos[0], pos[1] - tile_size)
        for enemy in enemies:
            # attack enemy
            if dest == enemy.pos:
                turn, attack = True, True
                return pos, turn, attack, dest
        for t in tiles:
            t_pos = (t[1], t[2])
            if dest == t_pos:
                if t[3] is True: #blocked movement
                    # Leaving turn alone on unsuccesful movement
                    return pos, turn, attack, dest
                else:
                    # Taking turn on succesful movement
                    turn = True
                    if flip_facing:
                        self.face_right = not self.face_right
                    return t_pos, turn, attack, dest
    
    def draw(self, screen):
        if self.dead:
            screen.blit(self.dead_sprite, self.pos)
            return
        #it's a little hacky to put the timer here, but it's OK for simple animation
        self.t -= 1
        if self.t <= 0:
            self.t = BOB_TIME
            self.i += 1
            if self.i >= len(self.sprites):
                self.i = 0
        screen.blit(self.hi,self.pos)
        sprite = self.sprites[self.i]
        if not self.face_right:
            sprite = pygame.transform.flip(sprite,True,False)
        screen.blit(sprite, (self.pos[0],self.pos[1]+self.off))
    
    import pygame

    def get_hp_panel(self):
        if self.health_panel is not None and self.last_hp == self.hp:
            return self.health_panel
        self.last_hp = self.hp
        WIDTH, HEIGHT = 304, 50
        self.health_panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # clamp
        self.hp = max(0, min(self.hp, self.max_hp))
        pct = self.hp / self.max_hp if self.max_hp > 0 else 0

        # panel
        self.health_panel.fill(BG)
        pygame.draw.rect(self.health_panel, PANEL, (2, 2, WIDTH-4, HEIGHT-4))
        pygame.draw.rect(self.health_panel, BORDER1, (1, 1, WIDTH-2, HEIGHT-2), 1)
        pygame.draw.rect(self.health_panel, BORDER2, (0, 0, WIDTH, HEIGHT), 1)

        # little corner "rivets"
        for x, y in [(4,4),(WIDTH-6,4),(4,HEIGHT-6),(WIDTH-6,HEIGHT-6)]:
            self.health_panel.set_at((x,y), BORDER1)

        # text
        font = pygame.font.Font("Book.ttf", 16)
        big_font = pygame.font.Font("Book.ttf", 19)
        label = font.render("Health", False, TEXT)
        label_pos = (12, 6)
        self.health_panel.blit(label, label_pos)

        # bar frame
        bx, by, bw, bh = 12, 28, 126, 14
        pygame.draw.rect(self.health_panel, BORDER2, (bx-1, by-1, bw+2, bh+2))
        pygame.draw.rect(self.health_panel, BAR_BG, (bx, by, bw, bh))

        # fill
        fill_w = int((bw-2) * pct)
        if fill_w > 0:
            pygame.draw.rect(self.health_panel, BAR_HP, (bx+1, by+1, fill_w, bh-2))
            pygame.draw.line(self.health_panel, BAR_HI,
                             (bx+1, by+1),
                             (bx+fill_w, by+1))
        
        if self.dead:
            dead_label = big_font.render("GAME OVER!", False, TEXT)
            dead_rect = dead_label.get_rect()
            right_rect = pygame.Rect((WIDTH//2, 0),(WIDTH//2-bx, HEIGHT))
            dead_rect.center = right_rect.center
            self.health_panel.blit(dead_label, dead_rect.topleft)
        
        return self.health_panel

class Enemy():
    def __init__(self, name, description, max_hp, hp, atk, pos, sprites):
        self.name = name
        self.description = description
        self.max_hp = max_hp
        self.hp = hp
        self.atk = atk # not used
        self.pos = pos
        self.face_right = True
        self.sprites = sprites
        self.i = 0
        self.t = BOB_TIME
        self.current_effects = []

    # enemy location list for combat
    def locations(self, enemies):
        locations = []
        for enemy in enemies:
            locations.append(enemy.pos)
        return locations

    def move_enemy(self, pos, tiles, tile_size, player_pos, enemies, turn):
        # attacking only if player is in correct position
        attack = False
        distance_x = abs(player_pos[0] - pos[0])
        distance_y = abs(player_pos[1] - pos[1])
        correct_facing = True
        if distance_y == 0:
            correct_facing = (player_pos[0] - pos[0] > 0 and self.face_right) or\
                (player_pos[0] - pos[0] < 0 and not self.face_right)
        if ((distance_x == tile_size and distance_y == 0) or (distance_y == tile_size and distance_x == 0)) and turn is True and correct_facing:
            attack = True
            return pos, attack
        # randomly picking direction
        direction = random.choice([0, 1])
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        if direction == 0:
            dy = 0
        else:
            dx = 0
        dest = 0
        t_pos = (0, 0)
        flip_facing = False #don't update until below
        # direction check
        if dx == 1:
            dest = (pos[0] + tile_size, pos[1])
            if not self.face_right:
                flip_facing = True
        elif dx == -1:
            dest = (pos[0] - tile_size, pos[1])
            if self.face_right:
                flip_facing = True
        elif dy == 1:
            dest = (pos[0], pos[1] + tile_size)
        elif dy == -1:
            dest = (pos[0], pos[1] - tile_size)
        for t in tiles:
            t_pos = (t[1], t[2])
            # if colliding with another enemy, don't move
            for enemy in enemies:
                if dest == enemy.pos:
                    return pos, attack
            if dest == t_pos:
                if t[3] is True:
                    # Unsuccesful move
                    return pos, attack
                else:
                    # Succesful move
                    if flip_facing:
                        self.face_right = not self.face_right
                    return t_pos, attack
                    
    def get_rect(self):
        return self.sprites[0].get_rect(topleft=self.pos)
    
    def draw(self, screen):
        self.t -= 1
        if self.t <= 0:
            self.t = BOB_TIME
            self.i += 1
            if self.i >= len(self.sprites):
                self.i = 0
        sprite = self.sprites[self.i]
        if not self.face_right:
            sprite = pygame.transform.flip(sprite,True,False)
        screen.blit(sprite, self.pos)

    def get_desc(self):
        desc = self.description
        if self.current_effects:
            desc = desc + (" with the current effects:",self.current_effects)
        return desc