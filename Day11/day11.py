def solve_problem(fname):
    """
    Solves the problem of counting distinct paths from 'you' to 'out' in a directed graph.
    The graph is read from a file specified by fname. If fname is empty, a default path is used.
    The file format is assumed to have each line as "source: dest1 dest2 dest
    ...", representing directed edges from source to each destination.
    param fname: str - the filename containing the graph data
    return: int - number of distinct paths from 'you' to 'out'
    """
    
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day11/input.txt'

    graph = {} # read in the graph as adjacency list
    
    try:
        with open(fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # we assume the format is "source: dest1 dest2 dest3 ..."
                parts = line.split(':')
                source = parts[0].strip()
                
                # destinations 
                destinations_str = parts[1].strip() #destinations as string
                if destinations_str: # if there are destinations
                    dests = destinations_str.split(' ') # list of destinations
                    graph[source] = dests # add to graph
                else:
                    graph[source] = [] # no destinations
                    
    except FileNotFoundError:
        print(f"Datei {fname} can not be found.")
        return

    print(f"Graph loaded from {fname}:")

    # Algorithm to count paths from 'you' to 'out'
    # 1. We will use Depth-First Search (DFS) with memoization to count paths
    #   2. Define a recursive function to count paths
    #   3. Start from 'you' and count paths to 'out'
    memo = {} # memoization dictionary

    def count_paths(current_node):
        """
        Counts the number of distinct paths from current_node to 'out'.
        Uses memoization to avoid redundant calculations.
        param current_node: str - the current node in the graph
        return: int - number of distinct paths from current_node to 'out'
        """
        
        if current_node == 'out':
            return 1
        
        #if already in memo, return stored result
        if current_node in memo: 
            return memo[current_node]
        
        # If the node leads nowhere (dead end) and is not 'out'
        if current_node not in graph:
            return 0
        
        total_paths = 0
        # Sum paths from all neighbors 
        for neighbor in graph[current_node]: # iterate over neighbors
            total_paths += count_paths(neighbor) # recursive call
            
        # Store result in memoization dictionary
        memo[current_node] = total_paths
        return total_paths

    # 3. Start from 'you' and count paths to 'out'
    result = count_paths('you')

    print(f"Number of distinct paths from 'you' to 'out': {result}")
    return result

if __name__ == "__main__":
    fname = input('Dateinamen eingeben (Enter für Standard): ')
    solve_problem(fname)