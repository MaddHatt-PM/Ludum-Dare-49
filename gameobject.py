from typing import Tuple, Type
from entity_manager import EntityManager
from render_layers import *
import pygame
from pygame import Rect, Surface

class GameObject:
    def __init__(self, name:str, graphic:Surface, position:Tuple, layer:LayerIDs, draw_order=0):
        self.name = name
        self.__isDirty = True
        self.graphic = graphic
        self.rect = Rect(position[0], position[1], graphic.get_width(), graphic.get_height())
        self.draw_order = draw_order

        self.renderer = RenderLayers()
        self.renderer.add(self)

        self.entitymanager = EntityManager()
        self.entitymanager.add(self)

        self.collision_tracker = []
        self.enabled = True

    

    def destroy(self):
        self.renderer.remove(self)
        self.entitymanager.remove(self)

    def mark_dirty(self):
        self.__isDirty = True
        
    def clear_dirty(self):
        self.__isDirty = False

    def tick(self):
        """Any per time based code goes here"""
        pass

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_position(self, position:Tuple[float, float]):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def set_graphic(self, graphic:Surface):
        self.graphic = graphic
        self.mark_dirty()

    def move(self, position:Tuple):
        # Mark the old spot to be rerendered
        # self.renderer.add_rect(self.rect)

        self.rect.x = position[0]
        self.rect.y = position[1]
        self.mark_dirty()

    def check_collision(self, collider:pygame.Rect) -> bool:
        return self.rect.colliderect(collider) and collider not in self.collision_tracker

    def do_draw(self):
        return self.enabled
        # return self.__isDirty and self.graphic != None
