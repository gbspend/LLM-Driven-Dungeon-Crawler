import pygame
import random
import math
from consts import *
from text import TextBox

class FightPanel:
    def __init__(self, sprite_a, sprite_b, surface_size, map_width, map_height, font):
        """
        sprite_a, sprite_b: 16x16 pygame.Surface objects
        surface_size: (w, h) bounds of animation area
        topleft: where to blit the animation surface in the window
        """

        self.sprite_a = sprite_a
        self.sprite_b = sprite_b

        self.surface_w, self.surface_h = surface_size
        
        map_rect = pygame.Rect(0,0,map_width,map_height)
        surf_rect = pygame.Rect((0,0),surface_size)
        surf_rect.center = map_rect.center
        self.topleft = surf_rect.topleft

        self.surface = self._make_surf()
        ell_rect = pygame.Rect(0, self.surface_h//2 + 6, 60, 20)
        ell_rect.centerx = self.surface.get_rect().centerx
        strip_rect = pygame.Rect(0,0,self.surface_w-10,50)
        strip_rect.center = ell_rect.center
        pygame.draw.ellipse(self.surface,PANEL,strip_rect)
        pygame.draw.ellipse(self.surface,(86,59,65),ell_rect)
        
        font = pygame.font.Font("Book.ttf", 18)
        self.txt_surf = font.render("COMBAT!",False,TEXT)
        txt_rect = self.txt_surf.get_rect()
        txt_rect.centerx = ell_rect.centerx
        txt_rect.y += 18
        txt_rect.left += self.topleft[0]
        txt_rect.top += self.topleft[1]
        self.txt_pos = txt_rect.topleft

        # Start positions (center-ish, offset slightly)
        self.pos_a = pygame.Vector2(self.surface_w * 0.35, self.surface_h * 0.5)
        self.pos_b = pygame.Vector2(self.surface_w * 0.65, self.surface_h * 0.5)

        self.vel_a = pygame.Vector2(0, 0)
        self.vel_b = pygame.Vector2(0, 0)
        
        self._rand_accel()
        
        self.l_vec = pygame.Vector2(-1,0)
        self.r_vec = pygame.Vector2(1,0)
        
        self.shake = pygame.Vector2(0, 0)
        self.stop = False
        self.last_col = False
        self.done_a = self.done_b = False
        self.final_t = 12
        self.msg_show = False
        
        box_w = (self.surface_w - FIGHT_TXT_OFF)*GAME_SCALE
        box_h = (self.surface_h - FIGHT_TXT_OFF)*GAME_SCALE
        box_x = (self.topleft[0] + FIGHT_TXT_OFF//2)*GAME_SCALE
        box_y = (self.topleft[1] + FIGHT_TXT_OFF//2)*GAME_SCALE
        self.box = TextBox(font, pygame.Rect(0,0,box_w,box_h), WHITE, BG, (box_x,box_y),True)
        #TEMP
        self.box.add("The goblin warrior charges at the knight, swinging its crude sword wildly. The knight easily parries the goblin's attack and counterattacks with a powerful swing of his longsword, striking the goblin with a solid blow.")
    
    def _make_surf(self):
        surf = pygame.Surface((self.surface_w, self.surface_h), pygame.SRCALPHA)
        surf.fill(BG)
        pygame.draw.rect(surf, BORDER1, (1, 1, self.surface_w-2, self.surface_h-2), 1)
        pygame.draw.rect(surf, BORDER2, (0, 0, self.surface_w, self.surface_h), 1)
        for x, y in [(4,4),(self.surface_w-6,4),(4,self.surface_h-6),(self.surface_w-6,self.surface_h-6)]:
            surf.set_at((x,y), BORDER1)
        return surf
    
    def _rand_accel(self):
        self.acc_a = random.uniform(0.15,0.3)
        self.acc_b = random.uniform(0.15,0.3)

    def _clamp_inside(self, pos):
        return pygame.Vector2(
            max(0, min(self.surface_w - 16, pos.x)),
            max(0, min(self.surface_h - 16, pos.y))
        )

    def _apply_bounds(self, pos, vel):
        # soft wall bounce
        if pos.x <= 0 or pos.x >= self.surface_w - 40:
            vel.x *= -0.6
        if pos.y <= 0 or pos.y >= self.surface_h - 40:
            vel.y *= -0.6

    def _resolve_collision(self):
        if self.last_col:
            return
        
        # simple distance-based push apart
        delta = self.pos_b - self.pos_a
        dist = delta.length()

        min_dist = 12  # slight overlap allowed for “contact feel”
        if dist < min_dist:
            if self.stop:
                self.last_col = True
            self._rand_accel()
            push = random.uniform(5,8)
            a_y = random.uniform(-1,1)
            b_y = random.uniform(-1,1)
            if random.random() < .9:
                self.vel_a = pygame.Vector2(-push, a_y)
            else:
                self.vel_a = pygame.Vector2(-push//2, a_y)
                self.acc_a *= 1.5
            if random.random() < .9:
                self.vel_b = pygame.Vector2(push, b_y)
            else:
                self.vel_b = pygame.Vector2(push, b_y)
                self.acc_b *= 1.5
            
            # SCREEN SHAKE IMPULSE
            strength = max(min(5, (min_dist - dist) * 2.0),2) * random.uniform(0.5,1)
            if random.random() < 0.5:
                strength *= -1
            self.shake += pygame.Vector2(
                strength,0
            )

    def end(self):
        self.stop = True
        
    def update(self):
        if self.done_a and self.done_b:
            if self.final_t > 0:
                self.final_t -= 1
                return
            if not self.msg_show:
                self.msg_show = True
                self.surface = self._make_surf()
            return
        
        if not self.last_col:
            center = pygame.Vector2(self.surface_w / 2, self.surface_h / 2)
            self.vel_a += (center - self.pos_a) * 0.01
            self.vel_b += (center - self.pos_b) * 0.01
        else:
            self.vel_a.y = 0
            self.vel_b.y = 0
            self.acc_a = 0
            self.acc_b = 0
        
        self.vel_a += (self.r_vec * self.acc_a)
        self.vel_b += (self.l_vec * self.acc_b)

        # integrate
        self.pos_a += self.vel_a
        self.pos_b += self.vel_b

        if self.vel_a.x < 0:
            self.vel_a *= 0.8
        if self.vel_b.x > 0:
            self.vel_b *= 0.8

        if not self.last_col:
            # bounds
            self._apply_bounds(self.pos_a, self.vel_a)
            self._apply_bounds(self.pos_b, self.vel_b)

        self.pos_a = self._clamp_inside(self.pos_a)
        self.pos_b = self._clamp_inside(self.pos_b)

        # collision interaction
        self._resolve_collision()
        
        if self.last_col:
            if self.vel_a.x < 0:
                self.vel_a.x += 0.1
            else:
                self.done_a = True
                self.vel_a.x = 0
            if self.vel_b.x > 0:
                self.vel_b.x -= 0.1
            else:
                self.done_b = True
                self.vel_b.x = 0
            self.shake = pygame.Vector2(0,0)
        else:
            self.shake *= 0.75

    def render(self, window):
        if self.msg_show:
            window.blit(self.surface, self.topleft)
            return
        surf = self.surface.copy()
        surf.blit(self.sprite_a, (int(self.pos_a.x), int(self.pos_a.y)))
        surf.blit(self.sprite_b, (int(self.pos_b.x), int(self.pos_b.y)))
        offset = (int(self.topleft[0] + self.shake.x),
                  int(self.topleft[1] + self.shake.y))
        window.blit(surf, offset)
        if not self.last_col:
            window.blit(self.txt_surf,self.txt_pos)

    #separate so it isn't scaled
    def draw_msg(self,window):
        if self.msg_show:
            self.box.render(window)

class ItemUsePanel:
    def __init__(self, sprite, surface_size, map_width, map_height):
        self.sprite = sprite

        self.surface_w, self.surface_h = surface_size
        
        map_rect = pygame.Rect(0,0,map_width,map_height)
        surf_rect = pygame.Rect((0,0),surface_size)
        surf_rect.center = map_rect.center
        self.topleft = surf_rect.topleft

        self.surface = self._make_surf()

        self.center = pygame.Vector2(
            self.surface_w // 2,
            self.surface_h // 2 - 4
        )

        self.t = 0

        # expanding rings
        self.rings = []

        # orbiting sparks
        self.sparks = []
        for _ in range(5):
            self.sparks.append({
                "angle": random.uniform(0, math.tau),
                "radius": random.uniform(10, 18),
                "speed": random.uniform(0.03, 0.08),
                "size": random.randint(1, 2)
            })

        # pulse effect
        self.pulse_timer = 0

        # completion animation
        self.done = False
        self.finish_t = 0

    def _make_surf(self):
        surf = pygame.Surface(
            (self.surface_w, self.surface_h),
            pygame.SRCALPHA
        )

        surf.fill(BG)

        pygame.draw.rect(
            surf,
            BORDER1,
            (1, 1, self.surface_w - 2, self.surface_h - 2),
            1
        )

        pygame.draw.rect(
            surf,
            BORDER2,
            (0, 0, self.surface_w, self.surface_h),
            1
        )

        for x, y in [
            (4, 4),
            (self.surface_w - 6, 4),
            (4, self.surface_h - 6),
            (self.surface_w - 6, self.surface_h - 6)
        ]:
            surf.set_at((x, y), BORDER1)

        return surf

    def end(self):
        """
        Call when threaded operation finishes.
        """
        self.done = True
        self.finish_t = 30

    def update(self):
        self.t += 1

        # Spawn rings
        if not self.done:
            if self.t % 12 == 0:
                self.rings.append({
                    "radius": 2,
                    "max_radius": random.randint(22, 32)
                })

        # Update rings
        new_rings = []

        for ring in self.rings:
            if self.done:
                ring["radius"] *= 0.75
            else:
                ring["radius"] += 1.4

            if ring["radius"] < ring["max_radius"]:
                new_rings.append(ring)

        self.rings = new_rings

        # Update sparks
        for spark in self.sparks:
            if self.done:
                spark["radius"] *= 0.93

            spark["angle"] += spark["speed"]

        self.pulse_timer = (self.pulse_timer + 1) % 40

        # Finish animation countdown
        if self.done and self.finish_t > 0:
            self.finish_t -= 1

    def render(self, window):
        surf = self.surface.copy()

        shadow_rect = pygame.Rect(0, 0, 16, 6)
        shadow_rect.center = (
            int(self.center.x),
            int(self.center.y + 10)
        )

        pygame.draw.ellipse(
            surf,
            PANEL,
            shadow_rect
        )

        pulse_phase = self.pulse_timer / 40.0

        pulse_radius = int(8 + pulse_phase * 16)
        pulse_alpha = int(60 * (1.0 - pulse_phase))

        if pulse_alpha > 0:
            pulse_surf = pygame.Surface(
                (pulse_radius * 2 + 4, pulse_radius * 2 + 4),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                pulse_surf,
                (120, 220, 255, pulse_alpha),
                (pulse_radius + 2, pulse_radius + 2),
                pulse_radius
            )

            surf.blit(
                pulse_surf,
                (
                    self.center.x - pulse_radius - 2,
                    self.center.y - pulse_radius - 2
                )
            )

        for ring in self.rings:
            r = int(ring["radius"])

            alpha = int(
                120 * (1.0 - (ring["radius"] / ring["max_radius"]))
            )

            if alpha <= 0:
                continue

            ring_surf = pygame.Surface(
                (r * 2 + 4, r * 2 + 4),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                ring_surf,
                (180, 240, 255, alpha),
                (r + 2, r + 2),
                r,
                1
            )

            surf.blit(
                ring_surf,
                (
                    self.center.x - r - 2,
                    self.center.y - r - 2
                )
            )

        for spark in self.sparks:
            x = (
                self.center.x +
                math.cos(spark["angle"]) * spark["radius"]
            )

            y = (
                self.center.y +
                math.sin(spark["angle"] * 1.3) *
                (spark["radius"] * 0.7)
            )

            pygame.draw.circle(
                surf,
                (220, 240, 255),
                (int(x), int(y)),
                spark["size"]
            )

        if self.done and self.finish_t > 0:
            flash_alpha = int(
                120 * (self.finish_t / 30)
            )

            flash = pygame.Surface(
                (self.surface_w, self.surface_h),
                pygame.SRCALPHA
            )

            flash.fill((255, 255, 255, flash_alpha))

            surf.blit(flash, (0, 0))

        bob_y = math.sin(self.t * 0.15) * 2

        sprite_x = int(self.center.x - 8)
        sprite_y = int(self.center.y - 8 + bob_y)

        surf.blit(
            self.sprite,
            (sprite_x, sprite_y)
        )

        window.blit(
            surf,
            self.topleft
        )
