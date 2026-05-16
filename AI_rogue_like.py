import pygame
import random
import api_call
from consts import *
from spritesheet import Spritesheet
from characters import Character, Enemy
from tiles import TileMap
from text import TextBox, Inventory
from enum import Enum
#from fight import FightPanel

class GameState(Enum):
    RUN = 1
    INV = 2
    GAMEOVER = 3

def parse_damage(combat, verb=True):
    # retrieving damage dealt and received values from API
    if verb: print(f"Parsing {combat}")
    damages = combat.split("DEALT: ")[1]
    split_damages = damages.split(", ")
    dealt = split_damages[0]
    rec_tuple = split_damages[1].split(" ")
    received = rec_tuple[1]
    return dealt, received

def hp_state(player, enemy):
    # helper function governing HP state of player and enemy
    if player.hp < int(0.7 * player.max_hp) and player.hp > int(0.3 * player.max_hp):
        pState = "WOUNDED"
    elif player.hp < int(0.3 * player.max_hp):
        pState = "MAIMED"
    else:
        pState = "HEALTHY"
    if enemy.hp < int(0.7 * enemy.max_hp) and enemy.hp > int(0.3 * enemy.max_hp):
        eState = "WOUNDED"
    elif enemy.hp < int(0.3 * enemy.max_hp):
        eState = "MAIMED"
    else:
        eState = "HEALTHY"
    return pState, eState

