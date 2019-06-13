import queue
import messages

class Wheel():
    def __init__(self, app):
        self.running = True
        self.app = app

    def PostMessage(self, message):
        self.app.queue.put(message)


#todo
#build wheel, reset wheel, delete wheel
#SPIN THE WHEEL
