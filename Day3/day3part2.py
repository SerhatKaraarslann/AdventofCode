def solve_problem(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day3/input.txt'

    total = 0
    K = 12
    with open(fname,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            n = len(line)
            result = ""

            start = 0
            for num in range(K):
                remaining = K - num
                end = n -remaining

                segment = line[start:end+1]
                max_digit = max(segment)

                position = line.find(max_digit, start)

                result += max_digit
                start = position + 1

            total += int(result)       
            
    print('Total:', total)


if __name__ == "__main__":
    fname = input("Enter input file name (or leave blank for default 'input.txt'): ")
    solve_problem(fname)




