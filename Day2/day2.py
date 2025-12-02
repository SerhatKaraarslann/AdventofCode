def solve_problem(arr):
   sum = 0
   for i in arr:
       nums = i.split('-')
       start = int(nums[0])
       end = int(nums[1])

       
       for num in range(start,end+1):
           number = str(num)
           
           if len(number) % 2 != 0:
             continue
           
           
           mid = len(number) // 2
           first_part = number[:mid]
           second_part = number[mid:]

           if (first_part == second_part):
               sum += int(number)
        
   return sum


with open('/workspaces/AdventofCode/Day2/input.txt') as f:
    lines = f.read()
    numbers = [x for x in lines.split(',')]
    print(numbers)
    total = solve_problem(numbers)
    print('Total :',total )