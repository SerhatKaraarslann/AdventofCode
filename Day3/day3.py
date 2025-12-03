def solve_problem(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day3/input.txt'

    total = 0
    with open(fname,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            num1 = max(line[:len(line)-1])
            maxindex = line.index(num1)
            total += int(num1)*10
            num2 = max(line[maxindex+1:])
            total += int(num2)            
    
    print('Total:', total)
            
    


if __name__ == "__main__":
    fname = input("Enter input file name (or leave blank for default 'input.txt'): ")
    solve_problem(fname)






