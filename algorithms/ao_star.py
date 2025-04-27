from collections import defaultdict
import math
from heapq import heappush, heappop

def ao_star(grid, start, goal):
    """
    Implementation of AO* algorithm for grid pathfinding.
    
    Args:
        grid: 2D list representing the grid where 0 is path and 1 is obstacle
        start: Tuple (x, y) representing start position
        goal: Tuple (x, y) representing goal position
    
    Returns:
        path: List of tuples representing the path from start to goal
        explored: Set of explored nodes for visualization
    """
    def heuristic(node):
        # Manhattan distance heuristic
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    
    def get_neighbors(node):
        x, y = node
        neighbors = []
        # Check all 4 directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(grid) and 
                0 <= new_y < len(grid[0]) and 
                grid[new_x][new_y] == 0):
                neighbors.append((new_x, new_y))
        return neighbors
    
    # Initialize data structures
    g_costs = defaultdict(lambda: float('inf'))
    g_costs[start] = 0
    f_costs = defaultdict(lambda: float('inf'))
    f_costs[start] = heuristic(start)
    
    open_list = [(f_costs[start], start)]
    closed_set = set()
    came_from = {}
    
    while open_list:
        current_f, current = heappop(open_list)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, closed_set
        
        closed_set.add(current)
        
        # Expand current node
        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue
                
            tentative_g = g_costs[current] + 1
            
            if tentative_g < g_costs[neighbor]:
                came_from[neighbor] = current
                g_costs[neighbor] = tentative_g
                f_costs[neighbor] = g_costs[neighbor] + heuristic(neighbor)
                heappush(open_list, (f_costs[neighbor], neighbor))
    
    return None, closed_set  # No path found