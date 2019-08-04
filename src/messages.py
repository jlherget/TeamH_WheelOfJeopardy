# Create Message:
# ------------------------------------------
# Message sent from App to sub classes to tell to build initial board setup


class CreateMessage():
    def run(self, target):
        print("Running CreateMessage")

# Question Result Message:
# ------------------------------------------
# result: boolean if the player got it right or wrong
# net_amount: net amount to be added to the player's score
# player_number: player number who answered question
# free_token_used: boolean if the player used their free token
# Message for results of how the question was answered


class QuestionsResultMessage():
    def __init__(self, result, net_amount, free_token_used, questions_left):
        self.result = result
        self.net_amount = net_amount
        self.free_token_used = free_token_used
        self.questions_left = questions_left

    def getResult(self):
        return self.result

    def getNetAmount(self):
        return self.net_amount

    def getQuestionsLeft(self):
        return self.questions_left

    def getFreeTokenUsed(self):
        return self.free_token_used


# Restart Message:
# ------------------------------------------
# Universal Message telling game to reset to original values and go to start screen


class RestartMessage():
    def run(self, target):
        print("Running RestartMessage")
        target.current_screen = target.start_screen
        target.game_over = False

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
        target.game_screen.PostMessage(doom)
        target.editor_screen.PostMessage(doom)
        target.running = False


class EditMessage():
    def run(self, target):
        print("Running EditMessage")
        target.current_screen = target.editor_screen


class SaveMessage():
    def run(self, target):
        print("Running SaveMessage")
        target.current_screen = target.start_screen


# Test Message:
# ------------------------------------------
# Messages which demos the ablity to bounce between threads.


class TestMessage():
    def run(self, target):
        print("Running KillTestMessage against ", target)
        doom = KillAppMessage()
        target.PostMessage(doom)
