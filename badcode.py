numbers = [5, 10, 24, 50, 103, 199, 99, 300]

current_min = 1000

for number in numbers:
    if number < current_min:
        current_min = number
minimum = current_min
print("the lowest number is: " + str(minimum))