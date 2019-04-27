## 
#  This application keeps track of the household chores completed in a shared
#  house over a number of weeks.
#
#  Author: Ryan Sulit and Mohammed Hasan
#  Date: April 2019

from household_module import Household
from chores_list_module import ChoresList, Chore
from participants_list_module import Participants

## Constants used for validation

MENU_CHOICES = ['A', 'C', 'V', 'L', 'S', 'Q', 'E', 'W', 'R']

## Importing SQLite for database storage

import sqlite3
sqlite_file = 'chore_chart.db'  
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

## Creating tables within database file
c.execute('CREATE TABLE IF NOT EXISTS HouseData (house_name TEXT, person_num INTEGER, person_name TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS ChoreData (house_name TEXT, chore_num INTEGER, chore_name TEXT, chore_freq INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS ScoreLog (house_name TEXT, person_num INTEGER, person_name TEXT, chore_name TEXT, chore_score INTEGER DEFAULT 0)')

## Prints the menu for the application. 
#
def print_menu():
    menu_string = ("\n\nWelcome to Chore Chart:\n\n"
                 "\tAbout \t\t\t (A)\n"
                 "\tCreate Household \t (C)\n"
                 "\tEdit Household \t\n"
                 "\t  Add to Household\t (E)\n"
                 "\t  Remove from Household  (R)\n"
                 "\t  Wipe entire database\t (W)\n"
                 "\tView Household \t\t (V)\n"
                 "\tLog Chores Done \t (L)\n"
                 "\tShow Leaderboard \t (S) \n"
                 "\tQuit \t\t\t (Q)")
    print(menu_string)


## Prints a description of the application. 
#
#
def about() :
    about_string = ("\n\nWelcome to Chore Chart. "
                   "Chore Chart helps housemates (people sharing a house) "
                   "to keep a record of what needs doing every week and "
                   "who is doing it. The leaderboard shows who has earned "
                   "the most points for household tasks so far.\n")
    print(about_string)


##  Creates a new household using the information entered by the user.
#   @param all_households a list of household objects
#
#
def create_household(all_households) :
    new_household_name = get_household_name()
    found = False
    household_obj = household_exists(new_household_name, all_households)
    
    if  household_obj == None:
        members_set = get_participants_names(new_household_name)
        chores_set = get_chores(new_household_name, members_set)
        household_obj = Household(new_household_name, members_set, chores_set)
        all_households.append(household_obj)        
        
    else:
       print("Household {} already exists, returning to the menu."
              .format(new_household_name))
 
    return 

##  Checks whether a household with a given name exists in the list of households.
#
#   @param all_households a list of household objects
#   @param household_name the household name to check
#   @return the household object if the household exists and None if it does not.
#
#
def household_exists(new_household_name, all_households) :
    h_obj = None

    c.execute('SELECT DISTINCT house_name FROM HouseData')
    allRows = c.fetchall()
    
    existing_households = []
    for item in allRows:
        existing_households.append(item[0])
        
    for household in existing_households:
        if household == new_household_name :
            h_obj = household

    return h_obj
        

##  Prompts the user for a household name and checks that the name is
#   reasonable.
#   @return a string containing the household name.
#
#   Invariants: a household name must be between the minimum and maximum length
#               and cannot be blank. The name must contain only alphanumeric
#               characters. 
#           
def get_household_name() :
    
    household_name = ""
    valid = False
    
    while not valid:
        household_name = input("\n\tEnter household name: ")
        try:
            Household.is_valid_name(household_name)
            valid = True
        except ValueError as err:
            print(err)

    return household_name


##  Prompts the user for the chore frequency and validates the number.
#   @return the chore frequency.
#
#   Invariants: the frequency must be between the minimum and maximum frequency.
#
def get_chore_frequency() :

    valid = False
    chore_frequency = 0
    
    
    while not valid :
        chore_frequency = input("\n\t\tTimes per week: ")
        try :
            Chore.is_valid_frequency(chore_frequency)
            valid = True
        except (TypeError, ValueError) as err:
            print(err)

    return int(chore_frequency)


##  Gets the names for the people in the household and stores them in a set
#   In addition, stores information into a database file
#   Invariants: duplicate names are not allowed
#
#   @return a set containing the names.
#
def get_participants_names(new_household_name):
    household_names = set()
    
    name = "AAA"    # dummy value so that we can start the while loop
    
    number_of_people = 1
    while name != "" :
        name = get_person_name(number_of_people)
 
        if name == "" :
            try :
                Participants.is_valid_length(household_names)
            except ValueError as err:
                print(err)
                name = "AAA"
        else:
            current_length = len(household_names)
            household_names.add(name)
            if current_length < len(household_names) :
                number_of_people = number_of_people + 1
            else:
                print(("\n\t\tSorry, you already have a household member called {}, " + \
                      "try again.").format(name))       
    
    #Storing to database
    houseTitleDB = new_household_name
    namesListDB = list(household_names)
    personNumberDB = range(len(namesListDB))
    for i in range(len(namesListDB)):
            c.execute("INSERT INTO HouseData (house_name, person_num, person_name) VALUES (?, ?, ?)", (houseTitleDB, int(personNumberDB[i])+1, namesListDB[i]))
    
    return household_names


