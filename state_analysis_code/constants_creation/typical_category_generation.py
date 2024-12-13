import itertools

# Function to generate each a list of every combination with a given number of categories
def typical_category_generation(num_of_categories):
    return [''.join(map(str, comb)) for comb in itertools.product(['0', '1'], repeat=num_of_categories)]