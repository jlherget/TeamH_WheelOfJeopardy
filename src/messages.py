# Question Result Message:
# ------------------------------------------
# result:           boolean if the player got it right or wrong
# net_amount:       net amount to be added to the player's score
# free_token_used:  boolean if the player used their free token
# questions_left:   number of questions left in the board
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