import os
import re
import pygame
from consts import SPRITE_DIR

def camel_to_spaces(filename):
    stem = os.path.splitext(filename)[0]
    return re.sub(r'(?<!^)([A-Z])', r' \1', stem)

def load_sprites(folder):
    entity_data = []

    for filename in os.listdir(folder):
        if not filename.lower().endswith(".png"):
            continue

        path = os.path.join(folder, filename)

        sheet = pygame.image.load(path).convert_alpha()

        frames = []
        for i in range(4):
            frame = pygame.Surface((16, 16), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * 16, 0, 16, 16))
            frames.append(frame)

        name = camel_to_spaces(filename)
        entity_data.append((name, frames))

    return entity_data

def get_name(entities,name):
    for n,anims in entities:
        if n == name:
            return anims
    return None

if __name__ == "__main__":
    pygame.init()

    SCREEN_W, SCREEN_H = 800, 600
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Enemy Animation Viewer")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 16)

    # Load all enemies
    all_enemies = sorted(load_sprites(SPRITE_DIR))

    # Layout settings
    cols = 10                          # 10 columns fits 75 nicely (8 rows)
    cell_w = SCREEN_W // cols         # 80 px
    rows = (len(all_enemies) + cols - 1) // cols
    cell_h = SCREEN_H // rows         # ~75 px

    # Pre-scale all frames once for efficiency
    scaled_enemies = []
    for name, frames in all_enemies:
        big_frames = [
            pygame.transform.scale(frame, (32, 32))
            for frame in frames
        ]
        scaled_enemies.append((name, big_frames))

    running = True
    frame_index = 0
    frame_timer = 0
    FRAME_DELAY = 200   # ms per animation frame

    while running:
        dt = clock.tick(60)
        frame_timer += dt

        if frame_timer >= FRAME_DELAY:
            frame_timer = 0
            frame_index = (frame_index + 1) % 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dark grey background
        screen.fill((40, 40, 40))

        # Draw all enemies
        for i, (name, frames) in enumerate(scaled_enemies):
            row = i // cols
            col = i % cols

            cell_x = col * cell_w
            cell_y = row * cell_h

            # center sprite in cell
            sprite = frames[frame_index]
            sx = cell_x + (cell_w - 32) // 2
            sy = cell_y + 5
            screen.blit(sprite, (sx, sy))

            # name underneath
            text = font.render(name, True, (220, 220, 220))
            tx = cell_x + (cell_w - text.get_width()) // 2
            ty = sy + 38 + (0 if i % 2 == 0 else 12)
            screen.blit(text, (tx, ty))

        pygame.display.flip()

    pygame.quit()