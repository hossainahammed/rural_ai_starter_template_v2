def water_jug_solver(jug1, jug2, target):
    """
    Solve the water jug problem using a DFS approach.
    jug1: Capacity of jug1
    jug2: Capacity of jug2
    target: Desired amount in either jug.
    
    This function returns a list of states (jug1, jug2) representing the steps
    from the initial state (0,0) to a state with either jug containing the target amount.
    """
    stack = [(0, 0)]
    visited = set()
    parent = {(0, 0): None}  # To keep track of the path

    while stack:
        state = stack.pop()
        a, b = state
        
        if state in visited:
            continue
        visited.add(state)
        
        # Check if the target is reached
        if a == target or b == target:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]
        
        # List all possible moves:
        next_states = set()
        # 1. Fill jug1
        next_states.add((jug1, b))
        # 2. Fill jug2
        next_states.add((a, jug2))
        # 3. Empty jug1
        next_states.add((0, b))
        # 4. Empty jug2
        next_states.add((a, 0))
        # 5. Pour jug1 to jug2
        # The amount to pour is the minimum of what's in jug1 and available space in jug2
        pour = min(a, jug2 - b)
        next_states.add((a - pour, b + pour))
        # 6. Pour jug2 to jug1
        pour = min(b, jug1 - a)
        next_states.add((a + pour, b - pour))

        for state_next in next_states:
            if state_next not in visited:
                parent[state_next] = (a, b)
                stack.append(state_next)

    return None
