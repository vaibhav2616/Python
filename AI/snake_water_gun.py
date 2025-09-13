import random
computer= random.choice([-1, 0, 1])  # -1 for snake, 0 for water, 1 for gun
user = int(input("Enter your choice: -1 for snake, 0 for water, 1 for gun: ")) 
if user not in [-1, 0, 1]:
    print("Invalid choice! Please enter -1, 0, or 1.")
    exit()
dict = {-1: "snake", 0: "water", 1: "gun"}
print("Computer chose:", dict[computer])
print("You chose:", dict[user])
if computer == user:
    print("It's a tie!")
else:
    if (computer == -1 and user == 0) or (computer == 0 and user == 1) or (computer == 1 and user == -1):
        print("Computer wins!")
    else:
        print("You win!")