##  Prompts the user for a person's name and validates it.
#   @param participant_number the number of participants entered so far.
#   @return a string containing the person's name.
#
#   Invariants: a person's name must be between the minimum and maximum length
#               and cannot be blank. The name must contain 
#               alphanumeric characters.
#
def get_person_name(participant_number) :
    
    # Finish when we have a valid answer which is either a blank or a valid name
    finish = False
    
    while not finish :
        person_name = input("\n\tEnter the name of participant {}: " \
                                    .format(participant_number)).strip()
        if is_blank(person_name) :
            finish = True
        else :
            try :
                Participants.is_valid_name_indiv(person_name)
                finish = True
            except ValueError as err:
                print(err)
                
    return person_name


##  Gets the chores. Stores chores into a set and a database file.
#
#   Invariants: duplicate chore names are not allowed,
#               names must consist of words which are alphanumeric characters,
#               names must >= the minimum valid length,
#               names must be <= the maximum valid length,
#               chore frequency must be >= the minimum frequency,
#               chore frequency must be <= the maximum frequency
#
#   @return a list containing chore objects.
#
def get_chores(new_household_name, members_set):

    chores_list = set()
    chores_frequency_list = set()
    chores_name_list = set()
    new_chore = "AAA"    # dummy value so that we can start the while loop
    number_of_chores = 0

    while new_chore != "" :
        new_chore = get_chore(number_of_chores + 1)
        if new_chore == "" :
            try :
                ChoresList.is_valid_length(chores_list)
            except ValueError as err:
                print(err)
                new_chore = "AAA"
        else:
            try :
                ChoresList.is_unique(new_chore, chores_list)
                chore_frequency = get_chore_frequency()
                chores_frequency_list.add(chore_frequency)
                chore_obj = Chore(new_chore, chore_frequency)
                chores_list.add(chore_obj)
                chores_name_list.add(new_chore)
                number_of_chores = number_of_chores + 1
                
            except ValueError as err :
                print(err)
    
    # Storing to database
    houseTitleDB = new_household_name
    namesListDB = list(members_set)
    personNumberDB = range(len(namesListDB))
    choresListDB = list(chores_name_list)
    choreNumberDB = range(len(choresListDB))
    choreFreqDB = list(chores_frequency_list)
    
    for i in range(len(choresListDB)):
        c.execute("INSERT INTO ChoreData (house_name, chore_num, chore_name, chore_freq) VALUES (?, ?, ?, ?)", (houseTitleDB, int(choreNumberDB[i])+1, str(choresListDB[i]), choreFreqDB[i]))
    
    for i in range(len(namesListDB)):
        for j in range(len(choresListDB)):
            c.execute("INSERT INTO ScoreLog (house_name, person_num, person_name, chore_name) VALUES (?, ?, ?, ?)", (houseTitleDB, int(personNumberDB[i])+1, namesListDB[i], str(choresListDB[j])))
    
    return chores_list 


##  Prompts the user for a chore name and validates it.
#   @param chore_number the number of chores entered so far.
#   @return a string containing the chore name.
#
#   Invariants: a chore name must be between the minimum and maximum length
#               and cannot be blank. The name must be composed of alphanumeric characters.
#
def get_chore(chore_number) :
    
    # A valid answer is either a blank or a valid name
    valid_answer = False
    
    while not valid_answer :

        chore_name = input("\n\tEnter the name of chore {}: ".format(chore_number))

        if chore_name == "" :
            valid_answer = True
        else : 
            try :
                Chore.is_valid_chore_name(chore_name)
                valid_answer = True
            except ValueError as err :
                print(err)
                
    return chore_name


##  Validates the option choice.
#
#   @return True or False
#
#   Invariants: The option must be a valid choice from MENU_CHOICES
#
def is_valid_option(option):
    if is_blank(option):
        return False
    elif option[0].upper() in MENU_CHOICES:
        return True
    else:
        return False

##  Checks whether a string contains only whitespace
#
#   @param any_string a string
#   @return True or False
#
#
def is_blank(any_string):
    test_str = "".join(any_string.split())
    if len(test_str) == 0:
        return True
    else :
        return False


