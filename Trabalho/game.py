import pygame
import math
import random
import numpy as np
from functools import reduce
import statistics
import copy
class Drone:
    def __init__(self,x = 0 , y=0,manouvers = 0,direction = (0,0),time_base = False, time_threshold = 0,communication_strategy = False,label = None):
        self.x = x
        self.y = y
        self.posBoard = ((x*91) +5,(y*91) +3)
        self.direction = direction
        self.manouvers = manouvers
        self.time_base = time_base
        self.time_threshold = time_threshold
        self.communication_strategy = communication_strategy
        self.path_water = []
        self.watershed_mode = False
        self.label = label
    
    def getBoardPos(self):

        return self.posBoard
    def move(self,grid,tick,grid_aux):
        if(self.y != -1 and self.x!= -1 and self.x<50):
            grid[self.y][self.x].color=1
            

        if len(self.path_water)>0:
            #for i in self.path_water:
             #   grid[i.x][i.y].color = 1
            #self.getSucessor(grid = grid,grid_aux = [])
            if self.path_water[-1].occupied== False:
                path = self.path_water.pop(-1)
                x = self.y
                y = self.x
                if x+1 == path.x:
                    path.dir_from_drone = (1,0)
                if x-1 == path.x:
                    path.dir_from_drone = (0,1)
                if y+1 == path.y:
                    path.dir_from_drone = (1,1)
                if y-1 == path.y:
                    path.dir_from_drone = (0,0)
                path.cost = abs((self.direction[0]-path.dir_from_drone[0]) + (self.direction[1]-path.dir_from_drone[1]))
                sucessors = [path]
            else:
                sucessors = []

        else:
            self.watershed_mode = False
            if self.time_base == True:
                sucessors = self.get_sucessor_time_base(grid,grid_aux)
            
            else :
                if self.communication_strategy:
                    sucessors = self.getSucessor(grid = grid_aux,grid_aux = grid)
                else : 
                    sucessors = self.getSucessor(grid = grid,grid_aux = grid_aux)
        if len(sucessors)==0:
            return grid,grid_aux

      
        sucessor = random.choice(sucessors)
        sucessor.occupied = True
        sucessor.visites+=1
        sucessor.u_value = sucessor.visites

        if self.communication_strategy:
            grid_aux[self.y][self.x].occupied = False
            grid[self.y][self.x].occupied = False
            grid[sucessor.x][sucessor.y].occupied = True
        else:
            if self.x<50:
                grid[self.y][self.x].occupied = False

        self.manouvers+=sucessor.cost
        self.direction = sucessor.dir_from_drone
        self.x = sucessor.y
        self.y = sucessor.x
        grid[self.y][self.x].intervals.append(tick -grid[self.y][self.x].visita_anterior)
        grid[self.y][self.x].visita_anterior = tick
        self.posBoard = [(self.x*15) +1,(self.y*15) +1] 
        
        return grid,grid_aux
    def getSucessor(self,grid,grid_aux):
        x = self.y
        y = self.x
        sucessors = []
        new_sucessors = []
        if  valide(x+1,y,grid,grid_aux,label = self.label):
            grid[x+1][y].dir_from_drone = (1,0)
            sucessors.append(grid[x+1][y])
        if valide(x-1,y,grid,grid_aux,label = self.label):
            grid[x-1][y].dir_from_drone = (0,1)
            sucessors.append(grid[x-1][y])
        if valide(x,y+1,grid,grid_aux,label = self.label):
            grid[x][y+1].dir_from_drone = (1,1)
            sucessors.append(grid[x][y+1])
        if valide(x,y-1,grid,grid_aux,label = self.label):
            grid[x][y-1].dir_from_drone = (0,0)
            sucessors.append(grid[x][y-1])
        if len(sucessors)==0:
            return []
        minimum_uvalue = min(sucessors,key = lambda x: x.u_value).u_value
        new_sucessors = list(filter(lambda x : x.u_value <= minimum_uvalue,sucessors))
        for suc in new_sucessors:
            suc.cost = abs((self.direction[0]-suc.dir_from_drone[0]) + (self.direction[1]-suc.dir_from_drone[1]))

        cost =  min(new_sucessors, key = lambda x: x.cost).cost
        new_sucessors = list(filter(lambda x : x.cost <= cost,new_sucessors))
        return new_sucessors
        
    def get_sucessor_time_base(self,grid,grid_aux):
        sucessors = self.getSucessor(grid,grid_aux)
        if len(sucessors)>1:
            if(abs(sucessors[0].visita_anterior - sucessors[1].visita_anterior)>=self.time_threshold ):
                
                min_visita = min(sucessors,key = lambda x: x.visita_anterior).visita_anterior
                   # sucessor = min(sucessors,key = lambda x: x.visita_anterior)
                sucessors = list(filter(lambda x : x.visita_anterior <= min_visita,sucessors))
            
        return (sucessors)



