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
        print "scores >>>>>" ,scores
        bestScore = max(scores)
        print "max of scores>>>> ",bestScore
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

        Print out these variables to see whateva're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print "successorGameState" ,successorGameState
        print " Pacman New Pos ::::::::::::" ,newPos
        # print " remaining Food position" , newFood.asList()
        #ghostPos = [ghostState.getPosition() for ghostState in newGhostStates]
        #print "ghost positions" ,ghostPos

        shortestDistFood = None
        for foodPos in newFood.asList():
          distToFood = manhattanDistance(newPos,foodPos)
          if (shortestDistFood == None or distToFood < shortestDistFood):
            shortestDistFood = distToFood


        shortestDistGhost = None
        for ghostState in newGhostStates:
          distToGhost = manhattanDistance(newPos,ghostState.getPosition())
          if (shortestDistGhost == None or distToGhost < shortestDistGhost):
            shortestDistGhost = distToGhost

        #return successorGameState.getScore()
        eval= successorGameState.getScore() 

        print "getScore::::", successorGameState.getScore() 

        #a = ( 10.0 / shortestDistGhost)

        #b = (10.0 / shortestDistFood)

        if (shortestDistGhost > 0):
            eval = eval - ( 10.0 / shortestDistGhost)

        
        if (len(newFood.asList())):
          eval = eval + (10.0 / shortestDistFood)

        print "eval fn is :",eval
        return eval

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
        agentIndex =self.index
        print " pacman state: " ,gameState.getLegalActions(0)

        totalCount= self.depth * gameState.getNumAgents()
        numOfAgent = gameState.getNumAgents()

        #agentIndex=0 means Pacman
        actions = self.maxValue(gameState, totalCount, numOfAgent , agentIndex)

        # print "  Minmax count >>>>>>>>>> \n" ,MinimaxAgent.count
        # actions[0]is max value and action[1] is path for selecting max value from  via leaf node 
        return actions[1]

  #to call maxValue recursively
    def maxValue(self, state, d, numOfAgent, agentIndex):

      print "MAX( d =%i ,na =%i , ai =%i) @@@@@@@@@@@@@@@@ ",d, numOfAgent, agentIndex

      #The evaluation function should be called when the no more depth left , max depth reached
      if state.isWin() or state.isLose() or  d == 0:
        return self.evaluationFunction(state)

      #list of legal actions for the agent
      legalActionsList = state.getLegalActions(agentIndex)
      print "legalActions are in Max Nodes :::::::",legalActionsList 

      nextStatesList = []

      for action in legalActionsList:
        nextStatesList.append(state.generateSuccessor(agentIndex,action))

      print "nextStatesList :::::" ,nextStatesList        

      # for max value = (- infinity )
      maxV = - 999999
      max = []
      action = legalActionsList[0]
      nextIndex =0

      for nextState in nextStatesList:
        #calling minValue in recursion
        v = self.minValue(nextState, d-1 ,numOfAgent-2 ,numOfAgent , int((agentIndex+1) % numOfAgent))
        max.append(v)

        if (v > maxV):
          maxV = v
          action = legalActionsList[nextIndex]
        nextIndex = nextIndex +1 
        
        print "action to max node ::::", action
        #action to max node :::: Stop ?????
        print "max value for current state is :::::", maxV
      return (maxV, action)


    #to call minValue recursively
    def minValue(self, state, d, unvisitedGhosts, numOfAgent, agentIndex):

      print " MIN( d =%i , UG = %i ,na =%i , ai =%i) @@@@@@@@@@@@@@@@ ",d , unvisitedGhosts,numOfAgent , agentIndex

       #The evaluation function should be called when the no more depth left , max depth reached
      if state.isWin() or state.isLose() or  d == 0:
        return self.evaluationFunction(state)

      legalActionsList = state.getLegalActions(agentIndex)
      print "legalActions are in Min nodes:::::::",legalActionsList 

      nextStatesList = []
      minValuelist = []

      # minV = 99999999
      #All states in minimax should be GameStates, either passed in to getAction or generated via
      #GameState.generateSuccessor

      for action in legalActionsList:
        nextStatesList.append(state.generateSuccessor(agentIndex,action))

      if not (unvisitedGhosts== 0):
        for nextState in nextStatesList:
          v=self.minValue(nextState,d-1,unvisitedGhosts-1, numOfAgent , int((agentIndex+1) % numOfAgent))
          minValuelist.append(v)

      else:
        for nextState in nextStatesList:
          v = self.maxValue(nextState, d-1 ,numOfAgent ,int((agentIndex+1) % numOfAgent))
          minValuelist.append(v)

      finalminValue = min(minValuelist)
      print "minValueList has :::" ,minValuelist
      print "min of minValuelist :: ",finalminValue
      return finalminValue




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        # util.raiseNotDefined()
        agentIndex =self.index
        print " pacman state: " ,gameState.getLegalActions(0)

        totalCount= self.depth * gameState.getNumAgents()
        numOfAgent = gameState.getNumAgents()

        actions = self.maxAB(gameState, totalCount, numOfAgent ,0 , -999999 ,999999)
        return actions[1]

    def maxAB(self, state, d, numOfAgent, agentIndex , alpha , beta):

      if state.isWin() or state.isLose() or  d == 0:
        return self.evaluationFunction(state)
      legalActionsList = state.getLegalActions(agentIndex)
      nextStatesList = []

      for action in legalActionsList:
        nextStatesList.append(state.generateSuccessor(agentIndex,action))       

      maxV = - 999999
      action = legalActionsList[0]
      nextIndex =0

      for nextState in nextStatesList:
        v = self.minAB(nextState, d-1 ,numOfAgent-2 ,numOfAgent , int((agentIndex+1) % numOfAgent), alpha , beta)

        if (maxV < v):
          maxV = v
          action = legalActionsList[nextIndex]
        if maxV > beta:
           return (maxV,action) 
        alpha = max (alpha, maxV)  
        nextIndex = nextIndex + 1   
      return (maxV, action)


    def minAB(self, state, d, unvisitedGhosts, numOfAgent, agentIndex,alpha, beta):

       #The evaluation function should be called when the no more depth left , max depth reached
      if state.isWin() or state.isLose() or d == 0:
        return self.evaluationFunction(state)

      legalActionsList = state.getLegalActions(agentIndex)
      nextStatesList = []
      minValuelist = []
      minV = 999999

      for action in legalActionsList:
        nextStatesList.append(state.generateSuccessor(agentIndex,action))

      if not (unvisitedGhosts== 0):
        for nextState in nextStatesList:
          v=self.minAB(nextState,d-1,unvisitedGhosts-1, numOfAgent , int((agentIndex+1) % numOfAgent), alpha, beta)
          # minValuelist.append(v)
          minV= min(minV ,v)
          if minV < alpha:
            return minV
          beta = min (beta, minV)

      else:
        for nextState in nextStatesList:
          v = self.maxAB(nextState, d-1 ,numOfAgent ,int((agentIndex+1) % numOfAgent), alpha , beta)
          # minValuelist.append(v)
          minV= min(minV ,v)
          if minV < alpha:
            return minV
          beta = min (beta, minV)

      return minV





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

        agentIndex =self.index

        numOfAgent = gameState.getNumAgents()

        # taking current depth =1 

        return self.expectiMax(gameState, 1, numOfAgent, agentIndex)
        # util.raiseNotDefined()


    def expectiMax(self, state, d, numOfAgent, agentIndex):

      if d > self.depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      legalActionsList = []

      for action in state.getLegalActions(agentIndex):
        if action!='Stop':
          legalActionsList.append(action)

    
      nextIndex = agentIndex + 1
      nextDepth = d
      #update the  nextDepth
      if nextIndex >= state.getNumAgents():
          nextIndex = 0
          nextDepth += 1
      # numAgents = state.getNumAgents()
    
     
      v = []
      for action in legalActionsList:
        nextState=state.generateSuccessor(agentIndex, action) 
        value =self.expectiMax(nextState, nextDepth, numOfAgent, nextIndex)

        v.append(value)
        
      if agentIndex == 0 and d == 1: # pacman first move
          bestMove = max(v)
          bestIndexList = []

          for index in range(len(v)):
            if v[index] == bestMove:
              bestIndexList.append(index)

            # using randon function to select  index  randomly from best 
          selectedIndex = random.choice(bestIndexList) 

          print 'pacman best move on chance %d' % bestMove
          return legalActionsList[selectedIndex]
    
      if agentIndex == 0:
          bestMove = max(v)
          print "bestMove", bestMove
          return bestMove
      else:
          # for agents >= 1 , ghost nodes
          #expected value  = average of values 
          expectedvalue = sum(v)/len(v)
          print  "sum(v), len(v) " ,sum(v), len(v)
          bestMove = expectedvalue 

          print " pacman best move when ghost ::" ,bestMove
          return bestMove





