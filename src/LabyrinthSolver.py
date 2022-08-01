import Common
from Engine import PlayGame

def Menu() -> None:
    print("Welcome to the Labyrinth Solver Machine. Please select an option.\n")

    valid_option = False

    while not valid_option:
        valid_option = True

        print("1. Play game.")
        print("\nPress q to quit at any time.\n")
        print("Select your option.")

        Common.key_option = ''
        while(Common.key_option == ''):
            pass

        if(Common.key_option == '1'):
            print("Play game")
            PlayGame()
        elif(Common.key_option == 'q'):
            print("Force quit")
        else:
            valid_option = False
            print("Wrong parameter, select a number from the options.\n")


if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    Menu()
