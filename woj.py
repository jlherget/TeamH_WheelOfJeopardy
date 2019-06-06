import queue
import board
import wheel
import start
import question
import threading

class WoJ:
    def __init__(self):
        self.start_queue = queue.Queue()
        self.wheel_command_queue = queue.Queue()
        self.wheel_input_queue = queue.Queue()
        self.wheel_result_queue = queue.Queue()
        self.question_result_queue = queue.Queue()
        self.app_to_board_queue = queue.Queue()
        self.board_to_question_queue = queue.Queue()

    def main():
        app = WoJ()
        w = threading.Thread(target=board.Board, args=(app,))
        x = threading.Thread(target=wheel.Wheel, args=(app,))
        y = threading.Thread(target=question.Question, args=(app,))
        z = threading.Thread(target=start.Start, args=(app,))
        w.start()
        x.start()
        y.start()
        z.start()

#        while True:
#            if not app.start_queue.empty():
#                message = app.start_queue.get()
#                #TODO: Decide what to do with message!

#            if not app.wheel_result_queue.empty():
#                message = app.wheel_result_queue.get()
#                #TODO: Decide what to do with message!

#            if not app.question_result_queue.empty():
#                message = app.question_result_queue.get()
#                #TODO: Decide what to do with message!

if __name__ == '__main__':
    WoJ.main()
