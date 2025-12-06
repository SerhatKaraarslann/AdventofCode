import itertools

def solve_problem(fname):
    if len(fname) < 1:
        fname = "/workspaces/AdventofCode/Day6/index.txt"
    
    with open(fname, 'r') as f:
        lines = f.readlines()
    
    rows = [] # Read all lines into rows
    for line in lines:
        parts = line.strip().split() # Split by whitespace
        if parts:
            rows.append(parts) # Append non-empty lines

    # Transpose rows to columns, filling missing values with None
    columns = list(itertools.zip_longest(*rows, fillvalue=None))

    grand_total = 0
  
    for i, col in enumerate(columns): # Iterate over columns
        
        clean_col = [x for x in col if x is not None] # Remove None values
        
        if not clean_col: # Skip empty columns
            continue

        operator = clean_col[-1] #last element is the operator
        raw_numbers = clean_col[:-1] #rest are the numbers

        # Convert numbers
        numbers = []
        for x in raw_numbers: 
            if x.lstrip('-').isdigit(): # Check if x is an integer
                numbers.append(int(x)) # Convert to int and add to numbers list
        
        if not numbers: # Skip if no valid numbers
            continue

        col_result = 0 # Initialize column result
        
        if operator == "+": # Addition
            col_result = sum(numbers)
            
        elif operator == "*": # Multiplication
            col_result = 1
            for n in numbers: # Multiply all numbers
                col_result *= n
        
        elif operator not in ["+", "*"]: # Skip unknown operators
             continue

        # Add column result to grand total
        grand_total += col_result


    print(f"Grand Total: {grand_total}")
    

if __name__ == "__main__":
    solve_problem(input("Dateiname: ")) 