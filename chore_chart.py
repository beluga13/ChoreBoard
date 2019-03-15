## 
#  This application keeps track of the household chores completed in a shared
#  house over a number of weeks.
#
#  Author: Rae Harbird
#  Date: December 2019

from household_module import Household
from chores_list_module import ChoresList, Chore
from participants_list_module import Participants

## Constants used for validation

MENU_CHOICES = ['A', 'C', 'V', 'L', 'S', 'Q']

## Prints the menu for the application. 
#
def print_menu():
    menu_string = ("\n\nWelcome to Chore Chart:\n\n"
                 "\tAbout \t\t\t(A)\n"
                 "\tCreate Household \t(C)\n"
                 "\tView Household \t\t(V)\n"
                 "\tLog Chores Done \t(L)\n"
                 "\tShow Leaderboard \t(S) \n"
                 "\tQuit \t\t\t(Q)")
    print(menu_string)


## Prints a description of the application. 
#
#
def about() :
    about_string = ("\n\nWelcome to Chore Chart. "
                   "Chore Chart helps housemates (people sharing a house) "
                   "to keep a record of what needs doing every week and "
                   "who is doing it. The leaderboard shows who has earned "
                   "the most points for household tasks so far\n")
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
        members_set = get_participants_names()
        chores_set = get_chores()
        household_obj = Household(new_household_name, members_set, chores_set)
        all_households.append(household_obj)
        print(all_households)
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

    for household in all_households :
        if household.household_name == new_household_name :
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
#
#   Invariants: duplicate names are not allowed
#
#   @return a set containing the names.
#
def get_participants_names():
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
                Participants.is_valid_name(person_name)
                finish = True
            except ValueError as err:
                print(err)
                
    return person_name


##  Gets the chores.
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
def get_chores():

    chores_list = set()
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
                chore_obj = Chore(new_chore, chore_frequency)
                chores_list.add(chore_obj)
                number_of_chores = number_of_chores + 1
                
            except ValueError as err :
                print(err)

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
# @param all_households, a list of household objects
#
def view_household(all_households):

    print("Not implemented yet")
    
    return    


##  Log chores.
# @param all_households, a list of household objects
#
def log_chores(all_households):
    
    print("Not implemented yet.")
        
    return    


##  Show the leaderboard for a house.
# @param all_households, a list of household objects
#
def show_leaderboard(all_households):
    print("Not implemented yet.")

    return 


    
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
    
    all_households = []   
    option = '*'
    
    while option != 'Q':
        option = get_option()        
        if option == 'A':
            about()
        elif option == 'C':
            create_household(all_households)
        elif option == 'V':
            view_household(all_households)
        elif option == 'L':
            log_chores(all_households)
        elif option == 'S':
            show_leaderboard(all_households)
            # print("\n\tNot implemented yet.\n")

    print("\n\nBye, bye.")

        
# Start the program
if __name__ == "__main__":
    main()



