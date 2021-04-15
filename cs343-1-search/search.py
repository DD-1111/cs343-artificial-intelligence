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
    return [s, s, w, s, w, w, s, w]


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
    "*** YOUR CODE HERE ***"
    # solution = []
    # closedSet = set()
    # closedSet.add(problem.getStartState())
    #
    # def DFSHelper(node, problem, solution, closedSet):
    #     if problem.isGoalState(node):
    #         return solution
    #
    #     for child, direction, cost in problem.getSuccessors(node):
    #         if child not in closedSet:
    #             solution.append(direction)
    #             closedSet.add(child)
    #             if DFSHelper(child, problem, solution, closedSet) != False:
    #                 return solution
    #             else:
    #                 solution.pop()
    #         else:
    #             return False
    #
    # solution = DFSHelper(problem.getStartState(), problem, solution, closedSet)
    # return solution

    # spend too much time on fixing my recursive solution but I can not still get it correct so i give up
    fringe = util.Stack()
    node = problem.getStartState()
    solution = {node: []}
    fringe.push(node)
    explored = set()
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node):
            return solution[node]
        else:
            if node not in explored:
                nextmove = problem.getSuccessors(node)
                for onemove in nextmove:
                    child, nextDir = onemove[0], onemove[1]
                    if child not in explored:
                        solution[child] = list(solution[node])
                        solution[child].append(nextDir)
                        fringe.push(child)
                explored.add(node)
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Strictly follow the sudocode in the textbook for BFS
    node = problem.getStartState()
    solution = {node: []}
    explored = set()
    frontier = util.Queue()
    frontier.push(node)
    while not frontier.isEmpty():
        # Run out of nodes, failed to find a solution
        node = frontier.pop()
        explored.add(node)
        if problem.isGoalState(node):
            return solution[node]
        nextmove = problem.getSuccessors(node)
        for onemove in nextmove:
            child, nextDir = onemove[0], onemove[1]
            if (child not in frontier.list) and (child not in explored):
                # Don't know whether this is hard/shallow copy, just trying
                solution[child] = list(solution[node])
                # Turns out to be working, copy the previous path to the next step
                solution[child].append(nextDir)
                frontier.push(child)

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Strictly follow the sudocode in the textbook for BFS, change the data structure to priority Q
    node = problem.getStartState()
    fringe = util.PriorityQueue()
    explored = set()
    solution = []
    fringe.push((node, solution), 0)
    while not fringe.isEmpty():
        # Run out of nodes, failed to find a solution
        node, curPath = fringe.pop()
        if problem.isGoalState(node):
            return curPath
        if not node in explored:
            explored.add(node)
            nextmove = problem.getSuccessors(node)
            for onemove in nextmove:
                child, nextDir = onemove[0], onemove[1]
                if (child not in explored) or (problem.isGoalState(child)):
                    fringe.update((child, curPath + [nextDir]), problem.getCostOfActions(curPath + [nextDir]))
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    fringe = util.PriorityQueue()
    explored = set()
    solution = []
    cost = 0
    start = (node, cost, solution)
    fringe.push(start, 0)
    while not fringe.isEmpty():
        node, cost, curPath = fringe.pop()
        if problem.isGoalState(node):
            return curPath
        if not node in explored:
            explored.add(node)
            nextmove = problem.getSuccessors(node)
            for onemove in nextmove:
                child, nextDir, nextstepcost = onemove[0], onemove[1], onemove[2]
                newcost = cost + nextstepcost
                newstate = (child, newcost, curPath + [nextDir])
                fringe.push(newstate, newcost + heuristic(child, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
