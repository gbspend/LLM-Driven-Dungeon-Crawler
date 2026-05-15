from groq import Groq
from secret import KEY

'''screen_width = 854
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing Example")
default_pos = (0, 0)
#tile_spritesheet = Spritesheet('Dungeon_Tileset.png')
char_spritesheet = Spritesheet('Dungeon_character.png')
knight_1 = char_spritesheet.get_sprite(0,32)
skel_g = char_spritesheet.get_sprite(64,48)
skel_r = char_spritesheet.get_sprite(96,48)
necro_l = char_spritesheet.get_sprite(32,48)
necro_g = char_spritesheet.get_sprite(48,48)
spirit_g = char_spritesheet.get_sprite(16,48)


knight = Character('Knight', 'A knight, armed with a spear. ',25, default_pos, knight_1)
skel_knife = Enemy('Skeleton Grunt', 'A weak skeleton, armed with a knife.',10, 10, 2, default_pos, skel_g)
skel_scy = Enemy('Reaper', 'The skeleton of a strong warrior, armed with a scythe.', 15, 15, 4, default_pos, skel_r)
necro = Enemy('Necromancer', 'A necromancer. Weak on its own, but capable of calling more undead to aid it.', 12, 12, 3, default_pos, necro_l)
necro_greater = Enemy('Greater Necromancer', 'A powerful necromancer.', 16, 16, 4, default_pos, necro_g)
spirit_greater = Enemy('Spirit', 'A spirit summoned to aid a necromancer.', 1, 1, 7, default_pos, spirit_g)'''
client = Groq(api_key = KEY )
'''completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "Resolve this video game combat scenario, given the name and description of the player character and enemy to engage. "
                       "Return a damage value of low, medium, or high."
                       "Example 1: "
                       "Player class: Knight"
                       "Class description: A knight, armed with a spear. A powerful melee combatant."
                       "Enemy: Skeleton Grunt"
                       "Enemy description: A weak skeleton, armed with a knife."
                       "Output: The knight pierces the skull of the skeleton grunt with his spear, destroying it. DEALT: FATAL, RECEIVED: NONE"
                       "Example 2: "
                       "Player class: Mage"
                       "Class description: A mage, armed with a staff. Weak in melee combat, but a powerful ranged combatant."
                       "Enemy: Reaper"
                       "Enemy description: The skeleton of a strong warrior, armed with a scythe."
                       "Output: The mage blasts the reaper with a fireball. The now charred reaper shambles back to its feet, missing an arm. It is too far from the mage to retaliate. DEALT: MEDIUM. RECEIVED: NONE"
                       f"Using the format from the examples, run a combat scenario with the player class Knight, with the description {knight.description}, attacking a reaper, with the description {skel_scy.description}."


        }
    ]
)
print(completion.choices[0].message.content)'''

#===COMMON FUNCTIONS====================================================================

def cleanup_response(response_str):
    output = response_str.replace("*", "")
    return output

def get_response(prompt_str, model_str="llama-3.3-70b-versatile", verb=False):
    completion = client.chat.completions.create(
        model=model_str,
        messages=[
            {
                "role": "system",
                "content": prompt_str
            }
        ]
    )
    response_str = completion.choices[0].message.content
    if verb: print(response_str)
    output = cleanup_response(response_str)
    return output
    

#====================================== combat prompts =================================================

def combat_state_update(player, enemy):
    prompt_str = f'''Resolve this video game combat scenario, given the name and description of the player character and enemy to engage. 
       Return a damage value of low, medium, or high.
       Example 1: 
       Player class: Knight
       Class description: A knight, armed with a spear. A powerful melee combatant.
       Enemy: Skeleton Grunt
       Enemy description: A weak skeleton, armed with a knife.
       Output: The knight pierces the skull of the skeleton grunt with his spear, destroying it. DEALT: FATAL, RECEIVED: NONE
       Example 2: 
       Player class: Mage
       Class description: A mage, armed with a staff. Weak in melee combat, but a powerful ranged combatant.
       Enemy: Reaper
       Enemy description: The skeleton of a strong warrior, armed with a scythe.
       Output: The mage blasts the reaper with a fireball. The now charred reaper shambles back to its feet, missing an arm. It is too far from the mage to retaliate. DEALT: MEDIUM. RECEIVED: NONE
       Using the format from the examples, run a combat scenario with the player class {player.name}, with the description {player.get_desc()}, attacking a {enemy.name}, with the description {enemy.get_desc()}. If the player or enemy is supposed to be defeated in the scenario, the corresponding dealt or received value should be FATAL.'''


    return get_response(prompt_str)

