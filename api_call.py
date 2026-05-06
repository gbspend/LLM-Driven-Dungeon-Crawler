import pygame
from spritesheet import Spritesheet
from characters import Character
from characters import Enemy
from groq import Groq
from secret import KEY

'''screen_width = 854
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing Example")
default_pos = (0, 0)
#tile_spritesheet = Spritesheet('Dungeon_Tileset.png')
char_spritesheet = Spritesheet('Dungeon_character.png')
knight_1 = char_spritesheet.get_sprite(0,32,16,16)
skel_g = char_spritesheet.get_sprite(64,48,16,16)
skel_r = char_spritesheet.get_sprite(96,48,16,16)
necro_l = char_spritesheet.get_sprite(32,48,16,16)
necro_g = char_spritesheet.get_sprite(48,48,16,16)
spirit_g = char_spritesheet.get_sprite(16,48,16,16)


knight = Character('Knight', 'A knight, armed with a spear. ',25, 25, 5, default_pos, knight_1)
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
    

#=======================================================================================

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
       Using the format from the examples, run a combat scenario with the player class {player.name}, with the description {player.get_desc()}, attacking a {enemy.name}, with the description {enemy.description}. If the player or enemy is supposed to be defeated in the scenario, the corresponding dealt or received value should be FATAL.'''


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
       Using the format from the examples, run a combat scenario with the {pStatus} player {player.name}, with the description {player.get_desc()}, attacking a {eStatus} enemy {enemy.name}, with the description {enemy.description}.'''

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
       Using the format from the examples, run a combat scenario with a {eStatus} enemy {enemy.name}, with the description {enemy.description}, attacking a {pStatus} player {player.name}, with the description {player.get_desc()}.'''

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
       Using the format from the examples, run a combat scenario with the {pStatus} player {player.name}, with the description {player.get_desc()}, attacking a {eStatus} enemy {enemy.name}, with the description {enemy.description}.'''

    return get_response(prompt_str)

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