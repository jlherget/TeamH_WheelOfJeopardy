import queue
import messages
import threading


class Board():
    def __init__(self, app):
        self.running = True
        self.app = app

    def PostMessage(self, message):
        self.app.queue.put(message)
