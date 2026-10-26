import random
def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"
options = ["rock", "paper", "scissors"]
playing = True
while playing:
    player_choice = None
    computer_choice = random.choice(options)
    while player_choice not in options:
        player_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        if player_choice not in options:
            print("Invalid choice. Please try again.")
    print(f"Computer chose: {computer_choice}")
    print(f"You chose: {player_choice}")
    print(determine_winner(player_choice, computer_choice))
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        playing = False
        print("Thanks for playing!")