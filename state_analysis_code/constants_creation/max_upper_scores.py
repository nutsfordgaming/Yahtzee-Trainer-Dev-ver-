from typical_category_generation import typical_category_generation

# Generate all upper combinations
all_upper_combinations = typical_category_generation(6)

# Iterate over each upper combination, finding each max score and adding it to a dictionary
max_upper_scores = {}
for combination in all_upper_combinations:
    max_upper_scores[combination] = int(combination[0]) * 5 + int(combination[1]) * 10 + int(combination[2]) * 15 + int(combination[3]) * 20 + int(combination[4]) * 25 + int(combination[5]) * 30

# Output all max upper scores, formatted for easy copy-pasting to use in module
print (f"MAX_UPPER_SCORES = {max_upper_scores}")

# Waits for user input to prevent program closing before the variables have been copied
pause = input()