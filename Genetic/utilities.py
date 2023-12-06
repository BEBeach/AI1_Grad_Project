from sudoku import Sudoku
import numpy as np
import random

def createGeneration(popSize,values) :

    population = []
    for i in range(popSize) :
        population.append(Sudoku(values).fillBoard())
    return population

def rankPopulation(population) :
    scores = {}
    for board in population : 
        scores[board] = board.fitness()
    return sorted(scores, key=scores.get)

def pickParents(rankedPop,selectionRate,randomSelectRate) :

    parents = []

    best = int(len(rankedPop) * selectionRate)
    random = int(len(rankedPop) * randomSelectRate)

    for i in range(best) :
        parents.append(rankedPop[i])
    for j in range(random):
        parents.append(rankedPop[j])

    np.random.shuffle(parents)
    return parents

def getChildrenFromParents(parents,numChildren,fixedValues) :
    
    nextGen = []

    rangeValue = int(len(parents)/2) * numChildren

    for _ in range(rangeValue) :
        mother = random.choice(parents)
        father = random.choice(parents)
        offspring = createChild(father,mother,fixedValues)
        nextGen.append(offspring)
    return nextGen

def mutatePop(population,mutationRate) :

    newPop = []

    for board in population: 
        if np.random.random() < mutationRate:
            board = board.swapValues()
        newPop.append(board)
    return newPop

def createChild(father,mother,fixedValues):

    numOfMomGrids = np.random.randint(0,9,np.random.randint(1,8))

    childGrids = []

    for i in range(9) :
        if i in numOfMomGrids : 
            childGrids.append(mother.grids[i])
        else :
            childGrids.append(father.grids[i])
    return Sudoku(fixedValues).fillBoardWithGrids(childGrids)



