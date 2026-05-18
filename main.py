# Kateryna Fedkova   ID: 260ADB019  GROUP: ADBD0
# TODO fill your info
# Programming language: Python
# To run the program: go into the folder which contains main.py and run "python main.py" in the terminal


from __future__ import annotations
from collections import deque
import heapq
import math


# Here we declare some constants, a type Position and custom exception to make code cleaner and
# easier to understand. They will be used later in the code
START_VALUE = 'S'
GOAL_VALUE = 'G'
OBSTACLE_VALUE = 'X'

Position = tuple[int, int]


class EmptyFileError(Exception):

    def __init__(self, message: str = "Graph doesn't have any rows and columns"):
        super().__init__(message)


# This class is used in subtask A and B. It contains all the necessary information about the "node" in the
# graph/maze. Position determines row and column of the node, g is the cost from the start to
# the node, h is heuristic value which is estimated value to the goal from the node, f is the total
# estimated value (g+h), and parent is the parent node of the current node
class GraphNode:

    def __init__(
            self,
            position: Position,
            g: float = float('inf'),
            h: float = 0.0,
            parent: GraphNode = None
    ):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent


# To run each subtask we will call a method of Maze class
class Maze:

    # in the __init__ during creation of a Maze instance we will read a file
    # To read a file we will use a standard python statement with, then we will create a list of strings
    # for example: ['S1234X6789', '1X2X4X6X89', ...]
    # As we can access an individual character of a string by index we will assume that we have 2d array

    # this 2d array will be our graph representation
    # we can create adjacency matrix, but each cell have at most 4 neighbours, so we will waste
    # lots of memory by creating adjacency matrix, adjacency list solves this problem, but there is no
    # need to create it if we already have a nice representation

    def __init__(self, filename: str):
        try:
            with open(filename, "r") as file:
                self.graph = [line.strip() for line in file]
                if len(self.graph) == 0:
                    raise EmptyFileError()

        except FileNotFoundError:
            print("This file does not exist")

        except Exception as e:
            print(f"Error while reading the file: {e}")


    # This method is used to find the position of a character in the graph (S or G), because they
    # might be located not in the same spot in all mazes. We use simple loop to find the position

    def find_position(self, char: str) -> Position | None:
        for row in range(len(self.graph)):
            for column in range(len(self.graph[0])):
                if self.graph[row][column] == char:
                    return row, column
        return None


    # This method is used to get the neighbours of the current node for 4-directional and 8-directional
    # movement (depends on the value of parameter allow_diagonals)
    # First, we calculate all possible position of neighbours and then check if they are in the boundaries
    # of the maze and if a neighbour is not an obstacle

    def get_neighbors(self, position: Position, allow_diagonals: bool) -> list[Position]:
        row, column = position
        rows, cols = len(self.graph), len(self.graph[0])
        possible_moves = [(row, column - 1), (row, column + 1), (row - 1, column), (row + 1, column)]
        if allow_diagonals:
            possible_moves.extend(
                [
                    (row - 1, column - 1), (row - 1, column + 1),
                    (row + 1, column - 1), (row + 1, column + 1)
                ]
            )
        return [
            (row, col) for row, col in possible_moves
            if 0 <= row < rows and 0 <= col < cols and self.graph[row][col] != OBSTACLE_VALUE
        ]


    # This method is used to build a path. It starts from the goal node, then takes its parent and
    # continues until the path is not fully explored (node becomes None, because the parent of start
    # node is None by default)

    def build_path(self, goal_node: GraphNode) -> str:
        path = []
        current = goal_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        return " -> ".join(str(pos) for pos in path[::-1])


    # Here we call function for subtask a and print the results
    # For solving the task we are using depth first search because it explores nodes level by level and
    # the first time we reach G, it is guaranteed that we have used the fewest moves.
    # Time complexity is O(V + E), where v is the number of vertices (row * column) and
    # E is the number of edges
    # The space complexity of the algorithm is O(V).

    def subtask_a(self, allow_diagonals : bool = False):
        num_of_moves, path = self.breadth_first_search(allow_diagonals)
        print("Subtask A")
        print(f"Minimum number of moves: {num_of_moves}")
        print(f"Path from S to G: {path}")
        print(f"Movement mode used: {'8-directional movement' if allow_diagonals else '4-directional movement'}")


    # This method is used to find the path with the smallest number of steps

    def breadth_first_search(self, allow_diagonals : bool = False):
        # we start with searching for start and goal position in the maze
        # find_position can return None if nothing is found, but we don't check for this condition
        # because the task states that "The maze contains exactly one S", so we assume that it exists
        start_pos = self.find_position(START_VALUE)
        goal_pos = self.find_position(GOAL_VALUE)

        # We take the start cell of a maze and create an instance of a GraphNode. We assign position,
        # distance from start to the node (which is 0) and parent is None
        start_node = GraphNode(position=start_pos, g=0, parent=None)

        # visited data structure is a set that stores all the nodes we have already visited (we store
        # positions)
        visited = set(start_pos)

        # we will add node objects to the queue to store them layer by layer and then explore
        queue = deque([start_node])

        # while there are nodes to be explored
        while queue:
            # we take the first added node from the queue
            current_node = queue.popleft()

            # if its position is equal to the position of goal node we stop exploring and return distance
            # from the start to the goal and build the path
            if current_node.position == goal_pos:
                return current_node.g, self.build_path(current_node)

            # otherwise, we take all the neighbours of the current node and for each of them:
            for neighbour_position in self.get_neighbors(current_node.position, allow_diagonals):

                # if neighbours has not been visited, we create an object of this node. We assign position,
                # g is equal to the distance from the start to the current node + 1, and parent is current node
                # we add position to the visited set and object to the queue
                if neighbour_position not in visited:
                    neighbour = GraphNode(position=neighbour_position, g=current_node.g + 1, parent=current_node)
                    visited.add(neighbour_position)
                    queue.append(neighbour)

        # if there is no path we return empty values
        return 0, []


    # Here we call function for subtask b and print the results
    # We assume that the cost of moving from cell u to cell v is the value of cell u (Leaving Cost)
    # For solving the task we are using A* algorithm because it's more efficient than Dijkstra's with a
    # good heuristic
    # Heuristic we are using is euclidian distance because it is commonly used in 2D mazes as it matches
    # how movement works (4 8-directional and 8-directional)
    # Time and space complexity: O(b^d), where b is branching factor and d is depth of the optimal path

    def subtask_b(self, allow_diagonals : bool = False):
        path_value, path = self.minimum_cost_path(allow_diagonals)
        print("Subtask B")
        print(f"Minimum total cost: {path_value}")
        print(f"Path from S to G: {path}")
        print("Cost model used: Leaving Cost")
        print(f"Movement mode used: {'8-directional movement' if allow_diagonals else '4-directional movement'}")


    # This method is used to calculate euclidian distance for heuristic. It uses a standard math formula

    def calculate_euclidean_distance(self, pos1: Position, pos2: Position) -> float:
        row1, col1 = pos1
        row2, col2 = pos2
        return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)


    # This is the main function for subtask b (looking for minimum cost path)

    def minimum_cost_path(self, allow_diagonals : bool = False):
        # we start with searching for start and goal position in the maze
        # find_position can return None if nothing is found, but we don't check for this condition
        # because the task states that "The maze contains exactly one S", so we assume that it exists
        start_pos = self.find_position(START_VALUE)
        goal_pos = self.find_position(GOAL_VALUE)

        # We take the start cell of a maze and create an instance of a GraphNode. We assign position,
        # distance from start to the node (which is 0) and we calculate heuristic (distance from the
        # start to the goal)
        start_node = GraphNode(position=start_pos, g=0, h=self.calculate_euclidean_distance(start_pos, goal_pos))

        # We initialize open list and dict - they will keep track of nodes which we have to visit
        # We have 2 data structures so that it is more convenient to work
        # List will be in form of a priority queue. Here we store total distance to the goal and position
        # of the node. We will take nodes from it to examine and delete after this
        # Dict will be in from of a storage where we will store nodes permanently. The key is a position
        # of a node, and value is the node itself
        # Also, we have closed set - it will keep track of nodes which we have already visited

        open_list = [(start_node.f, start_node.position)]
        open_dict = {start_node.position: start_node}
        closed_set = set()

        # this value will store the value of the minimum cost path
        path_value = 0

        # while there are nodes to be examined
        while open_list:
            # we take position of the node with the lowest total value
            _, current_pos = heapq.heappop(open_list)

            # we take node with this position
            current_node = open_dict[current_pos]

            # we take value of the node
            current_node_value = self.graph[current_pos[0]][current_pos[1]]

            # path cost is now equal to the cost from the start to the current node
            path_value = current_node.g

            # if position of the current node is equal to the position of the goal, we return path cost
            # and build the path
            if current_pos == goal_pos:
                return path_value, self.build_path(current_node)

            # otherwise we add current node to the examined nodes
            closed_set.add(current_pos)

            # then we take all the neighbours of the current node and for each of them:
            for neighbor_pos in self.get_neighbors(current_pos, allow_diagonals):

                # if neighbour has already been examined we move to the next one
                if neighbor_pos in closed_set:
                    continue

                # we calculate distance from start to the neighbour (distance from the start to the current
                # + cost of the current node - leaving cost)
                node_g = current_node.g + int(current_node_value) if (current_node_value not in
                                                                      (START_VALUE, GOAL_VALUE)) else 0

                # if neighbour has not been added to the list of the nodes we need to examine,
                # we create an object of the node and add it to both the list and dict
                if neighbor_pos not in open_dict:
                    neighbor = GraphNode(
                        position=neighbor_pos,
                        g=node_g,
                        h=self.calculate_euclidean_distance(neighbor_pos, goal_pos),
                        parent=current_node
                    )
                    heapq.heappush(open_list, (neighbor.f, neighbor.position))
                    open_dict[neighbor.position] = neighbor

                # if neighbours is already in the list of nodes we need to examine, but its current
                # distance is less then the one stored, we update values
                elif node_g < open_dict[neighbor_pos].g:
                    neighbor = open_dict[neighbor_pos]
                    neighbor.g = node_g
                    neighbor.f = node_g + neighbor.h
                    neighbor.parent= current_node

        # if there is no path we return empty values
        return path_value, []


    # Here we call functions for subtasks a and b and print the results
    # Difference is that in some calls diagonal movement is allowed, in others it is not
    # Allowing diagonal moves change the shortest path because instead of 2 moves we make only one, also
    # diagonal moves open new paths for us, which potentially can be shorter
    # Allowing diagonal moves change the cheapest path because they might help us avoid expensive cells,
    # reach cheap regions faster and reduce total leaving costs
    # The path with the fewest moves can be different from the path with the lowest cost because it can
    # take only 2 moves for us to get to the goal but its cost will be 100, and it can take 15 moves to
    # get to the same goal, but cost will be much smaller
    # Time and space complexity for subtask a and b stay the same

    def subtask_c(self):
        print("Subtask C")
        print()
        self.subtask_a(allow_diagonals=False)
        print()
        self.subtask_a(allow_diagonals=True)
        print()
        self.subtask_b(allow_diagonals=False)
        print()
        self.subtask_b(allow_diagonals=True)


maze = Maze("maze_10x10_A.txt")
maze.subtask_a()
print()
maze.subtask_b()
print()
maze.subtask_c()
