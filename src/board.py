import queue
import messages
import threading


class Board(threading.Thread):
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
            #build board, show board, reset board, delete board
            self.queue.task_done()

    def PostMessage(self, message):
        self.queue.put(message)
