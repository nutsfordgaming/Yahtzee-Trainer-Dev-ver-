import itertools

from typical_category_generation import typical_category_generation

"""Find each upper combination and assign a tuple of each possible upper total to it"""


# Generate all upper combinations
all_upper_combinations = typical_category_generation(6)

# Define variable for multiplying each category by
category = [1, 2, 3, 4, 5, 6]

# Create empty dictionary for storing each tuple of upper total
upper_combination_values = {}

def upper_values_recursive(upper_combination, all_values, index=0, partial_sum=0):
    # Base case: if we've processed all elements of upper_combination
    if index == 6:
        # Ensure the result is capped at 63 and formatted as a 2-digit string
        total = min(partial_sum, 63)
        total_str = f"{total:02}"
        all_values.add(total_str)
        return all_values

    # Get the current digit of upper_combination
    current_digit = int(upper_combination[index])

    # If the current digit is 0, skip all multiplications and proceed
    if current_digit == 0:
        return upper_values_recursive(upper_combination, all_values, index + 1, partial_sum)

    # Recur with all possible values for the current multiplier (0 to 5)
    for multiplier in range(6):
        new_sum = partial_sum + (current_digit * category[index] * multiplier)
        upper_values_recursive(upper_combination, all_values, index + 1, new_sum)

    return all_values

# Find the upper total for each upper combination and store it
for upper_combination in all_upper_combinations:
    all_values = set()
    all_values = upper_values_recursive(upper_combination, all_values)
    # Convert the set to a sorted tuple (to improve efficiency and memory usage) and update the dictionary
    upper_combination_values[upper_combination] = tuple(sorted(all_values))


"""Generate basic states (only describing categories)"""

# Generate all possible combinations for the first 12 categories (0 or 1)
initial_category_states = typical_category_generation(12)

# Generate all possible values for the yahtzee category (0, 1, or 2)
yahtzee_category_states = ['0', '1', '2']

# Generate all possible states of categiries by combining the first 12 categories and the yahtzee category
category_states = [binary + tri for binary, tri in itertools.product(initial_category_states, yahtzee_category_states)]

"""Sort each state"""

# Function to count the number of categories that are filled
def count_non_zeros(state):
    return sum(1 for digit in state[:13] if digit != '0')

# Sort the states based on the number of unfilled categories in descending order
sorted_states = sorted(category_states, key=count_non_zeros, reverse=True)


"""Add each corresponding upper total to each state"""

# Initialise an empty list to add completed states to
all_states = []

# Add upper total to the end of each category state
for state in sorted_states:
    all_totals = upper_combination_values[state[:6]]
    for result in all_totals:
        all_states.append(state + result)


# Output number of states for reference
print (len(all_states))

"""Save the states to a file, formatted for easy copy-pasting to use in module"""

# Write the sorted list of states to a text file in one operation
with open("all_states.txt", "w") as file:
    file.write(f"ALL_STATES = {str(all_states)}")  # Write the list as a string

print("The list of every state has been written to 'all_states.txt'")