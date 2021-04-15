# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #since we only have one ghost
        curghostpos = newGhostStates[0].getPosition()
        dangerdis = manhattanDistance(newPos, curghostpos)
        curscore = successorGameState.getScore()
        if  0 < dangerdis < 3:
            curscore -= 25.0

        if len(newFood.asList()):
            nextfood = (min([manhattanDistance(newPos, food) for food in newFood.asList()]))
            curscore += 10.0 /nextfood

        return curscore


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
        """

        "*** YOUR CODE HERE ***"
        maxVal = -999999
        optimal = None
        #from the beginning pos, get all possible next action
        for action in gameState.getLegalActions(0):
            value = self.minmaxHelper(gameState.generateSuccessor(0, action), False, 1)
            if value is not None and value > maxVal:
                maxVal = value
                optimal = action
        return optimal

    def minmaxHelper(self, gameState, maxbool, agentIndex, depth = 0):
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == self.depth or len(legalActions) == 0:
            return self.evaluationFunction(gameState)
        curVal = -999999 if maxbool else 999999
        for action in legalActions:
            if maxbool:
                value = self.minmaxHelper(gameState.generateSuccessor(agentIndex, action), False, 1, depth)
                if value is not None and value > curVal:
                    curVal = value
            else:
                # last ghost, need to call pacman next
                if agentIndex == gameState.getNumAgents() - 1:
                    # pacman go deeper
                    value = self.minmaxHelper(gameState.generateSuccessor(agentIndex, action),True, 0, depth + 1)
                else:
                    # go through every min agents on this layer, without diving deeper
                    value = self.minmaxHelper(gameState.generateSuccessor(agentIndex, action),False, agentIndex+1, depth)
                if value is not None and value < curVal:
                    curVal = value
        return curVal



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.prunHelper(gameState, True, 0)[0]

# small changes to previous algo, swap the min/max presetting with alpha and beta
    def prunHelper(self, gameState, maxbool, agentIndex = 0, depth=0, alpha=-999999, beta=999999):
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == self.depth or len(legalActions) == 0:
            return None, self.evaluationFunction(gameState)
        maxorminval = None
        optimalAct = None
        for action in legalActions:
            if maxbool:
                value = self.prunHelper(gameState.generateSuccessor(agentIndex, action), False, 1, depth, alpha, beta)[1]
                if value is not None :
                    if value > maxorminval or maxorminval is None:
                        maxorminval = value
                        optimalAct = action
                    if value > beta:
                        # no need to continue, directly return
                        return action, value
                    if value > alpha:
                        alpha = value
            else:
                # last ghost, need to call pacman next
                if agentIndex == gameState.getNumAgents() - 1:
                    value = self.prunHelper(gameState.generateSuccessor(agentIndex, action), True, 0, depth + 1, alpha, beta)[1]
                else:
                # move on through the agent index
                    value = self.prunHelper(gameState.generateSuccessor(agentIndex, action), False, agentIndex + 1, depth, alpha, beta)[1]
                if value is not None:
                    if maxorminval is None or value < maxorminval :
                        optimalAct = action
                        maxorminval = value
                    if value < alpha :
                        return action, value
                    if value < beta :
                        beta = value
        return optimalAct, maxorminval




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
        return self.getMax(gameState, 0)

    def getMax(self, gameState, depth):
        """
          maximizing agent in expectimax
        """
        legalActions = gameState.getLegalActions(0)
        if depth == self.depth or len(legalActions) == 0:
            return self.evaluationFunction(gameState)
        maxVal = -999999.0
        optimalAct = None
        # so far same as previous code
        for action in legalActions:
            # call a separate function to get expected value instead
            curVal = self.getExpecti(gameState.generateSuccessor(0, action), depth, 1)
            # update the biggest expected value and opt action
            if curVal > maxVal:
                maxVal = curVal
                optimalAct = action

        if depth is not 0:
            return maxVal
        else:
            return optimalAct

    def getExpecti(self, gameState, depth, agentIndex):
        """
          minimizing agent in minimax
        """
        # same thing
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == self.depth or len(legalActions) == 0:
            return self.evaluationFunction(gameState)
        expecti = 0.0
        # probabilty is uniform with its choices
        probablity = 1.0 / len(legalActions)
        for action in legalActions:
            successor = gameState.generateSuccessor(agentIndex, action)
            # then we will call pacman
            if agentIndex == gameState.getNumAgents() - 1:
                expecti += probablity * self.getMax(successor,depth + 1)
            # will loop through all ghosts
            else:
                expecti += probablity * self.getExpecti(successor,depth, agentIndex + 1)
        return expecti


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    curscore = currentGameState.getScore()

    # copy from the first question, here we remove the distance to the ghost since we are not using reflex agent
    if len(newFood):
        nextfood = (min([manhattanDistance(newPos, food) for food in newFood]))
        curscore += 10.0 / nextfood

    return curscore


"*** YOUR CODE HERE ***"

# Abbreviation
better = betterEvaluationFunction

