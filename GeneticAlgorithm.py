from src.EvolutiveAlgorithm import EvolutiveAlgorithm
import math
import matplotlib.pyplot as plt

import random
from datetime import datetime
random.seed(datetime.now())


POPULATION_SIZE = 400
GENERATIONS     = 170

SELECTION_RATE = 0.1
CROSSOVER_RATE = 0.1
MUTATION_RATE = 0.1
MUTATION_HILLCLIMBING_RATE=0.1

MAXIMIZE = True

evol = EvolutiveAlgorithm( POPULATION_SIZE, MAXIMIZE )
evol.data = [0,1,2,3,4]

@evol.set_fitness
def fitness(x,data):
    return math.sin(50*x[0])*(20-(x[0]-5)**2)## VAR
    # return (20-(x[0]-5)**2)

@evol.add_func_to_pipeline
@evol.map_process
def selection(population):
    parent1 = random.randint(0,len(population)-1)
    if random.random()<SELECTION_RATE:
        """VARIABLE pop"""
        parent2 = random.randint(0,len(population)-1)
        parent1 = population[parent1]
        parent2 = population[parent2]
        new_ind= parent1["ind"] if evol.compare(parent1,parent2) else parent2["ind"]
        """VARIABLE pop"""
    else:
        new_ind= population[parent1]["ind"]
    return new_ind

@evol.add_func_to_pipeline
@evol.map_process
def crossover(population):
    parent1 = random.randint(0,len(population)-1)
    if random.random()<CROSSOVER_RATE:    
        parent2 = random.randint(0,len(population)-1)
        parent1 = population[parent1]
        parent2 = population[parent2]
        sesgo = [parent1["fit"],parent2["fit"]]
        total = sum(sesgo)
        sesgo = [i/total for i in sesgo]
        # child = [sesgo[0]*parent1["ind"][0]+sesgo[1]*parent2["ind"][0],sesgo[0]*parent1["ind"][1]+sesgo[1]*parent2["ind"][1]]
        # child = [sesgo[0]*parent1["ind"][0]+sesgo[1]*parent2["ind"][0]]
        max_parent = parent1["ind"] if evol.compare(parent1,parent2) else parent2["ind"]
        min_parent = parent1["ind"] if not evol.compare(parent1,parent2) else parent2["ind"]
        new_ind=[random.random()*(max_p-min_p)+min_p for max_p,min_p in zip(max_parent,min_parent)]
    else:
        new_ind=population[parent1]["ind"]
    return new_ind

@evol.add_func_to_pipeline
@evol.map_process
def mutation(population):
    new_ind= {"ind":[random.random()*10],"fit":0,"Type":None}
    temp_best = evol.compare_list(population,key=lambda a:a['fit'])
    parent1 = random.randint(0,len(population)-1)
    dir_vect=[]
    if(random.random()<MUTATION_RATE):
        if(random.random()<MUTATION_HILLCLIMBING_RATE):
            # dir_vect = [temp_best['ind'][0]-population[parent1]['ind'][0],temp_best['ind'][1]-population[parent1]['ind'][1]] 
            dir_vect = [temp_best['ind'][0]-population[parent1]['ind'][0]] 
            dir_mod = 1 if evol.compare(temp_best,population[parent1]) else -1
            dir_vect=[i*dir_mod*random.random() for i in dir_vect]
        else:
            mod = random.random()     
            dir_vect.append((0.5 if random.random()>0.5 else -0.5)*mod)
            dir_vect.append((0.5 if random.random()>0.5 else -0.5)*mod)
        # child = [population[parent1]["ind"][0]+dir_vect[0]*random.random(),population[parent1]["ind"][1]+dir_vect[1]*random.random()]
        new_ind= [population[parent1]["ind"][0]+dir_vect[0]]
    else:
        new_ind= population[parent1]["ind"] 
    return new_ind

@evol.set_ind_func
def new_ind():
    # return {"ind":[random.random(),random.random()*8-4],"fit":0}
    return {"ind":[random.random()*10],"fit":0}

if __name__=='__main__':
    evol.run(generations=GENERATIONS)
    print(evol.best_all)
    print(evol.best_last)

    _x = [i[0] for i in evol.fitness_evolution]
    _y = [i[1] for i in evol.fitness_evolution]

    # print(_x)
    # print(_y)

    plt.scatter(x=_x,y=_y)
    plt.show()