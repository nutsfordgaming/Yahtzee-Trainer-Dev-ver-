if __name__ == '__main__':
    while True:
        program = input("Which program would you like to run? (0 for the state analysis, 1 for the state analysis testing and 2 for the main program): ")
        if program == '0':
            # Imports, runs and deletes the state analysis
            import state_analysis_code as analyse
            analyse
            
        elif program == '1':
            # Imports, runs and deletes the state analysis testing
            import state_analysis_testing as test
            test

        elif program == '2':
            # Imports, runs and deletes the main program
            import main_program as run
            run

        else:
            # Handling if the user inputs an incorrect code
            print ("You did not enter the correct code to run a program. Try again.")

# Code is untraditionally imported in the conditions and deleted after to prevent excess storage being used for a program that isn't running