from gameobject import GameObject
from typing import Tuple, Type
from render_layers import *
import pygame
import utilities, assets
from pygame import Rect, Surface

class cursor(GameObject):
    def __init__(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_sprite = pygame.image.load(assets.Cursor).convert_alpha()
        cursor_rect = Rect(cursor_pos[0], cursor_pos[1], cursor_sprite.get_size()[0], cursor_sprite.get_size()[1])
        cursor_rect = utilities.center_rect(cursor_rect)

        super().__init__("cursor", cursor_sprite, cursor_pos, LayerIDs.foreground, 30)

    def tick(self):
        super().move(pygame.mouse.get_pos())
        self.rect = utilities.center_rect(self.rect)

class IceBlock(GameObject):
    def __init__(self, position:Tuple[float, float]):
        self.spawn_pos = position
        self.default_melt_time = 12
        self.curr_melt_time = self.default_melt_time
        self.obtained = False
        graphic = pygame.image.load(assets.IceBlock).convert_alpha()
        super().__init__("Ice Block", graphic, position, LayerIDs.entities, draw_order=30)
        self.entitymanager.add_ice(obj=self)

    def reset(self):
        self.curr_melt_time = self.default_melt_time
        self.set_position(self.spawn_pos)
        self.obtained = False

    def destroy(self):
        self.entitymanager.remove_ice(obj=self)
        return super().destroy()

    def tick(self):
        print(self.curr_melt_time)
        return super().tick()

class Slime(GameObject):
    def __init__(self, name:str, position:Tuple[float, float]):
        self.click_pos = position
        self.ice_block = None
        self.is_selected = False
        self.startpos = position
        self.move_time_max = 0.0001
        self.move_time_curr = 0.0001
        self.graphic_sel = pygame.image.load(assets.Slime_Active).convert_alpha()
        self.graphic_unsel = pygame.image.load(assets.Slime_Deactive).convert_alpha()
        super().__init__(name, self.graphic_unsel, position, LayerIDs.entities, 15)
    
    def select(self, state:bool):
        self.is_selected = state
        self.change_sel_graphic()

    def change_sel_graphic(self):
        if self.is_selected is True:
            self.graphic = self.graphic_sel
        else:
            self.graphic = self.graphic_unsel

    def obtain_ice(self, ice:IceBlock):
        if (ice.obtained is False):
            self.ice_block = ice
            self.ice_block.obtained

    def set_click_pos(self):
        SPEED = 120.0

        if (self.is_selected):
            self.move_time_curr = 0.001
            self.startpos = float(self.get_position()[0]), float(self.get_position()[1])
            self.click_pos = float(pygame.mouse.get_pos()[0]), float(pygame.mouse.get_pos()[1])
            self.move_time_max = utilities.dist(self.startpos, self.click_pos) / SPEED

    def tick(self):
            self.move_time_curr += self.entitymanager.deltatime()
            if self.move_time_max != 0:
                self.set_position (utilities.berp_position(self.startpos, self.click_pos, self.move_time_curr / self.move_time_max))

            # move ice around
            actively_moving = 0.8 > (self.move_time_curr / self.move_time_max) 
            if (self.ice_block is not None):
                self.ice_block.set_position(self.get_position())

                # handle ice melting
                if (actively_moving == True):
                    self.ice_block.curr_melt_time -= self.entitymanager.deltatime()
                    if (self.ice_block.curr_melt_time < 0):
                        print("ice has died")
                        self.ice_block.reset()
                        self.ice_block = None
            
            # Check if close enough to any ice blocks
            else:
                if self.is_selected == True:
                    for ice in self.entitymanager.ice_blocks:
                        if ice.obtained == False:
                            if self.check_collision(ice.rect):
                                self.obtain_ice(ice)


