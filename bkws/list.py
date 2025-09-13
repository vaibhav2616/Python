numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))

even_sum = 0
odd_product = 1

for num in numbers:
    if num % 2 == 0:
        even_sum += num
    else:
        odd_product *= num

print("Sum of even numbers:", even_sum)
print("Product of odd numbers:", odd_product)
