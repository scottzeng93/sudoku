# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:14:49 2021

@author: Administrator
"""
import sys
import time
from enum import Enum
import pygame
from pygame.locals import *

from init_setting import *
from sudoku import *


class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


class LoadPic():
    
    def load(self, file_name):
        # 加载资源图片，因为资源文件大小不一，所以做了统一的缩放处理
        img0 = pygame.image.load('resources/%s.bmp'%file_name).convert()
        img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
        return img0

        
    def __init__(self):
        
        self.img_dict = [self.load(png_order) for png_order in range(0,10)]
       

def main(): 
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('数独')

    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)  # 得分的字体
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40)
    
    
    # load pngs
    png_collection = LoadPic()
    img_dict = png_collection.img_dict
    
    bgcolor = (225, 225, 225)   # 背景色
    
    block = generate_sudoku(mask_rate=0.05)[1]
    block_raw = block.copy()
    game_status = GameStatus.readied
    start_time = None   # 开始时间
    elapsed_time = 0    # 耗时

    while True:
        
        # 填充背景色
        screen.fill(bgcolor)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()
                # if game_status == GameStatus.started:
                #     # 鼠标左右键同时按下，如果已经标记了所有雷，则打开周围一圈
                #     # 如果还未标记完所有雷，则有一个周围一圈被同时按下的效果
                #     if b1 and b3:
                #         mine = block.getmine(x, y)
                #         if mine.status == BlockStatus.opened:
                #             if not block.double_mouse_button_down(x, y):
                #                 game_status = GameStatus.over
                
            elif event.type == MOUSEBUTTONUP:
                if game_status == GameStatus.readied:
                    game_status = GameStatus.started
                    start_time = time.time()
                    elapsed_time = 0

                if game_status == GameStatus.started:
                    
                    if b1 and not b3:       # 按鼠标左键，选择1-9
                        if block_raw[y][x] == 0:
                            if block[y][x]<9:
                                block[y][x] += 1    
                            else:
                                block[y][x] = 1
                    elif not b1 and b3:     # 按鼠标右键，重置为0
                        if block_raw[y][x] == 0:
                            block[y][x] = 0
                #         if mine.status == BlockStatus.normal:
                #             mine.status = BlockStatus.flag
                #         elif mine.status == BlockStatus.flag:
                #             mine.status = BlockStatus.ask
                #         elif mine.status == BlockStatus.ask:
                #             mine.status = BlockStatus.normal
                #     elif b1 and b3:
                #         if mine.status == BlockStatus.double:
                #             block.double_mouse_button_up(x, y)

        flag_count = 0
        opened_count = 0
        
        POS_X, POS_Y = 0,0
        for row in block:            
            for mine in row:       
                pos_x, pos_y = (POS_X * SIZE, (POS_Y + 2) * SIZE)
                
                
                    
                if mine != 0:
                    rect = pos_x, pos_y, pos_x+SIZE, pos_y+SIZE
                    pygame.draw.rect(screen, 'white', rect)
                    font = pygame.font.Font(None, 24)
                    
                    if block[POS_Y][POS_X] == block_raw[POS_Y][POS_X]:
                        imgText = font.render(str(mine), 1, 'black')
                    else:
                        imgText = font.render(str(mine), 1, 'blue')
                    
                    screen.blit(imgText, (pos_x, pos_y))
                else:
                    screen.blit(img_dict[mine], (pos_x, pos_y))
                POS_X += 1
            
            
            POS_X = 0
            POS_Y += 1
            

        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)
        
        if check_solution(block):
            game_status = GameStatus.win
            imgText = font.render('WIN!!!', 1, 'red')
            screen.blit(imgText, (0, 0))
        # if game_status == GameStatus.over:
        #     screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        # elif game_status == GameStatus.win:
        #     screen.blit(img_face_success, (face_pos_x, face_pos_y))
        # else:
        #     screen.blit(img_face_normal, (face_pos_x, face_pos_y))

        pygame.display.update()


if __name__ == '__main__':
    main()
