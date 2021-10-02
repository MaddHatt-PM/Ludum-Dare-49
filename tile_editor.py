import pickle
from tileID import TileID
import os, os.path
import json

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

TILE_SIZE = 32
MAP_SIZE = 30

class TileData:
    def __init__(self, filepath:str) -> None:
        self.filepath = filepath
        self.selectedLayer = 1
        print(self.filepath)

        if (os.path.isfile(self.filepath)):
            print("file exists")
            file = open(self.filepath, "w")
            self.leveldata = pickle.load(file)
            file.close
        else:
            layerA = [TileID.Slime.name] * (TILE_SIZE * MAP_SIZE)
            layerB = [TileID.Slime.name] * (TILE_SIZE * MAP_SIZE)
            layerC = [TileID.Slime.name] * (TILE_SIZE * MAP_SIZE)

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
        file = open(self.filepath, "w")
        pickle.dump(self.leveldata)
        file.close()

def load() -> TileData:
    print ("\n\nAvailable levels")
    level_path = os.path.join(os.getcwd(), "Levels")
    for root, dir, files in os.walk(level_path):
        pass

    for id in range(0, len(files)):
        print (id, "-" ,files[id])

    choice = input ("select level to edit or type in new level: ")

    try:
        tile_data = TileData(os.path.join(level_path, files[int(choice)]))
    except:
        level_path = os.path.join(level_path, choice + ".level")
        tile_data = TileData(level_path)

def start_editor(tileData):
    # ------------------------------------------------------
    # --- INITIAL SETUP ---
    pygame.init()

    # WINDOW SETUP
    LENGTH = 32*30
    WIN = pygame.display.set_mode((LENGTH, LENGTH))

    pygame.display.set_caption("LD49: >> game title goes here <<")
    # pygame.mouse.set_visible(False)

    # PERFORMANCE
    FPS = 60

    clock = pygame.time.Clock()

data = load()
# data.setTileID(TileID.Goal, tileID=0)
# data.save()
# start_editor(load())