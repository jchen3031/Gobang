# -*- coding: utf-8 -*-
"""
Created on Thu May 12 22:17:22 2022

@author: 12129
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 12 18:50:04 2022

@author: 12129
"""

from pygame.locals import *
#导入一些常用的函数和常量
from sys import exit
import pygame
from pygame import KEYDOWN
import numpy as np
import pickle
import board
from QAgent import QLearningAgent
f = open('GobangQ','rb')
Q = pickle.load(f)
QA = QLearningAgent()
QA.Q = Q
b = board.board(size = 15)
#print(b)
pygame.init()
screen = pygame.display.set_mode((1280, 960), 0, 32)
pygame.display.list_modes()
pygame.display.set_caption("Gobang")
# pygame.mouse.set_visible(False)
# pygame.event.set_grab(True)
withAI = True
running = True
player = True
stop = False
AI = True
hp = 96
def get_best_action(Q,state):
    state = str(state)
    m = -999
    action = 0
    for k in Q:
        if k[0] == state:
            if m<Q[k]:
                m = Q[k]
                action = k[1]
    return action,m
while running:
    size = 48
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if str(event.key) == '100': # 按 D 键（键码100）会立即退出
                print('get key ', str(event.key))
                running = False
                print('quit game. Thanks for playing!')
                exit()
            if str(event.key) == '119': # 按 w 键（键码119）
                print('get key ', str(event.key)) 
                print('reset the game!!!')
                b.reset()
                
        if event.type == pygame.MOUSEBUTTONDOWN and not stop:
            stone = 1 if player else -1
            x,y = pygame.mouse.get_pos()
            ls = [24+i*size+hp for i in range(b.size)]
            i = 0
            j = 0
            for n in range(len(ls)):
                if abs(ls[n]-x) < 24:
                    i = n
                if abs(ls[n]-y) < 24:
                    j = n
            b.put(i,j,stone)
            if b.checkwin(i,j):
                print(f'stone {stone} win')
                stop = True
            print(x,y)
        if event.type == pygame.MOUSEBUTTONUP:
            player = not player
    screen.fill((255,255,255))
    if b.full() and not stop:
        print('tie')
        stop = True
    if withAI and player == AI and not stop:
        stone = 1 if player else -1
        action,wr = QA.get_best_action(b)
        i,j = action
        b.put(i, j, stone)
        player = not player
    for i in range(2,b.size+2):
        for j in range(2,b.size+2):
            a = '#008000'
            rp = (j*size,i*size)
            rs = (size, size)
            pygame.draw.rect(screen, a, Rect(rp,rs))
    # a = '#008000'
    # rp = (b.size*size,b.size*size)
    # rs = (size, size)
    # pygame.draw.rect(screen, a, Rect(rp,rs))
    for i in range (1,b.size):
        pygame.draw.line(screen, (0, 0, 0), (i*size+hp, hp), (i*size+hp, b.size*size+hp))
    for j in range (1,b.size):
        pygame.draw.line(screen, (0, 0, 0), (hp, j*size+hp), (b.size*size+hp, j*size+hp))
    for i in range(b.size):
        for j in range(b.size):
            if b.get(i,j) == 1:
                pygame.draw.circle(screen,(0,0,0),(24+i*size+hp,24+j*size+hp),20)
            elif b.get(i,j) == -1:
                pygame.draw.circle(screen,(255,255,255),(24+i*size+hp,24+j*size+hp),20)
    pygame.display.update()