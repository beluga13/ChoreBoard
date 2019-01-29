import sys
import time

def about():
    print("\n\tThis program is so awesome. Give full marks plz")

def create():
    print("\n\tPending")

def view():
    print("\n\tPending")

def log():
    print("\n\tPending")

def scores():
    print("\n\tPending")

def quit():
    MenuLoop=False
    print("\n\tCya m8")
    time.sleep(1)
    sys.exit(0)


def main():
    print("Welcome to the ChoreBoard")

    MenuLoop=True

    while MenuLoop:
        MenuOption = str(input("\n\n\n\tAbout [A]"
          "\n\tCreate Household [C]"
          "\n\tView Household [V]"
          "\n\tLog Chores Done [L]\n\t"
          "Show Leaderboard [S]"
          "\n\tQuit [Q]"
            "\n\tSelect an option and press <Enter>:"))

        if MenuOption.lower() == "a":
            about()

        elif MenuOption.lower() == "c":
            create()

        elif MenuOption.lower() == "v":
            view()

        elif MenuOption.lower() == "l":
            log()

        elif MenuOption.lower() == "s":
            scores()

        elif MenuOption.lower() == "q":
            quit()
        else:
            print("\n\tInvalid input. Try again.")

main()
