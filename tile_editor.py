import pickle
from tileID import TileID
import tileID
import os, os.path
import json

from typing import Collection
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
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

TILE_SIZE = 32
MAP_SIZE = 30

def tileindex_to_tileRect(tileindex:int):
    x = tileindex % MAP_SIZE * TILE_SIZE
    y = tileindex // MAP_SIZE * TILE_SIZE
    size = (32, 32)

    return Rect( (x,y), size )

def position_to_tileID(position:Tuple[int, int]) -> int:
    x = position[0] // TILE_SIZE
    y = position[1] // TILE_SIZE
    return x + y * MAP_SIZE

def cycle_through_tileID(input:TileID, value) -> TileID:
    index = tileID.TileID_to_int(input)
    index += value
    if (index == -1):
        index = tileID.total - 1
    if (index == tileID.total):
        index = 0

    return tileID.int_to_TileID(index)

class TileData:
    def __init__(self, filepath:str) -> None:
        self.filepath = filepath
        self.selectedLayer = 1
        print(self.filepath)

        if (os.path.isfile(self.filepath)):
            print("file exists")
            file = open(self.filepath, "rb")
            self.leveldata = pickle.load(file)
            file.close
        else:
            layerA = [TileID.Empty] * (TILE_SIZE * MAP_SIZE)
            layerB = [TileID.Empty] * (TILE_SIZE * MAP_SIZE)
            layerC = [TileID.Empty] * (TILE_SIZE * MAP_SIZE)

            self.leveldata = [layerA, layerB, layerC]
            self.save()
        
        self.getTileID(0)

    def getTileID(self, tileID:int, layerid=-1) -> str:
        if layerid == -1:
            layerid = self.selectedLayer

        return self.leveldata[layerid][tileID]

    def setTileID(self, tile:TileID, tileID:int, layerid=-1):
        if layerid == -1:
            layerid = self.selectedLayer

        self.leveldata[layerid][tileID] = tile
    
    def save(self):
        file = open(self.filepath, "wb")
        pickle.dump(self.leveldata, file)
        file.close()
        print("file saved")

def load() -> TileData:
    print ("\n\nAvailable levels")
    level_path = os.path.join(os.getcwd(), "Levels")
    for root, dir, files in os.walk(level_path):
        pass

    for id in range(0, len(files)):
        print (id, "-" ,files[id])

    choice = input ("select level to edit or type in new level: ")

    try:
        print("reading file")
        tile_data = TileData(os.path.join(level_path, files[int(choice)]))
    except:
        print("making a new file")
        level_path = os.path.join(level_path, choice + ".level")
        tile_data = TileData(level_path)
    
    return tile_data

def start_editor(tileData:TileData):
    # ------------------------------------------------------
    # --- INITIAL SETUP ---
    pygame.init()

    # WINDOW SETUP
    LENGTH = 32*30
    WIN = pygame.display.set_mode((LENGTH, LENGTH))

    pygame.display.set_caption("LD49: >> game title goes here <<")
    # pygame.mouse.set_visible(False)

    # PERFORMANCE
    FPS = 120

    slime_gfx = pygame.image.load(assets.Slime).convert_alpha()
    cursor_gfx = pygame.image.load(assets.edit_cursor).convert_alpha()

    
    font = pygame.font.SysFont('consolas', 12)
    selected_tileID = TileID.Slime
    clock = pygame.time.Clock()
    isSaving = False
    isPainting = False

    while True:
        # clock.tick(FPS)
        WIN.fill(colors.GREY)

        # draw active layer
        for event in pygame.event.get():

            # Quit
            if event.type == QUIT and isSaving == False:
                tileData.save()
                isSaving = True
                WIN.fill(colors.GREY)
                pygame.display.update()

                clock.tick(FPS)
                pygame.time.wait(1000)

                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == pygame.K_TAB:
                    tileData.selectedLayer += 1
                    if tileData.selectedLayer == len(tileData.leveldata):
                        tileData.selectedLayer = 0
            
            if (event.type == MOUSEBUTTONDOWN):
                if (event.button == 1):
                    isPainting = True

                # Mouse scroll down
                if (event.button == 4):
                    selected_tileID = cycle_through_tileID(selected_tileID, -1)
                    
                # Mouse scroll up
                if (event.button == 5):
                    selected_tileID = cycle_through_tileID(selected_tileID, 1)

            if (event.type == MOUSEBUTTONUP):
                if (event.button == 1):
                    isPainting = False

        if (isPainting == True):
            sel_index = position_to_tileID(pygame.mouse.get_pos())
            tileData.leveldata[tileData.selectedLayer][sel_index] = selected_tileID


        layer = tileData.leveldata[tileData.selectedLayer]
        for tileID in range(0, len(layer)):
            if layer[tileID] != TileID.Empty:
                WIN.blit(slime_gfx, tileindex_to_tileRect(tileID))

        # draw cursor
        sel_index = position_to_tileID(pygame.mouse.get_pos())
        WIN.blit(cursor_gfx, tileindex_to_tileRect(sel_index))

        tileID_text = font.render(selected_tileID.name,False, colors.WHITE, colors.BLACK)
        textID_rect = tileID_text.get_rect()
        textID_rect.x += pygame.mouse.get_pos()[0] + 13
        textID_rect.y += pygame.mouse.get_pos()[1] + 10
        WIN.blit(tileID_text, textID_rect)

        # draw layer menu
        layer_info = "Press tab to cycle draw layers:\n"
        layer_text = font.render(layer_info, False, colors.WHITE)
        layer_rect = layer_text.get_rect()
        layer_rect.x += 5
        layer_rect.y += 10
        addable_height = layer_rect.height

        WIN.blit(layer_text, layer_rect)

        for id in range(0, len(tileData.leveldata)):
            if tileData.selectedLayer == id:
                layer_info = "> " + str(id) + " layer"
            else:
                layer_info = "o " + str(id) + " layer"

            layer_text = font.render(layer_info, False, colors.WHITE)
            layer_rect = layer_text.get_rect()
            addable_height += layer_rect.height
            layer_rect.x += 5
            layer_rect.y += addable_height
            WIN.blit(layer_text, layer_rect)



        pygame.display.update()

        
start_editor(load())