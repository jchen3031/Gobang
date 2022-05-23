# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:16:36 2022

@author: 12129
"""
import random
import numpy as np
import board
import tensorflow as tf
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
import time
class DeepQLearningAgent():
    def __init__(self, alpha = .2, DISCOUNT = -.99,eps = .9,MINIBATCH_SIZE = 16, size = 15, rule = 5):
        self.size = size
        self.rule = rule
        self.alpha = alpha
        self.eps = eps
        self.model = self.create_model()

        self.target_model = self.create_model()
        self.DISCOUNT = DISCOUNT
        self.MINIBATCH_SIZE = MINIBATCH_SIZE
        self.count = 0
        
        self.states = []
        self.newstates = []
        self.actions = []
        self.rewards = []
        self.MAXINT = 10
        self.update_count = 0
        #self.target_model.set_weights(self.model.get_weights())
    def computeQ(self, states, actions, rewards, newstates):
        current_qs_list = self.model.predict(np.expand_dims(states,-1), verbose=0)
        future_qs_list = self.target_model.predict(np.expand_dims(newstates,-1),verbose=0)
        X = []
        y = []

        # Now we need to enumerate our batches
        for index, (state, action, reward, newstate) in enumerate(zip(states, actions, rewards, newstates)):
            current_qs = current_qs_list[index]
            max_future_q = np.max(future_qs_list[index])
            new_q = (1-self.alpha)*current_qs[action]+ self.alpha*(reward + self.DISCOUNT * max_future_q)
            current_qs[action] = new_q
            X.append(state)
            y.append(current_qs)

        # Fit on all samples as one batch, log only on terminal state
        self.model.fit(np.array(X), np.array(y), batch_size=self.MINIBATCH_SIZE, verbose=0)
        if self.update_count == self.MAXINT:
            self.target_model.set_weights(self.model.get_weights())
            self.update_count = 0
            
        self.update_count+=1
    def update(self,ls,win):
        pop = ls.pop(-1)
        states = []
        newstates = []
        rewards = []
        actions = []
        if win == pop[2]:
            rewards.append(100)
        elif win == 0:
            rewards.append(50)
        else:
            rewards.append(-100)
        states.append(pop[0])
        newstates.append(pop[0])
        newstate = pop[0]
        actions.append(pop[1])
        while(True):
            if len(ls) == 0:
                break
            pop = ls.pop(-1)
            if pop[2] == win:
                rewards.append(10)
            elif win == 0:
                rewards.append(5)
            else:
                rewards.append(-10)
            
            states.append(pop[0])
            newstates.append(newstate)
            actions.append(pop[1])
            newstate = pop[0]
        #print('finish update')
        #print(states)
        self.states += states
        self.newstates += newstates
        self.actions += actions
        self.rewards += rewards
        if self.count == self.MAXINT:
            self.computeQ(self.states, self.actions, self.rewards, self.newstates)
            self.count = 0
            self.eps *= .99
            if len(self.states) > 0:
                self.states = []
                self.newstates = []
                self.actions = []
                self.rewards = []
        self.count+=1
    def simulate(self):
        b = board.board(size = self.size, rule = self.rule)
        state = b.getstate()
        #print(state)
        turn = True
        stone = 1 if turn else 2
        ls = []
        while(not b.full()):
            if np.random.uniform()<self.eps:
                action = random.choice(state)
            else:
                action = np.argmax(self.get_qs(b.board))
                if action not in state:
                    action = random.choice(state)
            i,j = b.get_from_action(action)
            if b.get(i,j) == 0:
                ls.append((b.board.copy(),action,stone))
                b.put(i,j,stone)
                #print(board,i,j,stone)
                if b.checkwin(i,j):
                    #print(f'{stone} win')
                    return ls,stone
                turn = not turn
                stone = 1 if turn else 2
                state.remove(action)
    #print(ls)
        return ls,0
    def get_qs(self,state):
        state = np.expand_dims(state,-1)
        state = np.expand_dims(state,0)
        #print(state.shape)
        return self.model.predict(state,verbose = 0)[0]
    def train(self,epoch):
        start = time.time()
        for i in range(epoch):    
            ls,win = self.simulate()
            self.update(ls,win)
            if (i+1) % self.MAXINT == 0:
                if i == epoch-1:
                    s = f'finsih update, takes {time.time()- start} seconds'
                else:
                    s = f'The {i+1}/{epoch} epoch update'
                print('\r',s,end = '')
        print()
        print(f'eps = {self.eps}')
    def save(self, i = ''):
        self.model.save(f'DQN{i}.h5')
        self.target_model.save(f'TDQN{i}.h5')
    def load(self,i = ''):
        self.model = tf.keras.models.load_model(f'DQN{i}.h5')
        self.target_model = tf.keras.models.load_model(f'TDQN{i}.h5')
    def create_model(self):
        model = Sequential()

        model.add(Conv2D(256, 5,1,padding= 'same',input_shape=(self.size,self.size,1)))  # OBSERVATION_SPACE_VALUES = (10, 10, 3) a 10x10 RGB image.
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2),padding = 'same'))
        model.add(Dropout(0.2))

        #model.add(Conv2D(256, 3,1, padding= 'same'))
        #model.add(Activation('relu'))
        #model.add(MaxPooling2D(pool_size=(2, 2),padding = 'same'))
        #model.add(Dropout(0.2))

        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(64))

        model.add(Dense(self.size**2))  # ACTION_SPACE_SIZE = how many choices (9)
        model.compile(loss='mse',
                  optimizer= 'adam',
                  metrics=['accuracy'])
        return model
# QAgent = QLearningAgent()
# QAgent.train(1000)
# print(len(QAgent.Q))
