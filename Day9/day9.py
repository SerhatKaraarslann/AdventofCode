def solve_problem(fname):
    if len(fname) < 1:
        fname = "/workspaces/AdventofCode/Day9/input.txt"

    coordinates = list() # list of (x,y) tuples
    with open(fname,'r') as f:
        lines = f.readlines()  # read all lines from the file
        for line in lines :  # process each line
            line = line.strip().split(',') # split by comma
            x = int(line[0]) #x coordinate
            y = int(line[1]) #y coordinate
            coordinates.append((x,y)) # add tuple to list

    max_area = 0 # maximum area 0
    best_pair = (None,None) # best pair of coordinates
    for i in range(len(coordinates)): # iterate through all coordinates
        for j in range(i+1,len(coordinates)): # iterate through all coordinates after i
           p1 = coordinates[i] # first point
           p2 = coordinates[j] # second point

           width = abs(p1[0] - p2[0]) + 1 # width of rectangle
           height = abs(p1[1] - p2[1]) + 1 # height of rectangle
           area = width*height # area of rectangle

           if area > max_area: # if area is greater than max area
               max_area = area # update max area
               best_pair = (p1,p2) # update best pair

    

    print(f'Result is : {max_area} and pair : {best_pair}')

if __name__ == "__main__":
    fname = input('Enter file name or press enter to use default: ')
    solve_problem(fname)
