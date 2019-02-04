#Course: COMP0015 Introduction to Programming
#Instructor: Rae Harbird
#Date: 05/02/2019
#Name:choreChartCoursework.py
#Description: Coursework Deliverable 1 - Main Menu and Create a Household
#Author(s): Ryan Sulit Velasquez (ID:17018087), Mohammed Hasan (ID:17014291)

import sys
import time               
import textwrap           #Use in descriptions

########################################################################################
# about()
# This function gives the description of the application itself, using
# the textwrap module to fit the window.
# Input: None.
# Returns: Written text (ie. description)
def about():                            
    textAbout = ("Welcome to the ChoreBoard! The purpose of this application is to " +
             "aid housemates in keeping a record of which chores need doing and to " +
             "assign who does each specific chore.")
    print("")
    for line in textwrap.wrap(textAbout, width=50):
        print(line)
    time.sleep(1)
    menuReturn=input("\nPress <Enter> to return to the main menu:")

########################################################################################
# creating()
# This function allows the user to input certain details, such as household name, participant
# name, chore name, and chore frequencies within a text file.
# Inputs: Names/Frequencies/etc.
# Returns: Certain strings(chores, household, participant, etc.)
def creating():
    household=str(input("\nEnter your household's name: "))
    textHousehold=open(household+'.txt','w')
    textHousehold.write("\n"+household+"\n")
    print("Enter participant's names:" + "")
    print("")

    textHousehold.write("\nParticipants:")
    members=True
    counter=1
    while str(members) != "":
        members=str(input("\tEnter the name of participant " + str(counter) + ": "))
        if str(members) != "":
            textHousehold.write("\n\t" + str(counter) + ". "  + members)
            counter += 1
    
    print("\n" + "Enter chores:")
    textHousehold.write("\n"+"\nWeekly Chores:")
    chores=True
    counter=1
    while str(chores) != "":
        chores=str(input("\tChore " + str(counter) + ": "))
        if chores != "":
            while True:
                    try:
                        choreFreq=int(input("\t\tTimes per week: "))
                        while choreFreq < 0:
                            print("Enter a positive frequency.")
                            choreFreq=int(input("\t\tTimes per week: "))
                        textHousehold.write("\n\t" + str(chores) + " (" + str(choreFreq) + ")")
                        counter += 1
                        break
                    except ValueError:
                        print("Please enter a number.")
    else:
        time.sleep(1)
        menuReturn=input("\nPress <Enter> to return to the main menu:")

########################################################################################
# view()
# This function allows the user to view previous inputs created by creating().
# Input: None.
# Returns: Inputs inside creating()
def view():
    searchHousehold=str(input("Enter the household you would like to view: "))
    try:
        textHousehold=open(searchHousehold+'.txt','r')
        textContents=textHousehold.read()
        print(textContents)
        
        
    except:
        print("\n\tThe household you have entered does not exist.")
    
    time.sleep(1)
    menuReturn=input("\nPress <Enter> to return to the main menu:")
########################################################################################
# log()
# This function allows the user to view the log of chores done / completed.
# Input: None.
# Returns: n/a
def log():
    print("\n\tChore logging still pending.")
    time.sleep(1)
    menuReturn=input("\nPress <Enter> to return to the main menu:")

########################################################################################
# scores()
# This function allows the user to view leaderboard of scores.
# Input: None.
# Returns: n/a
def scores():
    print("\n\tScoreboard still pending.")
    time.sleep(1)
    menuReturn=input("\nPress <Enter> to return to the main menu:")
########################################################################################
# quit()
# This function allows the user quit the application.
# Input: None.
# Returns: System exit.
def quit():
    menuLoop=False
    print("\n\tThank you for using ChoreBoard!")
    time.sleep(1)
    sys.exit(0)

########################################################################################
# main()
# This is the main function of the application, where all of the previous functions are used.
# The main() function is what runs when the .py file is initialised.
# Input: None.
# Returns: System exit.
def main():
    
    menuLoop=True

    while menuLoop:
        print("\n"+"Welcome to the ChoreBoard!")
        menuOption = str(input("\n\n\tAbout [A]"
          "\n\tCreate Household [C]"
          "\n\tView Household [V]"
          "\n\tLog Chores Done [L]\n\t"
          "Show Leaderboard [S]"
          "\n\tQuit [Q]"
          "\n\tSelect an option and press <Enter>:"))

        if menuOption.lower() == "a":                        #Accepts lower-/upper-case
            about()
            

        elif menuOption.lower() == "c":
            creating()

        elif menuOption.lower() == "v":
            view()

        elif menuOption.lower() == "l":
            log()

        elif menuOption.lower() == "s":
            scores()

        elif menuOption.lower() == "q":
            quit()

        else:
            print("\n\tInvalid input. Try again.")

if __name__ == "__main__" :
    main()
