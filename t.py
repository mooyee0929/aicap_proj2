import random
import numpy as np

# The UCT algorithm balances exploration and exploitation in the tree search
def UCT(node):
    if node.n == 0:
        return float('inf')
    return node.Q / node.n + 1.414 * np.sqrt(np.log(node.parent.n) / node.n)

# A Node represents a state in the game and its corresponding information in the tree search
class Node:
    def __init__(self, mapStat, gameStat, parent=None, step=None):
        self.mapStat = mapStat
        self.gameStat = gameStat
        self.parent = parent
        self.step = step
        self.children = []
        self.n = 0
        self.Q = 0
    
    # Expands the node by adding all possible child nodes
    def expand(self):
        possible_moves = self.get_possible_moves()
        for move in possible_moves:
            child_mapStat, child_gameStat = self.get_next_state(self.mapStat, self.gameStat, move)
            child_node = Node(child_mapStat, child_gameStat, self, move)
            self.children.append(child_node)
    
    # Returns a list of all possible moves from the current state
    def get_possible_moves(self):
        free_cells = checkRemainMove(self.mapStat)
        moves = []
        for cell in free_cells:
            for length in range(1, 4):
                for direction in range(1, 7):
                    move = (cell[0], cell[1], length, direction)
                    moves.append(move)
        return moves
    
    # Given a move, returns the next state of the game
    def get_next_state(self, mapStat, gameStat, move):
        x, y, l, d = move
        end_x, end_y = x, y
        for i in range(l):
            end_x, end_y = Next_Node(end_x, end_y, d)
        child_mapStat = np.copy(mapStat)
        child_gameStat = gameStat.copy()
        child_gameStat.append(move)
        for i in range(l):
            nx, ny = Next_Node(x+i, y, d)
            if child_mapStat[nx][ny] == -1:
                raise Exception('Invalid move')
            if child_mapStat[nx][ny] != 0:
                raise Exception('Invalid move')
            child_mapStat[nx][ny] = 1 if len(child_gameStat) % 2 == 0 else 2
        return child_mapStat, child_gameStat
    
    # Runs one iteration of the MCTS algorithm
    def select(self):
        node = self
        while node.children:
            # Select the best child node based on the UCT formula
            node = max(node.children, key=UCT)
        # If the node hasn't been expanded yet, expand it and return a random child
        if node.n == 0:
            node.expand()
            return random.choice(node.children)
        # Otherwise, return the best child based on the UCT formula
        return max(node.children, key=UCT)
    
    # Updates the statistics of the node with the result of a simulation
    def update(self, result):
        self.n += 1
        self.Q += result
    
    # Runs a simulation from the current node until the end of the game is reached, and returns the result
    def simulate(self):
        mapStat = np.copy(self.mapStat)
        gameStat = self.gameStat.copy()
        while True:
            free_cells = checkRemainMove(mapStat)
            if
