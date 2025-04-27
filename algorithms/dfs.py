def dfs_non_recursive(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    stack = [(start, 0)]  # (position, depth)
    visited = set()
    parent = {start: None}

    # DFS will prefer exploring in a clockwise pattern
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (0, -1),  # left
        (-1, 0),  # up
    ]

    while stack:
        current, depth = stack.pop()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        if current not in visited:
            visited.add(current)
            # Sort neighbors by their depth (prefer deeper paths)
            neighbors = []
            for dx, dy in directions:
                x, y = current[0] + dx, current[1] + dy
                if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 1:
                    neighbor = (x, y)
                    if neighbor not in visited:
                        neighbors.append((neighbor, depth + 1))
                        if neighbor not in parent:
                            parent[neighbor] = current
            
            # Add neighbors to stack in reverse order (to explore right and down first)
            for neighbor in reversed(neighbors):
                stack.append(neighbor)

    return None  # No path found