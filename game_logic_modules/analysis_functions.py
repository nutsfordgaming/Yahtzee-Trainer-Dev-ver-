from game_logic_modules.analysis_constants import *
from game_logic_modules.points_functions import *
from game_logic_modules.state_values import STATE_VALUES

# A list mapping the number of held dice to the possible rolls for those dice.
HELD_DICE_ROLLS = [ZERO_HELD_DICE_ROLLS, ONE_HELD_DICE_ROLLS, TWO_HELD_DICE_ROLLS, THREE_HELD_DICE_ROLLS, FOUR_HELD_DICE_ROLLS, FIVE_HELD_DICE_ROLLS]

# A list mapping each function to an index
CATEGORY_FUNCTIONS = [aces_points, twos_points, threes_points, fours_points, fives_points, sixes_points, three_of_a_kind_points, four_of_a_kind_points, full_house_points, small_straight_points, large_straight_points, chance_points, yahtzee_points]

def find_corresponding_state(state, category, points, roll):
    """Function to find the corresponding state when a category is chosen based on the roll and the number of points acquired from this category"""

    # Subtracts 100 points if the points gained are greater than 100 (a yahtzee bonus has been applied which is not included in the upper bonus and must be ignored)
    if points >= 100:
        points -= 100
        
    index = CATEGORY_FUNCTIONS.index(category)

    corresponding_state = state[:index] + (BONUS_AVAILABLE if index == 12 and is_roll_yahtzee(roll) else FILLED) + state[index + 1:13] + (f"{int(state[13:])+points:02}" if index < 6 else state[13:])
    
    # Caps the upper total at 63
    if int(corresponding_state[13:]) > 63:
        corresponding_state = corresponding_state[:13] + '63'
    
    return corresponding_state

def state_value_load(state, category, points, roll):
    """Function to find the the value of the corresponding state"""
    corresponding_state = find_corresponding_state(state, category, points, roll)
    corresponding_state_value = STATE_VALUES[corresponding_state]

    # Adds the upper bonus points to the value if the upper total surpasses 63

    if state[13:] != '63' and corresponding_state[13:] == '63':
        corresponding_state_value += 35
        
    return corresponding_state_value

def category_value(category, roll, state):
    """Function to calculate the total value of the category (Objective 3.2.1.)"""
    category_points = category(roll, state)
    return category_points + state_value_load(state, category, category_points, roll)

# Dictionaries used to cache values of the final roll, secondary hold, secondary roll and initial hold
final_roll_values = {}
secondary_hold_values = {}
secondary_roll_values = {}
initial_hold_values = {}

# List to map each cache to an index
ALL_CACHES = [initial_hold_values, secondary_roll_values, secondary_hold_values, final_roll_values]

def clear_caches(ALL_CACHES):
    for cache in ALL_CACHES:
        cache.clear()

def hold_value(state, hold, free_categories, roll_num):
    """Computes the value of a hold by simulating subsequent rolls."""
    hold.sort() # Ensure consistent ordering for caching
    hold_values = ALL_CACHES[2*roll_num-2]
    value_key = str(hold)
    # Return cached value if available
    if value_key in hold_values:
        return hold_values[value_key]
    
    # Calculate average value of all possible subsequent rolls
    total_value = 0
    rolls_lists = HELD_DICE_ROLLS[len(hold)]
    num_of_rolls = len(rolls_lists)
    for dice in rolls_lists:
        roll = hold + dice
        value_of_roll = roll_value(state, roll, free_categories, roll_num)
        total_value += value_of_roll
    value_of_initial_hold = total_value/num_of_rolls

    # Cache and return the value
    hold_values[value_key] = value_of_initial_hold
    return value_of_initial_hold

def is_category_unavailable(category, roll, state):
    """Determines if a category is unavailable using joker rules (Objective 3.2.)"""
    if is_roll_joker(roll, state) and category != CATEGORY_FUNCTIONS[roll[0]-1]:
        # Logic if a category is in the lower section (The corresponding category must be filled for it to be available)
        if category in CATEGORY_FUNCTIONS[6:]:
            return not is_corresponding_category_filled(roll, state)
        # Logic if a category is in the upper section (The corresponding category and the upper categories must be filled for it to be available)
        else:
            return not (is_corresponding_category_filled(roll, state) and are_lower_categories_filled(state))
    return False

def roll_value(state, roll, free_categories, roll_num):
    """Recursively computes the value of a roll by considering all possible holds and categories (Objective 3.2., 3.2.1.)"""
    roll.sort() # Ensure consistent ordering for caching
    # Return cached value if available
    if roll_num > 0:
        roll_values = ALL_CACHES[2*roll_num-1]
        value_key = str(roll)
        if value_key in roll_values:
            return roll_values[value_key]
    
    # Evaluate the value of the roll based on holds or categories
    highest_value_choice = 0

    # Base case: finds the highest value category
    if roll_num == 2:
        for category in free_categories:
            # Skips the category if it is unavailable
            if is_category_unavailable(category, roll, state):
                continue
            value_of_category = category_value(category, roll, state)
            if value_of_category > highest_value_choice:
                highest_value_choice = value_of_category

    else:
        # Recursive case: finds the highest value hold
        for hold_indexes in ALL_HOLD_INDEXES:
            hold = [roll[index] for index in hold_indexes]
            value_of_hold = hold_value(state, hold, free_categories, roll_num+1)
            if value_of_hold > highest_value_choice:
                highest_value_choice = value_of_hold
    
    # Cache and return the value
    if roll_num > 0:
        roll_values[value_key] = highest_value_choice
    return highest_value_choice

def calculate_choice(state, roll, free_categories, roll_num, points_away_from_optimal):
    """Calculates the value of each choice (category if roll_num == 2, else hold), and returns the choice which is the least valuable choice above the threshold (Objective 3.2.)"""
    values = {}

    # Finds the value of each category
    if roll_num == 2:
        for category in free_categories:
            # Skips the category if it is unavailable
            if is_category_unavailable(category, roll, state):
                continue
            value_of_category = category_value(category, roll, state)
            values[value_of_category] = category

    else:
        # Finds the value of each hold
        for hold_indexes in ALL_HOLD_INDEXES:
            hold = [roll[index] for index in hold_indexes]
            value_of_hold = hold_value(state, hold, free_categories, roll_num+1)
            values[value_of_hold] = hold
    
    # Finds the choice which is the least valuable choice above the threshold and returns it
    all_values = values.keys()
    threshold_value = (max(all_values) - points_away_from_optimal)
    return values[min([value for value in all_values if value >= threshold_value])]

def find_free_categories(state):
    """Finds the free categories of a given state"""
    return [CATEGORY_FUNCTIONS[index] for index in range(13) if state[index] == UNFILLED]