def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    curPos = currentGameState.getPacmanPosition()
    leftFood = currentGameState.getFood()
    ghostStates = successorGameState.getGhostStates()

    capsulesList = currentGameState.getCapsules()

    for ghostState in ghostStates:
        scaredTimes = ghostState.scaredTimer
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

      #print "cuurent GameState" ,currentGameState
    print " Pacman Current Pos ::::::::::::" ,curPos
        # print " remaining Food position" , newFood.asList()
        #ghostPos = [ghostState.getPosition() for ghostState in newGhostStates]
        #print "ghost positions" ,ghostPos

    shortestDistFood = None
    foodList = leftFood.asList()

    for foodPos in foodList:
      distToFood = manhattanDistance(curPos,foodPos)
      if (shortestDistFood == None or distToFood < shortestDistFood):
          shortestDistFood = distToFood


    shortestDistGhost = None
    for ghostState in newGhostStates:
      distToGhost = manhattanDistance(curPos,ghostState.getPosition())
    if (shortestDistGhost == None or distToGhost < shortestDistGhost):
      shortestDistGhost = distToGhost

    shortestDistToCapsule = None
    for capsule in capsulesList:
      distToCapsule = manhattanDistance( curPos, capsule)
    if(shortestDistCapsule == None or distToCapsule <shortestDistToCapsule):
          shortestDistToCapsule = distToCapsule


    eval= currentGameState.getScore() 


    if len(foodList) == 0:
        eval = eval  - 2 * shortestDistFood


    if shortestDistGhost > 0:
        eval = eval + shortestDistGhost




    # c = -3 / shortestDistToCapsule 


    # a = - 2 * shortestDistFood

    # b = -2 / shortestDistGhost


    return eval


# Abbreviation
better = betterEvaluationFunction

