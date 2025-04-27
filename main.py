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
from matplotlib.widgets import Button

ALGORITHM_COLORS = {
    "BFS": "blue",
    "DFS": "red",
    "A*": "green",
    "AO*": "purple"
}

class GridVisualizer:
    def __init__(self, maps_dir):
        self.maps_dir = maps_dir
        self.map_files = sorted([f for f in os.listdir(maps_dir) if f.startswith('grid_map_') and f.endswith('.txt')])
        self.current_map_index = 0
        self.grid = self.load_current_map()
        self.start = (0, 0)
        self.goal = find_goal(self.grid)
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.setup_mode = True
        self.current_selection = 'start'
        self.paths = {}
        self.current_algorithm = None
        self.algorithms = ["BFS", "DFS", "A*", "AO*"]
        self.algorithm_index = 0
        self.setup_plot()
        self.setup_change_map_button()

    def load_current_map(self):
        file_path = os.path.join(self.maps_dir, self.map_files[self.current_map_index])
        return load_grid_map(file_path)

    def setup_plot(self):
        self.ax.clear()
        grid_array = np.array(self.grid)
        self.ax.imshow(grid_array, cmap="Blues", interpolation="nearest")
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.ax.text(j, i, str(self.grid[i][j]), ha='center', va='center', color='black', fontsize=10, fontweight='bold')
        self.ax.text(self.start[1], self.start[0], 'S', ha='center', va='center', color='green', fontsize=14, fontweight='bold')
        self.ax.text(self.goal[1], self.goal[0], 'G', ha='center', va='center', color='yellow', fontsize=14, fontweight='bold')
        if self.setup_mode:
            title = f"Map {self.current_map_index+1}/{len(self.map_files)}: Click to set {'START' if self.current_selection == 'start' else 'GOAL'} position"
        else:
            title = f"Map {self.current_map_index+1}/{len(self.map_files)}: Path Finding: {self.current_algorithm}" if self.current_algorithm else "Path Finding"
        self.ax.set_title(title, fontsize=16, fontweight='bold')
        self.fig.canvas.draw()

    def setup_change_map_button(self):
        change_map_ax = plt.axes([0.8, 0.9, 0.15, 0.07])
        self.change_map_button = Button(change_map_ax, 'Change Map')
        self.change_map_button.on_clicked(self.change_map)

    def change_map(self, event):
        if hasattr(self, 'anim') and self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None
        self.current_map_index = (self.current_map_index + 1) % len(self.map_files)
        self.grid = self.load_current_map()
        self.start = (0, 0)
        self.goal = find_goal(self.grid)
        self.setup_mode = True
        self.current_selection = 'start'
        self.paths = {}
        self.current_algorithm = None
        self.algorithm_index = 0
        self.setup_plot()

    def onclick(self, event):
        if event.inaxes != self.ax:
            return
        x, y = int(round(event.ydata)), int(round(event.xdata))
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            if self.grid[x][y] != 1:
                if self.current_selection == 'start':
                    self.start = (x, y)
                    self.current_selection = 'goal'
                elif self.current_selection == 'goal':
                    self.goal = (x, y)
                    self.current_selection = 'start'
                    self.setup_mode = False
                    self.calculate_paths()
                    self.setup_animation_controls()
                self.setup_plot()

    def calculate_paths(self):
        self.paths['BFS'] = bfs(self.grid, self.start, self.goal)
        self.paths['DFS'] = dfs_non_recursive(self.grid, self.start, self.goal)
        self.paths['A*'] = a_star(self.grid, self.start, self.goal)
        ao_path, _ = ao_star(self.grid, self.start, self.goal)
        self.paths['AO*'] = ao_path
        self.current_algorithm = self.algorithms[0]

    def setup_animation_controls(self):
        plt.subplots_adjust(bottom=0.2)
        next_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
        self.next_button = Button(next_ax, 'Next Algorithm')
        self.next_button.on_clicked(self.next_algorithm)
        animate_ax = plt.axes([0.1, 0.05, 0.2, 0.075])
        self.animate_button = Button(animate_ax, 'Animate Path')
        self.animate_button.on_clicked(self.animate_current_path)

    def next_algorithm(self, event):
        self.algorithm_index = (self.algorithm_index + 1) % len(self.algorithms)
        self.current_algorithm = self.algorithms[self.algorithm_index]
        self.setup_plot()

    def animate_current_path(self, event):
        if not self.current_algorithm or not self.paths[self.current_algorithm]:
            return
        if hasattr(self, 'anim') and self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None
        path = self.paths[self.current_algorithm]
        color = ALGORITHM_COLORS[self.current_algorithm]
        line, = self.ax.plot([], [], color=color, marker='o', markersize=8, linewidth=2)
        def init():
            line.set_data([], [])
            return line,
        def update(frame):
            x_data = [p[1] for p in path[:frame+1]]
            y_data = [p[0] for p in path[:frame+1]]
            line.set_data(x_data, y_data)
            return line,
        self.anim = FuncAnimation(self.fig, update, frames=len(path), init_func=init, blit=True, interval=300)
        plt.draw()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    maps_dir = os.path.join(script_dir, "data/maps")
    visualizer = GridVisualizer(maps_dir)
    visualizer.fig.canvas.mpl_connect('button_press_event', visualizer.onclick)
    plt.show()

if __name__ == "__main__":
    main()
