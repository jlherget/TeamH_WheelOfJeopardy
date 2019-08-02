import start
import queue
import pygame
import data_editor
import ui_utils
import gamescreen

class WoJ():

    def __init__(self):

        pygame.init()
        self.queue              = queue.Queue()
        self.running            = True
        self.num_players        = 1
        self.updateQuestions    = False
        self.wheelTurn          = True

        # Set mode before creating the WoJ screens
        self.screen             = pygame.display.set_mode(ui_utils.SCREEN_SIZE)

        self.start_screen       = start.Start(self)
        self.game_screen        = gamescreen.GameScreen(self)
        self.editor_screen      = data_editor.DataEditor(self)

        self.current_screen     = self.start_screen

    def run(self):

        # This sets the name of the window
        pygame.display.set_caption('Wheel of Jeopardy')
        clock = pygame.time.Clock()
        print("After Start, Press 1 to Restart, Press 2 to Kill")

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
                # Send event to the current screen
                self.current_screen.ProcessUiEvent(event)

            #Clear the screen with gray background
            self.screen.fill(ui_utils.GRAY)

            # Draw the current screen
            self.current_screen.Draw(self.screen)

            # Draw the new screen
            pygame.display.flip()

            # Draw at 60Hz
            clock.tick(60)

    def main():
        app = WoJ()
        app.run()
        pygame.quit()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
