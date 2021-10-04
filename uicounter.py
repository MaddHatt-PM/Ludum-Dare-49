from typing import Tuple
import assets
import pygame

class UICounter():
    def __init__(self) -> None:
        self.Timer_F01 = pygame.image.load(assets.Timer_F01).convert_alpha()
        self.Timer_F02 = pygame.image.load(assets.Timer_F02).convert_alpha()
        self.ui_num_0 = pygame.image.load(assets.ui_num_0).convert_alpha()
        self.ui_num_1 = pygame.image.load(assets.ui_num_1).convert_alpha()
        self.ui_num_2 = pygame.image.load(assets.ui_num_2).convert_alpha()
        self.ui_num_3 = pygame.image.load(assets.ui_num_3).convert_alpha()
        self.ui_num_4 = pygame.image.load(assets.ui_num_4).convert_alpha()
        self.ui_num_5 = pygame.image.load(assets.ui_num_5).convert_alpha()
        self.ui_num_6 = pygame.image.load(assets.ui_num_6).convert_alpha()
        self.ui_num_7 = pygame.image.load(assets.ui_num_7).convert_alpha()
        self.ui_num_8 = pygame.image.load(assets.ui_num_8).convert_alpha()
        self.ui_num_9 = pygame.image.load(assets.ui_num_9).convert_alpha()
        self.ui_num_point = pygame.image.load(assets.ui_num_point).convert_alpha()
        self.UI_Pipes = pygame.image.load(assets.UI_Pipes).convert_alpha()
        self.ui_flavor = pygame.image.load(assets.ui_text_untilmeltdown).convert_alpha()

    def char_to_num(self, input:str) -> pygame.Surface:
        if "." == input: return self.ui_num_point
        if "0" == input: return self.ui_num_0
        if "1" == input: return self.ui_num_1
        if "2" == input: return self.ui_num_2
        if "3" == input: return self.ui_num_3
        if "4" == input: return self.ui_num_4
        if "5" == input: return self.ui_num_5
        if "6" == input: return self.ui_num_6
        if "7" == input: return self.ui_num_7
        if "8" == input: return self.ui_num_8
        if "9" == input: return self.ui_num_9

    def get_render_ui(self, windowsize:Tuple[int, int], counter:float):
        window_center = windowsize[0] // 2
        returnable = []

        pipes_rect = self.UI_Pipes.get_rect()
        pipes_rect.centerx = window_center
        returnable.append((self.UI_Pipes, pipes_rect))

        timer_rect = self.Timer_F01.get_rect()
        timer_rect.centerx = window_center
        timer_rect.centery = 80
        if (int(counter) % 2):
            returnable.append ( (self.Timer_F01, timer_rect) )
        else:
            returnable.append ( (self.Timer_F02, timer_rect) )

        charwidth = 35
        start_x = window_center - charwidth * 2 + 18
        text = "{:.1f}".format(counter)
        count = 0
        for char in text:
            charRect = self.char_to_num(char).get_rect()
            charRect.y = 85
            charRect.centerx = start_x + charwidth * count
            if (count == 2): charRect.centerx -= 5
            if (count == 3): charRect.centerx -= 10

            returnable.append ( (self.char_to_num(char), charRect) )
            count += 1


        flavor_rect = self.ui_flavor.get_rect()
        flavor_rect.centerx = window_center
        flavor_rect.centery = 146
        returnable.append ( (self.ui_flavor, flavor_rect) )

        return returnable