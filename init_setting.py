# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 19:11:13 2021

@author: Administrator
"""

BLOCK_WIDTH = 9
BLOCK_HEIGHT = 9
SIZE = 20           # 块大小
mask_rate=0.7       # 数独谜题遮盖率

# 游戏屏幕的宽
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
# 游戏屏幕的高
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE