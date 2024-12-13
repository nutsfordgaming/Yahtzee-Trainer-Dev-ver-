import itertools

# Possible outcomes for each die (1 through 6)
dice_faces = [1, 2, 3, 4, 5, 6]

def held_dice_rolls(num_of_dice):
    """Finds all combinations of dice when the given number of dice are being rolled"""

    # Use itertools.product to find all permutations of rolling the number of dice
    all_rolls = list(itertools.product(dice_faces, repeat=num_of_dice))

    # Convert the list of tuples into a tuple of sorted lists and returns it
    return tuple([list(sorted(roll)) for roll in all_rolls])

zero_held_dice_rolls = held_dice_rolls(5)
one_held_dice_rolls = held_dice_rolls(4)
two_held_dice_rolls = held_dice_rolls(3)
three_held_dice_rolls = held_dice_rolls(2)
four_held_dice_rolls = held_dice_rolls(1)
five_held_dice_rolls = [[]]

def index_combos():
    index_combinations = []
    for r in range(0, 6):  # r represents the number of indices in the combination, starting from 0
        index_combinations.extend(itertools.combinations(range(5), r))

    return tuple([list(index_combo) for index_combo in index_combinations]) # Convert the list of tuples into a tuple of lists and returns it

all_hold_indexes = index_combos()

numbers = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']
variables = [zero_held_dice_rolls, one_held_dice_rolls, two_held_dice_rolls, three_held_dice_rolls, four_held_dice_rolls, five_held_dice_rolls]

# Output all constants, formatted for easy copy-pasting to use in module

# Outputting all held dice rolls
print ("# All possible dice roll combinations based on the number of held dice.")
for number, variable in zip(numbers, variables):
    print(f"{number}_HELD_DICE_ROLLS = {variable if variable != five_held_dice_rolls else (f"{five_held_dice_rolls} # Stored as a list to prevent zero division error")}")
print ()

# Outputting all index combinations
print ("# A list of lists containing all possible indexes for selecting dice to hold.")
print (f"ALL_HOLD_INDEXES = {all_hold_indexes}")

# Waits for user input to prevent program closing before the variables have been copied
pause = input()