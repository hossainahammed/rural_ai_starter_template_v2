def ao_star(grid, start, goal):
    """
    AO* is generally used to solve AND/OR tree problems and not grid search directly.
    For this simplified project, we'll just print a message and use BFS as fallback.
    """
    print("AO* is not fully implemented for grid problems. Using BFS as fallback.")
    from .bfs import bfs
    return bfs(grid, start, goal)
