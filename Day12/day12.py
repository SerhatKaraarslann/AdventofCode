import sys

def parse_input(filename):
    """
    Parses the input file. 
    Returns:
        shapes: dict mapping shape_id (int) -> set of (row, col) tuples
        regions: list of dicts with 'width', 'height', and 'presents' (list of shape_ids)
    """
    shapes = {} # shape_id -> set of (row, col)
    regions = [] # list of {'width': int, 'height': int, 'presents': [shape_id, ...]}
    
    current_shape_id = None 
    current_shape_lines = [] # lines representing the current shape
    reading_shapes = True # Flag to switch between shapes and regions
    
    try:
        with open(filename, 'r') as f: 
            lines = [l.rstrip() for l in f.readlines()] # Strip trailing whitespace/newlines
    except FileNotFoundError: 
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    
    for line in lines:
        if not line: 
            # Empty line usually signals end of a block
            if current_shape_id is not None and current_shape_lines:
                shapes[current_shape_id] = parse_shape_grid(current_shape_lines) # Save the last shape
                current_shape_id = None # Reset for next shape
                current_shape_lines = [] # Reset shape lines
            continue
            
        # Detect switch to regions section (lines like "12x5: ...")
        if 'x' in line and ':' in line and line[0].isdigit(): # crude check for region line
            reading_shapes = False # Switch to regions parsing
            
        if reading_shapes: 
            # --- Parsing Shapes ---
            if ':' in line and line.split(':')[0].strip().isdigit(): 
                # Start of new shape (e.g., "0:")
                parts = line.split(':') # Split at ':'
                current_shape_id = int(parts[0]) # Shape ID
                current_shape_lines = [] # Reset lines for new shape
            else:
                # Visual representation of the shape
                current_shape_lines.append(line)
        else:
            # --- Parsing Regions ---
            # Format: "12x5: 1 0 1 0 2 2"
            parts = line.split(':') # Split at ':'
            dims = parts[0].split('x') # e.g., "12x5" -> ["12", "5"]
            width = int(dims[0]) # Width of the region
            height = int(dims[1]) # Height of the region
            
            # The part after ':' contains counts for each shape ID
            counts = list(map(int, parts[1].strip().split()))
            
            # Convert counts to a flat list of IDs needed. 
            # e.g., counts=[1, 2] for IDs 0 and 1 -> [0, 1, 1]
            presents_needed = [] # Flattened list of shape IDs
            for shape_id, count in enumerate(counts): # shape_id corresponds to index
                presents_needed.extend([shape_id] * count) # Add 'count' copies of shape_id
                
            regions.append({
                'width': width, 
                'height': height,
                'presents': presents_needed
            })
            
    # Catch the very last shape if file ends without newline
    if current_shape_id is not None and current_shape_lines:
        shapes[current_shape_id] = parse_shape_grid(current_shape_lines)
        
    return shapes, regions

def parse_shape_grid(lines):
    """
    Converts visual lines (###, .#.) into a set of (row, col) coordinates.
    """
    coords = set() # Set of (row, col) tuples
    for r, line in enumerate(lines): # Each line represents a row
        for c, char in enumerate(line): # Each character represents a column
            if char == '#': # Occupied cell
                coords.add((r, c)) # Add coordinate
    return normalize_shape(coords) # Normalize for easier placement

def normalize_shape(coords):
    """
    Shifts coordinates so the top-leftmost part is at (0,0).
    This makes placing shapes on the grid easier.
    """
    if not coords: 
        return frozenset() # Empty shape case
    min_r = min(r for r, c in coords) # Find topmost row
    min_c = min(c for r, c in coords) # Find leftmost column
    # Return as frozenset so it can be hashed/stored in sets
    return frozenset((r - min_r, c - min_c) for r, c in coords)

def generate_variations(base_shape):
    """
    Generates all 8 symmetries (4 rotations * 2 flips).
    Returns a list of unique coordinate sets (normalized).
    """
    variations = set() # Use a set to avoid duplicates
    current = base_shape # Start with the base shape
    
    # Try 4 rotations
    for _ in range(4):
        variations.add(normalize_shape(current)) # Add current rotation
        
        # Flip (mirror horizontally)
        flipped = frozenset((r, -c) for r, c in current) # Mirror horizontally
        variations.add(normalize_shape(flipped)) # Add flipped version
        
        # Rotate 90 degrees clockwise: (r, c) -> (c, -r)
        current = frozenset((c, -r) for r, c in current) # Rotate for next iteration
        
    return list(variations)

