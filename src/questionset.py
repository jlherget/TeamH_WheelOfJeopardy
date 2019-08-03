class GameSet():

    def __init__(self):
        self.roundSet = []

    def addRound(self, roundQSet):
        self.roundSet.append(roundQSet)

    def getRound(self, round_num):
        return self.roundSet[round_num]

class RoundSet():
    def __init__(self):
        self.category = []
    
    def addCategory(self, category):
        self.category.append(category)


class CategorySet():

    def __init__(self, title):
        self.title = title
        self.question = []
        self.answer   = []
        self.q_count  = 0

    def addQuestionAndAnswer(self, question_text, answer_text):
        self.question.append(question_text)
        self.answer.append(answer_text)
        self.q_count += 1

class Question():

    def __init__(self, question_text, answer_text, value):
        self.question_text = question_text
        self.answer_text = answer_text
        self.value = value
