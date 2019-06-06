import woj
import time

class Board():
    def __init__(self, app):
        print("Board Thread")
#        while True:
#            if not app.app_to_board_queue.empty():
#                message = app.app_to_board_queue.get()
#                #TODO: Decide what to do with message! 
#                #build board, show board, reset board, delete board
