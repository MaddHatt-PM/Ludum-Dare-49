from typing import Collection
from pygame.constants import QUIT
from pygame import mixer
import pygame

import sys
from enum import Enum, auto

import assets
import colors

# ------------------------------------------------------
# --- INITIAL SETUP ---
mixer.pre_init()
pygame.init()

# WINDOW SETUP
LENGTH = 640
WIN = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption("LD49 | > game title goes here <")

# PERFORMANCE
FPS = 60

# GAME STATES
class SceneID(Enum):
    splash = auto()
    mainmenu = auto()
    game = auto()

# ------------------------------------------------------
# --- Splash and Loading ---
def splashscreen():
    clock = pygame.time.Clock()
    time = int(1 * 1000)

    splashscreen = pygame.image.load(assets.Temp_Splashscreen).convert()

    # Play test sound
    mixer.music.load(assets.Temp_SoundTest)
    mixer.music.set_volume(0.25)
    mixer.music.play()

    while time > 0:
        time -= clock.tick()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # Draw splashscreen
        WIN.fill(colors.GREY)
        WIN.blit(splashscreen, (0,0))
        pygame.display.update()

    mainloop()
        

# ------------------------------------------------------
# --- Physics and Rendering Loop ---
def mainloop():
    clock = pygame.time.Clock()
    is_running = True
    active_scene = SceneID.mainmenu

    while is_running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if (active_scene == SceneID.mainmenu):
            pass
        elif(active_scene == SceneID.game):
            pass

        # User Input()
        # Collision()
        # GameLogic()
        # Audio()
        draw_screen()
        
        
def draw_screen():
    WIN.fill(colors.GREY)

    pygame.display.update()


# ------------------------------------------------------
# --- Kickstarter ---
if __name__ == "__main__":
    splashscreen()