from collections import deque

def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in directions:
            x, y = current[0] + dx, current[1] + dy

            if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 1:
                neighbor = (x, y)
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

    return None  # No path found