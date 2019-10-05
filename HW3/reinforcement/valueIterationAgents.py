# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0


        # Write value iteration code here

        print "getStates() gives:::::::", mdp.getStates()
        state =self.mdp.getStates()[2]
        print " START STATE ::::", state
        print "ACTIONS for start state :::", state, self.mdp.getPossibleActions(state)

        actions = self.mdp.getPossibleActions(state)[0]
        transitionFunc = self.mdp.getTransitionStatesAndProbs(state,actions)

        print "TRANSITION FN(next_state,prob):::", transitionFunc

        nextState = transitionFunc[0]
        states = self.mdp.getStates()
        print "ALL STATES ARE :::: \n", states


        for i in range(iterations):
            # initially v0 = 0
            # vPrev =v(k-1)
            vPrev = self.values.copy()
            for state in states:
                vMax = None
                for action in self.mdp.getPossibleActions(state):
                    curV = self.getQValue(state, action)
                    if vMax == None or vMax < curV:
                        vMax = curV

                if vMax == None:
                    vMax = 0

                vPrev[state] = vMax

            self.values = vPrev
            #print "Vmax for i ::::::: \n", vPrev
        #print "\tself.values::::::::\n", self.values



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qv = 0
        # q-value of (state,action) pair given by the value function given by self.values

        # print self.mdp.getTransitionStatesAndProbs(state, action)

        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qv = qv + prob * (self.mdp.getReward(state, action, nextState)
                                + (self.discount * self.getValue(nextState)))


        # print "QValue", qv
        return qv


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        v = None
        policy = None

        #check for terminal_state

        if self.mdp.isTerminal(state):
           return None

        # compute best action according to the value function given by self.values

        for action in self.mdp.getPossibleActions(state):
            temp = self.computeQValueFromValues(state, action)
            if v == None or temp > v:
                v = temp
                policy = action

        return policy



    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