def combat_state_update_alt(player, enemy, pStatus = "HEALTHY", eStatus = "HEALTHY", verb=False):
    prompt_str = f'''Resolve this video game combat scenario, given the name and description of the player character and enemy to engage. 
       Keep the output brief, within 4 sentences if possible.
       Return a damage value of LOW, MEDIUM, or HIGH. If the player or enemy is defeated, the dealt or received value should be FATAL.
       Example 1: 
       Player class: Knight
       Status: HEALTHY
       Class description: A knight, armed with a spear. A powerful melee combatant.
       Enemy: Skeleton Grunt
       Status: HEALTHY
       Enemy description: A weak skeleton, armed with a knife.
       Output: The knight pierces the skull of the skeleton grunt with his spear, destroying it. DEALT: FATAL, RECEIVED: NONE
       Example 2: 
       Player class: Mage
       Status: HEALTHY
       Class description: A mage, armed with a staff. Weak in melee combat, but a powerful ranged combatant.
       Enemy: Reaper
       Status: HEALTHY
       Enemy description: The skeleton of a strong warrior, armed with a scythe.
       Output: The mage blasts the reaper with a fireball. The now charred reaper shambles back to its feet, missing an arm. It is too far from the mage to retaliate. DEALT: HIGH, RECEIVED: NONE
       Using the format from the examples, run a combat scenario with the {pStatus} player {player.name}, with the description {player.get_desc()}, attacking a {eStatus} enemy {enemy.name}, with the description {enemy.get_desc()}.'''

    return get_response(prompt_str, verb=verb)

def combat_state_update_enemy(player, enemy, pStatus = "HEALTHY", eStatus = "HEALTHY"):
    prompt_str = f'''Resolve this video game combat scenario, given the name and description of the player character and enemy to engage. Adjust the strength of the player and enemy based on their status: HEALTHY, WOUNDED, or MAIMED.
       Keep the output brief, within 4 sentences if possible.
       Return a damage value of LOW, MEDIUM, or HIGH. If the player or enemy is defeated, the dealt or received value should be FATAL.
       Example 1: 
       Player class: Knight
       Status: HEALTHY
       Class description: A knight, armed with a spear. A powerful melee combatant.
       Enemy: Skeleton Grunt
       Status: HEALTHY
       Enemy description: A weak skeleton, armed with a knife.
       Output: The skeleton grunt viciously slashes at the knight, but its knife cannot penetrate his armor. The knight retaliates by bashing the grunt with the pole of his spear, knocking it to the ground. DEALT: MEDIUM, RECEIVED: NONE
       Example 2: 
       Player class: Mage
       Status: HEALTHY
       Class description: A mage, armed with a staff. Weak in melee combat, but a powerful ranged combatant.
       Enemy: Reaper
       Status: HEALTHY
       Enemy description: The skeleton of a strong warrior, armed with a scythe.
       Output: The reaper lunges at the mage, swinging its scythe at their neck. The mage attempts to dodge at the last minute, receiving a heavy cut to their arm instead. The mage retaliates, throwing the reaper across the room with a fireball. It lurches back to its feet, now charred. DEALT: MEDIUM, RECEIVED: HIGH
       Using the format from the examples, run a combat scenario with a {eStatus} enemy {enemy.name}, with the description {enemy.get_desc()}, attacking a {pStatus} player {player.name}, with the description {player.get_desc()}.'''

    return get_response(prompt_str)

def combat_state_update_necro(player, enemy, pStatus = "HEALTHY", eStatus = "HEALTHY"):
    prompt_str = f'''Resolve this video game combat scenario, given the name and description of the player character and enemy to engage. 
       In this scenario, the engaged enemy will be capable of calling reinforcements, but not guaranteed to.
       Keep the output brief, within 4 sentences if possible.
       Return a damage value of LOW, MEDIUM, or HIGH. If the player or enemy is defeated, the dealt or received value should be FATAL. If the player or enemy avoids an attack, the dealt or received value should be NONE.
       Example 1: 
       Player class: Knight
       Status: HEALTHY
       Class description: A knight, armed with a spear. A powerful melee combatant.
       Enemy: Necromancer
       Status: HEALTHY
       Enemy description: A necromancer. Weak on its own, but capable of calling more undead to aid it.
       Output: The knight charges the necromancer with his spear, interrupting its spell and knocking it down. The necromancer floats back to its feet, summoning undead to defend it. DEALT: MEDIUM, RECEIVED: NONE
       Example 2: 
       Player class: Mage
       Status: WOUNDED
       Class description: A mage, armed with a staff. Weak in melee combat, but a powerful ranged combatant.
       Enemy: Greater Necromancer
       Status: HEALTHY
       Enemy description: A powerful necromancer, skilled in offensive magic and capable of calling undead to aid it.
       Output: The mage shoots a fireball at the greater necromancer, but his wounds affect its strength. The necromancer diverts the blast with a barrier, receiving minimal damage. The necromancer retaliates with a wave of dark energy, which the mage also blocks. It then summons a wave of undead warriors. DEALT: LOW, RECEIVED: LOW
       Using the format from the examples, run a combat scenario with the {pStatus} player {player.name}, with the description {player.get_desc()}, attacking a {eStatus} enemy {enemy.name}, with the description {enemy.get_desc()}.'''

    return get_response(prompt_str)

