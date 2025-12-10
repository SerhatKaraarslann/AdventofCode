import pulp

def parse_machine(line):
    """
    Parses a machine configuration line into buttons and targets.
    """
    line = line.strip()
    parts = line.split()
    
    buttons = []
    targets = []
    
    for part in parts:
        if part.startswith('('):
            # Parse button: (0,1,2) -> [0, 1, 2]
            button_str = part[1:-1]  # Remove parentheses
            if button_str:
                indices = [int(x) for x in button_str.split(',')]
            else:
                indices = []
            buttons.append(indices)
        elif part.startswith('{'):
            # Parse targets: {3,5,4,7} -> [3, 5, 4, 7]
            target_str = part[1:-1]  # Remove curly braces
            if target_str:
                targets = [int(x) for x in target_str.split(',')]
    
    return buttons, targets

def solve_machine_joltage(buttons, targets):
    """
    Solves the joltage configuration for a single machine using ILP.
    Returns the minimum number of button presses needed.
    """
    num_buttons = len(buttons)
    num_counters = len(targets)
    
    # Create the optimization problem
    prob = pulp.LpProblem('JoltageConfiguration', pulp.LpMinimize)
    
    # Decision variables: how many times each button is pressed
    # Lower bound is 0 (can't press negative times)
    x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') 
         for i in range(num_buttons)]
    
    # Objective: minimize total button presses
    prob += pulp.lpSum(x)
    
    # Constraints: each counter must reach its target value
    for counter_idx in range(num_counters):
        # Sum contributions from all buttons that affect this counter
        contributing_buttons = []
        for btn_idx, btn_effects in enumerate(buttons):
            if counter_idx in btn_effects:
                contributing_buttons.append(x[btn_idx])
        
        if contributing_buttons:
            prob += pulp.lpSum(contributing_buttons) == targets[counter_idx]
        else:
            # If no button affects this counter, target must be 0
            if targets[counter_idx] != 0:
                raise ValueError(f"Counter {counter_idx} has target {targets[counter_idx]} but no button affects it")
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Check if a solution was found
    if pulp.LpStatus[prob.status] != 'Optimal':
        raise ValueError(f"No optimal solution found. Status: {pulp.LpStatus[prob.status]}")
    
    # Return the objective value (total presses)
    return int(pulp.value(prob.objective))

def solve_part2(input_file):
    """
    Solves Part 2 for all machines in the input file.
    """
    total_presses = 0
    
    try:
        with open(input_file, 'r') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                
                # Parse the machine configuration
                buttons, targets = parse_machine(line)
                
                # Solve for this machine
                presses = solve_machine_joltage(buttons, targets)
                
                print(f'Machine {i+1}: {presses} presses')
                total_presses += presses
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    
    print(f'\nTotal button presses for all machines: {total_presses}')
    return total_presses

def test_examples():
    """
    Test with the provided examples to verify correctness.
    """
    examples = [
        '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}',
        '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}',
        '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'
    ]
    
    print("Testing with examples:")
    expected_results = [10, 12, 11]
    total_expected = 33
    
    total = 0
    for i, example in enumerate(examples):
        buttons, targets = parse_machine(example)
        presses = solve_machine_joltage(buttons, targets)
        print(f"Machine {i+1}: {presses} presses (expected: {expected_results[i]})")
        total += presses
    
    print(f"Total: {total} (expected: {total_expected})")
    print(f"Test {'PASSED' if total == total_expected else 'FAILED'}")
    print()

if __name__ == "__main__":
    # First, test with the provided examples
    test_examples()
    
    # Get input file path from user
    input_file = input("Enter path to input file (or press Enter for default): ").strip()
    if not input_file:
        input_file = "/workspaces/AdventofCode/Day10/input.txt"
    
    # Solve part 2
    print("\nSolving Part 2...")
    total_presses = solve_part2(input_file)