##  View household.
#   @param all_households, a list of household objects
#
def view_household(all_households):
    #Obtain household name
    c.execute('SELECT DISTINCT house_name FROM HouseData')
    allRows = c.fetchall()
    
    householdPrintDB = []
    for item in allRows:
        householdPrintDB.append(item[0])
    
    print("\n \nHouseholds:")
    counter = 1
    for i in range(len(householdPrintDB)):
        print("\t " + str(counter) + ". " + householdPrintDB[i])
        counter += 1
    
    
    input_household = input("\nEnter the desired household name: ")
    chosen_household = household_exists(input_household, all_households)
    
    #Validation of input
    if chosen_household == None:        
        print("Household {} does not exist, returning to the menu.".format(input_household))
    else:
        #Obtain participant list
        c.execute('SELECT * FROM HouseData WHERE house_name=?', (chosen_household,))
        allRows = c.fetchall()

        namePrintingDB = []
        for item in allRows:
            namePrintingDB.append(item[2])

        print("\nHousehold: " + input_household)
        print("\nParticipants:")
        counter = 1
        for i in range(len(namePrintingDB)):
            print("\t " + str(counter) + ". " + namePrintingDB[i])
            counter += 1

        #Obtain chore list incl. frequency
        c.execute('SELECT * FROM ChoreData WHERE house_name=?', (chosen_household,))
        allRows = c.fetchall()

        chorePrintingDB = []
        for item in allRows:
            chorePrintingDB.append(item[2])
        chorefreqPrintingDB = []
        for item in allRows:
            chorefreqPrintingDB.append(item[3])

        print("\n \nWeekly Chores:")
        counter = 1
        for i in range(len(chorePrintingDB)):
            print("\t " + str(counter) + ". " + chorePrintingDB[i] + " (" + str(chorefreqPrintingDB[i]) + ")")   
            counter += 1

    return    
  

##  Log chores. Contains part of the view_household 
# @param all_households, a list of household objects
#
def log_chores(all_households):
    #Obtain household name
    c.execute('SELECT DISTINCT house_name FROM HouseData')
    allRows = c.fetchall()
    
    householdPrintDB = []
    for item in allRows:
        householdPrintDB.append(item[0])
    
    print("\n \nHouseholds:")
    counter = 1
    for i in range(len(householdPrintDB)):
        print("\t " + str(counter) + ". " + householdPrintDB[i])
        counter += 1
    
    
    input_household = input("\nEnter the desired household name: ")
    chosen_household = household_exists(input_household, all_households)
    
    #Validation of input
    if chosen_household == None:        
        print("Household {} does not exist, returning to the menu.".format(input_household))
    else:
        #Obtain participant list
        c.execute('SELECT * FROM HouseData WHERE house_name=?', (chosen_household,))
        allRows = c.fetchall()

        namePrintingDB = []
        for item in allRows:
            namePrintingDB.append(item[2])

        print("\nHousehold: " + input_household)
        print("\nParticipants:")
        counter = 1
        for i in range(len(namePrintingDB)):
            print("\t " + str(counter) + ". " + namePrintingDB[i])
            counter += 1
    
        listNumberDB=int(input("\nEnter the participant number: "))
        
        print("\nYou are logging " + namePrintingDB[listNumberDB-1] + "'s chores.")
        
        c.execute('SELECT * FROM ChoreData WHERE house_name=?', (chosen_household,))
        allRows = c.fetchall()
        
        chorePrintingDB = []
        for item in allRows:
            chorePrintingDB.append(item[2])
        
        print("\n \nWeekly Chores:")
        counter = 1
        for i in range(len(chorePrintingDB)):
            print("\t " + str(counter) + ". " + chorePrintingDB[i])
            counter += 1
        
        chorelistNumberDB = int(input("\nEnter the chore number: "))
        
        scorePrinting = []
        c.execute('SELECT chore_score FROM ScoreLog WHERE house_name=? AND person_name=? AND chore_name=? ', (chosen_household, namePrintingDB[listNumberDB-1], chorePrintingDB[listNumberDB-1]))
        allRows = c.fetchall()
        for item in allRows:
            scorePrinting.append(item[0])
        
        print("\n{} has done {} {} times.".format(namePrintingDB[listNumberDB-1], chorePrintingDB[chorelistNumberDB-1], scorePrinting[0]))
        
        moreTimes = int(input("\nHow many more times has {} done {}:".format(namePrintingDB[listNumberDB-1], chorePrintingDB[chorelistNumberDB-1])))
        updatedScore = scorePrinting[0] + moreTimes
        print("\n{} has done {} {} more times.".format(namePrintingDB[listNumberDB-1], chorePrintingDB[chorelistNumberDB-1], str(updatedScore)))
        
        #Update database
        c.execute('UPDATE ScoreLog SET chore_score=? WHERE house_name=? AND person_name=? AND chore_name=? ', (updatedScore, chosen_household, namePrintingDB[listNumberDB-1], chorePrintingDB[chorelistNumberDB-1]))
    return  


