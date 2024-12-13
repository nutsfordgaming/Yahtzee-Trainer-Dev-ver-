import tkinter as tk
import random

from game_logic_modules.analysis_functions import *

# Initialises basic constants
CATEGORIES = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", "Three of a kind", "Four of a kind", "Full House", "Small Straight", "Large Straight", "Chance", "Yahtzee"]
TOTALS = ["Upper total", "Upper bonus", "Total"]
SCORES = CATEGORIES[:6] + TOTALS[:2] + CATEGORIES[6:] + [TOTALS[2]]

SCORING_FUNCTIONS = {"Aces": aces_points, "Twos": twos_points, "Threes": threes_points, "Fours": fours_points, "Fives": fives_points, "Sixes": sixes_points, "Three of a kind": three_of_a_kind_points, "Four of a kind": four_of_a_kind_points, "Full House": full_house_points, "Small Straight": small_straight_points, "Large Straight": large_straight_points, "Chance": chance_points, "Yahtzee": yahtzee_points}
FUNCTIONS_SCORING = {aces_points: "Aces", twos_points: "Twos", threes_points: "Threes", fours_points: "Fours", fives_points: "Fives", sixes_points: "Sixes", three_of_a_kind_points: "Three of a kind", four_of_a_kind_points: "Four of a kind", full_house_points: "Full House", small_straight_points: "Small Straight", large_straight_points: "Large Straight", chance_points: "Chance", yahtzee_points: "Yahtzee"}

def points_away_to_difficulty(points):
    """Binds the points away from optimal value to its equivalent difficulty and colour"""
    if points == 0:
        return "Optimal", "red"
    elif 0 < points <= 1:
        return "Difficult", "orange"
    elif 1 < points <= 3:
        return "Hard", "yellow"
    elif 3 < points <= 5:
        return "Medium", "green"
    elif 5 < points < 10:
        return "Easy", "blue"
    else:
        return "Super Easy", "cyan"

class players:
    """Class for any player"""

    all_players = []
    def __init__(self, name, colour="white"):
        """Initialises a generic player and adds itself to a list"""
        self.name = name
        self.state = '000000000000000'
        self.scores = {**{score: None for score in CATEGORIES[:6]}, **{score: 0 for score in TOTALS[:2]}, **{score: None for score in CATEGORIES[6:]}, **{TOTALS[2]: 0}}
        self.points_away_from_optimal = 0
        self.colour = colour
        players.all_players.append(self)

    def update_player(self, category, points, roll):
        """Updates the players state and score"""

        # Updates the state
        self.state = find_corresponding_state(self.state, category, points, roll)

        # Updates the category chose
        self.scores[FUNCTIONS_SCORING[category]] = points

        # Updates the upper total
        upper_total = 0
        for category in CATEGORIES[:6]:
            score = self.scores[category]
            if score is not None:
                upper_total += score
        self.scores["Upper total"] = upper_total

        # Updates the upper bonus
        num_of_jokers_in_upper = 0
        for category in CATEGORIES[:6]:
            score = self.scores[category]
            if score is not None and self.scores[category] > 100:
                num_of_jokers_in_upper += 1
        # Ensures yahtzee bonuses do not cause an upper bonus
        if upper_total-(100*num_of_jokers_in_upper) >= 63:
            self.scores["Upper bonus"] = 35

        # Updates the total score
        total_score = 0
        for category in CATEGORIES:
            score = self.scores[category]
            if score is not None:
                total_score += score
        self.scores["Total"] = total_score


class computer_players(players):
    """Class for computer players, inheriting from players class"""

    all_computers = []
    def __init__(self, name, colour):
        """Initialises computer player and adds itself to a list"""
        super().__init__(name, colour)
        self.difficulty = 'Optimal'
        computer_players.all_computers.append(self)

    def update_difficulty(self, points_away):
        """Updating the difficulty of a player"""
        self.points_away_from_optimal = points_away
        self.difficulty, self.colour = points_away_to_difficulty(points_away)

