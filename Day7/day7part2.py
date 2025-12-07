from functools import lru_cache # Import lru_cache for memoization

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
    
    @lru_cache(maxsize=None)
    def count_pads(r, c):
        """
        This function counts the number of unique timelines that can be formed
        starting from position (r, c) in the grid.
        It uses memoization to avoid redundant calculations.
        param r: Current row index
        param c: Current column index
        return: Integer count of unique timelines from (r, c)
        """
        next_r = r + 1 # Move down
        next_c = c # Stay in the same column

        if next_r >= rows: # Check bounds
            return 1
        
        if not (0 <= next_c < cols): # Check bounds
            return count_pads(next_r, next_c)
        
        next_cell = grid[next_r][next_c] # Get the content of the next cell

        if next_cell == '^': # If it's a splitter
            left_timeline = count_pads(next_r, next_c - 1) # Move left
            right_timeline = count_pads(next_r, next_c + 1) # Move right
            return left_timeline + right_timeline # Sum timelines from both directions
        else:
            return count_pads(next_r, next_c) # Continue downwards
        
    if start_pos:
        total_timelines = count_pads(start_pos[0], start_pos[1]) # Start counting from the start position
        return total_timelines # Return the total count of unique timelines
    else:
        return 0
    

if __name__ == "__main__":
    fname = input("Enter the input file path (or press Enter to use default): ")
    result = solve_problem(fname)
    print(f"Number of the unique timelines: {result}")