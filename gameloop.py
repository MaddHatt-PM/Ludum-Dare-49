from typing import Collection
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame import Rect, mixer
import pygame

import sys
from enum import Enum, auto

import assets
import colors
from entities import *
from entity_manager import EntityManager
from render_layers import *
import utilities

# ------------------------------------------------------
# --- INITIAL SETUP ---
mixer.pre_init()
pygame.init()

# WINDOW SETUP
LENGTH = 540
WIN = pygame.display.set_mode((LENGTH, LENGTH))

INTERNAL_LENGTH = 270
pygame.display.set_caption("LD49: >> game title goes here <<")
# pygame.mouse.set_visible(False)

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
    time = utilities.float_to_milli(1.5)

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
    active_scene = SceneID.game
    deltatime = 0

    cursor_go = cursor()

    slimes = []
    slimes.append(Slime("Bill", (200, 400)))
    slimes.append(Slime("Jill", (400, 100)))
    slimes.append(Slime("Mill", (100, 300)))
    slimes.append(Slime("Zill", (100, 100)))
    sel_slime_id = 0
    slimes[sel_slime_id].is_selected = True
    slimes[sel_slime_id].change_sel_graphic()

    ice = IceBlock((270,270))


    entityManager = EntityManager()

    while is_running:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 

        if (active_scene == SceneID.mainmenu):
            pass
        elif(active_scene == SceneID.game):
            for event in events:
                
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    slimes[sel_slime_id].set_click_pos()

                elif event.type == KEYDOWN and pygame.key.get_pressed()[pygame.K_SPACE]:
                    slimes[sel_slime_id].select(False)

                    sel_slime_id += 1
                    if sel_slime_id == len(slimes):
                        sel_slime_id = 0

                    slimes[sel_slime_id].select(True)



        # User Input()
        # Collision()
        # Audio()

        deltatime = clock.get_time() * 0.001
        entityManager.tick_all(deltatime)
        print(len(entityManager.ice_blocks))

        draw_screen()
        
        
def draw_screen():
    WIN.fill(colors.BLACK)

    renderlayers = RenderLayers()
    for item in renderlayers.layers:
        if (item.do_draw):
            WIN.blit(item.graphic, item.rect)

    pygame.display.update()


# ------------------------------------------------------
# --- Starter ---
if __name__ == "__main__":
    
    mainloop()