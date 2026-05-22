import pygame
import api_call
from entities import load_sprites, get_name
from concurrent.futures import ThreadPoolExecutor
from characters import Character, Enemy
from consts import *
from fight import FightPanel
import logging

#rewriting api interface to be threaded and more flexible

#"link" in the chain of thought
class Task:
    #postf TAKES self.result (func return value) as arg!
    def __init__(self, func, args, postf=None):
        self.func = func
        self.args = args #list of arguments, in order
        self.postf = postf
        self.future = None
        self.result = None
        self.done = False
        self.proceed = False #True if next link in chain of thought should execute

    def start(self, executor):
        self.future = executor.submit(self.func, *self.args)

    def update(self):
        if self.future and self.future.done():
            self.result = self.future.result()
            if not self.postf:
                self.proceed = True
            else:
                self.proceed = self.postf(self.result)
            self.done = True



#complete chain of thought process
class Chain:
    #finalf takes the final "link's" output as its argument
    def __init__(self, executor, links, finalf):
        self.executor = executor
        self.links = links
        self.finalf = finalf
        self.i = 0
        self.running = False
        self.last_result = None
        self.output = None
        self.done = False
    
    def update(self):
        if not self.links or self.i >= len(self.links) or self.done:
            return
        curr = self.links[self.i]
        if not self.running:
            self.running = True
            curr.start(self.executor)
        else:
            print("curr update:",self.i)
            curr.update()
        if curr.done:
            self.running = False
            self.last_result = curr.result
            if curr.proceed and self.i < len(self.links)-1:
                self.i += 1
            else:
                print("CHAIN DONE!")
                print("\t",self.last_result)
                self.output = self.finalf(self.last_result)
                self.done = True

#testing threading and partial item drop Chain
def main1():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    entity_anims = load_sprites(SPRITE_DIR)

    warrior_1 = get_name(entity_anims,"Elf Lord")
    warrior_e = get_name(entity_anims,"Goblin Fighter")
    sk = pygame.transform.flip(warrior_e[0],True,False)
    base_font = pygame.font.Font("Book.ttf", 17)
    fight_panel = FightPanel(warrior_1[0], sk, (FIGHT_W,FIGHT_H),FIGHT_POS,base_font)
    
    enemy = Enemy('Greater Necromancer', 'A powerful necromancer, skilled in offensive magic and capable of calling undead to aid it.', 16, 16, 4, None,None)
    count = 5
    t1 = Task(api_call.drop_item_update_JSON,[count],lambda r: r["drop"].lower() != "no")
    t2 = Task(api_call.item_type_update_JSON,[enemy])
    
    executor = ThreadPoolExecutor()
    c = Chain(executor,[t1,t2],lambda a,f=fight_panel:f.end())
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        c.update()
        
        if fight_panel:
            fight_panel.update()
        
        game_surf = pygame.Surface((300,400), pygame.SRCALPHA)
        if fight_panel:
            fight_panel.render(game_surf)
        
        screen.blit(pygame.transform.scale_by(game_surf,GAME_SCALE),(0,0))
        
        if fight_panel:
            fight_panel.draw_msg(screen)
        
        # Update the display
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()


def main2():
    player = Character("Warrior", "A strong, brave warrior", 20,None,None,None)
    enemy = Enemy('Greater Necromancer', 'A powerful necromancer, skilled in offensive magic and capable of calling undead to aid it.', 16, 16, None,None)
    
    scen = api_call.combat_scenario(player,enemy)
    print(scen)
    vs = api_call.combat_vars_together(player,enemy,scen)
    print(vs)

#THIS ISN'T REALLY A GOOD TEST
def summon_test(N = 10):
    player = Character("Warrior", "A strong, brave warrior", 20,None,None,None)
    enemy = Enemy('Greater Necromancer', 'A powerful necromancer, skilled in offensive magic and capable of calling undead to aid it.', 16, 16, None,None)
    summ = 0
    count = 0
    error = 0
    i = 0
    while i < N:
        i+= 1
        scen = api_call.combat_scenario(player,enemy)
        if "summon" not in scen.lower():
            continue
        summ += 1 
        print(summ, count, error)
        vs = api_call.combat_vars(player,enemy,scen)
        if 'variables' not in vs:
            error += 1
            continue
        if 'enemy_count' in vs['variables']:
            count+= 1
        
if __name__ == "__main__":
    logging.basicConfig(
        filename="game.log",
        level=logging.INFO,
        format="%(asctime)s %(threadName)s %(levelname)s [%(name)s] %(message)s"
    )
    main2()
