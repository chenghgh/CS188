import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            '''
            Increase the success rate of the local search.
            If change the iteration from 100 to 1000,
            the autograder will up to 30/30
            '''
            if newNumberOfAttacks == 0 or (i >= 100 and currentNumberOfAttacks<=newNumberOfAttacks):
                break
            # if currentNumberOfAttacks <= newNumberOfAttacks:
            #     break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        minAttack=self.getNumberOfAttacks()
        costBoard = self.getCostBoard()

        # print("----")
        # print("Begin:",self.getCostBoard().squareArray)
        # print("End")
        # print("currentAttack:", minAttack)
        # Find the minimum number of attacks of the current board
        colList = []
        for row in range(0,8):
            tmp = min(costBoard.squareArray[row])
            if tmp < minAttack:
                minAttack = tmp;

        for row in range(0,8):
            for col in range(0,8):
                if costBoard.squareArray[row][col] == minAttack:
                    colList.append((row, col))

        # Have found the correct solution
        if len(colList) == 0:
            return (self, minAttack, -1, -1)

        colIndex = random.randint(0, len(colList)-1)
        newRow, newCol = colList[colIndex]

        '''
        This will change the queen's position, even the number of the minimum attacks
        is same with the number of current attacks.
        If change the position randomly, the situation will change and the result may be better.
        '''
        oldCol = [a[newCol] for a in self.squareArray]
        oldRow = oldCol.index(1)
        self.squareArray[oldRow][newCol] = 0
        self.squareArray[newRow][newCol] = 1

        return (self, minAttack, newRow, newCol)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        '''
        Calculate the attacks.
        If the two columns is same, then there is an attack.
        If the distance of the queens' position in the two column
        is same with the value of (j-i), then there is an attack(diagonal).
        '''
        numberOfAttacks = 0
        for i in range(0,7):
            col1 = [a[i] for a in self.squareArray]
            for j in range(i+1, 8):
                col2 = [a[j] for a in self.squareArray]
                if col1 == col2 or abs(col1.index(1) - col2.index(1)) == (j-i):
                    numberOfAttacks += 1
        return numberOfAttacks


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
