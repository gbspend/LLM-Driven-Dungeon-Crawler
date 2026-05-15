#use this to gather data by repeating a combat scenario
from characters import Character, Enemy
from AI_rogue_like import parse_damage, hp_state
import api_call
from collections import defaultdict

def runCombat(player, enemy, verb=False):
    pState, eState = hp_state(player, enemy)
    instructions = api_call.combat_state_update_alt(player, enemy, pState, eState, verb)
    return parse_damage(instructions, False)

def vsWeak():
    player = Character('Knight', 'A knight', 25, None, None, None)
    enemy = Enemy('Goblin', 'A weak, pathetic goblin', 5, 5, 1, None, None)
    return runCombat(player, enemy)

def vsStrong():
    player = Character('Knight', 'A knight', 25, None, None, None)
    enemy = Enemy('Stone Golem', 'A huge, indestructible granite construct.', 100, 100, 20, None, None)
    return runCombat(player, enemy)

def woundedVsGob():
    player = Character('Knight', 'A knight', 25, None, None, None)
    player.hp = 13
    enemy = Enemy('Goblin', 'A small but fierce goblin warrior', 5, 5, 1, None, None)
    return runCombat(player, enemy)

def maimedVsGob():
    player = Character('Knight', 'A knight', 25, None, None, None)
    player.hp = 1
    enemy = Enemy('Goblin', 'A small but fierce goblin warrior', 5, 5, 1, None, None)
    return runCombat(player, enemy)
    
def knifeVsGob():
    player = Character('Knight', 'A knight', 25, None, None, None)
    player.weapon_id = 0
    enemy = Enemy('Goblin', 'A small but fierce goblin warrior', 5, 5, 1, None, None)
    return runCombat(player, enemy, False)

def slayerVsGob():
    player = Character('Knight', 'A knight', 25, None, None, None)
    player.weapon_id = 2
    enemy = Enemy('Goblin', 'A small but fierce goblin warrior', 5, 5, 1, None, None)
    return runCombat(player, enemy, False)

def runTest(f, N):
    print(f.__name__, N)
    
    order = ["NONE", "LOW", "MEDIUM", "HIGH", "FATAL"]
    deal_counts = defaultdict(int)
    recv_counts = defaultdict(int)
    for _ in range(N):
        d, r = f()
        deal_counts[d]+=1
        recv_counts[r]+=1
    
    for s in order:
        line = s+":\t"+str(deal_counts[s])+"\t"+str(recv_counts[s])
        print(line)
    
    o_set = set(order)
    deal_ex = set(deal_counts.keys()) - o_set
    recv_ex = set(recv_counts.keys()) - o_set
    if deal_ex: print(deal_ex)
    if recv_ex: print(recv_ex)
    print()

if __name__ == "__main__":
    #print(vsWeak())
    #print(vsStrong())
    
    N = 10
    tests = [vsWeak, vsStrong, woundedVsGob, maimedVsGob, knifeVsGob, slayerVsGob]
    
    for f in tests:
        runTest(f, N)


'''
Results:
vsWeak 10
NONE:	0	4
LOW:	0	6
MEDIUM:	1	0
HIGH:	1	0
FATAL:	8	0

vsStrong 10
NONE:	0	0
LOW:	10	0
MEDIUM:	0	10
HIGH:	0	0
FATAL:	0	0

woundedVsGob 10
NONE:	0	0
LOW:	1	8
MEDIUM:	8	2
HIGH:	1	0
FATAL:	0	0

maimedVsGob 10
NONE:	0	0
LOW:	7	5
MEDIUM:	3	5
HIGH:	0	0
FATAL:	0	0

knifeVsGob 10
NONE:	0	1
LOW:	0	9
MEDIUM:	6	0
HIGH:	2	0
FATAL:	2	0

slayerVsGob 10
NONE:	0	0
LOW:	0	10
MEDIUM:	7	0
HIGH:	3	0
FATAL:	0	0
'''

