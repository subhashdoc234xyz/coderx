numbers = []
count = 0

while count < 10:
    n = int(input(f"Enter integer {count+1}: "))
    numbers.append(n)
    count += 1

print("You entered:", numbers)