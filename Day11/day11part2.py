import sys

def solve_problem(fname):
    """
    Solves the problem of counting distinct paths from 'svr' to 'out' in a directed graph.
    Crucially, only paths that visit BOTH 'dac' and 'fft' are counted.
    
    param fname: str - the filename containing the graph data
    return: int - number of valid distinct paths
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
                if ':' not in line: continue
                
                parts = line.split(':') # split into source and destinations
                source = parts[0].strip() # Get the source node
                
                # destinations 
                destinations_str = parts[1].strip() # destinations as string
                if destinations_str: 
                    dests = destinations_str.split(' ')  # list of destinations
                    graph[source] = dests # add to graph
                else:
                    graph[source] = [] # no destinations
                    
    except FileNotFoundError:
        print(f"File {fname} can not be found.")
        return

    print(f"Graph loaded with {len(graph)} nodes.")

    # Algorithm to count paths from 'svr' to 'out' passing through dac and fft
    # 1. We use DFS with memoization.
    # 2. The state must include whether we have seen 'dac' and 'fft'.
    
    # Memoization dictionary
    # Key: (current_node, visited_dac, visited_fft) -> Value: count of paths
    memo = {} # memoization dictionary

    def count_paths(current_node, visited_dac, visited_fft):
        """
        Counts the number of distinct paths from current_node to 'out'.
        
        param current_node: str - the current node in the graph
        param visited_dac: bool - True if 'dac' has been visited on this path
        param visited_fft: bool - True if 'fft' has been visited on this path
        return: int - number of valid paths found
        """
        
        # Update state if we are currently at dac or fft
        if current_node == 'dac':
            visited_dac = True
        if current_node == 'fft':
            visited_fft = True

        # Base case: Reached the end
        if current_node == 'out':
            # only count this path if BOTH special nodes were visited
            return 1 if (visited_dac and visited_fft) else 0
        
        # Create a unique key for the current state
        state_key = (current_node, visited_dac, visited_fft)
        
        # if already in memo, return stored result
        if state_key in memo: 
            return memo[state_key]
        
        # If the node leads nowhere (dead end)
        if current_node not in graph:
            return 0
        
        total_paths = 0
        # Sum paths from all neighbors 
        for neighbor in graph[current_node]: 
            # recursive call passing the current state flags
            total_paths += count_paths(neighbor, visited_dac, visited_fft)
            
        # Store result in memoization dictionary
        memo[state_key] = total_paths
        return total_paths

    # Start from 'svr' (server rack) as per instructions
    # Initially, I have seen neither dac nor fft (False, False)
    if 'svr' in graph:
        result = count_paths('svr', False, False)
    else:
        print("Error: Start node 'svr' not found in graph.")
        return 0

    print(f"Number of distinct paths from 'svr' to 'out' visiting both dac/fft: {result}")
    return result

if __name__ == "__main__":
    fname = input('Enter filename (Enter for default): ')
    solve_problem(fname)