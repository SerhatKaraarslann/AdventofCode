def count_zeros_in_rotation(start_pos, direction, steps):
    """
    Count how many times the dial points to 0 during a rotation.
    Uses step-by-step simulation for accuracy.
    
    start_pos: starting position (0-99)
    direction: 'R' for right (increasing), 'L' for left (decreasing)  
    steps: number of steps to rotate
    
    Returns: (count_of_zeros, final_position)
    """
    if steps == 0:
        return 0, start_pos
    
    count = 0
    current = start_pos
    
    for _ in range(steps):
        if direction == 'R':
            current = (current + 1) % 100
        else:  # 'L'
            current = (current - 1) % 100
        
        if current == 0:
            count += 1
    
    return count, current

counter = 0
number = 50

with open('C:\\Users\\sk019655\\AdventofCode\\Day1\\input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()  # Remove newline characters
        
        if line.startswith('R'):
            num = int(line[1:])  # Get the number after 'R'
            zeros_hit, number = count_zeros_in_rotation(number, 'R', num)
            counter += zeros_hit

        elif line.startswith('L'):
            num = int(line[1:])  # Get the number after 'L'
            zeros_hit, number = count_zeros_in_rotation(number, 'L', num)
            counter += zeros_hit

print('Counter:', counter)