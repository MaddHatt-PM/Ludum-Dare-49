from pygame import math as pymath
import math
from gameobject import GameObject
from typing import Tuple, Type
from render_layers import *
import pygame
import utilities, assets
from pygame import Rect, Surface

class Wall(GameObject):
    def __init__(self, position: Tuple):
        graphic = pygame.image.load(assets.Wall).convert_alpha()
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
        self.default_melt_time = 12
        self.curr_melt_time = self.default_melt_time
        self.obtained = False
        self.is_ice_block = True
        graphic = pygame.image.load(assets.IceBlock).convert_alpha()
        self.default_graphic = graphic
        super().__init__("Ice Block", graphic, position, LayerIDs.entities, draw_order=80)
        self.defaultRect = self.rect
        self.entitymanager.add_ice(obj=self)

    def reset(self):
        self.curr_melt_time = self.default_melt_time
        self.set_position(self.spawn_pos)
        self.obtained = False

    def destroy(self):
        self.entitymanager.remove_ice(obj=self)
        return super().destroy()

    def tick(self):
        size_change = self.curr_melt_time / self.default_melt_time
        x = int(self.default_graphic.get_width() * size_change)
        y = int(self.default_graphic.get_height() * size_change)
        self.graphic = pygame.transform.scale(self.default_graphic, (x, y))
        return super().tick()

class GoalArea(GameObject):
    def __init__(self, name: str, position:Tuple[float, float]):
        self.is_completed = False
        graphic = pygame.image.load(assets.GoalPoint).convert_alpha()
        super().__init__(name, graphic, position, LayerIDs.entities, draw_order= -1)

        self.entitymanager.add_goal(self)

    def set_completed(self):
        self.is_completed = True
        self.graphic = pygame.image.load(assets.GoalPoint_Good)

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

    def set_click_pos(self, pos=None):
        SPEED = 120.0

        if pos is not None:
            input = pos
        else:
            input = pygame.mouse.get_pos()


        if (self.is_selected):
            self.move_time_curr = 0.001
            self.startpos = float(self.get_position()[0]), float(self.get_position()[1])
            self.click_pos = float(input[0]), float(input[1])
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
                fut_rect = Rect (fut_pos, self.rect.size)

                #check for wall collision
                for col in self.entitymanager.collidables:
                    if fut_rect.colliderect(col.rect):
                        self.set_click_pos(self.get_position())
                        return

                self.set_position (fut_pos)

            # move ice around
            actively_moving = self.move_time_max != 0 and 0.8 > (self.move_time_curr / self.move_time_max) 
            if (self.ice_block is not None):
                print("I have ice")
                self.ice_block.set_position(self.get_position())

                # handle goal point
                for goal in self.entitymanager.goals:
                    if goal.is_completed == False and self.rect.colliderect(goal.rect):
                        self.ice_block.enabled = False
                        self.ice_block = None
                        goal.set_completed()
                        return

                # handle ice melting from movement
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
                        if ice.obtained == False and ice.enabled == True:
                            if self.check_collision(ice.rect):
                                self.obtain_ice(ice)