#======================================= summoning/reinforcement ========================================================

def enemy_summon_count(scenario):
    scenario = scenario.split("DEALT")[0]
    prompt_str = f'''Read this scenario {scenario}. If it explicitly states the enemy has called reinforcements, determine the number of enemies to be summoned.
        If enemies are summoned, the number of enemies should be 1 at minimum, or 3 at maximum. If no reinforcements are directly mentioned, provide 0 for the number of each enemy.
        Format the enemy count like so:
        Enemies: 2'''
    return get_response(prompt_str)

def parse_reinforcement(reinforcements):
  # Initializing enemy2 and enemy3 to 0, as they may not exist in the reinforcement instructions
  enemy2 = 0
  enemy3 = 0
  # parsing enemy 1 name and description
  split = reinforcements.split("Enemy 1: ")
  print(reinforcements)
  print(split[0])
  print(split[1])
  e1 = split[1]
  e1split = e1.split(", ", 1)
  e1name = e1split[0]
  e1desc = e1split[1]
  e1desc = e1desc.split(".")[0] + "."
  enemy1 = (e1name, e1desc)
  if "Enemy 2: " in reinforcements:
    # parsing enemy 2 name and description
    split = reinforcements.split("Enemy 2: ")
    e2 = split[1]
    e2split = e2.split(", ", 1)
    e2name = e2split[0]
    e2desc = e2split[1]
    e2desc = e2desc.split(".")[0] + "."
    enemy2 = (e2name, e2desc)
    if "Enemy 3: " in reinforcements:
      # parsing enemy 3 name and description
      # only checking if enemy 2 exists
      split = reinforcements.split("Enemy 3: ")
      e3 = split[1]
      e3split = e3.split(", ", 1)
      e3name = e3split[0]
      e3desc = e3split[1]
      e3desc = e3desc.split(".")[0] + "."
      enemy3 = (e3name, e3desc)
  return enemy1, enemy2, enemy3

def generate_reinforcement(scenario, count):
    prompt_str = f'''Based on the provided combat scenario {scenario} where the enemy calls for reinforcements, create appropriate enemies to be summoned.
        Here are some example enemies and their descriptions:
        Format the enemies like so:
        Enemy 1: Skeleton Grunt, A weak skeleton, armed with a knife.
        Enemy 2: Reaper, The skeleton of a strong warrior, armed with a scythe.
        Create a maximum of {count} enemies.'''
    return get_response(prompt_str)

def parse_sprite(name, desc, sprites):
  completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"Given the name {name} and description {desc} of an enemy, select the sprite from {sprites} that suits them the best."
            }
        ]
    )
  output = completion.choices[0].message.content
  for sprite in sprites:
    if sprite in output:
      return sprites[sprite]

def enemy_generator(scenario, enemy_count, sprites):
  scenario = scenario.split("DEALT")[0]
  # Determining number of enemies
  # Creating unique enemies
  reinforcements = generate_reinforcement(scenario, enemy_count)
  # Getting API output into usable form
  e1, e2, e3 = parse_reinforcement(reinforcements)
  # Selecting sprites, or returning if there are no enemies left to select for
  e1sprite = parse_sprite(e1[0], e1[1], sprites)
  enemy1 = (e1[0], e1[1], e1sprite)
  if e2 != 0:
    e2sprite = parse_sprite(e2[0], e2[1], sprites)
    enemy2 = (e2[0], e2[1], e2sprite)
  else:
    return enemy1, 0, 0
  if e3 != 0:
    e3sprite = parse_sprite(e3[0], e3[1], sprites)
    enemy3 = (e3[0], e3[1], e3sprite)
    return enemy1, enemy2, enemy3
  else:
    return enemy1, enemy2, 0
  
