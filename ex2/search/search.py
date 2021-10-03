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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"


    from game import Directions
    sta = util.Stack()
    bo = {}
    re = {}
    startPos = problem.getStartState()
    bo[startPos] = 0
    re[startPos] = problem.getStartState()

    sta.push((startPos, startPos, 0))  # (nowPos, faPos, action)
    while not sta.isEmpty():
        now = sta.pop()
        nowPos = now[0]
        re[nowPos] = (now[1], now[2])
        bo[nowPos] = 1
        if problem.isGoalState(nowPos) :
            goal = nowPos
            break
        nex = problem.expand(nowPos)
        for i in range(len(nex)):
            if nex[i][0] not in bo:
                # bo[nex[i][0]] = 1
                sta.push((nex[i][0], nowPos, nex[i][1]))
    ansSta = util.Stack()
    ans = []
    nowPos = goal
    while nowPos != problem.getStartState():
        ansSta.push(re[nowPos][1])
        nowPos = re[nowPos][0]
    while not ansSta.isEmpty():
        ans.append((ansSta.pop()))
    return ans
"""
主要出现的问题还是在栈形式dfs上，最后调整成，只在这个节点被拓展的时候，才将其打上标记，
同时在每次拓展节点时，记录被拓展到的节点和其父节点（当前正在拓展的节点），便于逆序搜索路径
"""

def breadthFirstSearch(problem, Directions=None):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    op = problem.getStartState()

    re = {op: op}
    q = util.Queue()
    pat = {op: (0, 0)}  # (位置：cost，action)
    q.push((op, 0))  # (位置，cost)

    while not q.isEmpty():
        now = q.pop()
        nowPos = now[0]
        nowCost = now[1]
        if problem.isGoalState(nowPos):
            goal = now
            break  # 找到了就退出
        nex = problem.expand(nowPos)  # [((34, 15), 'South', 1), ((33, 16), 'West', 1)]
        n = len(nex)
        for i in range(n):
            nexPos = nex[i][0]
            nexAction = nex[i][1]
            nexCost = nex[i][2]
            if nexPos not in pat:
                q.push((nexPos, nowCost + nexCost))
                re[nexPos] = nowPos
                pat[nexPos] = (nowCost + nexCost, nexAction)  # 如果能扩展则扩展
    goalPos = goal[0]
    goalCos = goal[1]
    ans = []
    las = pat[goalPos]
    nowPos = goalPos
    s = util.Stack()
    while las[1] != 0:
        s.push(las[1])
        nowPos = re[nowPos]
        # nowPos = problem.getNextState(nowPos, re[las[1]])
        las = pat[nowPos]
    while not s.isEmpty():
        ans.append(s.pop())
    return ans

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    util.raiseNotDefined()
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    from searchAgents import manhattanHeuristic
    q = util.PriorityQueue()
    bo = {}
    path = {}
    startPos = problem.getStartState()
    bo[startPos] = 0
    path[startPos] = (startPos, 0)
    # (上一个位置，action)
    q.push((startPos, startPos, 0, 0), manhattanHeuristic(startPos, problem))
    # (当前位置，上一个位置，action，总花费）
    goal = problem.goal
    while not q.isEmpty():
        now = q.pop()
        nowPos = now[0]
        nowCost = now[3]
        path[nowPos] = (now[1], now[2])
        nex = problem.expand(nowPos)
        # [((34, 15), 'South', 1), ((33, 16), 'West', 1)]
        if problem.isGoalState(nowPos):
            break
        for i in range(len(nex)):
            nexPos = nex[i][0]
            nexCost = nowCost + nex[i][2]

            if nexPos not in bo:
                nexH = manhattanHeuristic(nexPos, problem)
                bo[nexPos] = 1
                q.push((nexPos, nowPos, nex[i][1], nexCost), nexCost + nexH)
    nowPos = goal
    ansSta = util.Stack()
    ans = []
    while nowPos != startPos:
        ansSta.push(path[nowPos][1])
        nowPos = path[nowPos][0]
    while not ansSta.isEmpty():
        ans.append(ansSta.pop())
    return ans

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
