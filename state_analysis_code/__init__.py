import time

from state_analysis_code.state_analysis_modules.constants import *
from state_analysis_code.state_analysis_modules.functions import *

"""Analyse every state (Objective 3.1.1.)"""
# Start timing the analysis
start_time = time.time()
for i, state in enumerate(ALL_STATES):
    """Loops through each state, calculates its value and stores it"""

    # Resets each cache
    clear_caches(ALL_CACHES)

    # Finds the value of the state

    # If applicable, the value of the state is equalled to an "equivalent" state that has already been evaluated to prevent repeated calculation
    if MAX_UPPER_SCORES[state[:6]] + int(state[13:]) < 63 and state[13:] != '00': 
        value_of_state = state_values[state[:13] + '00']
    # Otherwise, calculates the value of the state traditionally
    else:
        # Finds all free categories given the state
        free_categories = find_free_categories(state)
        value_of_state = state_value(state, free_categories)
            
    # Stores the value in the dictionary, and outputs the state, its value and the percent of states which have been analysed, to ensure testing is working as expected
    state_values[state] = value_of_state
    print (f"{state}: {value_of_state} ({i/536448*100}%)")
    
# Stores the value in a text file for retrieval, formatted for easy copy-pasting
with open('state_values.txt', 'w') as state_file:
    state_file.write(f"STATE_VALUES = {state_values}")
    
# Stop timing the analysis
end_time = time.time()

# Output the total time taken to analyse every state
print (end_time - start_time)

# Waits for user input to prevent program closing before the time can be viewed
input()