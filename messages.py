# Message Class
# ------------------------------------------
# id: Unique id for each message type

class Message:
    def __init__(self, id):
        self.id = id 
    def getMessageId(self):
        return self.id

# Start Message:
# ------------------------------------------
# Unique ID 0
# numPlayers: Number of players playing the game
# list_categories: a list of 6 data structures, one representing each category (includes category name, questions, and answers)

class StartMessage(Message):
    def __init__(self, numPlayers, list_categories):
        Message.__init__(self, 0)
        self.numPlayers = numPlayers
        self.list_categories = list_categories

    def getNumPlayers(self):
        return self.numPlayers

    def getListCategories(self):
        return self.list_categories
