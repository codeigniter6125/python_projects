# import random
# # print(help(random))
# # Float between 0.0 and 1.0
# print(random.random())
# # Integer from 1 to 10 (inclusive)
# print(random.randint(1, 10))
# # Even integer from 0 to 98
# print(random.randrange(0, 100, 2))
# # Float between 5.0 and 10.0
# print(random.uniform(5.0, 10.0))
# cards = ["Ace", "King", "Queen", "Jack", "10"]
# # 1. Pick one element
# print(random.choice(cards))  # e.g., 'King'
# # 2. Pick multiple elements with replacement (can repeat)
# print(random.choices(cards, k=3))  # e.g., ['Ace', 'Ace', '10']
# # Weighted selection (biased probability)
# colors = ["red", "green", "blue"]
# print(random.choices(colors, weights=[10, 1, 1], k=5))  # mostly 'red'
# # 3. Pick unique elements (no duplicates)
# deck = list(range(1, 53))
# hand = random.sample(deck, 5)
# print(hand)  # 5 distinct cards
# # 4. Shuffle in place
# items = [1, 2, 3, 4, 5]
# random.shuffle(items)
# print(items)  # e.g., [3, 1, 5, 2, 4]
# random.seed(42)  # Set seed for reproducibility
# random.choice(cards)  # This will always return the same result when seed is set
# print(random.choice(cards))  # e.g., 'Queen' (will always be the same with seed 42)

# import random
# l_num=1
# h_num=100
# rand_num=random.randint(l_num,h_num)
# guesses=0
# is_guessed=True
# while is_guessed:
#     user_guess=input(f"Guess a number between {l_num} and {h_num}: ")
#     if user_guess.isdigit():
#         user_guess=int(user_guess)
#         guesses+=1
#         if user_guess==rand_num:
#             print(f"You guessed it! The number was {rand_num}. It took you {guesses} guesses.")
#             is_guessed=False
#         elif user_guess<rand_num:
#             print("Too low! Try again.")
#         else:
#             print("Too high! Try again.")
#     else:
#         print("Please enter a valid number.")