#===================================================== item gen =============================
def drop_item_update(dropchance):
   prompt_str = f"""the scenario is an enemy has just died. You must decide whether it drops something.
   a dropchance will be given and effect how likely something will drop.
   it will go from 0 (very unlikely), 1 (unlikely), 2 (50/50), 4 (likely), 5(very likely)
   you do not have to say what it drops just if it did. no for did not drop. yes for did drop.
   Output NOTHING except the one field
   
   Example output: 
   Drop: no

   here is the Count: {dropchance}
   """
   return get_response(prompt_str)

def item_spawn_update(enemy):
    prompt_str = f"""the scenario is an enemy has just died and it dropped something.
    You must decide what it is. then if it is a Weapon or Item.
    
    Rules:
    Only one drop maximum
    A Weapon is something that can be reused over and over e.g. sword
    if a Weapon it its self has to be the thing used e.g a bow is a Weapon but not arrows
    A Item is something that can be used once e.g. healing potion
    If an Item it cannot summon/make new thing
    Output NOTHING except the three fields
    
    Examples:
    Input:
    Enemy: Skeleton: A weak, unarmed, and unarmored warrior made entirely of brittle bones.
    Output:
    Drops: Sharp Bone
    Description: A sharp bone that can be used as a weapon if needed
    Type: Weapon
    2
    Input:
    Enemy: Goblin: A small, cunning creature with sharp ears and leather armor.
    Output:
    Drops: Small Healing Potion
    Description: A vial holding some healing liquid
    Type: Item
    
    Using the format from the examples, run a scenario with this enemy: {enemy.name} and the following description: {enemy.description}.'''
    """
    return get_response(prompt_str)

def parse_item(item_string):
   Item = item_string.split("Drops: ")[1].split("Description:")[0].strip()
   Description = item_string.split("Description: ")[1].split("Type:")[0].strip()
   Type = item_string.split("Type: ")[1].strip()
   item_and_description = (Item, Description)
   #print(item_and_description, Type)
   return item_and_description, Type

def parse_drop(diditdrop_string):
   diditdrop = diditdrop_string.split("Drop: ")[1].strip()
   return diditdrop.lower()

def gen_item(enemy,player,count):
    print(count)
    diditdrop_string = drop_item_update(count)
    diditdrop = parse_drop(diditdrop_string)
    print(diditdrop_string)
    print(diditdrop)

    if diditdrop == "no":
        return "N","N"
    
    item_string = item_spawn_update(enemy)
    print(item_string)
    item_and_description, Type = parse_item(item_string)
    print(item_and_description)

    if Type.lower() == "weapon":
        player.weapons.append(item_and_description)
    else:
        player.items.append(item_and_description)
    
    return item_and_description, Type

#===================================== item use ========================================================
def item_target_update(item_and_description):
    prompt_str = f'''Given an item with this a description determine whether the item should:
    
    target the player as a beneficial effect (healing, buff, support), or
    target an enemy as a harmful effect (damage, debuff, negative status).
    
    Then choose exactly one stat for the item to modify from the following list:
    1. description: use when the effect cannot be represented by the other stats e.g. buffs, debuffs
    2. max_hp: maximum health points
    3. hp: current health points

    Examples:
    Input:
    Small Healing Potion: A vial holding some healing liquid
    Output:
    Target: Player
    Stat: hp

    Input:
    four leaf clove: it might give you some luck
    Output:
    Target: Player
    Stat: description

    Input:
    throwing knife: a small knife that can be thrown
    Output:
    Target: Enemy
    Stat: hp
    Using the format from the examples, run a scenario with this Item: {item_and_description[0]} and the following description: {item_and_description[1]}.
    '''
    return get_response(prompt_str)

def target_parse(target_string):
   stat = target_string.split("Target: ")[1].split("Stat: ")[0].strip()
   target = target_string.split("Stat: ")[1].strip()
   return target,stat

def use_item(item_and_description,enemies,player):
    target_string = item_target_update(item_and_description)
    target,stat = target_parse(target_string)

    if target.lower() == "enemy": # item will effect enemy
        inrange = []
        range = 1
        for e in enemies:
            if abs(e.pos[0] - player.pos[0] <= range) and abs(e.pos[1] - player.pos[1] <= range):
                inrange.append(e)

        if inrange:
            target_enemy = inrange.pop()
            if stat.lower() == "description":
                #debuff_string = debuff_update(target_enemy,item_and_description)
                #debuff = parse_debuff(debuff_string)
                target_enemy.current_effects.append()
            else: # hp stat
               print("TODO")
        else: # not inrange
           print("TODO")
    
    else: # item will effect player
        if stat.lower() == "description":
            #buff_string = buff_update(target_enemy,item_and_description)
            #buff = parse_buff(debuff_string)
            target_enemy.current_effects.append()
          
               

      


