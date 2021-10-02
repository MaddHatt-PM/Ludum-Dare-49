from typing import Tuple
from pygame import Rect
import math

def float_to_milli(input:float) -> int:
    return int(input * 1000)

def milli_to_float(input:int) -> float:
    return input * 0.001

def clamp01(value):
    return max(0, min(value, 1))

def lerp(start, end, value, clamp=True):
    if clamp:
        value = clamp01(value)
    return ( (1.0 - (value)) * start) + (value * end)

def lerp_position(startpos:Tuple, endpos:Tuple, percentage, clamp=True ):
    x = lerp (startpos[0], endpos[0], percentage, clamp=clamp)
    y = lerp (startpos[1], endpos[1], percentage, clamp=clamp)
    return (x, y)

def center_rect(input:Rect):
    input[0] -= input[2] * 0.5
    input[1] -= input[3] * 0.5
    return input

def dist(p_a:Tuple[float, float], p_b:Tuple[float, float]) -> float:
    return math.sqrt ( ((p_a[0]-p_b[0])**2) + ((p_a[1]-p_b[1])**2) ) 

def berp(start:float, end:float, value) -> float:
    value = clamp01(value)
    value = (math.sin(value * math.pi * (0.2 + 1.5 * value * value * value)) * (1 - value ** 0.2) + value) * (1.0 + (1.2 * (1.0 - value)))
    return start + (end - start) * value

def berp_position(startpos:Tuple, endpos:Tuple, value):
    x = berp(startpos[0], endpos[0], value)
    y = berp(startpos[1], endpos[1], value)
    return ( x, y )