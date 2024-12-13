from game_logic_modules.analysis_functions import *

def standard_mode():
    """Repeatedly takes in the roll and finds the optimal choice for a standard game"""
    # Initialise variables
    state = '000000000000000'
    roll_num = 0
    points_away_from_optimal = 0

    print ('Input "end" at any point to exit standard testing')
    while True:
        # Outputs state to keep track of the game
        print (state)

        # Finds the free categories
        free_categories = find_free_categories(state) # Finds the unfilled categories of the given state

        roll = input('Input the roll here (seperating each dice value in the roll with a space): ')
        if roll == 'end':
            break
        try:
            roll = sorted(int(dice) for dice in roll.split()) # Convert roll from a string to a sorted list of integers
        except:
            print ("Incorect roll inputted. Try again.")
            continue
        
        # Calculates and outputs the optimal choice
        choice = (calculate_choice(state, roll, free_categories, roll_num, points_away_from_optimal))
        print (choice)

        # Increments the roll number
        roll_num += 1

        # Finds the corresponding state each time a category is chosen and resets the roll number, and ends the function if the game has finished
        if roll_num == 3:
            points = choice(roll, state)
            state = find_corresponding_state(state, choice, points, roll)
            roll_num = 0
            if sum(1 for category in state[:13] if category != '0') == 13:
                break
        
        # Clears each cache
        clear_caches(ALL_CACHES)


def in_depth_mode():
    """Repeatedly takes in an input for the state, roll, roll number and the number of points away from optimal the choice is, and outputs the choice representative of the inputs"""
    print ('Input "end" at any point to exit in depth testing')
    while True:
        # Takes the input for each parameter, and allows the user to break the loop, and therefore this module each time an input is taken. Also converts each input into a suitable parameter, containing exception handling to check if the values were inputted incorrectly
        state = input('Input the state: ')
        if state == 'end':
            break
        try:
            free_categories = find_free_categories(state) # Finds the unfilled categories of the given state
        except:
            print ("Incorect state inputted. Try again.")
            continue

        roll = input('Input the roll here (seperating each dice value in the roll with a space): ')
        if roll == 'end':
            break
        try:
            roll = sorted(int(dice) for dice in roll.split()) # Convert roll from a string to a sorted list of integers
        except:
            print ("Incorect roll inputted. Try again.")
            continue
        
        roll_num = input('Input the roll number here (0: initial roll, 1: secondary roll, 2: final roll): ')
        if roll_num == 'end':
            break
        try:
            roll_num = int(roll_num) # Convert roll_num from a string to an integer
        except:
            print ("Incorect roll number inputted. Try again.")
            continue

        points_away_from_optimal = input('Input the number of points away from optimal the choice is: ')
        if points_away_from_optimal == 'end':
            break
        try:
            points_away_from_optimal = float(points_away_from_optimal)
        except:
            print ("Incorect points away from optimal number inputted. Try again.")
            continue
        
        # Calculates and outputs each choice
        print (calculate_choice(state, roll, free_categories, roll_num, points_away_from_optimal))
        
        # Clears each cache
        clear_caches(ALL_CACHES)
        

while True:
    test_mode = input('Would you like to perform standard testing or in depth testing (0 for the standard mode and 1 for the in-depth mode, end to leave state analysis testing): ')
    if test_mode == '0':
        standard_mode()
        
    elif test_mode == '1':
        in_depth_mode()
        
    elif test_mode == 'end':
        break
        
    else:
        print ("Incorrect code inputted. Try again.")