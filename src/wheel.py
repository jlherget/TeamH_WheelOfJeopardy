import queue
import messages
import threading


class Wheel(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.running = True
        self.app = app

    def run(self):
        while self.running:
            task = self.queue.get()
            if task is None:
                break
            task.run(self)
            self.queue.task_done()

    def PostMessage(self, message):
        self.queue.put(message)


#todo
#build wheel, reset wheel, delete wheel
#SPIN THE WHEEL
