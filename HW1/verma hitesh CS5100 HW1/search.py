# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    frontier = util.Stack()
    state = problem.getStartState()    
    visitedNode= list()
    frontier.push((state,list()))

    print "start State:", state
    while not frontier.isEmpty():    
        current_state, actions = frontier.pop()
        print "========================================= \n"
        print "Current Node: \t",current_state
        print "Action order:" ,actions  

        if problem.isGoalState(current_state):
            return actions


        visitedNode.append(current_state) 
        print " visited Node:\t",visitedNode

        #print "successors of Current node: \t",problem.getSuccessors(current_state)
        for successor, directions ,stepCost in problem.getSuccessors(current_state):
            if not (successor in visitedNode or successor in frontier.list):
                frontier.push((successor,actions + [directions]))
                print "successor pushed to frontier:\t",successor
                #print "stack order :\t" , frontier.list()
      

    #util.raiseNotDefined()
          
             


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
  
    #code begins   
    qFrontier = util.Queue()
    state = problem.getStartState()
    visitedNode= list()
    print "start State:", state

    qFrontier.push((state,list()))

    while not qFrontier.isEmpty(): 
        current_state, actions = qFrontier.pop()
        print "========================================= \n"
        print "Current Node: \t",current_state
        print "Action order:" ,actions  

        #testing code
        if problem.isGoalState(current_state):
                    #print "check",actions
                    return actions
        if  current_state not in visitedNode:             
            visitedNode.append(current_state) 
            print " visited Node 1:\t",visitedNode

            for successor, directions, stepCost in problem.getSuccessors(current_state):
                if not (successor in visitedNode or successor in qFrontier.list):
               
                    qFrontier.push((successor,actions + [directions]))
                    print "successor pushed to frontier:\t",successor


    #code ends 
  

    #util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    pQueue = util.PriorityQueue()
    state = problem.getStartState()
    pQueue.push((state,list()),0)
    visitedNode= list()

    while not pQueue.isEmpty():
        current_state, actions = pQueue.pop()
        print "========================================= \n"
        #print "Current Node: \t",current_state
        #print "Action order:" ,actions  

        if problem.isGoalState(current_state):
            return actions
        if  current_state not in visitedNode:     
            visitedNode.append(current_state) 
            #print " visited Node:\t",visitedNode

            for successor, directions ,stepCost in problem.getSuccessors(current_state):
                if not (successor in visitedNode or successor in pQueue.heap):
                    pQueue.push((successor,actions + [directions]), problem.getCostOfActions(actions + [directions]))
                elif (successor in pQueue.heap and stepCost > problem.getCostOfActions(actions + [directions])):
                    pQueue.update((successor,actions + [directions]),stepCost)

                #print "successor pushed to frontier:\t",successor
                #print "cost of this action:\t", problem.getCostOfActions(actions + [directions])
                #print "Priorty Queue order :\t" , pqFrontier.printS() 
    

    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
  

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    visitedNode = []
    pQueue = util.PriorityQueue()
    start_state = problem.getStartState()
    pQueue.push((start_state, list()), heuristic(start_state, problem))

    while not pQueue.isEmpty():      
        current_state, actions =  pQueue.pop()
        print "========================================= \n"
        print "Current Node: \t",current_state
        print "Action order:" ,actions  

        if problem.isGoalState(current_state):
            return actions

        if  current_state not in visitedNode:  
            visitedNode.append(current_state)
            print " visited Node:\t",visitedNode

            for successor, directions, stepCost in problem.getSuccessors(current_state):
                if not (successor in visitedNode or successor in pQueue.heap):
                    nextActions = actions + [directions]
                    fn = problem.getCostOfActions(nextActions) + heuristic(successor, problem)
                    pQueue.push( (successor, nextActions), fn)
                    #print "h(n)#######", heuristic(successor, problem) ,successor


    return []

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