def solve_region(width, height, present_ids, shapes_variations_cache):
    """
    Attempts to fit the list of present_ids into a w x h grid.
    Uses backtracking to try all placements.
    parameters:
        width: int - width of the region
        height: int - height of the region
        present_ids: list of int - shape IDs to place
        shapes_variations_cache: dict - shape_id -> list of variations (sets of coords)
    returns:
        bool - True if all presents fit, False otherwise
    """
    
    # Create empty grid (False = empty, True = occupied)
    grid = [[False for _ in range(width)] for _ in range(height)]
    
    # Heuristic: Sort presents by size (largest first).
    # This helps "fail fast". If the big ones don't fit, we know sooner.
    presents_with_area = [] # List of (area, shape_id)
    for pid in present_ids:
        # Just grab the first variation to check area (len of set)
        area = len(shapes_variations_cache[pid][0]) # Area of the shape
        presents_with_area.append((area, pid)) # Tuple of (area, shape_id)
    
    # Sort descending by area
    presents_with_area.sort(key=lambda x: x[0], reverse=True)
    sorted_presents = [p[1] for p in presents_with_area] # Extract sorted shape IDs
    
    #  Start recursion
    return backtrack(grid, width, height, sorted_presents, shapes_variations_cache)

def backtrack(grid, width, height, remaining_presents, variations_cache):
    """
    Recursive function to place presents.
    parameters:
        grid: 2D list of bool - current state of the grid
        width: int - width of the grid
        height: int - height of the grid
        remaining_presents: list of int - shape IDs left to place
        variations_cache: dict - shape_id -> list of variations (sets of coords)
    returns:
        bool - True if successful placement, False otherwise
    """
    # Base Case: No presents left -> Success!
    if not remaining_presents:
        return True
    
    current_pid = remaining_presents[0] # Shape ID to place
    next_presents = remaining_presents[1:] # Remaining after this one
    
    # Try every variation (rotation/flip) of this shape
    possible_shapes = variations_cache[current_pid]
    
    for shape_coords in possible_shapes:
        # Calculate dimensions of this specific variation
        max_r = max(r for r, c in shape_coords) # Max row index
        max_c = max(c for r, c in shape_coords) # Max column index
        shape_h = max_r + 1 # Height of the shape
        shape_w = max_c + 1 # Width of the shape
        
        # Try every valid position on the grid
        # Optimization: Only loop up to where the shape still fits
        for r in range(height - shape_h + 1): # For each row
            for c in range(width - shape_w + 1): # For each column
                
                # Check for collision
                collision = False # Flag for collision
                for br, bc in shape_coords: # For each block in the shape
                    if grid[r + br][c + bc]: # If occupied
                        collision = True # Mark collision
                        break
                
                if not collision: # No collision, we can place it
                    # PLACE IT (Mark grid)
                    for br, bc in shape_coords: # For each block in the shape
                        grid[r + br][c + bc] = True # Mark as occupied
                    
                    # RECURSE
                    if backtrack(grid, width, height, next_presents, variations_cache):
                        return True
                    
                    # BACKTRACK (Unmark grid - undo the move)
                    for br, bc in shape_coords:# For each block in the shape
                        grid[r + br][c + bc] = False # Unmark
                        
    # If no variation fits in any position
    return False

def main():
    # Use input() or default to file
    fname = input("Enter input file path (or press Enter for default): ").strip()
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day12/input.txt'
        
    print(f"--- Loading data from {fname} ---")
    shapes, regions = parse_input(fname)
    
    # Pre-calculate all variations for all shapes to save time during recursion
    # This acts as a cache.
    variations_cache = {} # shape_id -> list of variations
    for sid, coords in shapes.items(): # For each shape
        variations_cache[sid] = generate_variations(coords) # Store variations
        
    solved_count = 0
    
    print(f"Loaded {len(shapes)} shapes and {len(regions)} regions.\n")
    
    for i, region in enumerate(regions): # For each region
        w = region['width'] # Width of the region
        h = region['height'] # Height of the region
        presents = region['presents'] # List of shape IDs to place
        
        print(f"Region {i}: {w}x{h}, requires {len(presents)} presents...", end=" ")
        sys.stdout.flush() # Force print before calculation
        
        # Quick sanity check: Total area
        total_area = 0
        for pid in presents: # For each present ID
            total_area += len(shapes[pid]) # Add area of that shape
            
        if total_area > w * h: # If total area exceeds region area
            print("Impossible (Not enough space).") 
            continue
            
        if solve_region(w, h, presents, variations_cache): # Try to solve
            print("Success!") 
            solved_count += 1 # Increment solved count
        else:
            print("Failed.")
            
    print(f"Total regions that can fit all presents: {solved_count}")

if __name__ == "__main__":
    main()