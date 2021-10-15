from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        '''
        Consider the food locations, the ghost locations and the food numbers.
        closer to the food, higher the score
        farther to the ghost, higher the score
        less the number of food, higher the score
        '''
        currentScore = currentGameState.getScore()

        foodList = newFood.asList()
        foodDistance = [manhattanDistance(food, newPos) for food in foodList]
        nearestFoodDistance = min(foodDistance, default=1)

        activaGhost = []
        scaredGhost = []
        for ghost in newGhostStates:
          if ghost.scaredTimer == 0:
            activaGhost.append(ghost)
          else:
            scaredGhost.append(ghost)
        activateGhostStateList = [ghost.getPosition() for ghost in activaGhost]
        activateGhostDistance = [manhattanDistance(ghostState, newPos) for ghostState in activateGhostStateList]
        nearestGhostDistance = min(activateGhostDistance, default=0)

        successorNumberofFood = successorGameState.getNumFood()

        score = -nearestFoodDistance  - 10 * 1/(nearestGhostDistance+1) - 1000*successorNumberofFood 
        return score
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # print(gameState.getNumAgents())

        def terminalTest(state, d):
          if state.isLose() or state.isWin() or self.depth == d:
            return True
          return False

        # max part in minmax
        def maxValue(state, d):
          if terminalTest(state, d):
            # print("MaxEnd:",self.evaluationFunction(state))
            return self.evaluationFunction(state)
          value = -1000000
          for action in state.getLegalActions(0):
            value = max(value, minValue(state.generateSuccessor(0,action), d, 1))
          return value

        # min part in minimax
        def minValue(state, d, ghostIndex):
          if terminalTest(state, d):
            # print("MinEnd:",self.evaluationFunction(state))
            return self.evaluationFunction(state)
          value = 1000000
          for action in state.getLegalActions(ghostIndex):
            if ghostIndex >= (state.getNumAgents()-1):
              value = min(value, maxValue(state.generateSuccessor(ghostIndex, action), d+1))
            else:
              value = min(value, minValue(state.generateSuccessor(ghostIndex, action), d, ghostIndex+1))
          return value

        # this state's next actions
        actions = gameState.getLegalActions(0)
        # this state's next states
        states = [gameState.generateSuccessor(0, action) for action in actions]
        
        # current gameState's next states are min part
        scores = [minValue(state, 0, 1) for state in states]
        # current gameState is max part
        # print(scores)
        maxScore = max(scores)

        index = random.choice([index for index,score in enumerate(scores) if score == maxScore])
        # print("action:",actions[index])
        return actions[index]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # whether is the ternimal state
        def terminalTest(state, d):
          if state.isLose() or state.isWin() or self.depth == d:
            return True
          return False

        def maxValue(state, d, alpha, beta):
          if terminalTest(state, d):
            # print("MaxEnd:", self.evaluationFunction(state))
            return self.evaluationFunction(state)
          value = -1000000
          for action in state.getLegalActions(0):
            value = max(value, minValue(state.generateSuccessor(0, action), d, 1, alpha, beta))
            if value > beta:
              return value
            alpha = max(alpha, value)
            # print("alpha:",alpha)
          return value

        def minValue(state, d, ghostIndex,alpha, beta):
          if terminalTest(state, d):
            # print("MinEnd:", self.evaluationFunction(state))
            return self.evaluationFunction(state)
          value = 1000000
          for action in state.getLegalActions(ghostIndex):
            if ghostIndex >= (state.getNumAgents()-1):
              value = min(value, maxValue(state.generateSuccessor(ghostIndex, action), d+1, alpha, beta))
              if value < alpha:
                return value
            else:
              value = min(value, minValue(state.generateSuccessor(ghostIndex, action), d, ghostIndex+1, alpha, beta))
              if value < alpha:
                return value
            beta = min(beta, value)
            # print("beta:",beta)
          return value

        actions = gameState.getLegalActions(0)

        alpha = -1000000
        beta = 1000000
        value = -1000000
        nextAction = Directions.STOP
        for action in actions:
          oldValue = value
          value = max(value, minValue(gameState.generateSuccessor(0, action), 0, 1, alpha, beta))
          if value > oldValue:
            # print("maxValueIteration:", value)
            nextAction = action
          alpha = max(alpha, value)
          # print("alpha:", alpha)
        return nextAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def terminalTest(state, d):
          if state.isLose() or state.isWin() or self.depth == d:
            return True
          return False

        def maxValue(state, d):
          if terminalTest(state, d):
            return self.evaluationFunction(state)
          value = -1000000
          for action in state.getLegalActions(0):
            value = max(value, chanceValue(state.generateSuccessor(0, action), d, 1))
          return value

        def chanceValue(state, d, ghostIndex):
          if terminalTest(state, d):
            return self.evaluationFunction(state)
          totalValue = 0.0
          numsAction = len(state.getLegalActions(ghostIndex))
          # print("depth in chanceValue:",d)
          for action in state.getLegalActions(ghostIndex):
            if ghostIndex == state.getNumAgents()-1:
              value = maxValue(state.generateSuccessor(ghostIndex, action), d+1)
            else:
              value = chanceValue(state.generateSuccessor(ghostIndex,action), d, ghostIndex+1)
            totalValue += value
          # print("totalValue:",totalValue)
          # print("return value:",totalValue/numsAction)
          return totalValue / numsAction

        initValue = -1000000.0
        maxAction = Directions.STOP

        for action in gameState.getLegalActions(0):
          # print(action)
          value = chanceValue(gameState.generateSuccessor(0,action), 0, 1)
          if value > initValue:
            # print("updateAction:", action)
            initValue = value
            maxAction = action
        return maxAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Use a linear combination of features to evaluate the state.

      The important features:
        Food's position (nearest)
        Food's number
        Active Ghost's position (nearest)
        Scared Ghost's position (nearest)
        Capsule's position (nearest)
        Capsule's number

      The capsule takes a large part of the score, followed by food.
      We consider the scared ghost, it takes a less part than food.
      The pacman also eats the scared ghost.
      Besides, we need to be aware of the distance of active ghost and dodge it when get close.
      Finally, the pacman need to get close to the food and capsule.

    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    foods = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    numOfFood = currentGameState.getNumFood()
    capsules = currentGameState.getCapsules()
    numOfCapsule = len(currentGameState.getCapsules())

    activeGhosts = []
    scaredGhosts = []

    for ghost in ghostStates:
      if ghost.scaredTimer == 0:
        activeGhosts.append(ghost)
      else:
        scaredGhosts.append(ghost)

    foodDistance = [manhattanDistance(food, position) for food in foods]
    nearestFoodDistance = min(foodDistance, default=0)

    activeGhostDistance = [manhattanDistance(ghost.getPosition(), position) for ghost in activeGhosts]
    nearestActiveGhost = min(activeGhostDistance, default=0)

    scaredGhostDistance = [manhattanDistance(ghost.getPosition(), position) for ghost in scaredGhosts]
    nearesetScaredDistance = min(scaredGhostDistance, default=0)

    capsuleDistance = [manhattanDistance(capsule, position) for capsule in capsules]
    nearestCapsuleDistance = min(capsuleDistance, default=0)

    score =  - 10*nearestFoodDistance - 100*1/(nearestActiveGhost+1) - 2000*numOfFood - 5000*numOfCapsule - 100*nearesetScaredDistance - 10*nearestCapsuleDistance
    return score

# Abbreviation
better = betterEvaluationFunction

