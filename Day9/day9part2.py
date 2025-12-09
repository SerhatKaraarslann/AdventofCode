def solve_problem(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day9/input.txt'

    coordinates = list() # list of (x,y) tuples
    with open(fname,'r') as f:
        lines = f.readlines()  # read all lines from the file
        for line in lines :  # process each line
            line = line.strip().split(',') # split by comma
            x = int(line[0]) #x coordinate
            y = int(line[1]) #y coordinate
            coordinates.append((x,y)) # add tuple to list

   
    n = len(coordinates)
    print(f"Number of points that can form a polygon: {n}")

    # Edges of the polygon
    edges = []
    for i in range(n): 
        p1 = coordinates[i]
        p2 = coordinates[(i + 1) % n] # the last point connects to the first
        edges.append((p1, p2))

    max_area = 0
    best_pair = (None, None)

    # 3. Check all pairs
    for i in range(n):
        # Small progress indicator to show that something is happening
        if i % 50 == 0: print(f"Checking point {i}/{n}...")
            
        for j in range(i + 1, n):
            p1 = coordinates[i]
            p2 = coordinates[j]

            # Determine rectangle boundaries
            min_x = min(p1[0], p2[0])
            max_x = max(p1[0], p2[0])
            min_y = min(p1[1], p2[1])
            max_y = max(p1[1], p2[1])

            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height

            # Optimization: If the area is smaller than what we already have,
            # we don't need to do the expensive checks.
            if area <= max_area:
                continue

            # Does a wall cut through the rectangle?
            cut_through = False
            for edge in edges:
                ep1, ep2 = edge
                
                # Vertical wall? (x is the same)
                if ep1[0] == ep2[0]:
                    ex = ep1[0]
                    # Is the wall's X coordinate strictly inside the rectangle? (not on the edge)
                    if min_x < ex < max_x:
                        # Does the wall also overlap in the Y dimension with the rectangle?
                        ey_min = min(ep1[1], ep2[1])
                        ey_max = max(ep1[1], ep2[1])
                        # Check if they overlap
                        if not (ey_max <= min_y or ey_min >= max_y):
                            cut_through = True
                            break
                
                # Horizontal wall? (y is the same)
                else:
                    ey = ep1[1]
                    # Is the wall's Y coordinate strictly inside the rectangle?
                    if min_y < ey < max_y:
                        ex_min = min(ep1[0], ep2[0])
                        ex_max = max(ep1[0], ep2[0])
                        if not (ex_max <= min_x or ex_min >= max_x):
                            cut_through = True
                            break
            
            if cut_through:
                continue # Rectangle is invalid, it is cut through

            # --- CHECK 2: Is the rectangle in the "empty" space? (Ray Casting) ---
            # We check the center of the rectangle
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            
            inside = False
            for edge in edges:
                e1, e2 = edge
                x1, y1 = e1
                x2, y2 = e2
                
                # Ray Casting Algorithm:
                # Check if the edge intersects our horizontal ray from the center to the right
                if (y1 > center_y) != (y2 > center_y):
                    intersect_x = x1 + (center_y - y1) * (x2 - x1) / (y2 - y1)
                    if center_x < intersect_x:
                        inside = not inside

            # If inside is True, we have a valid rectangle!
            if inside:
                max_area = area
                best_pair = (p1, p2)

    print("-" * 30)
    print(f"Valid maximum area: {max_area}")
    print(f"Between pair: {best_pair}")
    print("-" * 30)

if __name__ == "__main__":
    fname = input('Enter file name (or press Enter for default): ')
    solve_problem(fname)