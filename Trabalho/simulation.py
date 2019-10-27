import pygame
from pygame_run import *
from game import *
import copy
import random
import numpy as np
import time

def valide_start_point(grid):
    valide = []
    for row in grid:
        aux = []
        
        aux = list(filter(lambda x:x.color !=3,row))
        for i in aux:
            valide.append((i.y,i.x))

    #print(valide)
    return valide





def go():
  

    #NUMERO DE TICKS
    ticks =10000
    #ESTRATEGIAS ADOTADAS
    simulation_on_screen = True
    time_strategy =False
    evaporation_strategy = True
    quandrant_strategy = True

    #PARAMETROS DE SIMULAÇAO
    evap_time = 1
    evap_factor =  0.83
    threshold_time = 0
    num_simulations = 30
    #NUMERO DE VANTs
    number_drones = 4

    #TRUE PARA RODAR E FALSE PARA RODAR PASSO A PASSO 
    run = True


    #OUTRAS ESTRATEGIAS QUE FORAM DESCARTADAS
    communication_strategy = False
    watershed_strategy = False
    type_A = True
    watershed_time = 0
    communication_time = 0
    water_threshold =0

    color =0
    #INICIALIZAÇAO
    metrics_results = []
    grid_size = 8
    initial_grid = []

    for row in range(grid_size):
        initial_grid.append([])
        for column in range(grid_size):
            aux_patch = patch(u_value = 0,x = row,y = column,color = color,intervals = [],visites = 0,visita_anterior = 0)
            initial_grid[row].append(aux_patch)
            if color==0:
                color =1
            else:
                color= 0
        if color==0:
            color =1
        else:
            color= 0       
    for i in range(num_simulations):
        grid = []
        grids = []
        grid = copy.deepcopy(initial_grid)


        #ADCIONAR OBSTACULOS (BASTA DESCOMENTAR)

        #make_obstacles1(grid)
        #make_obstacles2(grid)
        #make_obstacles3(grid)
        if communication_strategy == True:    
            for j in range(number_drones):
                grids.append(copy.deepcopy(initial_grid))
            
        drones  = []
        drones2 = []
        if quandrant_strategy:
            if type_A:
                for k in range(0,8):
                    if k%2 != 0:
                        drone  = Drone(x = k,y = 0,label = 1,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                        drones.append(drone)
                for k in range(0,8):
                    if k%2 == 0:
                        drone  = Drone(x = k,y = 1,label = 1,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)   
                        drones.append(drone)
                for k in range(1,8):
                    if k%2 != 0:
                        drone  = Drone(x = k,y = 2,label = 2,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                        drones.append(drone)




                for k in range(0,8):
                    if k%2 == 0:
                        drone  = Drone2(x = k,y = 5,label = 1,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                        drones2.append(drone)
                for k in range(0,8):
                    if k%2 != 0:
                        drone  = Drone2(x = k,y = 6,label = 1,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)   
                        drones2.append(drone)
                for k in range(0,8):
                    if k%2 == 0:
                        drone  = Drone2(x = k,y = 7,label = 2,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                        drones2.append(drone)
            #drones.append(drone3)
        else:
            for num in range(number_drones):
                drone  = Drone(x = -1,y = 49,label = None,manouvers = 0, direction =(1,1),time_base =time_strategy ,time_threshold = threshold_time,communication_strategy = communication_strategy)
                drones.append(drone)

        

        if simulation_on_screen:
            select_initial_state(drones = drones,drones2 = drones2, grid = grid,grids = grids,ticks = ticks, run  =run   ,communication_strategy = communication_strategy, evap_strategy = evaporation_strategy, et = evap_time, ef = evap_factor)

    return








if '__main__' == __name__:
    inicio = time.time()
    go()
    fim = time.time()
    print('tempo de execução = ',fim - inicio)