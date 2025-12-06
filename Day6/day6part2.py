import itertools

def solve_problem(fname):
    if len(fname) < 1:
        fname = "/workspaces/AdventofCode/Day6/index.txt"
    
    with open(fname, 'r') as f: 
        lines = [line.rstrip('\n') for line in f] # remove trailing newlines

    max_width = max(len(line) for line in lines) # Find the maximum line length
    
    grid = [line.ljust(max_width) for line in lines] # Pad lines to max width

    columns = list(zip(*grid)) # Transpose rows to columns

    grand_total = 0
    
    current_block_numbers = [] # Numbers in the current block
    current_operator = None # Operator for the current block

    def calculate_block(numbers, operator): 
        """
        Docstring for calculate_block function
        Calculate the result of a block of numbers using the specified operator.
        param numbers: List of integers
        param operator: String, either "+" or "*"
        return: Integer result of the operation        
        """
        if not numbers:
            return 0
        if operator == "+":
            return sum(numbers)
        elif operator == "*":
            res = 1
            for n in numbers:
                res *= n
            return res
        return 0

    for col in columns: # Iterate over columns
        
        is_separator = all(char == ' ' for char in col) # Check if column is a separator (all spaces)

        if is_separator: # If separator, process current block
            if current_block_numbers: # If there are numbers to process
                op_to_use = current_operator if current_operator else "+" # Default to addition if no operator found
                grand_total += calculate_block(current_block_numbers, op_to_use) # Calculate and add to grand total
            
            current_block_numbers = []
            current_operator = None # Reset operator for the new block
            continue

        digits = [char for char in col if char.isdigit()] # Extract digits from the column
        if digits: # If there are digits, form the number
            number = int("".join(digits)) # Convert list of digit characters to integer
            current_block_numbers.append(number) # Add number to current block
        

        for char in col: # Check for operator in the column
            if char in "+*":    # If operator found, set current operator
                current_operator = char     

    if current_block_numbers: # Process any remaining numbers after the last column
        op_to_use = current_operator if current_operator else "+" # Default to addition if no operator found
        grand_total += calculate_block(current_block_numbers, op_to_use) # Calculate and add to grand total 

    print(f"Grand Total: {grand_total}") # Print the final grand total

if __name__ == "__main__":
    solve_problem(input("Dateiname: "))