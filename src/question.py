import queue
import messages


class Question():
    def __init__(self, app):
        self.running = True
        self.app = app

    def PostMessage(self, message):
        self.app.queue.put(message)


#TODO: Decide what to do with message!
#build board, show question, show answer, clear question
