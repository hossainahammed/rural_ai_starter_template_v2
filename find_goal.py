def find_goal(grid):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 2:
                return (i, j)
    return None