# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 21:15:34 2016

@author: ruslantrusewych

Night Light Simulation Version 2 

(Version 1 created a 100 x 100 x 100 numpy array to store values 
for the intensity at every point in the space. This is unnecessary since the only relevant points 
in the simualtion are the 200-400 {out of 1,000,000!} where objects are positioned!)
    
Gist of model:
Environment created by randomly positioning objects (from a uniform discrete distribution),and 
initializing object parameters from the normal distribution given the model parameters.
Each iteration calculates the 'local' intensity at every object position and changes the state 
according to the sensitivity of the object. 

The simulation is not deterministic since each object's brightness is randomly generated at
each iteration. 

"""

import numpy as np
import scipy.spatial.distance
from random import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from operator import add
#import time
from itertools import repeat 
import pandas as pd
#import collections
import matplotlib.cm as cm

class Env():
    def __init__(self, num = 250, size = 100, bm = 30.0, bsd = 3.0, sm = 35.0, ssd = 3.0):
        self.num = num      # Number of Objects to be initialized, default is 250.
        self.size = size    # Size of dimension for discretized 3D space, default is 100. Higher dims
                            # could potential create more precise models. 
        self.bm = bm        # Mean for Object's brightness, defualt is 30.
        self.bsd = bsd      # Standard Deviation for Object's brightness, default is 3.
        self.sm = sm        # Mean for Object's sensitivity (The threshold for turning off.) Defualt is 35.
        self.ssd = ssd      # Standard Deviation for Object's sensitivity, default is 3
        self.data = self.initData()                     # Initializes the (majority) of the model: see method comments.
        self.distMatrix = np.zeros([self.num,self.num]) # Initializes the 2D matrix of distnaces between all objects in model.
        self.getDist()      # Pouplates distMatrix with values.
        self.stateHistory = [] # Initalizes the list that records the states of each object at each iteration.
       
    def __str__(self):
        print(self.data)        
        return ""

    def initData(self): # Method to initalize model.
        d = {
            'Position'  : pd.Series(np.random.randint(0,self.size,3)    for i in range(self.num)),  # Position vector: Uniform random.
            'Bright'    : pd.Series(np.random.normal(self.bm,self.bsd)  for i in range(self.num)),  # Brightness: Normal with parameters: bm, bsd.
            'Sense'     : pd.Series(np.random.normal(self.sm,self.ssd)  for i in range(self.num)),  # Sensitivity: Normal with parameters: sm, ssd.
            'Local'     : pd.Series(np.repeat(0.0,self.num)),   # Initializes the Local variable which stores the current brightness at every Object's position.
            'State'     : pd.Series(np.repeat(1,self.num)),     # State = 0 if Object is off, 1 if Object is on.
            'Activity'  : pd.Series(np.repeat(0,self.num))      # Records how long an Object has been on for color coding plotting.
            }
        df = pd.DataFrame(d) # Combines attributes into a pandas DataFrame.
        return df
     
    def getDist(self):  # Creates 2D matrix of distances between all Objects using cdist. Remarkably fast.
        self.distMatrix = scipy.spatial.distance.cdist(self.data.Position.tolist(), self.data.Position.tolist(), 'euclidean')
        self.distMatrix[self.distMatrix == 0] = 1 # Sets distance from Object to itself as 1, avoids division by zero and "normalizes" brightness.
      
    def plotStars(self, index): # Method to plot each state. Explicit for loop adds subplot for each Object. (Slowest aspect of simulation.)
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111, projection='3d')
        mymap = np.array(['#FDEE0D', '#EE9C1C', '#E05E2A', '#D2363C', '#C43F71', '#B64794', '#A64DA8', '#80519A', '#66548C']) # Colormap for coloring objects based on activity.
        for idx, row in self.data.iterrows():
            if row['State'] == 1:             
                ax.scatter(row['Position'][0], row['Position'][1], row['Position'][2], c=mymap[row['Activity']], edgecolor=mymap[row['Activity']], marker='o', s=500, depthshade=True, linewidth=3)
        ax.set_xlim3d([0,self.size])
        ax.set_ylim3d([0,self.size])
        ax.set_zlim3d([0,self.size])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        fig.savefig('images/test' + str(index) + '.png',bbox_inches='tight')        

    def updateEnv(self): # First step in simulation: Calculate intensity matrix brightness/distance^2 and sums of for each star
                         # to calculate local intensity at each Object's location.
        new = (1 / (self.distMatrix*self.distMatrix) * np.array(test.data.Bright)[:, np.newaxis])
        for i in range(self.num):
            self.data.set_value(i,'Local', sum(new[:,i]))

    def updateStates(self): # If Intensity is greater than Object's sensitivity, Object turns off. And vice vera. Activity is recorded.
        for idx, row in self.data.iterrows():
            if row['Local'] > row['Sense']:
                self.data.set_value(idx,'State', 0)
                self.data.set_value(idx,'Activity', 0)                
            elif row['Local'] < row['Sense'] and row['State'] == 0:
                self.data.set_value(idx,'State', 1)
                self.data.set_value(idx,'Activity', 0)             
            if row['State'] == 1 and row['Activity'] == 0: self.data.set_value(idx,'Activity',1) 
            elif row['State'] == 1 and row['Activity'] == 1: self.data.set_value(idx,'Activity',2)
            elif row['State'] == 1 and row['Activity'] == 2: self.data.set_value(idx,'Activity',3)              
            elif row['State'] == 1 and row['Activity'] == 3: self.data.set_value(idx,'Activity',4) 
            elif row['State'] == 1 and row['Activity'] == 4: self.data.set_value(idx,'Activity',5)
            elif row['State'] == 1 and row['Activity'] == 5: self.data.set_value(idx,'Activity',6) 
            elif row['State'] == 1 and row['Activity'] == 6: self.data.set_value(idx,'Activity',7) 
            elif row['State'] == 1 and row['Activity'] == 7: self.data.set_value(idx,'Activity',8)                 
                     
    def recordStates(self): # Records a list of state values and appends to stateHisotry.
        temp = []
        for idx,row in self.data.iterrows():
            temp.append(row['State'])
        self.stateHistory.append(temp)
        
    def updateBright(self): # Method for changing each Object's brightness at each iteration. Produces stochastic, dynamic model.
                            # Without, system enters equilibrium: chess stale mate.
        for idx,row in self.data.iterrows():
            self.data.set_value(idx,'Bright',np.random.normal(self.bm,self.bsd))
            
    def findEquilibrium(self): # Checks for the first time oscillating states are repeated.
        for x in range(3,len(test.stateHistory)):
            if self.stateHistory[x] == self.stateHistory[x-2] and self.stateHistory[x-1] == self.stateHistory[x-3]:
                return x
#==============================================================================
#         eq = collections.Counter(self.stateHistory)
#         return eq
#         
#==============================================================================





#==============================================================================
# testing (will make into __main__ loop eventually)        
#==============================================================================
test = Env(num = 500, size = 100, bm = 30.0, bsd = 3.0, sm = 36.0, ssd = 3.0)
print('\n',test)
for x in range(10):
    print('Iteration %i' % x)
    test.plotStars(x)
    test.updateEnv()
    test.updateStates()
    test.recordStates()
    test.updateBright()

test.findEquilibrium()

#==============================================================================
# will make this into inferential method
#==============================================================================
numOn = []
for x in range(len(test.stateHistory)):
    numOn.append(sum(test.stateHistory[x]))
print(numOn)
numOn = pd.DataFrame(numOn)
print(numOn.mean(),numOn.std())
numOn.hist()

#==============================================================================
# Pandas DF calls for reference (I forget)
# for idx, row in df.iterrows():
#     print(row['Bright'])
# df.set_value(0,'Bright',99)
# print('\n', df[df.bright < 8])
# 
#==============================================================================
 
 
