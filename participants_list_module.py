class Participants():
 
    ## Constants used for validation
    MINIMUM_NAME_LENGTH = 3     # Used to validate team member's name
    MAXIMUM_NAME_LENGTH = 10
    
    MINIMUM_HOUSEHOLD_SIZE = 2
    MAXIMUM_HOUSEHOLD_SIZE = 5

    ## Constructor for the set containing participant's names.
    # @param the_participants a set containing the names
    #              
    def __init__(self, the_participants) :
        self.participants = the_participants

    ## Return the participants' list.
    #          
    @property
    def participants(self):
        return self._participants


    ## Sets the participants' list attribute.
    #  @param name the participants set
    #  @exception ValueError raised if:
    #           - any of the names in the list are invalid
    #           - the set is too long or too short
    @participants.setter
    def participants(self, the_participants) :
        try :
            self.valid_participants(the_participants)
            self._participants = the_participants
        except ValueError as err :
            raise


    def __str__(self):
        participant_length = len(self.participants)
        i = 1
        participants_string = ""
        for participant in self.participants :
            participant_string = participant_string + str(participant)
            if i < participant_length :
                chore_string = chore_string + ", "
            i = i + 1
            
        return participants_string


    ## Check the set of participants.
    # Verifies that the set of partcipants is a valid length.
    # Verifies that each participants is valid.
    # 
    # @param the_participants the set of participants to be validated
    # @return True if the set conforms to the validation conditions
    #         and raise exception if it does not.
    #
    @staticmethod
    def  valid_participants(the_participants) :
        # check that the the_participants is a set
        if not isinstance(the_participants, set) :
            raise TypeError("List of particpants is not a set.")
        
        try :
            Participants.is_valid_length(the_participants)
            Participants.is_valid_name(the_participants)
        except ValueError as err :
            raise
        
        return True


    ## Check the name contains only alphanumeric characters and check that it is the right length.
    # 
    # @param name the string to be validated
    # @return True if the string conforms to the validation conditions and
    #           generate an exception if not.
    #
    @staticmethod
    def is_valid_name(name) :
        if len(name) < Participants.MINIMUM_NAME_LENGTH \
            or len(name) > Participants.MAXIMUM_NAME_LENGTH :
            raise ValueError(("Participant Name: {}, is not valid. It should be " +
                        "more than {} characters long " +
                        "and less than {} characters long.")
                .format(name, Participants.MINIMUM_NAME_LENGTH, Participants.MAXIMUM_NAME_LENGTH))
        
        str_name = str(name)
        if str_name.isalum():
            raise ValueError(("{}, is not valid. Names in the ParticipantList should be " +
                                  "alphanumeric.").format(letter))
    
        return True

    ## Check the number of participants in the set is the right length.
    # 
    # @return True if valid and generate an exception if not.
    #           
    @staticmethod        
    def is_valid_length(the_participants) :
        if len(the_participants) < Participants.MINIMUM_HOUSEHOLD_SIZE or \
            len(the_participants) > Participants.MAXIMUM_HOUSEHOLD_SIZE :
            raise ValueError (("\n\t\tThe number of participants in the household must be" +
                " be more than {} and less than {}.")
                .format(Participants.MINIMUM_HOUSEHOLD_SIZE - 1, Participants.MAXIMUM_HOUSEHOLD_SIZE + 1))
 
        # If we reached this point then the checks passed
        return True
    
    @staticmethod
    def is_valid_participant(the_participants) :
        for participant in the_participants :
            if not isinstance(participant, Participants) :
                raise TypeError ("The ParticipantList does not contain objects which are Participants.")
        # If we reached this point, the participants are valid.
        return True


## main method
#
# Contains some simple tests
#
def main():
    print("Test 1: Create a valid participants list")    
    try:
        names = set(["personA","personB","personC"])
        p1 = Participants(names)
        print("\n\tVALID: ", p1)
    except Exception as err:
        print("\tERROR: ", err)


    print("\nTest 2: Create a set of participants with the wrong data type: list")    
    try:
        names = ["personA","personB","personC"]
        p2 = Participants(names)
        print("\tVALID: ", p2)
    except Exception as err:
        print("\tERROR: ", err)

    print("\nTest 3: Create a set of participants which is too short")    
    try:
        names = set(["personA"])
        p2 = Participants(names)
        print("\tVALID: ", p2)
    except Exception as err:
        print("\tERROR: ", err)    
       
    print("\nTest 4: Create a set of participants which is too long")    
    try:
        names = set(["personA","personB","personC", "personD", "personE", "personF"])
        p = Participants(names)
        print("\tVALID: ", p)
    except Exception as err:
        print("\tERROR: ", err)   
    
    print("\nTest 5: Create a set of participants with invalid name, punctuation character")    
    try:
        names = set(["*","personB","personC"])
        p = Participants(names)
        print("\tVALID: ", p)
    except Exception as err:
        print("\tERROR: ", err)   

    print("\nTest 6: Create a set of participants with name too long")    
    try:
        names = set(["tooooooooolllllllooooooonnnnnggggg","personB","personC"])
        p = Participants(names)
        print("\tVALID: ", p)
    except Exception as err:
        print("\tERROR: ", err)  

if __name__ == "__main__":
    main()    