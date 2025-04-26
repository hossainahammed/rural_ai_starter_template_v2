import heapq

def heuristic(a, b):
    # Using Manhattan distance as heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    # open_set keeps (priority, cost, node) tuples
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    
    parent = {start: None}
    g_score = {start: 0}  # Cost from start to current node

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        current_priority, current_cost, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        # Explore neighbors
        for dx, dy in directions:
            x, y = current[0] + dx, current[1] + dy
            neighbor = (x, y)
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 1:
                new_cost = current_cost + 1  # Assumes each step costs 1
                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, new_cost, neighbor))
                    parent[neighbor] = current

    return None  # No path found

