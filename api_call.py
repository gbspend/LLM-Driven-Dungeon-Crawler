from AI_rogue_like import hp_state
from groq import Groq
import json
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
    output = response_str.replace("`", "")
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
   Return ONLY valid JSON anything else will crash the game.
   
   Example output: 
   {{
    "drop": "yes"
   }}

   here is the dropchance: {dropchance}
   """
   return get_response(prompt_str)


def item_type_update(enemy):
   prompt_str = f"""the scenario is an enemy has just died and it dropped something.
   You must decide what it is, a Weapon or Item.
   Return ONLY a valid JSON anything else will crash the game.

   Examples:
   Enemy: Skeleton: A weak, unarmed, and unarmored warrior made entirely of brittle bones.
   output: 
   {{
    "type": "Weapon"
   }}

   Using the format from the examples, run a scenario with this enemy: {enemy.name} and the following description: {enemy.description}.
   """
   return get_response(prompt_str)
   

def item_spawn_item_update(enemy):
    prompt_str = f"""the scenario is an enemy has just died and has dropped a Item.
    You must decide what it is and then give it a description
    
    Rules:
    A Item is something that can be once e.g. Potion, throwing knife, firebomb
    Return ONLY a valid JSON

    Input:
    Enemy: Goblin: A small, cunning creature with sharp ears and leather armor.
    Output:
    {{
    "drops": "Small Healing Potion",
    "description": "A vial holding some healing liquid"
    }}
    
    Using the format from the examples, run a scenario with this enemy: {enemy.name} and the following description: {enemy.description}.'''
    """
    return get_response(prompt_str)


def item_spawn_weapon_update(enemy):
    prompt_str = f"""the scenario is an enemy has just died and has dropped a weapon.
    You must decide what it is and then give it a description
    
    Rules:
    A Weapon is something that can be reused over and over e.g. sword, bow, staff
    Return ONLY a valid JSON nothing more
    
    Examples:
    Input:
    Enemy: Skeleton: A weak, unarmed, and unarmored warrior made entirely of brittle bones.
    Output:
    {{
    "drops": "Sharp Bone",
    "description": "A sharp bone that can be used as a weapon if needed"
    }}

    Using the format from the examples, run a scenario with this enemy: {enemy.name} and the following description: {enemy.description}.'''
    """
    return get_response(prompt_str)


def make(Type,FType,enemy,player):
    weapon_string = FType(enemy)
    print(weapon_string)
    weapon = json.loads(weapon_string)
    weapon_and_description = (weapon["drops"],weapon["description"])

    if Type["type"].lower() == "weapon":
       print(weapon_and_description, "\n end")
       player.weapons.append(weapon_and_description)
       return weapon_and_description
    else:
       print(weapon_and_description, "\n end")
       player.items.append(weapon_and_description)
       return weapon_and_description
   
def gen_item(enemy,player=0,count=4):
    print(count)
    diditdrop_string = drop_item_update(count)
    print(diditdrop_string)
    diditdrop = json.loads(diditdrop_string)
    print(diditdrop)

    if diditdrop["drop"].lower() == "no":
        return "N","N"
    Type_string = item_type_update(enemy)
    print(Type_string)
    Type = json.loads(Type_string)

    if Type["type"].lower() == "weapon":
       wandd = make(Type,item_spawn_weapon_update,enemy,player)
       return wandd, Type["type"]
    else:
       iandd = make(Type,item_spawn_item_update,enemy,player)
       return iandd, Type["type"]

#===================================== item use ========================================================

def item_picktarget_update(item_and_description):
   prompt_str = f"""Given an item with this a description determine whether the item should:
    target the player as a beneficial effect (healing, buff, support), or
    target an enemy as a harmful effect (damage, debuff, negative status).
    Return ONLY a valid JSON like the example do not add anything

    Examples:
    Input:
    Small Healing Potion: A vial holding some healing liquid
    Output:
    {{
    "Target": "Player"
    }}

    Using the format from the examples, run a scenario with this Item: {item_and_description[0]} and the following description: {item_and_description[1]}.
    """
   return get_response(prompt_str)

#-------------------------
def item_enemystat_update(item_and_description):
    prompt_str = f"""An item has just been used by the player and will target an enemy.
    Choose exactly ONE stat for the item to negatively affect from the following list:
    
    description = use when the effect cannot be represented by other stats e.g. hp
    hp = current health points and direct damage
    
    Return ONLY a valid JSON like the example do not add anything
    
    Examples:

    Input:
    Throwing Knife: A small knife that can be thrown
    Output:
    {{
    "Stat": "hp"
    }}
    
    Input:
    Flash Bomb: A small explosive device that releases a blinding flash of light
    Output:
    {{
    "Stat": "description"
    }}
    
    Using the format from the examples, run a scenario with this Item: {item_and_description[0]} and the following description: {item_and_description[1]}.
    """
    return get_response(prompt_str)


def item_playerstat_update(item_and_description):
    prompt_str = f"""An item has just been used by the player and will target the player.
    Choose exactly ONE stat for the item to positively affect from the following list:

    description = use when the effect cannot be represented by other stats e.g. hp
    hp = current health points and healing

    Return ONLY a valid JSON like the example do not add anything

    Examples:

    Input:
    Small Healing Potion: A vial holding healing liquid
    Output:
    {{
    "Stat": "hp"
    }}
    
    Input:
    Iron Skin Potion: A potion that temporarily hardens the user's skin
    Output:
    {{
    "Stat": "description"
    }}
    
    Using the format from the examples, run a scenario with this Item: {item_and_description[0]} and the following description: {item_and_description[1]}.
    """
    return get_response(prompt_str)

#-------------------------
def item_enemy_descriptionstat_update(item_and_description,enemy):
    prompt_str = fprompt_str = f"""An item has just been used by the player and will target an enemy and change the enemy's description.
    How you will do this:
    
    1. Describe how the effect looks on the enemy.
    2. Give a short description of what the effect does such as defense down, blind, stunned, poisoned, burning, weakened, and so on.

    
    Return ONLY a valid JSON like the example do not add anything
    
    Example:
    
    Input:
    Flash Bomb: A small explosive device that releases a blinding flash of light
    enemy: goblin
    Output:
    {{
    "description": "The goblin covers its eyes as bright light burns its vision.",
    "effect": "blinded"
    }}
    
    Input:
    Poison Dart: A small dart coated in deadly poison
    enemy: zombie
    Output:
    {{
    "description": "Dark veins spread across the zombie's body as poison weakens it.",
    "effect": "poisoned"
    }}
    
    Using the format from the examples, run a scenario with this Item: {item_and_description[0]} and the following description: {item_and_description[1]}.
    and the enemy being targeted: {enemy.name}"""
    return get_response(prompt_str)


def item_player_descriptionstat_update(item_and_description, player):
    prompt_str = f"""An item has just been used by the player and will affect the player and change the player's description.
    How you will do this:

    1. Describe how the effect looks on the player.
    2. Give a short description of what the effect does such as defense up, strengthened, energized, and so on. (note that this does not include healing)

    Return ONLY a valid JSON like the example do not add anything

    Example:

    Input:
    iron Potion: A glowing red potion that makes skin hard as iron.
    player: knight
    Output:
    {{
        "description": "The knight's skin takes on a metallic sheen as their body hardens like iron.",
        "effect": "defense up"
    }}

    Input:
    four leaf clover: A rare four-leaf clover said to bring extraordinary luck to whoever carries it.
    player: mage
    Output:
    {{
        "description": "A soft green aura swirls around the mage as fate begins to favor their every move.",
        "effect": "lucky"
    }}

    Using the format from the examples, run a scenario with this Item: {item_and_description[0]} and the following description: {item_and_description[1]}.
    and the player being affected: {player.name}
    """
    
    return get_response(prompt_str)

#-------------------------
def item_enemy_hpstat_update(item_and_description, enemy, eState):
    prompt_str = f"""An item has just been used by the player against an enemy.
    The item attack will affect the enemy's HP.
    Adjust the strength of the enemy based on their status: HEALTHY, WOUNDED, or MAIMED.

    1. Describe how the attack looks and impacts the enemy.
    2. Return a damage value of "LOW", "MEDIUM", or "HIGH". If the enemy is defeated, the dealt value should be "FATAL". if the enemy takes no damage the dealt value should be "None"

    Return ONLY a valid JSON like the example do not add anything

    Examples:

    Input:
    Item: Magic Scroll
    Item Description: A glowing scroll that promises to unleash powerful magic once used.
    Enemy: Goblin
    Enemy Description: A small, cunning creature with sharp ears and leather armor.
    Current enemy state: WOUNDED
    Output:
    {{
    "description": "A burst of arcane fire erupts from the scroll and slams into the goblin, scorching its body.",
    "effect": "FATAL"
    }}

    Using the format from the examples, run a scenario with 
    this Item: {item_and_description[0]} description: {item_and_description[1]}
    and this enemy: {enemy.name} description: {enemy.get_desc} Current enemy state: {eState}

    """
    return get_response(prompt_str)

def item_player_hpstat_update(item_and_description, player, tState=0):
    prompt_str = f""""An item has just been used by the player and will affect the player and change the player's hp.
    How you will do this:

    1. Describe how the healing looks.
    2. Return a healing value of "Low", "Half", "Most", or "All".

    Return ONLY a valid JSON like the example do not add anything

    Input:
    Item: Healing Herb
    Item Description: A small glowing green herb that slowly restores vitality when crushed and consumed.
    player: mage
    Output:
    {{
    "description": "The mage crushes the Healing Herb in her hands, and a soft green glow spreads through her skin before fading into her, mending her wounds.",
    "effect": "Half"
    }}
    
    this Item: {item_and_description[0]} description: {item_and_description[1]}
    and this player: {player.name}
    """
    return get_response(prompt_str)

#========================

def use_item(item_and_description,enemies,player):
    target, target_type = use_item_target(item_and_description,enemies,player)
    if target == False:
        return target, "", "", ""
    
    stat = use_item_stat(item_and_description,target_type)
    if stat == "description":
        dbuff, ebuff = use_item_description(item_and_description,target,target_type)
        return dbuff, stat, ebuff, target.name
    else:
        dhp, ehp =use_item_hp(item_and_description,target,target_type)
        return dhp, stat, ehp, target.name


def use_item_target(item_and_description,enemies,player):
    target_string = item_picktarget_update(item_and_description)
    #print(target_string)
    target = json.loads(target_string)["Target"]
    
    if target.lower() == "enemy": # item will effect enemy
        inrange = []
        attack_range = 16
        for e in enemies:
            #print(e.pos[0] - player.pos[0], end=",   ")
            #print(e.pos[1] - player.pos[1])
            if (abs(e.pos[0] - player.pos[0]) <= attack_range) and (abs(e.pos[1] - player.pos[1]) <= attack_range):
                inrange.append(e)
        if inrange:
            target_enemy = inrange.pop()
            return target_enemy, "E"
        
        else: # not inrange
           #print("not in range")
           return False, ""
    
    else: # item will effect player
       return player, "P"
    

def use_item_stat(item_and_description,target_type):
    if target_type == "E":
        stat_string = item_enemystat_update(item_and_description)
        #print(stat_string)
        stat = json.loads(stat_string)["Stat"]
    else:
        stat_string = item_playerstat_update(item_and_description)
        #print(stat_string)
        stat = json.loads(stat_string)["Stat"]
    return stat.lower()
    

def use_item_description(item_and_description,target,target_type):
    if target_type == "E": 
        descriptionstat_update = item_enemy_descriptionstat_update
    else:
        descriptionstat_update = item_player_descriptionstat_update

    buff_string = descriptionstat_update(item_and_description,target)
    buff = json.loads(buff_string)
    dbuff, ebuff = buff["description"], buff["effect"]

    #print(dbuff, ebuff)
    target.current_effects.append(ebuff)
    return dbuff, ebuff


def use_item_hp(item_and_description,target,target_type):
    if target_type == "E": 
        hpstat_update = item_enemy_hpstat_update
        hp_handle = combat_handler_item
    else:
        hpstat_update = item_player_hpstat_update
        hp_handle = heal_handler_item
    
    tState, dupe_tState = hp_state(target, target)
    #print(tState)
    hp_string = hpstat_update(item_and_description,target,tState)
    print(hp_string)
    hp = json.loads(hp_string)
    #print(hp)
    dhp, ehp = hp["description"], hp["effect"].lower()

    hp_handle(ehp,target)
    #print(ehp,dhp)
    return dhp, ehp

def combat_handler_item(dealt,target):
    dealt = dealt.lower()
    if dealt == "fatal":
        dmg = target.max_hp
    elif dealt == "high":
        dmg = int(target.max_hp * 0.7)
    elif dealt == "medium":
        dmg = int(target.max_hp * 0.4)
    elif dealt == "low":
        dmg = int(target.max_hp * 0.2)
    # dealt == "NONE"
    else:
        dmg = 0

    target.hp = max(0, (target.hp - dmg))


def heal_handler_item(healed,target):
    healed = healed.lower()
    if healed == "all":
        heal = target.max_hp
    elif healed == "most":
        heal = int(target.max_hp * 0.7)
    elif healed == "half":
        heal = int(target.max_hp * 0.4)
    elif healed == "low":
        heal = int(target.max_hp * 0.2)
    # dealt == "NONE"
    else:
        heal = 1

    target.hp = min(target.max_hp, (target.hp + heal))