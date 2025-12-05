def solve_problem(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day5/index.txt'
    
    fresh = 0
    spoiled = 0
    list_interval = []
    list_numbers = []

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
                if line == '':
                    continue
                number = int(line)
                list_numbers.append(number)

            
    for number in list_numbers:
        is_fresh = False
        for interval in list_interval:
            if interval[0] <= number <= interval[1]:
                is_fresh = True
                break
        if is_fresh:
            fresh += 1
        else:
            spoiled += 1
    
    print(f"Fresh: {fresh}, Spoiled: {spoiled}")

if __name__ == "__main__":
    fname = input("Enter the filename (leave blank for default): ")
    solve_problem(fname)    