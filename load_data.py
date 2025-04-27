import os

def load_grid_map(file_path):
    try:
        with open(file_path, "r") as f:
            grid = []
            for line in f:
                line = line.strip()
                # Skip empty lines or lines starting with text
                if line and not line.startswith('Goal'):
                    try:
                        # Try to convert line to list of integers
                        row = [int(num) for num in line.split()]
                        if row:  # Only add non-empty rows
                            grid.append(row)
                    except ValueError:
                        # Skip lines that can't be converted to integers
                        continue
            return grid
    except FileNotFoundError:
        print(f"Error: Could not find the grid map file at {file_path}")
        raise
    except Exception as e:
        print(f"Error loading grid map: {str(e)}")
        raise

def load_queries(file_path):
    try:
        with open(file_path, "r") as f:
            return [{"query": line.strip()} for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find the queries file at {file_path}")
        raise
    except Exception as e:
        print(f"Error loading queries: {str(e)}")
        raise