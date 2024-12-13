# Functions used to calculate points (Objective 3., 3.4.)

# Using words to represent categories' state for readability and clarity
UNFILLED = '0'
FILLED = '1'
BONUS_AVAILABLE = '2'

# Use sets for efficient small and large straight checks
SMALL_STRAIGHTS = {frozenset([1, 2, 3, 4]), frozenset([2, 3, 4, 5]), frozenset([3, 4, 5, 6])}
LARGE_STRAIGHTS = {frozenset([1, 2, 3, 4, 5]), frozenset([2, 3, 4, 5, 6])}

def is_corresponding_category_filled(roll, state):
    """Checks if the category corresponding to the first die in the roll is already filled."""
    return state[roll[0]-1] == FILLED

def is_roll_yahtzee(roll):
    """Checks if the roll is a yahtzee by checking if all dice in the roll are the same."""
    return roll[0] == roll[4]

def are_lower_categories_filled(state):
    """Checks if all lower section categories are filled in the state."""
    return all(category != UNFILLED for category in state[6:12])

def is_roll_joker(roll, state):
    """Determines if a roll qualifies as a 'joker'"""
    return is_roll_yahtzee(roll) and state[12] != UNFILLED

def is_roll_joker_bonus(roll, state):
    """Determines if a roll qualifies as a 'joker'"""
    return is_roll_yahtzee(roll) and state[12] == BONUS_AVAILABLE

# Determines if a roll can be applied to a lower category, taking into account that if a yahtzee has been rolled and the yahtzee category has already been filled, then the corresponding category must be filled for the category to be available

def is_roll_three_of_a_kind(roll):
    """Checks if the roll is a three of a kind by checking if at least 3 dice in the roll are the same."""
    return any(roll[index] == roll[index + 2] for index in range(3))

def is_roll_four_of_a_kind(roll):
    """Checks if the roll is a four of a kind by checking if at least 4 dice in the roll are the same."""
    return any(roll[index] == roll[index + 3] for index in range(2))

def is_roll_full_house(roll, state):
    """Checks if the roll is a full house by checking if 3 dice in the roll are the same and 2 different numbers in the roll are the same."""
    return is_roll_joker(roll, state) or ((roll[0] == roll[1] and roll[2] == roll[4]) or (roll[0] == roll[2] and roll[3] == roll[4])) and not is_roll_yahtzee(roll)

def is_roll_small_straight(roll, state):
    """Checks if the roll is a small straight by checking if the roll is in the precomputed set of all possible small straights."""
    return is_roll_joker(roll, state) or any(small_straight.issubset(set(roll)) for small_straight in SMALL_STRAIGHTS)

def is_roll_large_straight(roll, state):
    """Checks if the roll is a large straight by checking if the roll is in the precomputed set of all possible large straights."""
    return is_roll_joker(roll, state) or frozenset(roll) in LARGE_STRAIGHTS

# Calculates the score for the upper categories by calling the upper totaller function with a number to represent the category.
def upper_totaller(roll, state, num):
    """Calculates the score for upper categories by calculating the sum of the dice  which are the same as the category num represents + 100 if the roll is an applicable joker"""
    return (100 if is_roll_joker_bonus(roll, state) else 0) + sum(dice for dice in roll if dice == num)

def aces_points(roll, state):
    return upper_totaller(roll, state, 1)

def twos_points(roll, state):
    return upper_totaller(roll, state, 2)

def threes_points(roll, state):
    return upper_totaller(roll, state, 3)

def fours_points(roll, state):
    return upper_totaller(roll, state, 4)

def fives_points(roll, state):
    return upper_totaller(roll, state, 5)

def sixes_points(roll, state):
    return upper_totaller(roll, state, 6)

# Calculates the score for lower categories
def totaller(roll, state):
    """Calculates the score for certain categories by calculating the sum of the dice + 100 if the roll is an applicable joker"""
    return (100 if is_roll_joker_bonus(roll, state) else 0) + sum(roll)

def three_of_a_kind_points(roll, state):
    """Calculates the score by calling the totaller function if the roll is a three of a kind"""
    return totaller(roll, state) if is_roll_three_of_a_kind(roll) else 0

def four_of_a_kind_points(roll, state):
    """Calculates the score by calling the totaller function if the roll is a four of a kind"""
    return totaller(roll, state) if is_roll_four_of_a_kind(roll) else 0

def full_house_points(roll, state):
    """Returns 125 if the roll is a lower joker, 25 if it is a full house, 0 if it is neither"""
    return 125 if is_roll_joker_bonus(roll, state) else (25 if is_roll_full_house(roll, state) else 0)

def small_straight_points(roll, state):
    """Returns 130 if the roll is a lower joker, 30 if it is a small straight, 0 if it is neither"""
    return 130 if is_roll_joker_bonus(roll, state) else (30 if is_roll_small_straight(roll, state) else 0)

def large_straight_points(roll, state):
    """Returns 130 if the roll is a lower joker, 30 if it is a large straight, 0 if it is neither"""
    return 140 if is_roll_joker_bonus(roll, state) else (40 if is_roll_large_straight(roll, state) else 0)

def chance_points(roll, state):
    """Calculates the score by calling the totaller function"""
    return totaller(roll, state)

def yahtzee_points(roll, state):
    """Returns 50 if the roll is a yahtzee, 0 if it is not"""
    return 50 if is_roll_yahtzee(roll) else 0