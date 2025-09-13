import random

def PROTIP():
    tips = [
    "Pro tip: Using a binary search strategy, you can always guess the number in 7 tries or fewer for 1-100.",
    "Fun fact: Always guess the midpoint between your range — it halves the possible answers each time.",
    "Strategy tip: Start at 50 — it's the most efficient first guess for 1-100.",
    "Math tip: Every wrong guess lets you eliminate at least half of the remaining numbers if you guess strategically.",
    "Did you know? Random guessing could take over 50 tries on average — strategy matters!",
    "Probability fact: After k guesses using binary search, you'll have at most 100 / 2^k numbers left to check."
]
    print("\n--- Tip ---")
    print(random.choice(tips))

n =random.randint(1,101)
attempts=0
a=-1
while a!=n:
    a= int(input("Guess the NUMBER (between 1 and 100): "))
    if a<n:
        print("Too low! Try again.")
        attempts+=1
        PROTIP()
    elif a>n:
        print("Too high! Try again.")
        attempts+=1
        PROTIP()

print("Congratulations! You've guessed the number.")
print(f"It took you {attempts+1} attempts to guess the number {n}.")
PROTIP()