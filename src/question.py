import queue
import messages
import threading


class Question(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.running = True

    def run(self):
        while self.running:
            task = self.queue.get()
            if task is None:
                break
            task.run(self)
            self.queue.task_done()

    def PostMessage(self, message):
        self.queue.put(message)


#TODO: Decide what to do with message!
#build board, show question, show answer, clear question
