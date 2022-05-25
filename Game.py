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
f = open('Q','rb')
Q = pickle.load(f)

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.list_modes()
pygame.display.set_caption("TicTacToe")
# pygame.mouse.set_visible(False)
# pygame.event.set_grab(True)
withAI = True
running = True
b = [[0 for i in range(3)] for i in range(3)]
player = True
stop = False
AI = True
def full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True
def out_bound(i,j):
    return i <0 or j <0 or i>2 or j>2
def checkwin(board,i,j,stone):
    c = 0
    c1 = 0
    for a in range(3):
        if board[a][j] == stone:
            c+=1
    for a in range(3):
        if board[i][a] == stone:
            c1+=1
    c2 = 0
    for a in range(3):
        if board[a][a] == stone:
            c2+=1
    c3 = 0
    for a in range(3):
        if board[a][2-a] == stone:
            c3+=1
    return c == 3 or c1 == 3 or c2 == 3 or c3 == 3
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
    size = 128
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
            ls = [64+i*size for i in range(3)]
            i = 0
            j = 0
            for n in range(len(ls)):
                if abs(ls[n]-x) < 64:
                    i = n
                if abs(ls[n]-y) < 64:
                    j = n
            b[i][j] = stone
            if checkwin(b,i,j,stone):
                print(f'stone {stone} win')
                stop = True
            print(x,y)
        if event.type == pygame.MOUSEBUTTONUP:
            player = not player
    screen.fill((255,255,255))
    if full(b) and not stop:
        print('tie')
        stop = True
    if withAI and player == AI and not stop:
        stone = 1 if player else -1
        action,wr = get_best_action(Q,b)
        i,j = action
        b[i][j] = stone
        player = not player
    for i in range(0,3):
        for j in range(0,3):
            a = '#008000'
            rp = (j*size,i*size)
            rs = (size, size)
            pygame.draw.rect(screen, a, Rect(rp,rs))
    for i in range (1,3):
        pygame.draw.line(screen, (0, 0, 0), (i*size, 0), (i*size, 3*size))
    for j in range (1,3):
        pygame.draw.line(screen, (0, 0, 0), (0, j*size), (3*size, j*size))
    for i in range(3):
        for j in range(3):
            if b[i][j] == 1:
                pygame.draw.circle(screen,(0,0,0),(64+i*size,64+j*size),60)
            elif b[i][j] == -1:
                pygame.draw.circle(screen,(255,255,255),(64+i*size,64+j*size),60)
    pygame.display.update()