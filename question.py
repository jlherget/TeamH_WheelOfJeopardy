import woj
import time

class Question():
    def __init__(self, app):
        print("Question Thread")
#        while True:
#            if not app.board_to_question_queue.empty():
#                message = app.board_to_question_queue.get()
#                #TODO: Decide what to do with message!
#                #build board, show question, show answer, clear question
