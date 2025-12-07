def solve_problem(fname):
    if len(fname) < 1:
        fname = "/workspaces/AdventofCode/Day7/input.txt"

    with open(fname, 'r') as f:
        grid = [list(line) for line in f.read().strip().split('\n')] # Read grid from file
        rows = len(grid) # Number of rows in the grid
        cols = len(grid[0]) # Number of columns in the grid

    start_pos = None # To store the starting position 'S'
    for r in range(rows): # Find the starting position 'S'
        for c in range(cols): # Iterate through each column in the current row
            if grid[r][c] == 'S': # Found the start position
                start_pos = (r, c)
                break
        if start_pos:
            break
    if not start_pos:
        raise ValueError("Start position 'S' not found in the grid.")
    
    queue = [start_pos] # Start BFS from the start position
    hit_splitters = set() # To track unique splitters hit
    visited = set() # To track visited positions
    visited.add(start_pos) # Mark start position as visited

    while queue: # BFS loop
        r,c = queue.pop(0) # Dequeue the next position

        next_r = r + 1 # Move down
        next_c = c # Stay in the same column

        if not (0 <= next_r < rows and 0 <= next_c < cols): # Check bounds
            continue

        next_cell = grid[next_r][next_c] # Get the content of the next cell

        if next_cell == '^': # If it's a splitter

            if (next_r, next_c) not in hit_splitters: # If this splitter hasn't been hit yet
                hit_splitters.add((next_r, next_c)) # Mark splitter as hit

                if 0 <= next_c - 1 < cols: # Check left column
                    queue.append((next_r, next_c - 1)) # Add left position to queue

                if 0 <= next_c + 1 < cols: # Check right column
                    queue.append((next_r, next_c + 1)) # Add right position to queue
        
        else:
            if (next_r, next_c) not in visited: # If not visited yet
                visited.add((next_r, next_c)) # Mark position as visited
                queue.append((next_r, next_c)) # Add position to queue
                             
    
    return len(hit_splitters) # Return the count of unique splitters hit


if __name__ == "__main__":
    fname = input("Enter the input file path (or press Enter to use default): ")
    result = solve_problem(fname)
    print(f"Number of unique splitters hit: {result}")