class Drone2:
    def __init__(self,x = 0 , y=0,manouvers = 0,direction = (0,0),time_base = False, time_threshold = 0,communication_strategy = False,label = None):
        self.x = x
        self.y = y
        self.posBoard = ((x*91),(y*91) )
        self.direction = direction
        self.manouvers = manouvers
        self.time_base = time_base
        self.time_threshold = time_threshold
        self.communication_strategy = communication_strategy
        self.path_water = []
        self.watershed_mode = False
        self.label = label
    
    def getBoardPos(self):

        return self.posBoard
    def move(self,grid,tick,grid_aux):
        if(self.y != -1 and self.x!= -1 and self.x<50):
            grid[self.y][self.x].color=1
            

        if len(self.path_water)>0:
            #for i in self.path_water:
             #   grid[i.x][i.y].color = 1
            #self.getSucessor(grid = grid,grid_aux = [])
            if self.path_water[-1].occupied== False:
                path = self.path_water.pop(-1)
                x = self.y
                y = self.x
                if x+1 == path.x:
                    path.dir_from_drone = (1,0)
                if x-1 == path.x:
                    path.dir_from_drone = (0,1)
                if y+1 == path.y:
                    path.dir_from_drone = (1,1)
                if y-1 == path.y:
                    path.dir_from_drone = (0,0)
                path.cost = abs((self.direction[0]-path.dir_from_drone[0]) + (self.direction[1]-path.dir_from_drone[1]))
                sucessors = [path]
            else:
                sucessors = []

        else:
            self.watershed_mode = False
            if self.time_base == True:
                sucessors = self.get_sucessor_time_base(grid,grid_aux)
            
            else :
                if self.communication_strategy:
                    sucessors = self.getSucessor(grid = grid_aux,grid_aux = grid)
                else : 
                    sucessors = self.getSucessor(grid = grid,grid_aux = grid_aux)
        if len(sucessors)==0:
            return grid,grid_aux

      
        sucessor = random.choice(sucessors)
        sucessor.occupied = True
        sucessor.visites+=1
        sucessor.u_value = sucessor.visites

        if self.communication_strategy:
            grid_aux[self.y][self.x].occupied = False
            grid[self.y][self.x].occupied = False
            grid[sucessor.x][sucessor.y].occupied = True
        else:
            if self.x<50:
                grid[self.y][self.x].occupied = False

        self.manouvers+=sucessor.cost
        self.direction = sucessor.dir_from_drone
        self.x = sucessor.y
        self.y = sucessor.x
        grid[self.y][self.x].intervals.append(tick -grid[self.y][self.x].visita_anterior)
        grid[self.y][self.x].visita_anterior = tick
        self.posBoard = [(self.x*15) +1,(self.y*15) +1] 
        
        return grid,grid_aux
    def getSucessor(self,grid,grid_aux):
        x = self.y
        y = self.x
        sucessors = []
        new_sucessors = []
        if  valide(x+1,y,grid,grid_aux,label = self.label):
            grid[x+1][y].dir_from_drone = (1,0)
            sucessors.append(grid[x+1][y])
        if valide(x-1,y,grid,grid_aux,label = self.label):
            grid[x-1][y].dir_from_drone = (0,1)
            sucessors.append(grid[x-1][y])
        if valide(x,y+1,grid,grid_aux,label = self.label):
            grid[x][y+1].dir_from_drone = (1,1)
            sucessors.append(grid[x][y+1])
        if valide(x,y-1,grid,grid_aux,label = self.label):
            grid[x][y-1].dir_from_drone = (0,0)
            sucessors.append(grid[x][y-1])
        if len(sucessors)==0:
            return []
        minimum_uvalue = min(sucessors,key = lambda x: x.u_value).u_value
        new_sucessors = list(filter(lambda x : x.u_value <= minimum_uvalue,sucessors))
        for suc in new_sucessors:
            suc.cost = abs((self.direction[0]-suc.dir_from_drone[0]) + (self.direction[1]-suc.dir_from_drone[1]))

        cost =  min(new_sucessors, key = lambda x: x.cost).cost
        new_sucessors = list(filter(lambda x : x.cost <= cost,new_sucessors))
        return new_sucessors
        
    def get_sucessor_time_base(self,grid,grid_aux):
        sucessors = self.getSucessor(grid,grid_aux)
        if len(sucessors)>1:
            if(abs(sucessors[0].visita_anterior - sucessors[1].visita_anterior)>=self.time_threshold ):
                
                min_visita = min(sucessors,key = lambda x: x.visita_anterior).visita_anterior
                   # sucessor = min(sucessors,key = lambda x: x.visita_anterior)
                sucessors = list(filter(lambda x : x.visita_anterior <= min_visita,sucessors))
            
        return (sucessors)
        
        
class patch: 
    
    def __init__(self,u_value = 0,x = None , y=None,color = 0,dir_from_drone = (0,0),cost = 0,intervals = [],visites = 0,visita_anterior = 0):
        self.u_value = u_value
        self.x = x
        self.y = y
        self.color = color
        self.dir_from_drone = dir_from_drone
        self.cost = cost
        self.intervals = intervals
        self.visites = visites
        self.visita_anterior = visita_anterior
        self.occupied = False
