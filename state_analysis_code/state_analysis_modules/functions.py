from game_logic_modules.analysis_functions import *

def state_value(state, free_categories):
    """Function to find the value of the state by returning the average value of each initial roll"""
    return sum(roll_value(state, initial_roll, free_categories, 0) for initial_roll in ZERO_HELD_DICE_ROLLS) / 7776

# Dictionary to contain each state and its value
state_values = {}