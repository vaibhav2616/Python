def sum_digits_until_last_non_zero(number):
  """Calculates the sum of digits in a number until the last non-zero digit.

  Args:
      number: The number to process.

  Returns:
      The sum of digits until the last non-zero digit.
  """

  sum_of_digits = 0
  while number > 0:
    digit = number % 10
    if digit != 0:
      sum_of_digits += digit
    number //= 10
  return sum_of_digits

def sum_digits_recursively(number):
  """Calculates the sum of digits in a number recursively.

  Args:
      number: The number to process.

  Returns:
      The sum of digits.
  """

  if number == 0:
    return 0
  else:
    return number % 10 + sum_digits_recursively(number // 10)

# Get user input
number = int(input("Enter a number: "))

# Calculate and print the sum using the iterative approach
result_iterative = sum_digits_until_last_non_zero(number)
print("Sum of digits until the last non-zero digit (iterative):", result_iterative)

# Calculate and print the sum using the recursive approach
result_recursive = sum_digits_recursively(number)
print("Sum of digits (recursive):", result_recursive)