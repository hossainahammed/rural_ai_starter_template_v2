import heapq

def heuristic(a, b):
    # Using Manhattan distance as heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_terrain_cost(grid, pos):
    # Different terrain costs:
    # 0: Easy terrain (cost: 1)
    # 2: Goal (cost: 1)
    # 3: Rough terrain (cost: 2)
    # 4: Very rough terrain (cost: 3)
    # 1: Obstacle (infinity - handled in main loop)
    x, y = pos
    val = grid[x][y]
    if val == 0 or val == 2:
        return 1
    elif val == 3:
        return 2
    elif val == 4:
        return 3
    return 1

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    
    parent = {start: None}
    g_score = {start: 0}

    # Only orthogonal movements (no diagonals)
    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1),   # right
    ]

    while open_set:
        current_priority, current_cost, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in directions:
            x, y = current[0] + dx, current[1] + dy
            neighbor = (x, y)
            
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 1:
                terrain_cost = get_terrain_cost(grid, neighbor)
                new_cost = current_cost + terrain_cost

                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, new_cost, neighbor))
                    parent[neighbor] = current

    return None

