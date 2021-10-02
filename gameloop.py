from typing import Collection
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame import Rect, mixer
import pygame

import os, sys
from enum import Enum, auto

from pygame.mouse import get_focused

import assets
import colors
from entities import *
from entity_manager import EntityManager
from render_layers import *
import utilities

# ------------------------------------------------------
# --- INITIAL SETUP ---
os.system("cls")
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
    entityManager = EntityManager()
    deltatime = 0

    cursor_go = Cursor()

    # Level Scripting to be replaced later
    slimes = []
    slimes.append(Slime("Bill", (200, 400)))
    slimes.append(Slime("Jill", (400, 100)))
    slimes.append(Slime("Mill", (100, 300)))
    slimes.append(Slime("Zill", (100, 100)))

    sel_slime_id = 0
    slimes[sel_slime_id].is_selected = True
    slimes[sel_slime_id].change_sel_graphic()

    wall = Wall((180, 180))

    ice = IceBlock((270,270))
    ice = IceBlock((270,370))

    goal = GoalArea("goal a", (400,400))
    goal = GoalArea("goal b", (0,0))

    countdown = 60.0
    font = pygame.font.SysFont('consolas', 12)

    while is_running:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 

        if (get_focused()):
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
    
                deltatime = utilities.milli_to_float(clock.get_time())
                entityManager.tick_all(deltatime)
    
                # Win State
                if entityManager.is_level_completed() is True:
                    # Add next level loading here
                    print("Do win state stuff")

                # Lose State
                else:
                    countdown -= deltatime
                    if countdown < 0.0:
                        # pass
                        print("You lose")

        # Audio()

        draw_screen()
        countdown_text = font.render("{:.2f}".format(countdown), False, colors.WHITE)
        WIN.blit(countdown_text, (( LENGTH // 2 - countdown_text.get_width() // 2, 0) , countdown_text.get_rect().size))
        pygame.display.update()
        
        
def draw_screen():
    WIN.fill(colors.BLACK)

    renderlayers = RenderLayers()
    for item in renderlayers.layers:
        if (item.do_draw()):
            WIN.blit(item.graphic, item.rect)

    pygame.display.update()


# ------------------------------------------------------
# --- Starter ---
if __name__ == "__main__":
    mainloop()