# Initialise starting players
players(name="You")
computer_players(name="Player 1", colour="red")

# Initialise helper functions
def clear_ui(root):
    """Clears the current UI"""
    for widget in root.winfo_children():
        widget.destroy()

is_full_screen = True
def switch_fullscreen(root, current_is_full_screen):
    """Changes if the program is in fullscreen or not"""
    global is_full_screen
    is_full_screen = not current_is_full_screen
    root.attributes("-fullscreen", is_full_screen)

def draw_dice_face(canvas, value):
    """Draw the dice face with a certain value (1-6) on the given canvas."""
    canvas.delete("all")  # Clear previous drawings
    size = 50
    margin = 10
    radius = 5

    # Coordinates for the dice dots
    positions = {
        1: [(size // 2, size // 2)],
        2: [(margin, margin), (size - margin, size - margin)],
        3: [(margin, margin), (size // 2, size // 2), (size - margin, size - margin)],
        4: [(margin, margin), (margin, size - margin), (size - margin, margin), (size - margin, size - margin)],
        5: [(margin, margin), (margin, size - margin), (size - margin, margin), (size - margin, size - margin), (size // 2, size // 2)],
        6: [(margin, margin), (margin, size // 2), (margin, size - margin), (size - margin, margin), (size - margin, size // 2), (size - margin, size - margin)],
    }

    for x, y in positions[value]:
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")

def home(root):
    """Generates the home page UI (Objective 1.)"""
    # Clear the UI, so it can be replaced
    clear_ui(root)

    def render_player_labels():
        """Renders each player label"""
        # Clears the current player labels
        for widget in player_frame.winfo_children():
            widget.destroy()
        
        for i, players in enumerate(computer_players.all_computers):
            players.name = f"Player {i+1}"
            label = tk.Label(player_frame, text=f"{players.name}\n{players.difficulty}", font=("Arial", 12), bg="black", fg=players.colour, width=10, height=3)
            label.grid(row=0, column=i, padx=5, pady=5)
            label.bind("<Button-1>", lambda e, idx=i: select_player(idx))

    def select_player(index):
        """Selects the player with the given index"""
        nonlocal selected_player
        selected_player = computer_players.all_computers[index]
        points_label.config(text=f"{selected_player.name}: {selected_player.difficulty}")
        difficulty_slider.set(selected_player.points_away_from_optimal)
        render_difficulty(selected_player.points_away_from_optimal)

    def add_player():
        """Adds a new generic player"""
        computer_players(name=f"Player {len(computer_players.all_computers)+1}", colour="red")
        render_player_labels()
        render_plusminus_buttons()  # Render the visibility of + and - buttons

    def remove_player(selected_player):
        """Removes the selected player"""
        computer_players.all_computers.remove(selected_player)
        players.all_players.remove(selected_player)
        # Select the first players again, or reset state
        select_player(0)
        render_player_labels()
        render_plusminus_buttons()  # Render the visibility of + and - buttons

    def render_difficulty(val):
        """Renders the new difficulty when the difficulty of the player is changed (Objective 1.1.2.)"""
        selected_player.update_difficulty(float(val))
        render_player_labels()
        points_label.config(text=f"{selected_player.name}: {selected_player.difficulty}")

    def render_plusminus_buttons():
        """Re-renders the plus and minus button to remove them or add them depending on the number of players"""
        if len(computer_players.all_computers) <= 1:
            remove_button.grid_forget()  # Hide the remove button when there's only one players
        else:
            remove_button.grid(row=0, column=1, padx=20)

        if len(computer_players.all_computers) >= 9:
            add_button.grid_forget()  # Hide the add button when there are 9 players
        else:
            add_button.grid(row=0, column=0, padx=20)

    # Create UI for the home screen

    # Title label
    title_label = tk.Label(root, text="Yahtzee", font=("Arial", 40, "bold"), bg="red", fg="black")
    title_label.pack(pady=10)

    # Frame for the play and about buttons
    top_frame = tk.Frame(root, bg="white")
    top_frame.pack(fill="x", pady=5)

    # Play button (Objective 1.2.)
    play_button = tk.Button(top_frame, text="Play", font=("Arial", 20), bg="black", fg="white", width=5, command=lambda: play(root, players))
    play_button.pack(side="left", padx=20)

    # About button (Objective 1.3.)
    about_button = tk.Button(top_frame, text="About", font=("Arial", 20), bg="black", fg="white", width=5, command=lambda: about(root))
    about_button.pack(side="right", padx=20)

    # Frame for the add
    control_frame = tk.Frame(root, bg="white")
    control_frame.pack(pady=20)

    # (Objective 1.1.)
    # Add button
    add_button = tk.Button(control_frame, text="+", font=("Arial", 40), bg="green", fg="white", command=add_player)
    add_button.grid(row=0, column=0, padx=20)

    # Remove button
    remove_button = tk.Button(control_frame, text="-", font=("Arial", 40), bg="red", fg="white", command=lambda: remove_player(selected_player))
    remove_button.grid(row=0, column=1, padx=20)

    # Frame for each player
    player_frame = tk.Frame(root, bg="white")
    player_frame.pack()

    # Label to explain points away from optimal slider
    points_label = tk.Label(root, font=("Arial", 16), bg="white", fg="black")
    points_label.pack(pady=10)

    # Points away from optimal slider (Objective 1.1.1.)
    difficulty_slider = tk.Scale(root, from_=0, to=10, orient="horizontal", length=400, showvalue=1, resolution=0.01, command=render_difficulty)
    difficulty_slider.pack(pady=20)

    # Initially selects the pre-created player
    selected_player = computer_players.all_computers[0]

    # Render the UI
    render_plusminus_buttons()
    render_player_labels()
    render_difficulty(selected_player.points_away_from_optimal)

    root.mainloop()

def play(root, players):
    """Allows the user to play the game with the players added (Objective 1.2.1., 2.)"""
    # Clear the UI, so it can be replaced
    clear_ui(root)

    # Create functions to manage game logic
    def roll_dice_func():
        """Rolls the dice (Objective 2.2.1)"""
        nonlocal roll_dice, roll, roll_num
        if roll_num != 2 and player not in computer_players.all_computers:
            roll_dice = [random.randint(1, 6) for _ in range(5 - len(keep_dice))]
            roll = roll_dice + keep_dice
            roll_num += 1
            render_game(roll_num)

    def render_roll_count(roll_num):
        """Render the label showing the number of rolls left."""
        roll_count_label.config(text=f"Roll ({2-roll_num} left)")

    def move_to_keep(index):
        """Move a die from the roll area to the keep area. (Objective 2.4.)"""
        if player not in computer_players.all_computers and index < len(roll_dice):
            keep_dice.append(roll_dice.pop(index))
            render_dice()

    def move_to_roll(index):
        """Move a die from the keep area back to the roll area."""
        # Ensures the dice can be moved
        if player not in computer_players.all_computers and index < len(keep_dice):
            roll_dice.append(keep_dice.pop(index))
            render_dice()
    
    def render_game_finished_screen():
        """Display the game finished screen with the winner's details."""
        # Find the winners
        highest_score = max(player.scores["Total"] for player in players.all_players)
        winners = str([player.name for player in players.all_players if player.scores["Total"] == highest_score])[1:-1]

        # Clear the existing root window
        clear_ui(root)

        # Create a black background
        root.configure(bg="black")

        # Display the "Game Finished" message
        game_finished_label = tk.Label(root, text="Game Finished", font=("Arial", 36, "bold"), fg="red", bg="black")
        game_finished_label.pack(pady=40)

        # Display the winner details
        winner_details_label = tk.Label(root, text=f"{winners} won with a score of {highest_score}", font=("Arial", 16), fg="white", bg="black")
        winner_details_label.pack(pady=20)

    def on_category_select(category, is_acceptable=None):
        """Handle when a category is selected. (Objective 2.6.3.)"""
        nonlocal roll_dice, keep_dice, player_index, player, roll_num, turn, roll, state

        # Prevent box that isn't a category (e.g upper bonus) being clicked
        if category not in CATEGORIES:
            return

        # Initialises required functions
        scoring_function = SCORING_FUNCTIONS[category]
        state = player.state
        if is_acceptable is None:
            is_acceptable = not(player in computer_players.all_computers)

        # Check if the category is usable (if the category has been scored, if the category has been clicked during a computer player's turn, and if the category is available using joker rules)
        if player.scores[category] is None and is_acceptable and not is_category_unavailable(scoring_function, sorted(roll), state):
            # Calculates the score for the category
            total_roll = sorted(roll_dice + keep_dice)
            score = scoring_function(total_roll, state)
            
            # Save the player's info
            player.update_player(scoring_function, score, total_roll)

            # Moves to the next player
            player_index = (player_index + 1) % len(players.all_players)
            player = players.all_players[player_index]
            if player_index == 0:
                turn += 1
            state = player.state

            # Checks if the game is over
            if turn == 13:
                render_game_finished_screen()
                return
            
            # Generates a new set of dice for the next player
            roll_dice = [random.randint(1, 6) for _ in range(5)]
            keep_dice = []
            roll = roll_dice

            # Resets the player's roll number
            roll_num = 0
            
            # Renders the next turn
            render_turn()

    def perform_choice(points_away_from_optimal, state, free_categories):
        """Handles when the suitable choice is wanted (Objective 2.7, 3.3.)"""
        nonlocal roll_dice, keep_dice, roll, roll_num
        roll = roll_dice + keep_dice
        
        # Calculates the choice of the player
        choice = calculate_choice(state, roll, free_categories, roll_num, points_away_from_optimal)
        clear_caches(ALL_CACHES)
        
        # Re-rolls the dice when hold is suitable
        if choice == keep_dice:
            roll_dice = [random.randint(1, 6) for _ in range(5-len(keep_dice))]
            roll = roll_dice + keep_dice
            roll_num += 1
        else:
            # Holds the suitable dice
            if roll_num != 2:
                roll_dice = list(roll)
                keep_dice = choice
                for dice in keep_dice:
                    roll_dice.remove(dice)
            
            # Selects the optimal category
            else:
                on_category_select(FUNCTIONS_SCORING[choice], True)
                return
        render_game(roll_num)

    def render_turn_label():
        """Renders the turn label"""
        turn_label.config(text=f"{player.name}'s Turn", fg=player.colour)

    def render_players_score():
        """Calculate and display scores for the current players's column. (Objective 2.6.2.)"""
        players_state = player.state
        function_roll = sorted(roll)
        # Render preview scores for the current players's column
        for row, func in enumerate(SCORES, start=1):
            saved_score = player.scores[func]
            score_label = table_frame.grid_slaves(row=row, column=player_index + 1)[0]

            # Renders the score for a used category
            if saved_score is not None:
                score_label.config(text=saved_score, fg="black")
                continue
            
            function = SCORING_FUNCTIONS[func]

            # Displays nothing when the category is unavailable
            if is_category_unavailable(function, roll, players_state):
                score_label.config(text="")
            
            # Renders the preview score
            else:
                score = function(function_roll, players_state)
                score_label.config(text=str(score), fg="red")

    def render_score_card():
        """Renders the entire score card (2.6.1.)"""
        # Renders the current player's score
        render_players_score()

        # Render stored categories scores for all other players
        for row in range(16):
            for col in range(len(players.all_players)):

                # Skips the current player's column
                if player_index == col:
                    continue

                # Renders the score for the category and player
                rendering_player = players.all_players[col]
                score_label = table_frame.grid_slaves(row=row+1, column=col+1)[0]
                score = str(rendering_player.scores[SCORES[row]])
                score_label.config(text="" if score == "None" else score, fg="black")
    
    def render_dice():
        """Render the dice display for roll and keep areas."""
        # Render roll dice
        for i, value in enumerate(roll_dice):
            draw_dice_face(roll_dice_canvases[i], value)
        
        # Clear remaining roll dice canvases
        for i in range(len(roll_dice), 5):
            roll_dice_canvases[i].delete("all")

        # Render keep dice
        for i, value in enumerate(keep_dice):
            draw_dice_face(keep_dice_canvases[i], value)

        # Clear remaining keep dice canvases
        for i in range(len(keep_dice), 5):
            keep_dice_canvases[i].delete("all")
    
    def render_choose_button():
        """Renders the button to step through each choice"""
        # Initialises variables for the function to use
        points_away_from_optimal = player.points_away_from_optimal
        free_categories = find_free_categories(state)

        # Renders the button
        choose_button.config(text=f"Step through {player.name}'s turn" if player in computer_players.all_computers else "Perform optimal choice", command=lambda: perform_choice(points_away_from_optimal, state, free_categories))
        
    # Initialize game UI

    # Create a frame for the score card (Objective 2.6.)
    table_frame = tk.Frame(root, bg="white")
    table_frame.pack(side="right")

    # Create the initial row ("Category", and the player's names)
    tk.Label(table_frame, text="Category", font=("Arial", 14, "bold"), width=7, bg="white").grid(row=0, column=0)
    for col, player in enumerate(players.all_players):
        tk.Label(table_frame, text=player.name, font=("Arial", 14, "bold"), width=10, bg="black", fg=player.colour).grid(row=0, column=col + 1, padx=5)
    
    # Creates labels for each category to be used for
    for row, category in enumerate(SCORES, start=1):
        tk.Label(table_frame, text=category, font=("Arial", 12), width=15, bg="white").grid(row=row, column=0, padx=5, pady=5)
        for col, players in enumerate(players.all_players):
            score_label = tk.Label(table_frame, text="", font=("Arial", 12), width=10, bg="white", relief="solid")
            score_label.grid(row=row, column=col + 1, padx=5, pady=5)
            # Bind click event to on_category_select
            score_label.bind("<Button-1>", lambda e, c=category: on_category_select(c))

    # Creates a frame for the dice area
    game_frame = tk.Frame(root, bg="white")
    game_frame.pack(side="left", padx=10, pady=10)

    # Label to display the number of rolls the player has left (Objective 2.5)
    roll_count_label = tk.Label(game_frame, font=("Arial", 12), bg="white")
    roll_count_label.grid(row=3, column=0, columnspan=5, pady=10)

    # Creates canvases for each dice in the roll area (Objective 2.1.)
    roll_dice_canvases = []
    for i in range(5):
        canvas = tk.Canvas(game_frame, width=50, height=50, bg="white", relief="solid", bd=1)
        canvas.grid(row=2, column=i, padx=5)
        canvas.bind("<Button-1>", lambda e, idx=i: move_to_keep(idx))
        roll_dice_canvases.append(canvas)

    # Creates a frame for the keep area
    keep_frame = tk.Frame(game_frame, bg="red", width=250, height=100)
    keep_frame.grid(row=5, column=0, columnspan=5, pady=10)
    keep_frame.grid_propagate(False)

    # Creates a label for the keep area
    tk.Label(keep_frame, text="Keep", font=("Arial", 12), bg="red", fg="black").pack(anchor="w", padx=5)

    # Creates canvases for each dice in the keep area (Objective 2.4.)
    keep_dice_canvases = []
    for i in range(5):
        canvas = tk.Canvas(keep_frame, width=50, height=50, bg="white", relief="solid", bd=1)
        canvas.pack(side="left", padx=5)
        canvas.bind("<Button-1>", lambda e, idx=i: move_to_roll(idx))
        keep_dice_canvases.append(canvas)

    # Creates a roll button (Objective 2.2.)
    roll_button = tk.Button(game_frame, text="Roll", font=("Arial", 12), command=roll_dice_func)
    roll_button.grid(row=10, column=0, columnspan=5, pady=10)

    # Creates the choose button
    choose_button = tk.Button(game_frame, font=("Arial", 12))
    choose_button.grid(row=4, column=0, columnspan=5, pady=10)

    # Creates the turn label, to show which player's turn it is
    turn_label = tk.Label(game_frame, font=("Arial", 16), bg="black")
    turn_label.grid(row=0, column=0, columnspan=5, pady=10)

    def render_game(roll_num):
        """Renders the game every time a new roll occurs"""
        render_players_score()
        render_dice()
        render_roll_count(roll_num)
    
    def render_turn():
        """Renders the game each time a turn finishes"""
        render_score_card()
        render_game(roll_num)
        render_choose_button()
        render_turn_label()
    
    turn = 0
    player_index = 0
    player = players.all_players[player_index]
    state = player.state
    roll_num = 0
    roll_dice = [random.randint(1, 6) for _ in range(5)]
    keep_dice = []
    roll = roll_dice
    
    render_turn()

def about(root):
    """Displays the About screen (Objective 1.3.1.)"""
    # Clear the existing UI
    clear_ui(root)
    
    # Back Button (Objective 1.3.2.)
    back_button = tk.Button(
        root,
        text="Back",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="black",
        command=lambda: home(root),  # Function to return to the home screen
    )
    back_button.place(x=20, y=20, width=100, height=50)

    # Title for Interface
    interface_label = tk.Label(
        root,
        text="Interface:",
        font=("Arial", 20, "bold"),
        fg="black",
        bg="white",
        anchor="w",
    )
    interface_label.place(x=50, y=100)

    # Interface Details
    interface_text = (
        "Menu:\n"
        "  • Press the green + symbol to add a player and the red - to remove one.\n"
        "  • To change a player's difficulty, click on the player who you\n"
        "    would like to change and move the slider until their difficulty is\n"
        "    your desired 'points from optimal' (The number of points below\n"
        "    the optimal choice's value that the player would decide to choose).\n"
        "\nGame:\n"
        "  • Click on the 'roll' button to roll/re-roll your dice\n"
        "  • Click on a dice to switch it between keeping and re-rolling\n"
        "  • Click on a category to select it"
    )
    interface_details = tk.Label(
        root,
        text=interface_text,
        font=("Arial", 12),
        fg="black",
        bg="white",
        justify="left",
        anchor="nw",
    )
    interface_details.place(x=50, y=150, width=500, height=500)  # Increased width

    # Rules Section
    rules_label = tk.Label(
        root,
        text="Rules:",
        font=("Arial", 20, "bold"),
        fg="black",
        bg="white",
        anchor="w",
    )
    rules_label.place(x=550, y=100)

    rules_text = (
        "Objective:\n"
        "  The goal is to score the highest total of all the players.\n\n"
        "Gameplay:\n"
        "  Rolling the Dice:\n"
        "    • Each player takes a turn to roll all five dice.\n"
        "    • After the first roll, the player can choose to reroll any of the\n"
        "      dice up to two more times.\n"
        "    • After the third roll, or if the player is satisfied with a\n"
        "      previous roll, they must choose a category\n"
        "      on their scorecard to score that turn.\n"
        "  Choosing a Category:\n"
        "    • The player must select one of the 13 available categories on the\n"
        "      scorecard to score the roll.\n"
        "    • Each category can be filled in only once per game.\n"
        "    • The score for that roll is recorded in the chosen category, and\n"
        "      the turn ends.\n\n"
        "Scoring:\n"
        "  Players can score in any unfilled category, even if it results in 0 points.\n"
        "  Upper Section:\n"
        "    • Aces (Ones): Sum of all ones.\n"
        "    • Twos: Sum of all twos.\n"
        "    • Threes: Sum of all threes.\n"
        "    • Fours: Sum of all fours.\n"
        "    • Fives: Sum of all fives.\n"
        "    • Sixes: Sum of all sixes.\n"
        "  Bonus: If the total score in the Upper Section is 63 or more, the\n"
        "    player receives a 35-point bonus.\n\n"
        "  Lower Section:\n"
        "    • Three of a Kind: At least three dice of the same number.\n"
        "      Score is the sum of all dice.\n"
        "    • Four of a Kind: At least four dice of the same number.\n"
        "      Score is the total of all dice.\n"
        "    • Full House: Three of one number and two of another. Score is 25 points.\n"
        "    • Small Straight: A sequence of four consecutive numbers.\n"
        "      Score is 30 points.\n"
        "    • Large Straight: A sequence of five consecutive numbers.\n"
        "      Score is 40 points.\n"
        "    • Yahtzee: Five dice of the same number. Score is 50 points.\n"
        "    • Chance: Any combination of dice. Score is the sum of all dice.\n"
        "    • Yahtzee Bonus: If a player rolls a Yahtzee when the Yahtzee\n"
        "      category has been filled, they can fill in the upper section\n"
        "      category with the corresponding number. If that category has\n"
        "      already been filled, they can pick any lower section category.\n"
        "      If the Yahtzee category had already been filled with a score\n"
        "      of 50, they can add an additional 100 points.\n\n"
        "End of the Game:\n"
        "  The game ends after 13 rounds."
    )
    rules_details = tk.Label(
        root,
        text=rules_text,
        font=("Arial", 12),
        fg="black",
        bg="white",
        justify="left",
        anchor="nw",
    )
    rules_details.place(x=550, y=150, width=500, height=600)  # Increased width

    # Tips Section
    tips_label = tk.Label(
        root,
        text="Tips:",
        font=("Arial", 20, "bold"),
        fg="black",
        bg="white",
        anchor="w",
    )
    tips_label.place(x=1100, y=100)

    tips_text = (
        "Adjust your risk based on your position:\n"
        "  • If you're significantly behind, take more risks, and aggressively\n"
        "    aim for the higher scoring categories, even if the odds are lower,\n"
        "    because you have less to lose and more to gain. However, if you're\n"
        "    significantly ahead, play conservatively by focusing on securing\n"
        "    safe, consistent points, rather than risking low-chance combinations.\n"
        "    This can help you maintain your lead without jeopardising your\n"
        "    position.\n\n"
        "Prioritise the upper section early:\n"
        "  • Focus on scoring high in the upper section early in the game. Aim\n"
        "    to secure the upper bonus, as it can make a big difference in your\n"
        "    final score.\n\n"
        "Be strategic with your Yahtzee rolls:\n"
        "  • Don’t always aim for a Yahtzee unless it’s a high probability.\n"
        "    Instead, use your rolls to fill out other categories.\n\n"
        "Use the chance category wisely:\n"
        "  • The chance category can be a lifesaver for bad rolls or when you\n"
        "    have a mix of numbers that don't fit other categories. Save it for\n"
        "    when you can’t fill another category effectively.\n\n"
        "Know When to Take a Zero:\n"
        "  • Sometimes, it’s better to take a zero in a difficult category like\n"
        "    Yahtzee, rather than wasting good rolls on trying to fill it. This\n"
        "    allows you to maximise your points in other categories instead of\n"
        "    chasing an unlikely outcome."
    )
    tips_details = tk.Label(
        root,
        text=tips_text,
        font=("Arial", 12),
        fg="black",
        bg="white",
        justify="left",
        anchor="nw",
    )
    tips_details.place(x=1100, y=150, width=500, height=600)


# Create root details
root = tk.Tk()  # Create the root window once
root.title("Yahtzee")
root.geometry("800x500")
root.configure(bg="white")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: switch_fullscreen(root, is_full_screen))
        
home(root)