# -*- coding: utf-8 -*-
"""
Created on Thu May 12 22:18:41 2022

@author: 12129
"""
import numpy as np
class board:
    def __init__(self, size = 15, rule = 5):
        self.board = np.zeros((size,size),dtype = int)
        self.size = size
        self.mapping = [(i,j) for i in range(size) for j in range(size)]
        self.rule = rule
    def put(self,i,j,stone):
        if self.board[i,j] == 0:
            self.board[i,j] = stone
        else:
            return False
    def get(self,i,j):
        return self.board[i,j]
    def __str__(self):
        s = []
        for i in range(self.size):
            for j in range(self.size):
                s.append(self.board[i,j]) 
        return str(s).strip('][')
    def checkbound(self,i,j):
        return i <0 or i>=self.size or j <0 or j>=self.size
    def full(self):
        b = self.board
        for i in range(self.size):
            for j in range(self.size):
                if b[i,j] == 0:
                    return False
        return True
    def checkwin(self,i,j):
        b = self.board
        stone = b[i,j]
        c = 0
        for u in range(i-self.rule+1,i+self.rule):
            if self.checkbound(u, j):
                continue
            if b[u,j] == stone:
                c+=1
            else:
                c=0
                continue
            if c == self.rule:
                return True
        c = 0
        for u in range(j-self.rule+1,j+self.rule):
            if self.checkbound(i, u):
                continue
            if b[i,u] == stone:
                c+=1
            else:
                c=0
                continue
            if c == self.rule:
                return True
        c = 0
        for u in range(-self.rule+1,self.rule):
            if self.checkbound(i+u,j+u):
                continue
            if b[i+u,j+u] == stone:
                c+=1
            else:
                c=0
                continue
            if c == self.rule:
                return True
        c = 0
        for u in range(-self.rule+1,self.rule):
            if self.checkbound(i-u,j+u):
                continue
            if b[i-u,j+u] == stone:
                c+=1
            else:
                c=0
                continue
            if c == self.rule:
                return True
        return False
    def reset(self):
        self.board = np.zeros((self.size,self.size))
    def getstate(self):
        ls = []
        flatten = self.board.flatten()
        for i,pos in enumerate(flatten):
            if pos == 0:
                ls.append(i)
        return ls
    def get_from_action(self, action):
        return self.mapping[action]
#b = board()
# print(b.full())
# b.put(2, 2, 1)
# for i in range(3,3+5):
#     if i != 4:
#         b.put(i, 5, 1)
# print(b)
# print(b.checkwin(5, 5))
# b = board()
# b.put(1, 1, 1)
# print(b.getstate())
# print(b.get_from_action(16))