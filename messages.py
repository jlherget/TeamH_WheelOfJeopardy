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
# Message sent from start screen to main app to tell the game has started

class StartMessage(Message):
    def __init__(self, numPlayers, list_categories):
        Message.__init__(self, 0)
        self.numPlayers = numPlayers
        self.list_categories = list_categories

    def getNumPlayers(self):
        return self.numPlayers

    def getListCategories(self):
        return self.list_categories

# Create Message:
# ------------------------------------------
# Unique ID 1
# Message sent from App to sub classes to tell to build initial board setup

class CreateMessage(Message):
    def __init__(self):
        Message.__init__(self, 1)

# SpinIn Message:
# ------------------------------------------
# Unique ID 2
# Message for wheel to start spin

class SpinInMessage(Message):
    def __init__(self):
        Message.__init__(self, 2)

# SpinOut Message:
# ------------------------------------------
# Unique ID 3
# out_id: The id for the result of the wheel spin:
#	- 0-5: The 6 categories of questions
#	- 6: Player's Choice
#	- 7: Opponents' Choice
#	- 8: Lose Turn
# 	- 9: Free Turn
#	- 10: Bankrupt
#	- 11: Double Your Score
# Message for result of wheel spin

class SpinOutMessage(Message):
    def __init__(self, out_id):
        Message.__init__(self, 3)
        self.out_id = out_id

    def getOutId(self):
        return self.out_id

# Initial Questions Message:
# ------------------------------------------
# Unique ID 4
# list_categories: a list of 6 data structures, one representing each category (includes category name, questions, and answers)
# Message sent from  main app to board to tell the list of questions for the game

class InitialQuestionsMessage(Message):
    def __init__(self, list_categories):
        Message.__init__(self, 4)
        self.numPlayers = numPlayers
        self.list_categories = list_categories

    def getNumPlayers(self):
        return self.numPlayers

    def getListCategories(self):
        return self.list_categories

# App to Board Message:
# ------------------------------------------
# Unique ID 5
# category: The number category (int) that was chosen from the spin wheel
#	- 0-5: Of the 6 normal categories
#	- 6: Player's Choice
#	- 7: Opponents' Choice
# player_number: The player number who is answering
# free_token: boolean telling if player_number has a free turn token
# Message sent from  main app to board to tell which category is being asked, the player number, and if they have a free token

class AppToBoardMessage(Message):
    def __init__(self, category, player_number, free_token):
        Message.__init__(self, 5)
        self.category = category
        self.player_number = player_number
        self.free_token = free_token

    def getCategory(self):
        return self.category

    def getPlayerNumber(self):
        return self.player_number
  
    def getFreeToken(self):
        return self.free_token

# Out of Questions Message:
# ------------------------------------------
# Unique ID 6
# out_id: The category id number that has run out of question. tells wheel not to pick that category anymore
# Message for result of wheel spin

class OutOfQuestionsMessage(Message):
    def __init__(self, out_id):
        Message.__init__(self, 6)
        self.out_id = out_id

    def getOutId(self):
        return self.out_id

# Board to Question Message:
# ------------------------------------------
# Unique ID 7
# q_text: Text of the question
# q_answer: Answer of the question
# player_number: Player number that is answering
# free_token: does player have free token
# value: question value
# Message sent from board to question to tell information regarding question and player

class BoardToQuestionMessage(Message):
    def __init__(self, q_text, q_answer, player_number, free_token, value): 
        Message.__init__(self, 7)
        self.q_text = q_text
        self.q_answer = q_answer
        self.player_number = player_number
        self.free_token = free_token
        self.value = value

    def getQText(self):
        return self.q_text

    def getQAnswer(self):
        return self.q_answer

    def getPlayerNumber(self):
        return self.player_number

    def getFreeToken(self):
        return self.free_token

    def getValue(self):
        return self.value

# Question Result Message:
# ------------------------------------------
# Unique ID 8
# result: boolean if the player got it right or wrong
# net_amount: net amount to be added to the player's score
# player_number: player number who answered question
# free_token_used: boolean if the player used their free token
# Message for results of how the question was answered

class QuestionsResultMessage(Message):
    def __init__(self, result, net_amount, player_number, free_token_used):
        Message.__init__(self, 8)
        self.result = result
        self.net_amount = net_amount
        self.player_number = player_number
        self.free_token_used = free_token_used

    def getResult(self):
        return self.result

    def getNetAmount(self):
        return self.net_amount

    def getPlayerNumber(self):
        return self.player_number

    def getFreeTokenUsed(self):
        return self.free_token_used

# Restart Message:
# ------------------------------------------
# Unique ID 9
# Universal Message telling game to reset to original values and go to start screen

class RestartMessage(Message):
    def __init__(self):
        Message.__init__(self, 9)

# Kill Message:
# ------------------------------------------
# Unique ID 10
# Universal Message telling game to terminate all threads

class KillMessage(Message):
    def __init__(self):
        Message.__init__(self, 10)

