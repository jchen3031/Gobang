# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:16:36 2022

@author: 12129
"""
import random
import numpy as np
import board
import pickle
import sys
class QLearningAgent():
    def __init__(self, alpha = .2, gamma = -.8,eps = .2):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.Q = {}
    def computeQ(self, state, action, reward, newstate):
        Qvalue = self.get_best_action(newstate)
        if (state,action) not in self.Q.keys():
            self.Q[(state,action)] = 0
        self.Q[(state,action)] = (1-self.alpha)*self.Q[(state,action)]+self.alpha*(reward+self.gamma*Qvalue[1])
    def get_best_action(self,state):
        state = str(state)
        m = -999
        action = 0
        for k in self.Q:
            if k[0] == state:
                if m<self.Q[k]:
                    m = self.Q[k]
                    action = k[1]
        return action,m
    def update(self,ls,win):
        pop = ls.pop(-1)
        if win == pop[2]:
            self.Q[(pop[0],pop[1])] = 1
        elif win == -pop[2]:
            self.Q[(pop[0],pop[1])] = 0
        else:
            self.Q[(pop[0],pop[1])] = 0.5
        newstate = pop[0]
        while(True):
            if len(ls) == 0:
                break
            pop = ls.pop(-1)
            if pop[2] == win:
                self.computeQ(pop[0],pop[1],1,newstate)
            elif pop[2] == -win:
                self.computeQ(pop[0],pop[1],-1,newstate)
            else:
                self.computeQ(pop[0],pop[1],.5,newstate)
            newstate = pop[0]
        #print('finish update')
    def simulate(self):
        b = board.board(size = 3, rule = 3)
        state = b.getstate()
        #print(state)
        stone = 1
        ls = []
        while(not b.full()):
            if np.random.uniform()>self.eps:
                i,j = random.choice(state)
            else:
                action, wr = self.get_best_action(state)
                if action!=0:
                    i,j = action
                else:
                    i,j = random.choice(state)
            if b.get(i,j) == 0:
                ls.append((b.board,(i,j),stone))
                b.put(i,j,stone)
                #print(board,i,j,stone)
                if b.checkwin(i,j):
                    #print(f'{stone} win')
                    return ls,stone
                stone = -stone
                state.remove((i,j))
    #print(ls)
        return ls,0
    def train(self,epoch):
        for i in range(epoch):    
            ls,win = self.simulate()
            self.update(ls,win)
            if (i+1) % 2 == 0:
                if i == epoch-1:
                    s = 'finsih update'
                else:
                    s = f'The {i+1}/{epoch} epoch update'
                print('\r',s,end = '')
            sys.stdout.flush()
        print()
    def save(self,file):
        f = open(file,'wb')
        pickle.dump(self.Q, f)
    def load(self,file):
        f = open(file,'rb')
        self.Q = pickle.load(f)
# QAgent = QLearningAgent()
# QAgent.train(1000)
# print(len(QAgent.Q))
