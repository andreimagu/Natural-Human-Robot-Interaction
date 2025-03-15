"""
Very often, problems related to the field of artificial intelligence are abstracted as a **state space search**. The following script aims to present an informed search algorithm: **A***.

Trying to solve the following problem: finding a path between two positions on a 2D map with obstacles.

Search problems are generally abstracted with graphs. The 2D map can be seen as an undirected graph where each node corresponds to a cell on the map, and an edge connects nodes corresponding to adjacent cells.
"""

#### The labyrinth

# We will represent the labyrinth as a two-dimensional array (a list of lists)

height = 10
width = 20

# We build the labyrinth as a list of lists
labyrinth = [[0 for c in range(width)] for r in range(height)]

# We place some obstacles on the map
for r in range(2, 7):
    labyrinth[r][6] = 1
    labyrinth[6][r] = 1
labyrinth[2][7] = 1

# Display the labyrinth
import matplotlib.pyplot as pyplot
from heapq import heappop, heappush
from math import sqrt

# Starting and goal positions
start = (5, 5)
final = (8, 8)

# Labyrinth goal check
is_final_labyrinth = lambda position: position == final

# Valid neighbor check
def is_good(pos):
    return 0 <= pos[0] < height and 0 <= pos[1] < width and labyrinth[pos[0]][pos[1]] == 0

# Neighbor function for labyrinth
def get_neighbours_labyrinth(pos):
    return list(filter(is_good, [(pos[0] + d, pos[1]) for d in [-1, 1]] + [(pos[0], pos[1] + d) for d in [-1, 1]]))

# Display the state with path and discovered cells
def print_state_labyrinth(discovered, results):
    cost_map = [[discovered[(r, c)][0] if (r, c) in discovered else 0 for c in range(width)] for r in range(height)]
    fig, ax = pyplot.subplots()
    ax.imshow(cost_map, cmap='Greys', interpolation='nearest')
    for (i, j) in results:
        ax.text(j, i, '•', ha='center', va='center', color='blue')  # Path in blue dots
    pyplot.show()
    print("Path:", results)

# Heuristic functions
def euclidean_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

#### A* Algorithm
def astar(start, end, h, neighbours, is_final, print_state, print_flag=True):
    # Frontier, as a list (heap) of tuples (cost_f, node)
    min_heap = []
    heappush(min_heap, (0 + h(start, end), start))  # Initialize with start node

    # Discovered nodes as a dictionary node -> (cost_g-to-node, parent)
    discovered = {start: (0, None)}  # Start node cost_g=0 and no parent

    while min_heap:
        # Extract the first node from min_heap
        current_cost_f, crt_node = heappop(min_heap)

        # Check if current node is the final state
        if is_final(crt_node):
            break

        # Search all states neighboring the current one
        for next_node in neighbours(crt_node):
            # Calculate cost_g to the neighbor through the current node
            new_cost_g = discovered[crt_node][0] + 1

            # If the neighbor is undiscovered or a shorter path is found to it
            if next_node not in discovered or new_cost_g < discovered[next_node][0]:
                # Save the new node in discovered with updated cost_g and parent
                discovered[next_node] = (new_cost_g, crt_node)
                # Push the neighbor into the heap with the updated f cost
                heappush(min_heap, (new_cost_g + h(next_node, end), next_node))

    # Path reconstruction from end to start using the discovered dictionary
    path = []
    last_node = end
    while last_node in discovered:
        path.append(last_node)
        last_node = discovered[last_node][1]
    path.reverse()  # Reverse path from start to end

    # Print the path if flag is set
    if print_flag:
        print_state(discovered, path)

# Running A* with Euclidean Distance
print("Path using Euclidean distance heuristic:")
astar(start, final, euclidean_distance, get_neighbours_labyrinth, is_final_labyrinth, print_state_labyrinth)

# Running A* with Manhattan Distance
print("\nPath using Manhattan distance heuristic:")
astar(start, final, manhattan_distance, get_neighbours_labyrinth, is_final_labyrinth, print_state_labyrinth)
