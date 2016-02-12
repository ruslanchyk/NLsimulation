# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 21:15:34 2016

@author: ruslantrusewych
"""

import numpy as np
import scipy.spatial.distance
from random import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from operator import add
import time
from itertools import repeat 
import pandas as pd
import collections
import matplotlib.cm as cm

class Env():
    def __init__(self, num = 10, size = 100, bm = 10.0, bsd = 3.0, sm = 12.0, ssd = 3.0):
        self.num = num
        self.size = size
        self.bm = bm
        self.bsd = bsd
        self.sm = sm
        self.ssd = ssd
        self.data = self.initData()
        self.distMatrix = np.zeros([self.num,self.num])
        self.getDist()
        self.stateHistory = []
       
    def __str__(self):
        print(self.data)        
        return ""

    def initData(self):      
        d = {
            'Position'  : pd.Series(np.random.randint(0,self.size,3)    for i in range(self.num)),
            'Bright'    : pd.Series(np.random.normal(self.bm,self.bsd)  for i in range(self.num)),
            'Sense'     : pd.Series(np.random.normal(self.sm,self.ssd)  for i in range(self.num)),
            'Local'     : pd.Series(np.repeat(0.0,self.num)),
            'State'     : pd.Series(np.repeat(1,self.num)),
            'Activity'  : pd.Series(np.repeat(0,self.num))
            }
        df = pd.DataFrame(d)
        return df
     
    def getDist(self):
        self.distMatrix = scipy.spatial.distance.cdist(self.data.Position.tolist(), self.data.Position.tolist(), 'euclidean')
        self.distMatrix[self.distMatrix == 0] = 1
      
    def plotStars(self, index):
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111, projection='3d')
        mymap = np.array(['#FDEE0D', '#EE9C1C', '#E05E2A', '#D2363C', '#C43F71', '#B64794', '#A64DA8', '#80519A', '#66548C'])

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

    def updateEnv(self):
        new = (1 / (self.distMatrix*self.distMatrix) * np.array(test.data.Bright)[:, np.newaxis])
        for i in range(self.num):
            self.data.set_value(i,'Local', sum(new[:,i]))

    def updateStates(self):
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
                     
    def recordStates(self):
        temp = []
        for idx,row in self.data.iterrows():
            temp.append(row['State'])
        self.stateHistory.append(temp)
        
    def updateBright(self):
        for idx,row in self.data.iterrows():
            self.data.set_value(idx,'Bright',np.random.normal(self.bm,self.bsd))
            
    def findEquilibrium(self):
        for x in range(2,len(test.stateHistory)):
            if test.stateHistory[x] == test.stateHistory[x-2]:
                return x
#==============================================================================
#         eq = collections.Counter(self.stateHistory)
#         return eq
#         
#==============================================================================





#==============================================================================
# testing        
#==============================================================================
test = Env(num = 500, size = 100, bm = 30.0, bsd = 3.0, sm = 36.0, ssd = 3.0)
print('\n',test)
for x in range(100):
    print('Iteration %i' % x)
    test.plotStars(x)
    test.updateEnv()
    test.updateStates()
    test.recordStates()
    test.updateBright()
