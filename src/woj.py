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
        self.queue              = queue.Queue()
        self.running            = True
        self.num_players        = 1

        self.start       = start.Start(self)
        self.board       = board.Board(self)
        self.wheel       = wheel.Wheel(self)

        self.startUp            = True
        self.boardWheelUp       = False
        self.questionUp         = False
        self.updateQuestions    = False

    def main():
        
        pygame.init()
        
        # Create a screen
        screen = pygame.display.set_mode(gameboard.SCREEN_SIZE)
        
        # This sets the name of the window
        pygame.display.set_caption('Wheel of Jeopardy')
        clock = pygame.time.Clock()
        
        app = WoJ()
        while app.running:
            
            # Pop tasks off the message queue
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
                    app.start.ProcessUiEvent(event)
                elif app.boardWheelUp:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            app.wheel.Spin()
                elif app.questionUp:
                    print("Question Up")
 
            #Redraw the gray background on the board
            screen.fill(gameboard.GRAY)     
     
            #Determine what should be drawn
            if app.startUp:
                app.start.Draw(screen)
            elif app.boardWheelUp:
                app.wheel.Draw(screen)
                app.board.Draw(screen)
            elif app.questionUp:
                print("Question Up")
                   
            pygame.display.flip()
            clock.tick(60)
                      
        pygame.quit()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
