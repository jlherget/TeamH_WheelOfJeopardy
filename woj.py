import board
import wheel
import start
import question
import queue
import threading
import messages


class WoJ(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.running = True

        self.start_screen = start.Start(self)
        self.board_screen = board.Board(self)
        self.question_screen = question.Question(self)
        self.wheel_screen = wheel.Wheel(self)

        self.start_screen.start()
        self.board_screen.start()
        self.question_screen.start()
        self.wheel_screen.start()

    def main():
        app = WoJ()

        # Send a few of test messages as an example:
        start_message = messages.StartMessage(1, None)
        app.start_screen.PostMessage(start_message)
        app.board_screen.PostMessage(start_message)
        app.question_screen.PostMessage(start_message)
        app.wheel_screen.PostMessage(start_message)

        # Send a test message which posts back a message to app
        # which causes an exit.
        message = messages.TestMessage()
        app.wheel_screen.PostMessage(message)

        while app.running:
            task = app.queue.get()
            if task is None:
                break
            task.run(app)
            app.queue.task_done()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
