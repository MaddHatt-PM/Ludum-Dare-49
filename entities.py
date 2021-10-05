from pygame import math as pymath
import math
from entity_manager import EntityManager
from gameobject import GameObject
from typing import Tuple, Type
from render_layers import *
import pygame
import utilities, assets
from pygame import Rect, Surface

class Wall(GameObject):
    def __init__(self, position: Tuple, graphic):
        super().__init__("wall", graphic, position, LayerIDs.background, draw_order=0)
        self.entitymanager.add_collidable(self)

class Cursor(GameObject):
    def __init__(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_sprite = pygame.image.load(assets.Cursor).convert_alpha()
        cursor_rect = Rect(cursor_pos[0], cursor_pos[1], cursor_sprite.get_size()[0], cursor_sprite.get_size()[1])
        cursor_rect = utilities.center_rect(cursor_rect)

        super().__init__("cursor", cursor_sprite, cursor_pos, LayerIDs.foreground, 50)

    def tick(self):
        super().move(pygame.mouse.get_pos())
        self.rect = utilities.center_rect(self.rect)

class IceBlock(GameObject):
    def __init__(self, position:Tuple[float, float]):
        self.spawn_pos = position
        self.default_melt_time = 1000
        self.curr_melt_time = self.default_melt_time
        self.obtained = False
        self.is_ice_block = True
        self.icebin_empty = pygame.image.load(assets.IceBin_Empty).convert_alpha()
        self.icebin_full = pygame.image.load(assets.IceBin_Full).convert_alpha()
        graphic = self.icebin_full
        super().__init__("Ice Block", graphic, position, LayerIDs.entities, draw_order=80)
        self.defaultRect = self.rect
        self.entitymanager.add_ice(obj=self)

    def reset(self):
        self.curr_melt_time = self.default_melt_time
        self.set_position(self.spawn_pos)
        self.obtained = False
        self.graphic = self.icebin_full

    def destroy(self):
        self.entitymanager.remove(obj=self)
        return super().destroy()

    def collect(self):
        self.graphic = self.icebin_empty

    def tick(self):
        # size_change = self.curr_melt_time / self.default_melt_time
        # x = int(self.icebin_empty.get_width() * size_change)
        # y = int(self.icebin_empty.get_height() * size_change)
        # self.graphic = pygame.transform.scale(self.icebin_empty, (x, y))
        return super().tick()

class GoalArea(GameObject):
    def __init__(self, name: str, position:Tuple[float, float]):
        self.is_completed = False
        graphic = pygame.image.load(assets.GoalPoint).convert_alpha()
        super().__init__(name, graphic, position, LayerIDs.entities, draw_order= -1)

        self.entitymanager.add_goal(self)

    def set_completed(self):
        self.is_completed = True
        self.entitymanager.add_time = True
        self.graphic = pygame.image.load(assets.GoalPoint_Good)

class Slime(GameObject):
    def __init__(self, name:str, position:Tuple[float, float]):
        self.click_pos = position
        self.ice_block = None
        self.is_selected = False
        self.startpos = position
        self.move_time_max = 0.0001
        self.move_time_curr = 0.0001
        self.gfx_normal = pygame.image.load(assets.Slime_Normal).convert_alpha()
        self.gfx_iced = pygame.image.load(assets.Slime_Iced).convert_alpha()

        super().__init__(name, self.gfx_normal, position, LayerIDs.entities, 15)
        self.col_rect = self.rect
        self.col_rect.y += 12
        self.col_rect.height -= 12
        self.col_rect.x += 8
        self.col_rect.width -= 8
    
    def select(self, state=True):
        self.is_selected = state
        self.change_sel_graphic()

    def change_sel_graphic(self):
        if self.is_selected is True:
            self.graphic = self.gfx_normal

    def obtain_ice(self, ice:IceBlock):
        if (ice.obtained is False):
            self.ice_block = ice
            ice.collect()
            self.graphic = self.gfx_iced
        else:
            self.graphic = self.gfx_normal

    def set_click_pos(self, pos=None):
        SPEED = 120.0

        if pos is not None:
            input = pos
        else:
            input = pygame.mouse.get_pos()


        if (self.is_selected):
            self.move_time_curr = 0.001
            self.startpos = float(self.get_position()[0]), float(self.get_position()[1])
            self.click_pos = float(input[0] - self.rect.width * 0.5), float(input[1] - self.rect.height * 0.5)
            self.move_time_max = utilities.dist(self.startpos, self.click_pos) / SPEED

    def rotate_to_click(self):
        """not working"""
        cli_x, cli_y = self.click_pos[0], self.click_pos[1]
        self_x, self_y = self.get_position()[0], self.get_position()[1]

        rel_x, rel_y = cli_x - self_x, cli_y - self_y
        angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        self.graphic = pygame.transform.rotate(self.graphic, int(angle))
        self.rect = self.graphic.get_rect(center=self.get_position())

    def tick(self):
            self.move_time_curr += self.entitymanager.deltatime()
            # movement
            if self.move_time_max != 0:
                fut_pos = utilities.berp_position(self.startpos, self.click_pos, self.move_time_curr / self.move_time_max)
                fut_rect = Rect (fut_pos, self.col_rect.size)

                #check for wall collision
                for col in self.entitymanager.collidables:
                    if fut_rect.colliderect(col.rect):
                        self.set_click_pos(self.get_position())
                        return

                self.set_position (fut_pos)

            # move ice around
            actively_moving = self.move_time_max != 0 and 0.8 > (self.move_time_curr / self.move_time_max) 
            if (self.ice_block is not None):
                # self.ice_block.set_position(self.get_position())

                # handle goal point
                for goal in self.entitymanager.goals:
                    if goal.is_completed == False and self.rect.colliderect(goal.rect):
                        self.ice_block.enabled = False
                        self.ice_block = None            
                        self.graphic = self.gfx_normal
                        goal.set_completed()
                        self.enabled = False
                        return

                # handle ice melting from movement
                if (actively_moving == True):
                    self.ice_block.curr_melt_time -= self.entitymanager.deltatime()
                    if (self.ice_block.curr_melt_time < 0):
                        print("ice has died")   
                        self.graphic = self.gfx_normal
                        self.ice_block.reset()
                        self.ice_block = None
            
            # Check if close enough to any ice blocks
            else:
                if self.is_selected == True:
                    for ice in self.entitymanager.ice_blocks:
                        if ice.obtained == False and ice.enabled == True:
                            if self.check_collision(ice.rect):
                                self.obtain_ice(ice)