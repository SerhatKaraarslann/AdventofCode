def solve_problem(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day4/input.txt'

    grid = [] #2D list for the grid
    with open(fname,'r') as f:
        lines = f.readlines()
        for line in lines: # Read each line from the input file
            line = line.strip() # Remove leading/trailing whitespace

            if line:
                grid.append(list(line)) # Convert the line into a list of characters and add to the grid

    rows = len(grid) # Number of rows in the grid
    cols = len(grid[0]) # Number of columns in the grid (assuming all rows are of equal length)
    total = 0
    changed = False # Flag to track if any changes were made in the iteration

    while True:
        for r in range(rows): # Iterate over each row
            for c in range(cols): # Iterate over each column
                if grid[r][c] == '.': # Empty cell, skip
                    continue
                elif grid[r][c] == '@': # Occupied cell
                    nachbarn = 0

                    for dr in [-1,0,1]: # Check all 8 neighboring cells
                        for dc in [-1,0,1]: # Check all 8 neighboring cells
                            if dr == 0 and dc == 0: # Skip the cell itself
                                continue

                            nachbarnrow = r + dr # Row index of the neighbor
                            nachbarncol = c + dc # Column index of the neighbor


                            if 0 <= nachbarnrow < rows and 0 <= nachbarncol < cols: # Check if neighbor is within grid bounds
                                if grid[nachbarnrow][nachbarncol] == '@': # If neighbor is occupied
                                    nachbarn += 1 # Increment neighbor count


                    if nachbarn < 4: # If less than 4 neighbors are occupied
                        total +=1   # Increment total count
                        grid[r][c] = '.'  # Mark the cell as empty
                        changed = True # Set the changed flag to True

        if not changed: # If no changes were made, exit the loop
            break
        else:
            changed = False

    print('Total :',total)  


if __name__ == '__main__':
    fname = input("Enter input file name (or leave blank for default 'input.txt'): ")
    solve_problem(fname)