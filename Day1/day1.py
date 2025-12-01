counter = 0
number = 50

with open('C:\\Users\\sk019655\\AdventofCode\\Day1\\input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith('R'):
            num = line.split('R')[1]
            number = (number + int(num)) % 100
        elif line.startswith('L'):
            num = line.split('L')[1]
            number = (number - int(num)) % 100

        if number == 0:
            counter +=1

print('Counter:',counter)