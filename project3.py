import random 
# print("\u25cf \u250c \u2500 \u2510 \u2502 \u2514 \u2518")
# ● ┌ ─ ┐ │ └ ┘
"┌──────────┐"
"│          │"
"│          │"
"│          │"
"└──────────┘"
dice_faces = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"
    ),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"
    ),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"
    ),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"
    ),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"
    ),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"
    )
}
dice=[]
total=0
num_dice = int(input("Enter the number of dice to roll: "))
for die in range(num_dice):
    roll = random.randint(1, 6)
    dice.append(roll)
for die in range(num_dice):
    for line in dice_faces.get(dice[die]):
        print(line)
# for line in range(5):
#     for die in dice:
#         print(dice_faces[die][line], end=" ")
#     print()
for die in dice:
    total += die
print(f"total: {total}")



