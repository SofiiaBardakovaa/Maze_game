# Maze Graph Algorithms

Graph algorithms project based on maze representation using Python.

This project was created for the Final Group Project on Algorithms.  
The maze is interpreted as a graph and different graph algorithms are applied to solve several subtasks.

---

# Team Members

- Kateryna Fedkova 
- Sofiia Bardakova

---

# Features

The project supports:

- Subtask A - Shortest Path by Number of Moves
- Subtask B - Minimum-Cost Path
- Subtask C - Movement Mode Comparison
- Subtask D - Maximum Flow
- Subtask E - Minimum Spanning Tree

Additional extensions:

- Support for 4-directional movement
- Support for 8-directional movement
- Interactive console menu
- Command selection system

---

# Maze Format

Maze is stored in a text file (maze_10x10_A.txt).

Example:

```text
S1234
1XX24
230X5
2X111
3333G
```

Symbols:

| Symbol | Meaning |
|---|---|
| S | Start |
| G | Goal |
| X | Wall |
| 0-9 | Passable cell |

---

# Graph Representation

The maze is represented as graph where:

- every non-wall cell is treated as a vertex
- neighbouring cells are connected with edges

Graph is stored using adjacency list representation.

---

# Algorithms Used

| Subtask | Algorithm |
|---|---|
| A | Breadth First Search |
| B | A* Algorithm |
| C | BFS + A* |
| D | Edmonds-Karp Maximum Flow |
| E | Prim’s Minimum Spanning Tree |

---

# How To Run

Run program:

```bash
python main.py
```

Program will ask:

- which subtask to execute
- which movement mode to use

---

# Movement Modes

## 4-directional movement

Allowed moves:

- up
- down
- left
- right

## 8-directional movement

Allowed moves:

- up
- down
- left
- right
- diagonals

---

# Subtask Descriptions

## Subtask A — Shortest Path

Finds path with minimum number of moves from S to G using BFS.

Output:

- minimum moves
- path
- movement mode

---

## Subtask B — Minimum-Cost Path

Finds minimum-cost path using A* algorithm.

Cost model used:

```text
Leaving Cost
cost(u, v) = value(u)
```

Output:

- minimum cost
- path
- movement mode

---

## Subtask C — Movement Comparison

Compares results between:

- 4-directional movement
- 8-directional movement

---

## Subtask D — Maximum Flow

Interprets maze as directed flow network.

- Source = G
- Sink = S

Capacity rule:

```text
capacity(u, v) = value(v)
```

Special cases:

```text
capacity into S = 100
capacity into G = 100
```

Algorithm used:

- Edmonds-Karp

Output:

- maximum flow value
- positive flow edges
- movement mode

---

## Subtask E — Minimum Spanning Tree

Interprets maze as undirected weighted graph.

Weight rule:

```text
weight(u, v) = value(u) + value(v)
```

Algorithm used:

- Prim’s algorithm

Output:

- total MST weight
- number of vertices
- number of edges
- MST edges
- whether G is reachable from S

---

# Time Complexities

| Algorithm | Complexity |
|---|---|
| BFS | O(V + E) |
| A* | O(b^d) |
| Edmonds-Karp | O(VE^2) |
| Prim’s Algorithm | O(E log V) |

---

# Data Structures Used

- Lists
- Dictionaries
- Sets
- Queues
- Priority Queues (Heap)
- Graph adjacency lists

---

# Project Structure

```text
main.py
maze_10x10_A.txt
README.md
maze_output.txt
```

---

# Notes

- Program supports mazes up to 100x100
- Walls are ignored during graph construction
- Cycles in MST are avoided using visited set
- Residual graph is used in maximum flow algorithm

---

# License

Educational project.
