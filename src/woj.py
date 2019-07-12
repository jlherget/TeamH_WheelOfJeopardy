import board
import wheel
import start
import queue
import gameboard
import pygame
import data_editor

class WoJ():
    
    START_SCREEN    = 1
    BOARD_SCREEN    = 2
    EDIT_SCREEN     = 3
    QUESTION_SCREEN = 4
    
    def __init__(self):
        self.queue              = queue.Queue()
        self.running            = True
        self.num_players        = 1
        self.current_screen     = self.START_SCREEN
        
        self.start       = start.Start(self)
        self.board       = board.Board(self)
        self.wheel       = wheel.Wheel(self)
        self.editor      = data_editor.DataEditor(self)
        
    def run(self, screen):
                
        # This sets the name of the window
        pygame.display.set_caption('Wheel of Jeopardy')
        clock = pygame.time.Clock()
    
        while self.running:
            
            # Pop tasks off the message queue
            if not self.queue.empty():
                task = self.queue.get()
                if task is None:
                    break
                task.run(self)
                self.queue.task_done()
                
            #Fetch Game event
            for event in pygame.event.get():
                #If game ends, program ends
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if self.current_screen == self.START_SCREEN:
                    self.start.ProcessUiEvent(event)
                elif self.current_screen == self.BOARD_SCREEN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.wheel.Spin()
                elif self.current_screen == self.EDIT_SCREEN:
                    self.editor.ProcessUiEvent(event)
                elif self.current_screen == self.QUESTION_SCREEN:
                    print("Question Up")

            #Clear the screen with gray background
            screen.fill(gameboard.GRAY)     
     
            #Determine what should be drawn
            if self.current_screen == self.START_SCREEN:
                self.start.Draw(screen)
            elif self.current_screen == self.BOARD_SCREEN:
                self.wheel.Draw(screen)
                self.board.Draw(screen)
            elif self.current_screen == self.EDIT_SCREEN:
                self.editor.Draw(screen)
            elif self.current_screen == self.QUESTION_SCREEN:
                print("Question Up")
                   
            # Draw the new screen
            pygame.display.flip()
            
            # Draw at 60Hz
            clock.tick(60)
        
    def main():
        
        pygame.init()
        screen = pygame.display.set_mode(gameboard.SCREEN_SIZE)
        app = WoJ()
        app.run(screen)
        pygame.quit()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
