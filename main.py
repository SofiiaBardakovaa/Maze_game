# Kateryna Fedkova   ID: 260ADB019  GROUP: ADBD0
# Sofiia Bardakova ID: 260ADB020
# Programming language: Python
# To run the program: go into the folder which contains main.py and run "python main.py" in the terminal
# Command-line options are added for selecting tasks, cost models, and movement modes.

from __future__ import annotations
from collections import deque
import heapq
import math
import sys


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

    #Idea for Breadth First Search was adapted from: https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
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
        visited = {start_pos}

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

    # The idea of A* algorithm was adapted from https://www.geeksforgeeks.org/dsa/a-search-algorithm/
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


    # Here we call function for subtask D and print the results
    # For solving the task we are using Edmonds-Karp algorithm
    # Edmonds-Karp is an implementation of Ford-Fulkerson algorithm which uses Breadth-First Search
    # to find augmenting paths in the residual graph.
    #
    # Every non-wall cell is treated as a vertex in this subtask. Directed edges are created between
    # neighbouring cells. Capacity(u, v) = value(v), Capacities into S and G are set to 100.
    #
    # This algorithm repeatedly 1) finds a path from G to S using BFS, 2) finds the minimum residual
    # capacity on this path (bottleneck), 3) increase total flow by this bottleneck value, 4) update residual capacity.
    #
    # Time complexity: O(V*(E**2)), where V is the number of vertices and E is the number of edges.
    # Explanation: Breadth first search works in O(V + E). In graphs E is usually larger than V, so BFS becomes O(E).
    # Edmonds-Karp may run BFS up to O(VE) times. Therefore total complexity becomes:
    # O(VE) * O(E) = O(V*(E**2))
    #
    # Space complexity: O(V + E)

    def subtask_d(self, allow_diagonals=False):

        # We call maximum_flow method which returns
        # maximum flow value, graph with final positive flows, original graph with capacities
        max_flow, flow_graph, original_graph = self.maximum_flow(allow_diagonals)

        print("Subtask D")
        print(f"Maximum flow value from G to S: {max_flow}")

        print("Positive flow edges:")

        # We go through all edges in the flow graph
        # and print only edges with positive flow
        for u in flow_graph:
            for v, flow in flow_graph[u].items():

                if flow > 0:
                    capacity = self.build_flow_graph(
                        allow_diagonals
                    )[u][v]

                    print(f"{u} -> {v}: {flow}/{capacity}")

        print(
            f"Movement mode used: "
            f"{'8-directional movement' if allow_diagonals else '4-directional movement'}"
        )

    # This method is used to get numeric value of a maze cell.
    # We need it when building capacities for the flow network.
    #
    # First, we get row and column from the position tuple.
    # Then we take the character stored in the maze at this position.
    #
    # If the cell is S or G, we return 0.
    # Otherwise, digit characters are converted into integers.

    def get_cell_value(self, position: Position) -> int:
        row, col = position
        value = self.graph[row][col]

        if value in (START_VALUE, GOAL_VALUE):
            return 0

        return int(value)


    # This method is used to build a graph for subtask d (maximum flow)
    # We represent the maze as directed graph where every non-wall cell is a vertex
    # and edges connect neighbouring cells
    #
    # We use adjacency list representation because each cell has only few neighbours,
    # so it is memory efficient

    def build_flow_graph(self, allow_diagonals=False):
        # Graph is stored as adjacency list.
        # For every vertex we store neighbours and capacities.
        graph = {}

        # Get maze dimensions
        rows = len(self.graph)
        cols = len(self.graph[0])

        # Go through all cells of the maze.
        # We examine every possible position.
        for row in range(rows):
            for col in range(cols):

                # Walls are not part of the graph
                if self.graph[row][col] == OBSTACLE_VALUE:
                    continue

                # Current cell becomes graph vertex
                current = (row, col)

                # Create adjacency list for current vertex
                graph[current] = {}

                # Get all valid neighbouring cells.
                # Depending on movement mode this includes: 4-directional neighbours or 8-directional neighbours
                for neighbor in self.get_neighbors(current, allow_diagonals):

                    # Get neighbour coordinates
                    nr, nc = neighbor

                    # Get value stored in neighbour cell
                    neighbor_value = self.graph[nr][nc]

                    # Capacities into S and G are set to 100
                    if neighbor_value in (START_VALUE, GOAL_VALUE):
                        capacity = 100

                    # Otherwise capacity equals value of destination cell
                    else:
                        capacity = int(neighbor_value)

                    # Add directed edge with its capacity
                    # from current vertex to neighbour vertex
                    graph[current][neighbor] = capacity

        # Return complete flow network
        return graph

    # This method is used in Edmonds-Karp algorithm to find augmenting path
    # in the residual graph using breadth first search.
    # We use BFS because Edmonds-Karp always searches shortest augmenting paths
    # by number of edges.

    def bfs_flow(self, residual_graph, source, sink, parent):

        # Visited set is used to avoid revisiting vertices
        visited = set()

        # Queue is used for breadth first search traversal
        queue = deque([source])

        # We mark source node as visited
        # because BFS starts from this vertex
        visited.add(source)

        # Main BFS loop.
        # Continue while there are vertices left to explore.

        while queue:
            # Take first added vertex from the queue.
            # BFS explores graph level by level.
            current = queue.popleft()

            # Explore all neighbours of current vertex.
            # We also get residual capacity of every edge.
            for neighbor, capacity in residual_graph[current].items():

                # We only visit vertices which were not visited before and have positive residual capacity
                if neighbor not in visited and capacity > 0:
                    visited.add(neighbor)

                    # Save parent to reconstruct path
                    parent[neighbor] = current

                    # If sink is reached, augmenting path exists
                    if neighbor == sink:
                        return True

                    # Add neighbour to queue for further exploration
                    queue.append(neighbor)

        # If BFS finishes without reaching sink,
        # augmenting path does not exist anymore.
        return False


    # This method is used to solve subtask d (maximum flow)
    # We use Edmonds-Karp algorithm because it is a standard algorithm
    # for finding maximum flow in directed graphs.
    # It repeatedly searches for augmenting paths using breadth first search.
    # Idea of Maximum flow problem was adapted from: https://www.geeksforgeeks.org/dsa/max-flow-problem-introduction/

    def maximum_flow(self, allow_diagonals=False):

        # In this subtask G is source and S is sink
        source = self.find_position(GOAL_VALUE)
        sink = self.find_position(START_VALUE)

        # Then we build original flow graph from the maze.
        # This graph stores all directed edges and their capacities.

        graph = self.build_flow_graph(allow_diagonals)

        # Residual graph is needed for Edmonds-Karp algorithm.
        # It stores remaining capacities after sending flow through edges.

        residual_graph = {}

        # Here we initialize residual graph.
        # Initially residual capacities are equal to original capacities
        # because no flow has been sent yet.

        for u in graph:

            # Create adjacency list for current vertex
            residual_graph[u] = {}

            # Go through all neighbours of current vertex
            for v in graph[u]:

                # Copy original capacities into residual graph
                residual_graph[u][v] = graph[u][v]


        # Edmonds-Karp algorithm also needs reverse edges.
        # Reverse edges allow the algorithm to redistribute flow later
        # if a better augmenting path is found

        for u in graph:

            # Go through all neighbours
            for v in graph[u]:

                # If neighbour is not yet in residual graph
                if v not in residual_graph:

                    # Create empty adjacency list
                    residual_graph[v] = {}

                # If reverse edge does not exist
                if u not in residual_graph[v]:

                    # Reverse edge initially has capacity 0
                    residual_graph[v][u] = 0

        # Variable which stores final maximum flow
        max_flow = 0

        # Graph which stores final positive flows
        flow_graph = {}

        # Initialize all flows with value 0

        for u in graph:

            # Create adjacency list for current vertex
            flow_graph[u] = {}

            # Go through all neighbours
            for v in graph[u]:

                # Initially all flows are 0
                flow_graph[u][v] = 0

        # Main Edmonds-Karp loop.
        # We repeatedly search for augmenting paths until none exist.

        while True:

            # Parent dictionary is used to reconstruct augmenting path
            parent = {}

            # Use BFS to search augmenting path in residual graph.
            # If no path exists algorithm stops.
            if not self.bfs_flow(residual_graph, source, sink, parent):
                break

            # path_flow stores bottleneck capacity of augmenting path.
            # We initialize it with infinity because we will search
            # for minimum edge capacity on the path.

            path_flow = float('inf')

            # Start from sink vertex
            current = sink

            # Traverse augmenting path backwards until source is reached

            while current != source:

                # Get parent of current vertex
                previous = parent[current]

                # Update bottleneck capacity
                path_flow = min(path_flow,
                                residual_graph[previous][current])

                # Move to previous vertex
                current = previous

            # Add bottleneck value to total maximum flow
            max_flow += path_flow

            # Start again from sink
            current = sink

            # Update residual capacities and flow graph
            # Traverse path backwards again
            while current != source:
                # Get parent vertex
                previous = parent[current]

                # Reduce residual capacity of forward edge
                residual_graph[previous][current] -= path_flow

                # Increase residual capacity of reverse edge
                residual_graph[current][previous] += path_flow

                # Add flow to final flow graph
                flow_graph[previous][current] += path_flow

                # Move to previous vertex
                current = previous

        # Return maximum flow, final flow graph and original graph
        return max_flow, flow_graph, graph



    # Here we call function for subtask e and print results.
    #
    # We use Prim's algorithm to compute minimum spanning tree.
    #
    # Time complexity: O(E log V), where V is the number of vertices and E is the number of edges.
    # Space complexity: O(V + E)

    def subtask_e(self, allow_diagonals=False):
        (
            total_weight,
            vertex_count,
            edge_count,
            mst_edges,
            goal_reachable
        ) = self.minimum_spanning_tree(allow_diagonals)

        print("Subtask E")

        print(f"Total MST weight: {total_weight}")

        print(f"Number of vertices: {vertex_count}")

        print(f"Number of edges in tree: {edge_count}")

        print("Tree edges:")

        for u, v, weight in mst_edges:
            print(f"{u} -> {v}: {weight}")

        print(
            f"Movement mode used: "
            f"{'8-directional movement' if allow_diagonals else '4-directional movement'}"
        )

        print(f"G reachable from S: {goal_reachable}")

    # This method builds undirected weighted graph for subtask e.
    # Every non-wall cell is treated as vertex.
    # Edges connect neighbouring cells.
    #
    # Weight rule:
    # weight(u, v) = value(u) + value(v)
    #
    # We use adjacency list representation because each cell
    # has only few neighbours, therefore adjacency list
    # is memory efficient.

    def build_weighted_graph(self, allow_diagonals=False):
        # Dictionary is used as adjacency list representation.
        graph = {}

        # Get maze dimensions
        rows = len(self.graph)
        cols = len(self.graph[0])

        # Go through all maze cells
        # Every valid cell may become graph vertex
        for row in range(rows):
            for col in range(cols):

                # Walls are not vertices
                if self.graph[row][col] == OBSTACLE_VALUE:
                    continue

                # Current maze cell becomes graph vertex
                current = (row, col)

                # Create adjacency list
                graph[current] = []

                # Get all neighbouring cells.
                # Depending on movement mode neighbours can be 4-directional or 8-directional

                for neighbor in self.get_neighbors(current, allow_diagonals):

                    # Weight = value(current) + value(neighbor)
                    weight = (
                            self.get_cell_value(current)
                            + self.get_cell_value(neighbor)
                    )
                    # Add neighbour and edge weight
                    # into adjacency list
                    graph[current].append((neighbor, weight))

        # Return completed weighted graph
        return graph

    # This method is used to compute minimum spanning tree
    # for subtask e using Prim's algorithm.
    #
    # Prim's algorithm always chooses minimum weight edge
    # which connects visited and unvisited vertices.
    #
    # Cycles are avoided because we never add edges
    # leading to already visited vertices.
    #
    # The algorithm only explores connected component
    # containing S, which matches task requirements.
    #
    # The idea of MST was adapted from: https://www.geeksforgeeks.org/dsa/what-is-minimum-spanning-tree-mst/

    def minimum_spanning_tree(self, allow_diagonals=False):

        # Build weighted graph from the maze
        graph = self.build_weighted_graph(allow_diagonals)

        # Find start and goal positions
        start = self.find_position(START_VALUE)
        goal = self.find_position(GOAL_VALUE)

        # Visited set stores vertices already included into MST
        visited = set()

        # List of edges included into minimum spanning tree
        mst_edges = []

        # Variable storing total weight of MST
        total_weight = 0

        # Priority queue is used to always select
        # edge with minimum weight.
        #
        # Heap format:
        # (weight, from_vertex, to_vertex)

        priority_queue = []

        # Prim's algorithm starts from start vertex
        visited.add(start)

        # Initially we add all edges from start vertex into heap.
        # Heap automatically keeps smallest edge on top.
        for neighbor, weight in graph[start]:
            heapq.heappush(
                priority_queue,
                (weight, start, neighbor)
            )

        # Main Prim's algorithm loop.
        # Continue while there are candidate edges in heap.
        while priority_queue:

            # Take edge with minimum weight
            weight, u, v = heapq.heappop(priority_queue)

            # If destination vertex was already visited,
            # adding this edge would create cycle,
            # therefore we skip it.
            if v in visited:
                continue

            # Add new vertex into MST
            visited.add(v)

            # Add edge into MST
            mst_edges.append((u, v, weight))

            # Increase total weight
            total_weight += weight

            # Add all outgoing edges from new vertex into heap.
            # Only edges leading to unvisited vertices are useful.
            for neighbor, edge_weight in graph[v]:

                if neighbor not in visited:
                    heapq.heappush(
                        priority_queue,
                        (edge_weight, v, neighbor)
                    )

        # Goal is reachable if it belongs
        # to connected component containing S
        goal_reachable = goal in visited

        return (
            total_weight,
            len(visited),
            len(mst_edges),
            mst_edges,
            goal_reachable
        )

