from random import shuffle, randint
import numpy as np

class Sudoku :

    def __init__(self, fixedValues) :
        self.fixedValues = fixedValues
        self.board = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]        
        self.grids = {}
        self.cols = {}
        self.fitnessScore = None
        self.fixedValuesIndexs = list(fixedValues.keys())

        for i in range(9):
            self.grids[i] = []
            self.cols[i] = []
        
        for i in range(9) :
            for j in range(9):
                self.board[i][j] = self.fixedValues.get("({},{})".format(str(i),str(j)), 0)
                gridIndex = int(j // 3 + ((i // 3) * 3))
                self.grids[gridIndex].append(self.fixedValues.get("({},{})".format(str(i),str(j)),0))
                colIndex = int(j % 9)
                self.cols[colIndex].append(self.fixedValues.get("({},{})".format(str(i),str(j)),0))

        


    def fillBoard(self) :

        for gindex, grid in self.grids.items() :

            unusedValues = self.getUnusedValues(grid)

            for index, val in enumerate(unusedValues) :
                row = (index // 3) + (3 * (gindex // 3))
                col = (index % 3) + (3 * (gindex % 3))
                self.board[row][col] = val
                self.cols[col][row] = val            
            self.grids[gindex] = unusedValues
        
        return self
    
    def fillBoardWithGrids(self,grids) :

        for gindex, gridVal in enumerate(grids) :

            for index, val in enumerate(gridVal) :
                row = (index // 3) + (3 * (gindex // 3))
                col = (index % 3) + (3 * (gindex % 3))
                self.board[row][col] = val
                self.cols[col][row] = val
            
                self.grids[gindex][index] = val
        return self

    def getUnusedValues(self,grid) :
        
        fixedValues = [value for value in grid if value > 0]
        
        values = [i for i in range(1,10) if not i in fixedValues]
        
        indexs = [(i,val) for (i,val) in enumerate(grid) if val > 0]
        
        shuffle(values)

        for index , value in indexs :
            values.insert(index,value)
        
        return values
   
    def fitness(self):

        if self.fitnessScore is None:
            duplicates = 0
            for i in range(9) :
                duplicates += self.countDuplicates(self.board[i],self.cols[i])
            self.fitnessScore = duplicates
        
        return self.fitnessScore
    
    def countDuplicates(self,row, col) :
        duplicates = 0
        duplicates += len(row) - len(set(row))
        duplicates += len(col) - len(set(col))

        return duplicates

    def swapValues(self) :

        gIndex = np.random.randint(0,8)

        randomIndex1, row1, col1 = self.getRandomNotFixed(gIndex,-1)
        randomIndex2, row2, col2 = self.getRandomNotFixed(gIndex,randomIndex1)

        grid = self.grids[gIndex]
        value1 = grid[randomIndex1]
        value2 = grid[randomIndex2]

        grid[randomIndex1] = value2
        grid[randomIndex2] = value1
        self.cols[col1][row1] = value2
        self.cols[col2][row2] = value1
        self.board[row1][col1] = value2
        self.board[row2][col2] = value1

        index = "({},{})".format(str(row1),str(col1))
        index2 = "({},{})".format(str(row2),str(col2))
        if index in self.fixedValuesIndexs:
            print(index)
        elif index2 in self.fixedValuesIndexs:
            print(index2)
        

        # print("({},{}) : {}".format(row1,col1,value1))
        # print("({},{}) : {}".format(row2,col2,value2))


        return self

    def getRandomNotFixed(self,gridIndex,value) :

        randomIndex = -1
        row = -1
        col = -1
        Fixed = True

        while Fixed or randomIndex == value :
            randomIndex = randint(0,8)
            row = (randomIndex // 3) + (3 * (gridIndex // 3))
            col = (randomIndex % 3) + (3 * (gridIndex % 3))
            index = "({},{})".format(str(row),str(col))
            if index in self.fixedValuesIndexs:
                Fixed = True
            else:
                Fixed = False
        return randomIndex, row, col

        






    

