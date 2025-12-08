import math

class UnionFind:
    """
    Union-Find Datastructure with Path Compression and Union by Rank
    """
    def __init__(self, size): # initialize Union-Find structure
        self.parent = list(range(size)) # each element is its own parent
        self.rank = [1] * size # size of each component (initially 1 for each element)

    def find(self, p):
        """
        Find the root of the component/set
        with path compression optimization
        param p: element to find the root of
        return: root of the component/set
        """
        if self.parent[p] != p: # if p is not the root
            self.parent[p] = self.find(self.parent[p]) # path compression
        return self.parent[p] #return root

    def union(self, p, q):
        """"
        Connect two elements p and q
        param p: first element
        param q: second element
        return: True if union was successful, False if already connected
        """
        rootP = self.find(p) # find root of p
        rootQ = self.find(q) # find root of q

        # Connect only if they are not already connected
        if rootP != rootQ:
            # Always attach the smaller tree to the larger one
            if self.rank[rootP] < self.rank[rootQ]: 
                rootP, rootQ = rootQ, rootP # swap to ensure rootP is the larger tree
            
            self.parent[rootQ] = rootP # attach smaller tree under larger tree
            self.rank[rootP] += self.rank[rootQ] # update size of the tree
            return True
        else:
            return False # already connected

def solve_problem(fname):
    """
    solve the problem by performing the following steps:
    1. read coordinates from the input file.
    2. calculate the Euclidean distance between all points.
    3. connect the points based on the shortest distances.
    4. calculate the sizes of the connected components and return the product of the top
    5. two X coordinates of the last two junction boxes connected.
    6. The difference from part 1 is that we stop when all points are connected into a single group.
    7. In the end, we multiply the X coordinates of the last two connected junction boxes.
    
    :param fname: description
    """
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day8/input.txt'
    coordinate = [] # list to store coordinates
   
    try:
        with open(fname, 'r') as f:
            lines = f.readlines() # read all lines from the file
            for line in lines: # process each line
                line = line.strip() # remove whitespace and newline characters
                if not line: continue # skip empty lines
                line = line.split(',') # split by comma
                coordinate.append(list(map(int, line))) # convert to integers and store
    except FileNotFoundError: 
        print(f"Datei {fname} nicht gefunden.")
        return

    edges = [] # list to store edges (distances between points)
    n = len(coordinate) # number of coordinates

    for i in range(n): # calculate distances between all pairs
        for j in range(i + 1, n): # avoid duplicate pairs
            p1 = coordinate[i] # first point
            p2 = coordinate[j] # second point
            # Euclidean distance
            dist = math.sqrt(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2)) # 3D distance
            edges.append((dist, i, j)) # store distance and point indices

    edges.sort(key=lambda x: x[0]) # sort edges by distance
    uf = UnionFind(n) # initialize Union-Find scructure

    groups_count = n  # initial number of groups
    
    last_u = -1 # to store last connected elements  
    last_v = -1 # to store last connected elements

    for dist, u, v in edges:
        # connect points u and v
        was_merged = uf.union(u, v)
        
        if was_merged:
            # If successfully connected, we now have one less group
            groups_count -= 1
            
            # If we only have 1 group left, we are done!
            if groups_count == 1:
                last_u = u
                last_v = v
                break

    # Calculate result
    # "What do you get if you multiply together the X coordinates 
    # of the last two junction boxes you need to connect?"
    
    box1 = coordinate[last_u] # first box
    box2 = coordinate[last_v] # second box
    
    x1 = box1[0] # X coordinate of first box
    x2 = box2[0] # X coordinate of second box
    
    result = x1 * x2 # multiply X coordinates
    
    print("Final Result:", result)

if __name__ == "__main__":
    fname = input('Enter file name or press enter to use default: ')
    solve_problem(fname)