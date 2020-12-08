# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    foodLeft = len(currentGameState.getFood().asList())
    newFoodLeft = len(newFood.asList())
    shortestDotDist = 9999999999 
    for location in newFood.asList():
        distance = manhattanDistance(newPos, location)
        if(distance < shortestDotDist):
            shortestDotDist = distance
     
    ghostPositions = successorGameState.getGhostPositions() 
    totalGhostDist = 0
    for pos in ghostPositions:
        totalGhostDist += manhattanDistance(newPos,pos)
    if(totalGhostDist == 0):
        totalGhostDist = 0.1
    score = 1/float(shortestDotDist) - 1/float(totalGhostDist)
    if(newFoodLeft < foodLeft):
        score += 1
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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    depth = self.depth
    actionValue = [-9999999999999] 
    bestAction = [None]
    def getValue(state,depthIndex,agentIndex):
        if(depthIndex > depth or state.isWin() or state.isLose()):
            return self.evaluationFunction(state)
        elif(agentIndex == 0):
            value = -9999999999999
            actions = state.getLegalActions(agentIndex)
            nextAgent = 0
            nextDepth = depthIndex + 1
            if(agentIndex != (gameState.getNumAgents() -1)):
                nextAgent = agentIndex + 1
                nextDepth = depthIndex
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                value = max(value, getValue(newState, nextDepth, nextAgent))
                if(depthIndex == 1 and actionValue[0] < value):
                    actionValue[0] = value
                    bestAction[0] = action 
            return value
        elif(agentIndex > 0):
            value =  9999999999999
            nextAgent = agentIndex + 1 
            nextDepth = depthIndex
            if(agentIndex == (gameState.getNumAgents() -1)):
                nextAgent = 0 
                nextDepth = depthIndex + 1
            actions = state.getLegalActions(agentIndex)
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                newValue = getValue(newState, nextDepth, nextAgent)
                value = min(value,newValue)
            return value
    result = getValue(gameState, 1, 0)  
    return bestAction[0] 
        

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    depth = self.depth
    actionValue = [-9999999999999]
    bestAction = [None]
    def getValue(state,depthIndex,agentIndex, alpha, beta):
        if(depthIndex > depth or state.isWin() or state.isLose()):
            return self.evaluationFunction(state)
    
        elif(agentIndex == 0):
            value = -9999999999999
            actions = state.getLegalActions(agentIndex)
            nextAgent = 0
            nextDepth = depthIndex + 1
            if(agentIndex != (gameState.getNumAgents() -1)):
                nextAgent = agentIndex + 1
                nextDepth = depthIndex
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                value = max(value, getValue(newState, nextDepth, nextAgent,alpha, beta))
                if(depthIndex == 1 and actionValue[0] < value):
                    actionValue[0] = value
                    bestAction[0] = action
                alpha = max(alpha,value)
                if(alpha >= beta):
                    break
            return value
    
        elif(agentIndex > 0):
            value =  9999999999999
            nextAgent = agentIndex + 1
            nextDepth = depthIndex
            if(agentIndex == (gameState.getNumAgents() -1)):
                nextAgent = 0
                nextDepth = depthIndex + 1
            actions = state.getLegalActions(agentIndex)
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                newValue = getValue(newState, nextDepth, nextAgent, alpha, beta)
                value = min(value,newValue)
                beta = min(beta, value)
                if(beta <= alpha):
                    break
            return value
    
    result = getValue(gameState, 1, 0, -99999999999, 999999999999)
    return bestAction[0]

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
    depth = self.depth
    actionValue = [-9999999999999] 
    bestAction = [None]
    def getValue(state,depthIndex,agentIndex):
        if(depthIndex > depth or state.isWin() or state.isLose()):
            return self.evaluationFunction(state)
        elif(agentIndex == 0):
            value = -9999999999999
            actions = state.getLegalActions(agentIndex)
            nextAgent = 0
            nextDepth = depthIndex + 1
            if(agentIndex != (gameState.getNumAgents() -1)):
                nextAgent = agentIndex + 1
                nextDepth = depthIndex
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                value = max(value, getValue(newState, nextDepth, nextAgent))
                if(depthIndex == 1 and actionValue[0] < value):
                    actionValue[0] = value
                    bestAction[0] = action 
            return value
        elif(agentIndex > 0):
            nextAgent = agentIndex + 1 
            nextDepth = depthIndex
            if(agentIndex == (gameState.getNumAgents() -1)):
                nextAgent = 0 
                nextDepth = depthIndex + 1
            actions = state.getLegalActions(agentIndex)
            value = 0
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                newValue = getValue(newState, nextDepth, nextAgent)
                value += (1/float(len(actions))) * newValue
            return value
    result = getValue(gameState, 1, 0)  
    return bestAction[0] 

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I calculated and gathered all the relevant state data and whether or not the game was a win or not.
    If the game was a win or lose, return values rewarding or punishing that. Other than that combine score and food
    remaining as the most important variables because we want high score and being productive getting pellets. 
    If all ghosts are scared, then don't worry about their positions. Otherwise, be conscious of how close both and the
    nearest one is.
  """
  "*** YOUR CODE HERE ***"
  pacmanPos = currentGameState.getPacmanPosition()
  ghostPosList = currentGameState.getGhostPositions()
  ghostStates = currentGameState.getGhostStates()
  food = currentGameState.getFood().asList()
  foodRemaining = len(food)
  isWin = currentGameState.isWin()
  isLose = currentGameState.isLose()
  scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
  currentScore = currentGameState.getScore()
  closestFoodDist = 999999999999
  closestGhostDist = 999999999999
  totalGhostDist = 0
  totalFoodDist = 0
  for location in food:
      distance = manhattanDistance(pacmanPos,location)
      totalFoodDist += distance
      if (distance < closestFoodDist):
          closestFoodDist = distance

  for location in ghostPosList:
      distance = manhattanDistance(pacmanPos, location)
      totalGhostDist += distance
      if (distance < closestGhostDist):
          closestGhostDist = distance
  if(closestGhostDist == 0):
     return -999999999999 

  if (isLose):
      return -999999999999 
  elif(isWin):
      return 999999999999
 
  #if(closestGhostDist == 1):
      #closestGhostDist = 0.1
  if(currentScore == 0):
      currentScore = 1
  if(currentScore < 0):
      currentScore = 0.1
      
  #score = (1/float(closestFoodDist)) 
  score = (7/float(totalFoodDist))
  
  if(sum(scaredTimes) == 0):
      score += -(1/float(totalGhostDist))
      score += -(1/float(closestGhostDist))
  elif(sum(scaredTimes) > 0):
      score += -(1/float(sum(scaredTimes)))
  score += -13/float(currentScore)
  score += 15/float(foodRemaining)
  return score 

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