# Interactive menu for running subtasks.
# Program asks user which subtask and movement mode should be used.

if __name__ == "__main__":

    # Default maze file
    filename = "maze_10x10_A.txt"

    # Create maze object
    maze = Maze(filename)

    # Main program loop
    # Program continues until user chooses to stop

    while True:

        print("Maze Graph Algorithms")
        print()

        # Ask user which subtask should be executed
        print("Choose subtask:")
        print("A - Shortest Path")
        print("B - Minimum Cost Path")
        print("C - Movement Comparison")
        print("D - Maximum Flow")
        print("E - Minimum Spanning Tree")
        print("ALL - Run all subtasks")

        task = input("Enter task: ").upper()

        # Ask user for movement mode
        print()
        print("Choose movement mode:")
        print("4 - 4-directional movement")
        print("8 - 8-directional movement")

        movement = input("Enter movement mode: ")

        # Enable diagonals only for mode 8
        allow_diagonals = movement == "8"

        print()

        # Execute selected subtask

        if task == "A":
            maze.subtask_a(allow_diagonals)

        elif task == "B":
            maze.subtask_b(allow_diagonals)

        elif task == "C":
            maze.subtask_c()

        elif task == "D":
            maze.subtask_d(allow_diagonals)

        elif task == "E":
            maze.subtask_e(allow_diagonals)

        elif task == "ALL":

            maze.subtask_a(allow_diagonals)
            print()

            maze.subtask_b(allow_diagonals)
            print()

            maze.subtask_c()
            print()

            maze.subtask_d(allow_diagonals)
            print()

            maze.subtask_e(allow_diagonals)

        else:
            print("Unknown task")

        # Ask user if program should continue
        print()

        continue_program = input(
            "Do you want to continue? (yes/no): "
        ).lower()

        # Stop program if user enters no
        if continue_program != "yes":
            print("Program finished")
            break

        print()