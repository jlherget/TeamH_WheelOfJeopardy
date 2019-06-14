import board
import wheel
import start
import question
import queue
import threading
import messages
import gameboard
import pygame

class WoJ(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.running = True

        self.start_screen = start.Start(self)
        self.board_screen = board.Board(self)
        self.question_screen = question.Question(self)
        self.wheel_screen = wheel.Wheel(self)

        self.startUp = True
        self.boardWheelUp = False
        self.questionUp = False

    def main():
        app = WoJ()

        pygame.init()
        # Create a screen
        screen = pygame.display.set_mode(gameboard.SCREEN_SIZE)

        # This sets the name of the window
        pygame.display.set_caption('Wheel of Jeopardy')

        clock = pygame.time.Clock()

        # Set positions of graphics
        wheel = gameboard.WheelUI(10, 60)
        board = gameboard.QuestionsBoardUI(320, 0)
        start_button = gameboard.StartButtonUI(20,70, gameboard.BLUE, 159, 315, "hello")

        # Send a few of test messages as an example:
        start_message = messages.StartMessage(1, None)
        app.start_screen.PostMessage(start_message)
        app.board_screen.PostMessage(start_message)
        app.question_screen.PostMessage(start_message)
        app.wheel_screen.PostMessage(start_message)

        # Send a test message which posts back a message to app
        # which causes an exit.
#        message = messages.TestMessage()
#        app.wheel_screen.PostMessage(message)

        while app.running:
            if not app.queue.empty():
                task = app.queue.get()
                if task is None:
                    break
                task.run(app)
                app.queue.task_done()
            #Fetch Game event
            for event in pygame.event.get():
                #If game ends, program ends
                if event.type == pygame.QUIT:
                    app.running = False
                #If we are in the start screen, check to see if the mouse is moving. If so,
                #Highlight the button. If the button is clicked, send a start message to the 
                #Queue, and set variables so that we are no longer on the start screen but on
                #the wheel/board screen
                if app.startUp:
                    if event.type == pygame.MOUSEMOTION:
                        if start_button.isHighlighted(pygame.mouse.get_pos()):
                            start_button.color = gameboard.GREEN
                        else:
                            start_button.color = gameboard.BLUE
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        app.start_screen.PostMessage(messages.StartMessage(2, None))
                        app.startUp = False
                        app.boardWheelUp = True
                elif app.boardWheelUp:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            wheel.Spin()
                elif app.questionUp:
                    print("Question Up")
 
            #Redraw the gray background on the board
            screen.fill(gameboard.GRAY)     
     
            #Determine what should be drawn
            if app.startUp:
                start_button.Draw(screen)
            elif app.boardWheelUp:
                wheel.Draw(screen)
                board.Draw(screen)
            elif app.questionUp:
                print("Question Up")
                   
            pygame.display.flip()
            clock.tick(60)
                      
        pygame.quit()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