'''
Modifying weapon tests Knife vs Slayer, but still got results that don't reflect those weapons...
('Knife', 'A small dull knife.'), ...,
('Dragon Slayer', 'A massive sword, magically empowered by slain dragons.'),

combatsim with verbose prompt responses (may give clues)

knifeVsGob 10
The knight swings his longsword at the goblin, striking it down with a powerful blow. The goblin attempts to retaliate, but its small dagger barely scratches the knight's armor. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin, striking it down with a powerful swing of his longsword. The goblin attempts to dodge, but the knight's attack is too strong, dealing significant damage. The goblin is now badly hurt, but still alive. DEALT: HIGH, RECEIVED: LOW
The knight charges at the goblin, striking it down with a swift swing of his longsword. The goblin attempts to dodge, but the knight's attack is too strong, dealing significant damage. DEALT: HIGH, RECEIVED: LOW
The knight swings his longsword at the goblin, striking it down with a powerful blow. The goblin attempts to retaliate, but its small dagger barely scratches the knight's armor. DEALT: MEDIUM, RECEIVED: LOW
The knight swings his well-forged longsword at the goblin, striking true and cutting deeply into its side. The goblin yelps in pain, but remains standing and readies its crude spear for a counterattack. DEALT: MEDIUM, RECEIVED: LOW
The knight swings his longsword at the goblin, striking true and slicing through its defenses. The goblin is badly hurt but still standing, too small and quick for the knight to land a fatal blow. The goblin retaliates with a crude spear, scratching the knight's armor but failing to pierce it. DEALT: HIGH, RECEIVED: LOW
The knight swings his longsword at the goblin, striking its side and landing a solid blow. The goblin yelps in pain, but quickly recovers and stabs at the knight with its crude spear, grazing his armor. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin warrior, swinging his longsword in a wide arc, striking the goblin with a powerful blow. The goblin, though small, manages to dodge the worst of the attack but still takes significant damage. The goblin retaliates with a quick jab from its crude spear, but the knight's armor absorbs the impact. DEALT: HIGH, RECEIVED: LOW
The knight charges at the goblin with his longsword, striking true and slicing through its defenses. The goblin attempts to counterattack, but its small dagger barely scratches the knight's armor. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin, swinging his longsword in a wide arc, and strikes the goblin's side. The goblin yelps in pain, stumbling backward, but quickly regains its footing and readies its crude spear for a counterattack. DEALT: MEDIUM, RECEIVED: LOW
NONE:   0       0
LOW:    0       10
MEDIUM: 6       0
HIGH:   4       0
FATAL:  0       0

slayerVsGob 10
The knight charges at the goblin warrior, swinging his longsword in a wide arc. The goblin attempts to dodge, but the knight's blade bites deep into its shoulder. The goblin yelps in pain and strikes back with its crude spear, but the knight's armor absorbs the blow. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin, swinging his longsword in a wide arc, striking the goblin and sending it to the ground. The goblin attempts to retaliate with its crude spear, but the knight's armor absorbs the impact. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin and strikes it down with his longsword, delivering a crushing blow. The goblin attempts to counterattack, but the knight's armor protects him from the goblin's weak dagger thrust. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin warrior, striking it down with a powerful slash of his longsword. The goblin attempts to retaliate, but its small dagger barely scratches the knight's armor. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin warrior, swinging his longsword in a wide arc. The goblin attempts to dodge, but the knight's sword bites deep into its shoulder. The goblin yelps in pain and retaliates with a crude spear thrust, but the knight's armor absorbs the blow. DEALT: HIGH, RECEIVED: LOW
The knight swings his longsword at the goblin, striking its chest and sending it to the ground. The goblin attempts to retaliate with its crude spear, but the knight's armor absorbs the blow. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin, swinging his longsword in a wide arc, striking the goblin's side. The goblin, though wounded, quickly retaliates with its crude spear, but the knight's armor absorbs the impact. DEALT: MEDIUM, RECEIVED: LOW
The knight swings his longsword at the goblin, slicing through its defenses and striking true. The goblin yelps in pain, stumbling back but remaining on its feet. DEALT: MEDIUM, RECEIVED: LOW
The knight charges at the goblin, striking it down with a powerful swing of his longsword. The goblin attempts to dodge, but the knight's blade bites deep into its side. The goblin retaliates with a wild stab of its crude spear, but the knight's armor absorbs the blow. DEALT: HIGH, RECEIVED: LOW
The knight charges at the goblin, swinging his longsword in a wide arc, striking the goblin's side. The goblin yelps in pain, stumbling backward, but quickly recovers and retaliates with a crude dagger, grazing the knight's armor. DEALT: MEDIUM, RECEIVED: LOW
NONE:   0       0
LOW:    0       10
MEDIUM: 8       0
HIGH:   2       0
FATAL:  0       0
'''
