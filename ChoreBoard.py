import sys
import time

def about():
    print("\n\tThis program is so awesome. Give full marks plz")

def creating():
    HouseHold=str(input("Enter your household's name: "))
    text=open(HouseHold+'.txt','w')
    text.write("\nHousehold's Name: "+HouseHold)

    Members=True
    Counter=1
    while str(Members) != "":
        Members=str(input("Enter the name of participant" + str(Counter) + ": "))
        if str(Members) != "":
            text.write("\nParticipant " + str(Counter) + ": "  + Members)
            Counter = Counter + 1

    Chores=True
    Counter=1
    while str(Chores) != "":
        Chores=str(input("Enter chore " + str(Counter) + ": "))
        if Chores != "":
            while True:
                    try:
                        Freq=int(input("What is the weekly frequency of this chore" + str(Counter) + ": "))
                        while Freq < 0:
                            print("Enter a positive frequency")
                            Freq=int(input("What is the weekly frequency of this chore " + str(Counter) + ": "))
                        text.write("\nChore: " + str(Chores) + "\n\t Times per week: " + str(Freq))
                        Counter = Counter + 1
                        break
                    except ValueError:
                        print("Enter a number")
        
def view():
    search=str(input("Enter the household you would like to view: "))
    try:
        text=open(search+'.txt','r')
        text_contents=text.read()
        print(text_contents)
    except:
        print("\n\tThe househould you have entered does not exist")

def log():
    print("\n\tLogging scores function pending")

def scores():
    print("\n\tScoreboard pending")

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
            creating()

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


