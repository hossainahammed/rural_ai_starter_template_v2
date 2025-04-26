import matplotlib.pyplot as plt
import numpy as np
import os
from load_data import load_grid_map, load_queries
from algorithms.bfs import bfs
from algorithms.dfs import dfs_non_recursive
from algorithms.a_star import a_star
from algorithms.ao_star import ao_star
from algorithms.water_jug import water_jug_solver
from find_goal import find_goal
from query_matcher import match_goal_from_query
import random
from matplotlib.animation import FuncAnimation

# Color-coding for different algorithms
ALGORITHM_COLORS = {
    "BFS": "blue",
    "DFS": "red",
    "A*": "green",
    "AO*": "purple"
}

# Visualize the grid with a step-by-step animation of the path
def animate_path(grid, path, title="Grid Visualization", path_color="red"):
    grid_array = np.array(grid)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(grid_array, cmap="Blues", interpolation="nearest")
    ax.set_title(title, fontsize=16, fontweight='bold')

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ax.text(j, i, str(grid[i][j]), ha='center', va='center', color='black', fontsize=12, fontweight='bold')

    # Highlight the start and goal positions
    ax.text(0, 0, 'S', ha='center', va='center', color='green', fontsize=15, fontweight='bold')
    goal = find_goal(grid)
    ax.text(goal[1], goal[0], 'G', ha='center', va='center', color='yellow', fontsize=15, fontweight='bold')

    # Prepare the path for animation
    path_line, = ax.plot([], [], color=path_color, marker='o', markersize=8, linestyle='-', linewidth=2)

    def init():
        path_line.set_data([], [])
        return path_line,

    def update(frame):
        x_vals = [p[1] for p in path[:frame+1]]
        y_vals = [p[0] for p in path[:frame+1]]
        path_line.set_data(x_vals, y_vals)
        return path_line,

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, interval=300)

    # Show the animation
    plt.show()

# Visualize and optionally save to file
def visualize_grid(grid, path=None, title="Grid Visualization", path_color="red", save_path=None, ax=None):
    grid_array = np.array(grid)

    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    ax.imshow(grid_array, cmap="Blues", interpolation="nearest")
    ax.set_title(title, fontsize=14, fontweight='bold')

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ax.text(j, i, str(grid[i][j]), ha='center', va='center', color='black', fontsize=10, fontweight='bold')

    # Path
    if path:
        for (i, j) in path:
            ax.text(j, i, 'P', ha='center', va='center', color=path_color, fontsize=12, fontweight='bold')

    # Start and Goal
    ax.text(0, 0, 'S', ha='center', va='center', color='green', fontsize=14, fontweight='bold')
    goal = find_goal(grid)
    ax.text(goal[1], goal[0], 'G', ha='center', va='center', color='yellow', fontsize=14, fontweight='bold')

    ax.set_xticks([])
    ax.set_yticks([])

    if save_path:
        plt.savefig(save_path)
        plt.close()

def main():
    grid = load_grid_map("data/maps/grid_map_1.txt")
    queries = load_queries("data/queries/queries.txt")

    query = random.choice(queries)
    classified_goal = match_goal_from_query(query['query'])

    start = (0, 0)
    goal = find_goal(grid)

    print("Selected Query:", query['query'])
    print("Matched Goal:", classified_goal)
    print("Goal Position in grid:", goal)

    # Make sure output directory exists
    os.makedirs("visualizations", exist_ok=True)

    # BFS
    bfs_path = bfs(grid, start, goal)
    print("\nBFS Path Found:", bfs_path)
    animate_path(grid, bfs_path, title="BFS Path", path_color=ALGORITHM_COLORS["BFS"])

    # DFS
    dfs_path = dfs_non_recursive(grid, start, goal)
    print("\nDFS Path Found:", dfs_path)
    animate_path(grid, dfs_path, title="DFS Path", path_color=ALGORITHM_COLORS["DFS"])

    # A*
    astar_path = a_star(grid, start, goal)
    print("\nA* Path Found:", astar_path)
    animate_path(grid, astar_path, title="A* Path", path_color=ALGORITHM_COLORS["A*"])

    # AO*
    ao_star_path = ao_star(grid, start, goal)
    print("\nAO* (Fallback BFS) Path Found:", ao_star_path)
    animate_path(grid, ao_star_path, title="AO* Path", path_color=ALGORITHM_COLORS["AO*"])

    # Combine all visualizations side-by-side
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    visualize_grid(grid, bfs_path, title="BFS", path_color=ALGORITHM_COLORS["BFS"], ax=axs[0])
    visualize_grid(grid, dfs_path, title="DFS", path_color=ALGORITHM_COLORS["DFS"], ax=axs[1])
    visualize_grid(grid, astar_path, title="A*", path_color=ALGORITHM_COLORS["A*"], ax=axs[2])
    visualize_grid(grid, ao_star_path, title="AO*", path_color=ALGORITHM_COLORS["AO*"], ax=axs[3])
    plt.tight_layout()
    plt.savefig("visualizations/combined.png")
    plt.show()

    # Water Jug
    print("\nWater Jug Problem (Jug capacities: 4 and 3; Target: 2):")
    jug_path = water_jug_solver(4, 3, 2)
    if jug_path:
        for state in jug_path:
            print(state)
    else:
        print("No solution found for the water jug problem.")

if __name__ == "__main__":
    main()
