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

print("Welcome to the ChoreBoard m80"
      "\n\n\n\tAbout [A]"
      "\n\tCreate Household [C]"
      "\n\tView Household [V]"
      "\n\tLog Chores Done [L]\n\t"
      "Show Leaderboard [S]"
      "\n\tQuit [Q]")

MenuLoop=True

while MenuLoop:
    MenuOption = str(input("\n\tSelect an option and press <Enter>:"))

    if MenuOption.lower() == "a":
        about()

    if MenuOption.lower() == "c":
        create()

    if MenuOption.lower() == "v":
        view()

    if MenuOption.lower() == "l":
        log()

    if MenuOption.lower() == "s":
        scores()

    if MenuOption.lower() == "q":
        quit()












