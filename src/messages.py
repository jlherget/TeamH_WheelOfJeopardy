import woj

# Start Message:
# ------------------------------------------
# numPlayers: Number of players playing the game
# list_categories: a list of 6 data structures, one representing each category (includes category name, questions, and answers)
# Message sent from start screen to main app to tell the game has started


class StartMessage():
    def __init__(self, numPlayers, list_categories):
        self.numPlayers = numPlayers
        self.list_categories = list_categories

    def run(self, target):
        print("Running StartMessage: (numPlayers=", self.numPlayers, ")")
        target.current_screen = woj.WoJ.BOARD_SCREEN

    def getNumPlayers(self):
        return self.numPlayers

    def getListCategories(self):
        return self.list_categories


# Create Message:
# ------------------------------------------
# Message sent from App to sub classes to tell to build initial board setup


class CreateMessage():
    def run(self, target):
        print("Running CreateMessage")


# SpinIn Message:
# ------------------------------------------
# Message for wheel to start spin


class SpinInMessage():
    def run(self, target):
        print("Running SpinInMessage from queue")

# SpinOut Message:
# ------------------------------------------
# out_id: The id for the result of the wheel spin:
#	- 0-5: The 6 categories of questions
#	- 6: Player's Choice
#	- 7: Opponents' Choice
#	- 8: Lose Turn
# 	- 9: Free Turn
#	- 10: Bankrupt
#	- 11: Double Your Score
# Message for result of wheel spin


class SpinOutMessage():
    def __init__(self, out_id):
        self.out_id = out_id

    def run(self, target):
        print("Running SpinOutMessage; sending out to app: (out_id=", self.out_id, ")")
        print("SENDING APP TO BOARD MESSAGE")
        target.board_screen.PostMessage(AppToBoardMessage(6, target.num_players, False))
        target.wheelTurn = False

    def getOutId(self):
        return self.out_id


# Initial Questions Message:
# ------------------------------------------
# list_categories: a list of 6 data structures, one representing each category (includes category name, questions, and answers)
# Message sent from  main app to board to tell the list of questions for the game


class InitialQuestionsMessage():
    def __init__(self, list_categories):
        self.numPlayers = numPlayers
        self.list_categories = list_categories

    def run(self, target):
        print("Running InitialQuestionsMessage: (numPlayers=", self.numPlayers,
              ")")

    def getNumPlayers(self):
        return self.numPlayers

    def getListCategories(self):
        return self.list_categories


# App to Board Message:
# ------------------------------------------
# category: The number category (int) that was chosen from the spin wheel
#	- 0-5: Of the 6 normal categories
#	- 6: Player's Choice
#	- 7: Opponents' Choice
# player_number: The player number who is answering
# free_token: boolean telling if player_number has a free turn token
# Message sent from  main app to board to tell which category is being asked, the player number, and if they have a free token


class AppToBoardMessage():
    def __init__(self, category, player_number, free_token):
        self.category = category
        self.player_number = player_number
        self.free_token = free_token

    def run(self, target):
        print("Running AppToBoardMessage: (category=", self.category, ")")
        target.wheelTurn = False
        print("SENDING QUESTION INFO TO GUI; CLICK SPACEBAR TO REPRESENT ANSWERING A QUESTION; OR TAB TO BE OUT OF QUESTIONS")
        target.board_screen.PostMessage(BoardToQuestionMessage("What's your name?", "Justin", 1, True, 1000)) 

    def getCategory(self):
        return self.category

    def getPlayerNumber(self):
        return self.player_number

    def getFreeToken(self):
        return self.free_token


# Out of Questions Message:
# ------------------------------------------
# Tells when the board is out of questions
# Message for result of wheel spin


class OutOfQuestionsMessage():
    def run(self, target):
        print("Running OutOfQuestionsMessage")


# Board to Question Message:
# ------------------------------------------
# q_text: Text of the question
# q_answer: Answer of the question
# player_number: Player number that is answering
# free_token: does player have free token
# value: question value
# Message sent from board to question to tell information regarding question and player


class BoardToQuestionMessage():
    def __init__(self, q_text, q_answer, player_number, free_token, value):
        self.q_text = q_text
        self.q_answer = q_answer
        self.player_number = player_number
        self.free_token = free_token
        self.value = value

    def run(self, target):
        print("Running BoardToQuestionMessage: (q_text=", self.q_text, ")")

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
# result: boolean if the player got it right or wrong
# net_amount: net amount to be added to the player's score
# player_number: player number who answered question
# free_token_used: boolean if the player used their free token
# Message for results of how the question was answered


class QuestionsResultMessage():
    def __init__(self, result, net_amount, player_number, free_token_used):
        self.result = result
        self.net_amount = net_amount
        self.player_number = player_number
        self.free_token_used = free_token_used

    def run(self, target):
        print("Running QuestionsResultMessage: (result=", self.result, "), (net_amount=", self.net_amount, "), (player #=", self.player_number, "), (free_token=", self.free_token_used, ")")
        print("QUESTION ANSWERED, PRESS SPACE TO SPIN THE WHEEL") 
        target.wheelTurn = True

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
# Universal Message telling game to reset to original values and go to start screen


class RestartMessage():
    def run(self, target):
        print("Running RestartMessage")
        target.startUp = True
        target.boardWheelUp = False
        target.questionUp = False

# Kill Message:
# ------------------------------------------
# Message telling a view to terminate


class KillMessage():
    def run(self, target):
        print("Running KillMessage against ", target)
        target.running = False


# Kill App Message:
# ------------------------------------------
# Message is sent to the app and cleans up all threads and causes an exit


class KillAppMessage():
    def run(self, target):
        print("Running KillAppMessage against ", target)
        doom = KillMessage()
        target.start_screen.PostMessage(doom)
        target.board_screen.PostMessage(doom)
        target.question_screen.PostMessage(doom)
        target.wheel_screen.PostMessage(doom)
        target.running = False
        
        
class EditMessage():
    def run(self, target):
        print("Edit")
        target.current_screen = woj.WoJ.EDIT_SCREEN
        
        
class SaveMessage():
    def run(self, target):
        print("Saved")
        target.current_screen = woj.WoJ.START_SCREEN


# Test Message:
# ------------------------------------------
# Messages which demos the ablity to bounce between threads.


class TestMessage():
    def run(self, target):
        print("Running KillTestMessage against ", target)
        doom = KillAppMessage()
        target.PostMessage(doom)
