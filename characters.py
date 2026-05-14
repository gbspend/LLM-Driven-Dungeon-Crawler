import pygame
import random

class Character():
    def __init__(self, name, description, max_hp, hp, atk, pos, sprite):
        self.name = name
        self.description = description
        self.max_hp = max_hp
        self.hp = hp
        self.atk = atk # not used
        self.pos = pos
        self.current_effects = []
        if sprite:
            temp = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            temp.fill((255,255,0))
            temp.blit(sprite, (0,0))
            self.sprite = temp
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
        # direction check
        if dx == 1:
            dest = (pos[0] + tile_size, pos[1])
        elif dx == -1:
            dest = (pos[0] - tile_size, pos[1])
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
                if t[3] is True:
                    # Leaving turn alone on unsuccesful movement
                    return pos, turn, attack, dest
                else:
                    # Taking turn on succesful movement
                    turn = True
                    return t_pos, turn, attack, dest
    
    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

class Enemy():
    def __init__(self, name, description, max_hp, hp, atk, pos, sprite):
        self.name = name
        self.description = description
        self.max_hp = max_hp
        self.hp = hp
        self.atk = atk # not used
        self.pos = pos
        self.sprite = sprite
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
        if ((distance_x == tile_size and distance_y == 0) or (distance_y == tile_size and distance_x == 0)) and turn is True:
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
        # direction check
        if dx == 1:
            dest = (pos[0] + tile_size, pos[1])
        elif dx == -1:
            dest = (pos[0] - tile_size, pos[1])
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
                    return t_pos, attack
                    
    def get_rect(self):
        return self.sprite.get_rect(topleft=self.pos)
    
    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    def get_desc(self):
        desc = self.description
        if self.current_effects:
            desc = desc + (" with the current effects:",self.current_effects)
        return desc