class rogue_like:
    # simple class to eliminate need for globals
    def __init__(self, enemies, player, textBox, default_pos, fair_distance, collision_list, re_sprites, playerAggress = False):
        self.enemies = enemies
        self.player = player
        self.textBox = textBox
        self.default_pos = default_pos
        self.fair_distance = fair_distance
        self.collision_list = collision_list
        self.re_sprites = re_sprites
        self.playerAggress = False
        self.dropchance = 0

    def spawn_enemy(self, enemy, fair_distance, collision_list):
        # while an enemy has not been spawned
        while True:
            # generate random spawn point
            enemy_spawn_index = random.randint(0, len(collision_list) - 1)
            enemy_spawn = (collision_list[enemy_spawn_index][1], collision_list[enemy_spawn_index][2])
            # check spawn distance, if too close to player, generate again
            spawn_distance = (abs(spawn[0] - enemy_spawn[0]), abs(spawn[1] - enemy_spawn[1]))
            if spawn_distance[0] >= fair_distance or spawn_distance[1] >= fair_distance:
                enemy.pos = enemy_spawn
                self.enemies.append(enemy)
                return

    def combat_handler(self, combat_enemy, instructions):
        self.textBox.add(instructions.split(" DEALT: ")[0])
        # parsing combat damage instructions
        dealt, received = parse_damage(instructions)
        # providing damage value based on API instruction
        if dealt == "FATAL":
            dmg = combat_enemy.max_hp
        elif dealt == "HIGH":
            dmg = int(combat_enemy.max_hp * 0.7)
        elif dealt == "MEDIUM":
            dmg = int(combat_enemy.max_hp * 0.4)
        elif dealt == "LOW":
            dmg = int(combat_enemy.max_hp * 0.2)
        # dealt == "NONE"
        else:
            dmg = 0
        # providing damage received value based on API instruction
        if received == "FATAL":
            rec = self.player.max_hp
        elif received == "HIGH":
            rec = int(self.player.max_hp * 0.7)
        elif received == "MEDIUM":
            rec = int(self.player.max_hp * 0.4)
        elif received == "LOW":
            rec = int(self.player.max_hp * 0.2)
        # received == "NONE"
        else:
            rec = 0
        combat_enemy.hp -= dmg
        self.player.hp -= rec
        if dealt != "NONE":
            print(f'You attacked the {combat_enemy.name} for {dmg} damage.')
        else:
            print(f'You missed the {combat_enemy.name}.')
        if combat_enemy.hp > 0:
            print(f'It has {combat_enemy.hp} HP remaining.')
        if rec != "NONE":
            print(f'You received {rec} damage.')
        else:
            print(f'You avoided the {combat_enemy.name}\'s attack.')
        if self.player.hp > 0:
            print(f'You have {self.player.hp} HP remaining.')
        if combat_enemy.hp <= 0:
            print(f'You defeated the {combat_enemy.name}.')
            self.enemies.remove(combat_enemy)
            return True

        return False
    
    def item_spawn(self,enemy):
        new_item, new_item_Type = api_call.gen_item(enemy,self.player,self.dropchance)
        if new_item != "N":
            textBox.add("you got a new " + new_item_Type)
            textBox.add(new_item[0])
            textBox.add(new_item[1])
            self.dropchance =0
        else:
            self.dropchance += 1

    def state_update(self, order):
        if player.hp <= 0: #avoids processing reinforcements after game over
            return
        # order is tuple with parameters: action, target, amount
        # Skip turn
        if order == "SKIP" or order[0] == "ITEM":
            if order[0] == "ITEM":
                item = player.items.pop(order[1]) #TODO
                print("USE ITEM:",item)
            turn = True
            self.playerAggress = False
            self.state_update(("MOVE", enemies, turn))
        # Movement
        if order[0] == "MOVE":
            # Player movement
            if order[1] == player:
                player.pos, turn, player_attack, attack_pos = player.move(*order[2], player.pos, tiles_list, tile_size, enemies)
                # Calling state update to attack an enemy
                if player_attack is True:
                    self.state_update(("ATK", player, attack_pos))
                else:
                    #TODO: pick up items on that square
                    self.playerAggress = False
                # Calling state update to move enemies
                self.state_update(("MOVE", enemies, turn))
            # Enemy movement
            if order[1] == enemies:
                # If turn is true, move
                if order[2] is True:
                    for enemy in enemies:
                        enemy.pos, enemy_attack = enemy.move_enemy(enemy.pos, tiles_list, tile_size, player.pos, enemies, order[2])
                        # Allowing certain enemies to cover multiple spaces
                        if enemy in fast_enemy and enemy_attack is False:
                            enemy.pos, enemy_attack = enemy.move_enemy(enemy.pos, tiles_list, tile_size, player.pos, enemies, order[2])
                        # Enemy attacking player
                        if enemy_attack is True and self.playerAggress is False:
                            # Only attacking if the player hasn't attacked previously, preventing doubled combat scenarios
                            pState, eState = hp_state(player, enemy)
                            instructions = api_call.combat_state_update_enemy(player, enemy, pState, eState)
                            if enemy == necro or enemy == necro_greater or enemy == goblin:
                                # Providing enemy spawn instructions and calling necro state update
                                enemy_number = api_call.enemy_summon_count(instructions)
                                enemy_number = int(enemy_number.split("Enemies: ")[1])
                                if enemy_number != 0:
                                    e1, e2, e3 = api_call.enemy_generator(instructions, enemy_number, self.re_sprites) # this will crash the game (missing parameter)
                                    self.state_update(("NECRO", e1, e2, e3))
                            # Bias towards player seems to be present in scenarios where the enemy attacks first.
                            # Experiment with prompt.
                            # Throw away prompt output if inadequate
                            EnemyDie = self.combat_handler(enemy, instructions)
                            if EnemyDie:
                                # TODO
                                self.item_spawn(enemy)

        elif order[0] == "ATK":
            # Rename attack command?
                if order[1] == player:
                    for enemy in enemies:
                        # Check position of each enemy to see which one you attack
                        if enemy.pos == order[2]:
                            # Calling API for combat
                            pState, eState = hp_state(player, enemy)
                            if enemy == necro or enemy == necro_greater or enemy == goblin:
                                # Providing enemy spawn instructions and calling necro state update
                                instructions = api_call.combat_state_update_necro(player, enemy, pState, eState)
                                enemy_number = api_call.enemy_summon_count(instructions)
                                enemy_number = int(enemy_number.split("Enemies: ")[1])
                                if enemy_number != 0:
                                    e1, e2, e3 = api_call.enemy_generator(instructions, enemy_number, self.re_sprites)
                                    self.state_update(("NECRO", e1, e2, e3))
                            else:
                                instructions = api_call.combat_state_update_alt(player, enemy, pState, eState)
                            # Throw away prompt output if inadequate
                            # printing combat description
                            EnemyDie = self.combat_handler(enemy, instructions)
                            if EnemyDie:
                                # TODO
                                self.item_spawn(enemy)

                            self.playerAggress = True

        # Necromancer enemy spawn state
        elif order[0] == "NECRO":
            # Spawning reinforcement enemy
            temp_enemy = Enemy(order[1][0], order[1][1], 10, 10, 2, default_pos, order[1][2])
            #print(temp_enemy.name, temp_enemy.description)
            self.spawn_enemy(temp_enemy, self.fair_distance, self.collision_list)
            if order[2] != 0:
                # Spawning second enemy if eligible
                temp_enemy = Enemy(order[2][0], order[2][1], 10, 10, 2, default_pos, order[2][2])
                #print(temp_enemy.name, temp_enemy.description)
                self.spawn_enemy(temp_enemy, self.fair_distance, self.collision_list)
                if order[3] != 0:
                    # Spawning third enemy if eligible, only checking if second enemy was present
                    temp_enemy = Enemy(order[3][0], order[3][1], 10, 10, 2, default_pos, order[3][2])
                    #print(temp_enemy.name, temp_enemy.description)
                    self.spawn_enemy(temp_enemy, self.fair_distance, self.collision_list)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # variable to quickly change for differently sized tiles
    tile_size = 16

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Roguelike")

    # Text setup
    base_font = pygame.font.Font("Book.ttf", 17)
    text_font = pygame.font.Font("Book.ttf", 18)
    title_font = pygame.font.Font("Book.ttf", 20)
    
    text_pos = (SCREEN_WIDTH - TEXT_WIDTH - 15, 0)
    textBox = TextBox(text_font,pygame.Rect(0,0, TEXT_WIDTH, SCREEN_HEIGHT), WHITE, BLACK, text_pos)

    # Spritesheet
    tile_spritesheet = Spritesheet('Dungeon_Tileset.png')
    char_spritesheet = Spritesheet('Dungeon_character.png')

    # Loading map tile
    tilemap = TileMap('test_tile2.csv', tile_spritesheet, 'objs2.csv')
    tiles_list,map_width,map_height = tilemap.get_tiles()
    
    collision_list = []
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    turn = False

    # 16x16 sprites: adjust each coordinate by 16 to swap sprite
    default_pos = (0, 0)
    knight_1 = char_spritesheet.get_sprite_pair(0,32)
    knight_e = char_spritesheet.get_sprite_pair(80,32)
    skel_g = char_spritesheet.get_sprite_pair(64,48)
    skel_r = char_spritesheet.get_sprite_pair(96,48)
    necro_l = char_spritesheet.get_sprite_pair(32,48)
    necro_g = char_spritesheet.get_sprite_pair(48,48)
    spirit_g = char_spritesheet.get_sprite_pair(16,48)
    # sprite list for random enemy spawns
    sprites = {"Knight": knight_e, "Spirit": spirit_g, "Vampire": necro_l, "Knife Skeleton": skel_g, "Scythe Skeleton": skel_r}


    dead_sprite = tile_spritesheet.get_sprite_rc(9,6)
    knight = Character('Knight', 'A knight', 25, default_pos, knight_1, dead_sprite)
    skel_knife = Enemy('Skeleton Grunt', 'A weak skeleton, armed with a knife.',10, 10, 2, default_pos, skel_g)
    skel_knife2 = Enemy('Skeleton Grunt', 'A weak skeleton, armed with a knife.',10, 10, 2, default_pos, skel_g)
    skel_scy = Enemy('Reaper', 'The skeleton of a strong warrior, armed with a scythe.', 15, 15, 4, default_pos, skel_r)
    necro = Enemy('Necromancer', 'A necromancer. Weak on its own, but capable of calling more undead to aid it.', 12, 12, 3, default_pos, necro_l)
    necro_greater = Enemy('Greater Necromancer', 'A powerful necromancer, skilled in offensive magic and capable of calling undead to aid it.', 16, 16, 4, default_pos, necro_g)
    spirit_greater = Enemy('Spirit', 'A spirit summoned to aid a necromancer.', 1, 1, 7, default_pos, spirit_g)
    spirit_greater2 = Enemy('Spirit', 'A spirit summoned to aid a necromancer.', 1, 1, 7, default_pos, spirit_g)
    spirit_greater3 = Enemy('Spirit', 'A spirit summoned to aid a necromancer.', 1, 1, 7, default_pos, spirit_g)
    goblin = Enemy('Goblin', 'A goblin warrior. Individually weak, but capable of calling for reinforcements.', 10, 10, 2, default_pos, knight_e)
    enemies = []
    fair_distance = 32
    player = knight
    state = ()

    n_reinforcements = [(skel_knife.name, skel_knife.description), (skel_scy.name, skel_scy.description)]

    roguelike = rogue_like(enemies, player, textBox, default_pos, fair_distance, collision_list, sprites)

    tooltip = TextBox(base_font, pygame.Rect(0,0,TIP_WIDTH,TIP_HEIGHT), WHITE, BLACK)
    last_enemy = None
    
    #TEST
    sk = pygame.transform.flip(skel_g[0],True,False)
    fight_panel = None#FightPanel(knight_1[0], sk, (FIGHT_W,FIGHT_H),FIGHT_POS,base_font)

    # Game loop
    running = True
    # Giving player spawn location
    spawn = player.spawn(tiles_list, collision_list)
    player.pos = spawn
    attack_pos = (0, 0)

    # enemy spawn
    spirit_count = 0
    fast_enemy = [spirit_greater]
    # enemy spawn batches
    all_batch = [skel_knife, skel_scy, necro, necro_greater, spirit_greater]
    easy_batch = [skel_knife, skel_knife2]
    medium_batch = [skel_knife, skel_scy, spirit_greater]
    necro = [necro, necro_greater, goblin]
    batch = necro
    for enemy in batch:
        roguelike.spawn_enemy(enemy, fair_distance, collision_list)
        
    state = GameState.RUN
    shade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    shade_surf.fill((0, 0, 0))
    shade_surf.set_alpha(160)
    inv = Inventory(SCREEN_WIDTH, SCREEN_HEIGHT, base_font, title_font)

    while running:
        if player.hp <= 0:
            player.dead = True
            state = GameState.GAMEOVER
        
        #--INPUT----------------------------------------
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if state == GameState.RUN:
                        state = GameState.INV
                        inv.prep(player)
                    elif state == GameState.INV:
                        state = GameState.RUN
                
                if state == GameState.RUN:
                    # Cardinal direction movement
                    if event.key == pygame.K_w:
                        # state = ("MOVE", player, direction)
                        roguelike.state_update(("MOVE", player, up))
                    elif event.key == pygame.K_a:
                        roguelike.state_update(("MOVE", player, left))
                    elif event.key == pygame.K_s:
                        roguelike.state_update(("MOVE", player, down))
                    elif event.key == pygame.K_d:
                        roguelike.state_update(("MOVE", player, right))
                    # Skip turn
                    elif event.key == pygame.K_SPACE:
                        roguelike.state_update("SKIP")
                        
                    #-- TEMP ----------------------------------
                    elif event.key == pygame.K_l:
                        textBox.add("asdkfjhaslkdfj asjlkdfh lkajsdhf lkjashdf kjahsdf jkashdf kj hasd flkj hasdflkjh aslkdjfh alksjf asdf")
                    elif event.key == pygame.K_k and fight_panel:
                        print("FP STOP")
                        fight_panel.stop = True
                    #------------------------------------------
        
        mouse_pos = pygame.mouse.get_pos()
        game_mouse_pos = [v//GAME_SCALE for v in mouse_pos]
        
        #--RENDER & UPDATE------------------------------
        tilemap.update()
        
        if fight_panel:
            fight_panel.update()
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Render text to screen
        textBox.render(screen)
        
        hp_panel = player.get_hp_panel()
        hp_h = hp_panel.get_height()
        
        game_surf = pygame.Surface((map_width,map_height+hp_h), pygame.SRCALPHA)
        tilemap.draw(game_surf)
        game_surf.blit(hp_panel,(0,game_surf.get_height()-hp_h))

        # Add sprite to screen
        player.draw(game_surf)
        for enemy in enemies:
            enemy.draw(game_surf)
        player_attack = False
        enemy_attack = False
        
        if fight_panel:
            fight_panel.render(game_surf)
        
        screen.blit(pygame.transform.scale_by(game_surf,GAME_SCALE),(0,0))
        
        if state == GameState.RUN:
            for enemy in enemies:
                enemy_rect = enemy.get_rect()
                if enemy_rect.collidepoint(game_mouse_pos) and not fight_panel:
                    if enemy != last_enemy:
                        last_enemy = enemy
                        tooltip.clear()
                        #add lines
                        tooltip.add(enemy.name)
                        tooltip.add(enemy.get_desc())
                        tooltip.resize_to_text()
                    offset_pos = (mouse_pos[0] + 15, mouse_pos[1] + 10)
                    tooltip.render(screen, offset_pos)
        elif state == GameState.INV:
            screen.blit(shade_surf, (0,0))
            isWeap, i = inv.update(mouse_pos)
            if mouse_click and i is not None:
                if isWeap:
                    if player.weapon_i != i:
                        player.weapon_i = i
                        w_name = player.weapons[player.weapon_i][0]
                        textBox.add("You equipped "+w_name)
                        inv.prep(player)
                else:
                    state = GameState.RUN
                    roguelike.state_update(("ITEM", i))
            inv.draw(screen)
        
        if fight_panel:
            fight_panel.draw_msg(screen)
        
        # Update the display
        pygame.display.flip()
        clock.tick(30)

    # Quit Pygame
    pygame.quit()