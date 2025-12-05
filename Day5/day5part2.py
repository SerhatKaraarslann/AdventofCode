def solve_problem(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day5/index.txt'
    
   
    list_interval = []
    set_numbers = set()

    with open(fname, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if '-' in line:
                parts = line.split('-')
                start = int(parts[0])
                end = int(parts[1])
                list_interval.append((start, end))
            else:
                continue


        list_interval.sort(key=lambda x: x[0])  # sort intervals by start value  
   
        curr_start, curr_end = list_interval[0] # initialize with the first interval
        merged_intervals = [] # list to hold merged intervals, to prevent double counting
        for i in range(1,len(list_interval)):
            next_start,next_end = list_interval[i]
            if next_start <= curr_end: # there is an overlap
                curr_end = max(curr_end, next_end) # extend the current interval
            else:
                merged_intervals.append((curr_start, curr_end)) # no overlap, add the current interval to the list
                curr_start, curr_end = next_start, next_end # move to the next interval

        merged_intervals.append((curr_start, curr_end)) # add the last interval

        count = 0
        for start, end in merged_intervals:
            count += (end - start + 1) # count all numbers in the merged intervals
    
    print(f"Fresh ingredient ID count: {count}")

if __name__ == "__main__":
    fname = input("Enter the filename (leave blank for default): ")
    solve_problem(fname)    