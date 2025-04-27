def dfs_non_recursive(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    visited = set()
    parent = {start: None}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack.pop()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        if current not in visited:
            visited.add(current)
            for dx, dy in directions:
                x, y = current[0] + dx, current[1] + dy
                if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 1:
                    neighbor = (x, y)
                    if neighbor not in visited:
                        stack.append(neighbor)
                        if neighbor not in parent:
                            parent[neighbor] = current

    return None  # No path found