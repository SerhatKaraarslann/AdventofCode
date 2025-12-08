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

    # The task requires exactly 1000 pairs
    limit = 1000
    
    if len(edges) < limit: # if there are less than 1000 edges, take all
        limit = len(edges) # adjust limit

    top_edges = edges[:limit] # take the top 1000 shortest edges

    uf = UnionFind(n) # initialize Union-Find structure
   
    # Connect points based on the top edges
    for dist, u, v in top_edges:
        uf.union(u, v) # connect the points

    circuit_sizes = [] # list to store sizes of connected components
    for i in range(n): # iterate through all points
        if uf.parent[i] == i: # if i is a root
            circuit_sizes.append(uf.rank[i]) # store size of the component
    
    circuit_sizes.sort(reverse=True) # sort sizes in descending order
    print(f"Top Circuit Sizes: {circuit_sizes[:5]}") # print top 5 sizes for verification

    result = 1
    count = 0
    # We take the top 3 (or fewer if less than 3 exist)
    for size in circuit_sizes:  
        result *= size # multiply sizes
        count += 1 
        if count >= 3: 
            break

    print("Final Result:", result)

if __name__ == "__main__":
    fname = input('Enter file name or press enter to use default: ')
    solve_problem(fname)