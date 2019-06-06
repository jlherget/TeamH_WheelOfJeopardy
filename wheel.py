import woj
import time

class Wheel():
    def __init__(self, app):
        print("Wheel Thread")
#        while True:
#            if not app.wheel_command_queue.empty():
#                message = app.wheel_command_queue.get()
#                #TODO: Decide what to do with message!
#                #build wheel, reset wheel, delete wheel

#            if not app.wheel_input_queue.empty():
#                message = app.wheel_input_queue.get()
#                #TODO: Decide what to do with message!
#                #SPIN THE WHEEL
