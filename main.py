import matplotlib.pyplot as plt
import numpy as np
import os
import random
from matplotlib.animation import FuncAnimation

from load_data import load_grid_map, load_queries
from algorithms.bfs import bfs
from algorithms.dfs import dfs_non_recursive
from algorithms.a_star import a_star
from algorithms.ao_star import ao_star
from algorithms.water_jug import water_jug_solver
from find_goal import find_goal
from query_matcher import match_goal_from_query

# Color-coding for different algorithms
ALGORITHM_COLORS = {
    "BFS": "blue",
    "DFS": "red",
    "A*": "green",
    "AO*": "purple"
}

# Animate the path step-by-step on the grid
def animate_path(grid, path, title="Grid Visualization", path_color="red"):
    grid_array = np.array(grid)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(grid_array, cmap="Blues", interpolation="nearest")
    ax.set_title(title, fontsize=16, fontweight='bold')

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ax.text(j, i, str(grid[i][j]), ha='center', va='center', color='black', fontsize=12, fontweight='bold')

    # Highlight start
    ax.text(0, 0, 'S', ha='center', va='center', color='green', fontsize=15, fontweight='bold')

    # Highlight dynamic goal (last node in path) or fallback
    if path:
        goal_node = path[-1]
    else:
        goal_node = find_goal(grid)
    ax.text(goal_node[1], goal_node[0], 'G', ha='center', va='center', color='yellow', fontsize=15, fontweight='bold')

    path_line, = ax.plot([], [], color=path_color, marker='o', markersize=8, linestyle='-', linewidth=2)

    def init():
        path_line.set_data([], [])
        return path_line,

    def update(frame):
        x_vals = [p[1] for p in path[:frame+1]]
        y_vals = [p[0] for p in path[:frame+1]]
        path_line.set_data(x_vals, y_vals)
        return path_line,

    anim = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, interval=300)
    plt.show()

# Static visualization (used for combined plots)
def visualize_grid(grid, path=None, title="Grid Visualization", path_color="red", save_path=None, ax=None):
    grid_array = np.array(grid)

    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    ax.imshow(grid_array, cmap="Blues", interpolation="nearest")
    ax.set_title(title, fontsize=14, fontweight='bold')

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ax.text(j, i, str(grid[i][j]), ha='center', va='center', color='black', fontsize=10, fontweight='bold')

    if path:
        for (i, j) in path:
            ax.text(j, i, 'P', ha='center', va='center', color=path_color, fontsize=12, fontweight='bold')

    ax.text(0, 0, 'S', ha='center', va='center', color='green', fontsize=14, fontweight='bold')

    # Highlight dynamic goal (last node in path) or fallback
    if path:
        goal_node = path[-1]
    else:
        goal_node = find_goal(grid)
    ax.text(goal_node[1], goal_node[0], 'G', ha='center', va='center', color='yellow', fontsize=14, fontweight='bold')

    ax.set_xticks([])
    ax.set_yticks([])

    if save_path:
        plt.savefig(save_path)
        plt.close()

def main():
    # Load grid map and queries
    grid = load_grid_map("data/maps/grid_map_1.txt")
    queries = load_queries("data/queries/queries.txt")

    # Pick random query and classify goal
    query = random.choice(queries)
    classified_goal = match_goal_from_query(query['query'])

    # Merged query_to_goal dictionary mapping goals to grid coordinates
    query_to_goal = {
        "hospital": (3, 4),
        "shelter": (2, 4),
        "resource_delivery": (0, 3),
        "alt_path": (2, 2),
        "flood": (3, 3),
        "road_block": (1, 1),
        "road_open": (0, 0),
        "road": (1, 2),
        "traffic": (0, 2),
        "fire": (1, 0),
        "earthquake": (2, 0),
        "landslide": (3, 0),
        "storm": (3, 2),
        "accident": (1, 3),
        "crime": (2, 1),
        "rescue": (3, 1),
        "search": (0, 3),
        "report": (1, 4),
        "unknown": (0, 0),
        # add more if needed
    }

    start = (0, 0)
    goal = query_to_goal.get(classified_goal, (0, 0))

    print("Selected Query:", query['query'])
    print("Matched Goal:", classified_goal)
    print("Goal Position in grid:", goal)

    os.makedirs("visualizations", exist_ok=True)

    # Run BFS and animate
    bfs_path = bfs(grid, start, goal)
    print("\nBFS Path Found:", bfs_path)
    animate_path(grid, bfs_path, title="BFS Path", path_color=ALGORITHM_COLORS["BFS"])

    # Run DFS and animate
    dfs_path = dfs_non_recursive(grid, start, goal)
    print("\nDFS Path Found:", dfs_path)
    animate_path(grid, dfs_path, title="DFS Path", path_color=ALGORITHM_COLORS["DFS"])

    # Run A* and animate
    astar_path = a_star(grid, start, goal)
    print("\nA* Path Found:", astar_path)
    animate_path(grid, astar_path, title="A* Path", path_color=ALGORITHM_COLORS["A*"])

    # Run AO* and animate
    ao_star_path = ao_star(grid, start, goal)
    print("\nAO* (Fallback BFS) Path Found:", ao_star_path)
    animate_path(grid, ao_star_path, title="AO* Path", path_color=ALGORITHM_COLORS["AO*"])

    # Combined visualization of all paths side-by-side
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    visualize_grid(grid, bfs_path, title="BFS", path_color=ALGORITHM_COLORS["BFS"], ax=axs[0])
    visualize_grid(grid, dfs_path, title="DFS", path_color=ALGORITHM_COLORS["DFS"], ax=axs[1])
    visualize_grid(grid, astar_path, title="A*", path_color=ALGORITHM_COLORS["A*"], ax=axs[2])
    visualize_grid(grid, ao_star_path, title="AO*", path_color=ALGORITHM_COLORS["AO*"], ax=axs[3])
    plt.tight_layout()
    plt.savefig("visualizations/combined.png")
    plt.show()

    # Water Jug Problem demonstration
    print("\nWater Jug Problem (Jug capacities: 4 and 3; Target: 2):")
    jug_path = water_jug_solver(4, 3, 2)
    if jug_path:
        for state in jug_path:
            print(state)
    else:
        print("No solution found for the water jug problem.")

if __name__ == "__main__":
    main()
