import json

def load_grid_map(file_path):
    with open(file_path, "r") as f:
        grid = []
        for line in f:
            row = list(map(int, line.strip().split()))
            grid.append(row)
    return grid

def load_queries(file_path):
    queries = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            queries.append(json.loads(line.strip()))
    return queries