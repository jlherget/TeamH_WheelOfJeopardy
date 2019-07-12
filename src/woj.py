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
        self.num_players = 1

        self.start_screen = start.Start(self)
        self.board_screen = board.Board(self)
        self.question_screen = question.Question(self)
        self.wheel_screen = wheel.Wheel(self)

        self.startUp = True
        self.boardWheelUp = False
        self.questionUp = False
        self.updateQuestions = False
        self.wheelTurn = True

    def main():
        app = WoJ()

        pygame.init()
        # Create a screen
        screen = pygame.display.set_mode(gameboard.SCREEN_SIZE)

        # This sets the name of the window
        pygame.display.set_caption('Wheel of Jeopardy')

        clock = pygame.time.Clock()

        # Set positions of graphics
        wheel = gameboard.WheelUI(10, 60, app)
        board = gameboard.QuestionsBoardUI(320, 0)
        start_button = gameboard.StartButtonUI(350,30, gameboard.BLUE, 200, 150, "START")
        numPlayers1_button = gameboard.StartButtonUI(40,210, gameboard.GREEN, 260, 75, "Number Of Players: 1")
        numPlayers2_button = gameboard.StartButtonUI(40,300, gameboard.BLUE, 260, 75, "Number Of Players: 2")
        numPlayers3_button = gameboard.StartButtonUI(40,390, gameboard.BLUE, 260, 75, "Number Of Players: 3")
        numPlayers4_button = gameboard.StartButtonUI(40,480, gameboard.BLUE, 260, 75, "Number Of Players: 4")
        update_button = gameboard.StartButtonUI(400,300, gameboard.BLUE, 250, 250, "Update Jeopardy \nQuestions/Answers")
        print("After Start, Press 1 to Restart, Press 2 to Kill")
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
                            start_button.color = gameboard.PURPLE
                        else:
                            start_button.color = gameboard.BLUE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.isHighlighted(pygame.mouse.get_pos()):
                        print("Mouse down")
                        app.start_screen.PostMessage(messages.StartMessage(app.num_players, None))     
                        app.startUp = False
                        app.boardWheelUp = True
                    if numPlayers1_button.isHighlighted(pygame.mouse.get_pos()):
                        app.num_players = 1
                        numPlayers1_button.color = gameboard.GREEN
                        numPlayers2_button.color = gameboard.BLUE
                        numPlayers3_button.color = gameboard.BLUE
                        numPlayers4_button.color = gameboard.BLUE
                    if numPlayers2_button.isHighlighted(pygame.mouse.get_pos()):
                        app.num_players = 2
                        numPlayers1_button.color = gameboard.BLUE
                        numPlayers2_button.color = gameboard.GREEN
                        numPlayers3_button.color = gameboard.BLUE
                        numPlayers4_button.color = gameboard.BLUE
                    if numPlayers3_button.isHighlighted(pygame.mouse.get_pos()):
                        app.num_players = 3
                        numPlayers1_button.color = gameboard.BLUE
                        numPlayers2_button.color = gameboard.BLUE
                        numPlayers3_button.color = gameboard.GREEN
                        numPlayers4_button.color = gameboard.BLUE
                    if numPlayers4_button.isHighlighted(pygame.mouse.get_pos()):
                        app.num_players = 4
                        numPlayers1_button.color = gameboard.BLUE
                        numPlayers2_button.color = gameboard.BLUE
                        numPlayers3_button.color = gameboard.BLUE
                        numPlayers4_button.color = gameboard.GREEN
                elif app.boardWheelUp:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            app.board_screen.PostMessage(messages.RestartMessage())
                        if event.key == pygame.K_2:
                            app.board_screen.PostMessage(messages.KillMessage())
                        if event.key == pygame.K_TAB and not app.wheelTurn:
                                app.board_screen.PostMessage(messages.OutOfQuestionsMessage())
                                app.wheelTurn = True
                        if event.key == pygame.K_SPACE:
                            if app.wheelTurn:
                                app.wheel_screen.PostMessage(messages.SpinInMessage())
                                wheel.Spin()
                            else:
                                print("SPACEBAR CLICKED, SENDING QUESTION RESULTS TO APP")
                                app.wheel_screen.PostMessage(messages.QuestionsResultMessage(True, 1000, 1, False))
                elif app.questionUp:
                    print("Question Up")
 
            #Redraw the gray background on the board
            screen.fill(gameboard.GRAY)     
     
            #Determine what should be drawn
            if app.startUp:
                start_button.Draw(screen, 60)
                update_button.Draw(screen, 40)
                numPlayers1_button.Draw(screen, 35)
                numPlayers2_button.Draw(screen, 35)
                numPlayers3_button.Draw(screen, 35)
                numPlayers4_button.Draw(screen, 35)
            elif app.boardWheelUp:
                wheel.Draw(screen)
                board.Draw(screen, app.wheelTurn)
            elif app.questionUp:
                print("Question Up")
                   
            pygame.display.flip()
            clock.tick(60)
                      
        pygame.quit()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