##  Show the leaderboard for a house.
# @param all_households, a list of household objects
#
def show_leaderboard(all_households):
    #Obtain household name
    c.execute('SELECT DISTINCT house_name FROM HouseData')
    allRows = c.fetchall()
    
    householdPrintDB = []
    for item in allRows:
        householdPrintDB.append(item[0])
    
    print("\n \nHouseholds:")
    counter = 1
    for i in range(len(householdPrintDB)):
        print("\t " + str(counter) + ". " + householdPrintDB[i])
        counter += 1
    
    
    input_household = input("\nEnter the desired household name: ")
    chosen_household = household_exists(input_household, all_households)
    
    #Validation of input
    if chosen_household == None:        
        print("Household {} does not exist, returning to the menu.".format(input_household))
    else:
        c.execute('SELECT * FROM HouseData WHERE house_name=? ', (chosen_household,))
        allRows = c.fetchall()
        
        namePrintingDB = []
        for item in allRows:
            namePrintingDB.append(item[2])
        
        for i in range(len(namePrintingDB)):
            print(namePrintingDB[i]+":")
            allRows=[]
            c.execute('SELECT * FROM ScoreLog WHERE house_name=? AND person_name=?', (chosen_household, namePrintingDB[i]))
            allRows = c.fetchall()
            allChores=[]
            allScores=[]
            for item in list(allRows):
                allScores.append(item[4])
                allChores.append(item[3])
            for j in range(len(allScores)):
                print("\t" + str(allChores[j]) + "    (" + str(allScores[j]) + ")")
    
    return



## Add to a household (whether participants or chores)
#  @param all_households
#  
def addto_household(all_households):
    new_household_name = get_household_name()
    found = False
    household_obj = household_exists(new_household_name, all_households)
    
    if  household_obj == None:
        print("Household {} does not exist, returning to the menu."
              .format(new_household_name))
    else:
        members_set = get_participants_names(new_household_name)
        chores_set = get_chores(new_household_name, members_set)
        household_obj = Household(new_household_name, members_set, chores_set)
        all_households.append(household_obj)        
        print("\nCurrently Existing Households: ")
        print([Household.household_name for Household in all_households])
    return 

## Wipe the database of all households.
#  @param all_households
#  
def wipe_households(all_households):
    wipe=input("Are you sure you want to remove all data? \nEnter <w> to wipe, otherwise input any other character: ")

    if wipe.lower()=="w":
        c.execute("DELETE from HouseData")
        c.execute("DELETE from ScoreLog")
        c.execute("DELETE from ChoreData")
        print("\nData has been wiped.")
    else:
        print("\nData has not been wiped.")

## Remove participants or chores from a household
#  @param all_households
#  
def remove_household(all_households):
    view_household(all_households)
    
    
    
    removalPrompt = str(input("\nRemove participant (P), chore (C) or both(B):"))
    
    if removalPrompt == 'P':
        removalName=str(input("\nEnter the name of the participant you would like to remove: "))
        remove_participant(removalName)
        
    elif removalPrompt == 'C':
        removalChore=input("\nEnter the name of the chore you would like to remove: ")
        remove_participant(removalChore)
    elif removalPrompt == 'B':
        removalName=str(input("\nEnter the name of the participant you would like to remove: "))
        removalChore=input("\nEnter the name of the chore you would like to remove: ")
        remove_participant(removalName)
        remove_chore(removalChore)
    else:
        print("Invalid input.")

## Remove participant from household
#
def remove_participant(removalName):
    c.execute("DELETE from HouseData where person_name=?", (removalName,))
    c.execute("DELETE from ScoreLog where person_name=?", (removalName,))
    print(removalName + " has been removed from the household.")

## Remove chore from household
#
def remove_chore(removalChore):
    c.execute("DELETE from ChoreData where chore_name=?", (removalChore,))
    c.execute("DELETE from ScoreLog where chore_name=?", (removalChore,))
    print(removalChore + " has been removed from the household.")
        
        
##  Prints the menu, prompts the user for an option and validates the option.
#
#   @return a character representing the option.
#
def get_option():  
    option = '*'
    
    while is_valid_option(option) == False:
        print_menu()
        option = input("\nEnter an option: ")
   
    return option.upper()


## The menu is displayed until the user quits
# 
def main() :
    global c
    global conn
    global sqlite_file
    all_households = []   
    option = '*'
    
    while option != 'Q':
        option = get_option()        
        if option == 'A':
            about()
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'C':
            create_household(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'E':
            addto_household(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'W':
            wipe_households(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'R':
            remove_household(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'V':
            view_household(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'L':
            log_chores(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
        elif option == 'S':
            show_leaderboard(all_households)
            returnMenu = input("\nPress Enter to return to menu:")
    
    conn.commit()
    conn.close()
    print("\n\nBye, bye.")

        
# Start the program
if __name__ == "__main__":
    main()