import utilities 


class GA:

    fixedValues = {}

    def __init__(self, popSize,initalValues,genNumber,generationsBeforeRestart,children,mutateRate,selectRate,randSelectRate) :
        self.populationSize = popSize
        self.fixedValues = initalValues
        self.maxGen = genNumber
        self.restartGen = generationsBeforeRestart
        self.numOfChildren = children
        self.mutationRate = mutateRate
        self.selectionRate = selectRate
        self.randomSelectRate = randSelectRate

    def run(self) :
        
        bestScore = None
        worstScore = None
        total_gen = 0
        solFound = False
        restartCount = 0

        while total_gen < self.maxGen and not solFound :
            newPop = utilities.createGeneration(self.populationSize,self.fixedValues)
            generationsDone = 0
            prevBestScore = 0
            genWithoutImprovement = 0

            while generationsDone < self.maxGen and not solFound :
                rankedPop = utilities.rankPopulation(newPop)
                bestSolution = rankedPop[0]
                bestScore = bestSolution.fitnessScore
                worstScore = rankedPop[-1].fitnessScore

                if prevBestScore == bestScore:
                    genWithoutImprovement += 1
                else:
                    prevBestScore = bestScore
                
                if 0 < self.restartGen and self.restartGen < genWithoutImprovement:
                    print("No Improvement for {} generations".format(genWithoutImprovement))
                    print("\nBest solution so far\n")
                    self.print_sudoku(bestSolution.board)    
                    restartCount += 1
                    break

                if bestScore > 0 :
                    print("Problem not solved for generation {} (times restarted {}). Best score is {} and Worst is {}"
                          .format(generationsDone, restartCount, bestScore, worstScore))        
                               
                    nextGenParents = utilities.pickParents(rankedPop,self.selectionRate,self.randomSelectRate)
                    
                    children = utilities.getChildrenFromParents(nextGenParents,self.numOfChildren,self.fixedValues)
                    newPop = utilities.mutatePop(children,self.mutationRate)

                    generationsDone += 1
                    total_gen += 1
                else:
                    print("Solution Found")
                    self.print_sudoku(bestSolution.board)
                    solFound = True
                    print("total amount of generations: ",total_gen, "\n")
        
        if not solFound :
            rankedPop = utilities.rankPopulation(newPop)
            bestSolution = rankedPop[0]
            worstSolution = rankedPop[-1]
            print("Best is:")
            self.print_sudoku(bestSolution.board)
            print("Worst is:")
            self.print_sudoku(worstSolution.board)
            

    def print_sudoku(self, puzzle): 
        for i in range(9): 
            if i % 3 == 0 and i != 0: 
                print("- - - - - - - - - - - ") 
            for j in range(9): 
                if j % 3 == 0 and j != 0: 
                    print(" | ", end="") 
                print(puzzle[i][j], end=" ") 
            print() 
            
                

