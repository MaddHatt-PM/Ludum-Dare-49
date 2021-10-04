from enum import Enum

from pygame import Surface
import pygame
import assets

total = 14
class TileID(Enum):
    Empty = " "
    Slime = "Slime"
    Ice = "Ice"
    Goal = "Goal"
    Wall = "Wall"
    Wall_tl = "Wall_tl"
    Wall_tm = "Wall_tm"
    Wall_tr = "Wall_tr"
    Wall_ml = "Wall_ml"
    Floor = "Floor"
    Wall_mr = "Wall_mr"
    Wall_bl = "Wall_bl"
    Wall_bm = "Wall_bm"
    Wall_br = "Wall_br"
    reactor = "reactor"

def int_to_TileID(input:int) -> TileID:
    if input == 0:
        return TileID.Empty
    if input == 1:
        return TileID.Slime
    if input == 2:
        return TileID.Ice
    if input == 3:
        return TileID.Goal
    if input == 4:
        return TileID.Wall
    if input == 5:
        return TileID.Wall_tl
    if input == 6:
        return TileID.Wall_tm
    if input == 7:
        return TileID.Wall_tr
    if input == 8:
        return TileID.Wall_ml
    if input == 9:
        return TileID.Floor
    if input == 10:
        return TileID.Wall_mr
    if input == 11:
        return TileID.Wall_bl
    if input == 12:
        return TileID.Wall_bm
    if input == 13:
        return TileID.Wall_br

def TileID_to_int(input:TileID):
    if input == TileID.Empty:
        return 0
    if input == TileID.Slime:
        return 1
    if input == TileID.Ice:
        return 2
    if input == TileID.Goal:
        return 3
    if input == TileID.Wall:
        return 4
    if input == TileID.Wall_tl:
        return 5
    if input == TileID.Wall_tm:
        return 6
    if input == TileID.Wall_tr:
        return 7
    if input == TileID.Wall_ml:
        return 8
    if input == TileID.Floor:
        return 9
    if input == TileID.Wall_mr:
        return  10
    if input == TileID.Wall_bl:
        return  11
    if input == TileID.Wall_bm:
        return  12
    if input == TileID.Wall_br:
        return 13

def TileID_to_gfx_path(input:TileID) -> str:
    if input == TileID.Empty:
        print("You shouldn't get an empty gfx")
        return 0
    if input == TileID.Slime:
        return assets.Slime
    if input == TileID.Ice:
        return assets.IceBlock
    if input == TileID.Goal:
        return assets.GoalPoint
    if input == TileID.Wall:
        return assets.Wall
    if input == TileID.Wall_tl:
        return assets.Wall_tl
    if input == TileID.Wall_tm:
        return assets.Wall_tm
    if input == TileID.Wall_tr:
        return assets.Wall_tr
    if input == TileID.Wall_ml:
        return assets.Wall_ml
    if input == TileID.Floor:
        return assets.Floor
    if input == TileID.Wall_mr:
        return  assets.Wall_mr
    if input == TileID.Wall_bl:
        return  assets.Wall_bl
    if input == TileID.Wall_bm:
        return  assets.Wall_bm
    if input == TileID.Wall_br:
        return  assets.Wall_br

class tileID_gfx():
    def __init__(self, path:str, tileID:TileID, has_alpha=True) -> None:
        self.path = path
        self.tileID = tileID
        self.has_alpha = has_alpha
        self.surface = None

    def get_gfx(self) -> Surface:
        if (self.surface is None):
            if (self.has_alpha is True):
                self.surface = pygame.image.load(self.path).convert_alpha()
            else:
                self.surface = pygame.image.load(self.path).convert()

        return self.surface