from enum import Enum

total = 4
class TileID(Enum):
    Empty = " "
    Slime = "Slime"
    Ice = "Ice"
    Goal = "Goal"
    Wall = "Wall"

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
