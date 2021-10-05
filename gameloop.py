from typing import Collection
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import Rect, mixer
import pygame
import subprocess

import os, sys
from enum import Enum, auto

from pygame.mouse import get_focused

import assets
import colors
from entities import *
from entity_manager import EntityManager
from render_layers import *
from tileID import TileID
from tile_editor import TileData, tileindex_to_tileRect
from uicounter import UICounter
import utilities

# ------------------------------------------------------
# --- INITIAL SETUP ---
os.system("cls")
mixer.pre_init()
pygame.init()

# WINDOW SETUP
LENGTH = 32*30
WIN = pygame.display.set_mode((LENGTH, LENGTH))

pygame.display.set_caption("LDJam 49: Nuclear Home")
pygame.display.set_icon(pygame.image.load(assets.Timer_F01))
# pygame.mouse.set_visible(False)

# PERFORMANCE
FPS = 60

# GAME STATES
class SceneID(Enum):
    splash = auto()
    mainmenu = auto()
    game = auto()

# Level Data
GAMETIME = 45.0
ADDITIONAL_TIME = 5.0
levelfiles = [
    assets.DemoLevel,
]

# ------------------------------------------------------
# --- Splash and Loading ---
def splashscreen():
    clock = pygame.time.Clock()
    time = utilities.float_to_milli(0.5)

    splashscreen = pygame.image.load(assets.Temp_Splashscreen).convert()

    # Play test sound
    mixer.music.load(assets.Temp_SoundTest)
    mixer.music.set_volume(0.75)
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

    while True:
        mainloop()
        

# ------------------------------------------------------
# --- Physics and Rendering Loop ---
def mainloop():
    clock = pygame.time.Clock()
    is_running = True
    active_scene = SceneID.mainmenu
    entityManager = EntityManager()
    deltatime = 0

    cursor_go = Cursor()
    slimes = []

    # LEVEL LOADER
    floortile = pygame.image.load(assets.Floor).convert()
    Wall_tl_tile = pygame.image.load(assets.Wall_tl).convert()
    Wall_tm_tile = pygame.image.load(assets.Wall_tm).convert()
    Wall_tr_tile = pygame.image.load(assets.Wall_tr).convert()
    Wall_ml_tile = pygame.image.load(assets.Wall_ml).convert()
    Wall_mr_tile = pygame.image.load(assets.Wall_mr).convert()
    Wall_bl_tile = pygame.image.load(assets.Wall_bl).convert()
    Wall_bm_tile = pygame.image.load(assets.Wall_bm).convert()
    Wall_br_tile = pygame.image.load(assets.Wall_br).convert()

    tileData = TileData(levelfiles[0])
    for layer in tileData.leveldata:
        for id in range(0, len(layer)):
            position = tileindex_to_tileRect(id).topleft

            if layer[id] == TileID.Wall_tl:
                Wall(position, Wall_tl_tile)
            if layer[id] == TileID.Wall_tm:
                Wall(position, Wall_tm_tile)
            if layer[id] == TileID.Wall_tr:
                Wall(position, Wall_tr_tile)
            if layer[id] == TileID.Wall_ml:
                Wall(position, Wall_ml_tile)
            if layer[id] == TileID.Wall_mr:
                Wall(position, Wall_mr_tile)
            if layer[id] == TileID.Wall_bl:
                Wall(position, Wall_bl_tile)
            if layer[id] == TileID.Wall_bm:
                Wall(position, Wall_bm_tile)
            if layer[id] == TileID.Wall_br:
                Wall(position, Wall_br_tile)
            if layer[id] == TileID.Floor:
                GameObject("", floortile, position, LayerIDs.background, -100)
            if layer[id] == TileID.Slime:
                slimes.append(Slime("", position))
            if layer[id] == TileID.Ice:
                IceBlock(position)
            if layer[id] == TileID.Goal:
                print("asdbjkasd")
                GoalArea("", position)

    scr_gameover = pygame.image.load(assets.GameOver).convert()
    scr_youwin = pygame.image.load(assets.YouWin).convert()
    scr_mainmenu = pygame.image.load(assets.MainMenu).convert()

    gfx_playbutton_normal = pygame.image.load(assets.PlayButton).convert_alpha()
    gfx_playbutton_hover = pygame.image.load(assets.PlayButton_hover).convert_alpha()
    gfx_playbutton_pressed = pygame.image.load(assets.PlayButton_pressed).convert_alpha()
    ui_playbutton = gfx_playbutton_normal

    sel_slime_id = 0
    slimes[sel_slime_id].select()

    ui_counter = UICounter()

    countdown = GAMETIME

    while is_running:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 

        if (active_scene == SceneID.mainmenu):
            WIN.fill(colors.BACKGROUND)
            WIN.blit(scr_mainmenu, scr_mainmenu.get_rect())

            ui_playbutton = gfx_playbutton_normal
            play_rect = ui_playbutton.get_rect()
            play_rect.center = ( LENGTH // 2, 580 )
            if play_rect.collidepoint(pygame.mouse.get_pos()):
                ui_playbutton = gfx_playbutton_hover
                for event in events:
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        ui_playbutton = gfx_playbutton_pressed

                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        active_scene = SceneID.game
            else:
                ui_playbutton = gfx_playbutton_normal
            WIN.blit(ui_playbutton, play_rect)

            pygame.display.update()

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
    

                draw_gameobjects()

                if entityManager.add_time == True:
                    entityManager.add_time = False
                    countdown += ADDITIONAL_TIME

                # Win State
                if entityManager.is_level_completed() is True:
                    WIN.fill(colors.BACKGROUND)
                    WIN.blit(scr_youwin, scr_youwin.get_rect())
                    
                # Lose State
                else:
                    countdown -= deltatime
                    if countdown < 0.0:
                        WIN.fill(colors.BACKGROUND)
                        WIN.blit(scr_gameover, scr_gameover.get_rect())

                        ui_playbutton = gfx_playbutton_normal
                        play_rect = ui_playbutton.get_rect()
                        play_rect.center = ( LENGTH // 2, 580 )
                        if play_rect.collidepoint(pygame.mouse.get_pos()):
                            ui_playbutton = gfx_playbutton_hover
                            for event in events:
                                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                                    ui_playbutton = gfx_playbutton_pressed

                                if event.type == MOUSEBUTTONUP and event.button == 1:
                                    entityManager.clear()
                                    RenderLayers().clear()
                                    entityManager.reload()
                                    RenderLayers().reload()
                                    gc.collect()
                                    return
                        else:
                            ui_playbutton = gfx_playbutton_normal
                        WIN.blit(ui_playbutton, play_rect)

                ui = ui_counter.get_render_ui(WIN.get_size(), countdown)
                for item in ui:
                    WIN.blit(item[0], item[1])

                pygame.display.update()
        

slime_selector = pygame.image.load(assets.Slime_Selector).convert_alpha()

def draw_gameobjects():
    WIN.fill(colors.BACKGROUND)

    renderlayers = RenderLayers()
    for item in renderlayers.layers:
        if (item.do_draw()):
            WIN.blit(item.graphic, item.rect)

            if type(item) is Slime and item.is_selected:
                WIN.blit(slime_selector, item.rect)


# ------------------------------------------------------
# --- Starter ---
if __name__ == "__main__":
    splashscreen()