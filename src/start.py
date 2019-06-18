import queue
import messages


class Start():
    def __init__(self, app):
        self.running = True
        self.app = app

    def PostMessage(self, message):
        self.app.queue.put(message)
