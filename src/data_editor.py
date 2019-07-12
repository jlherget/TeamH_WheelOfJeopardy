import messages
import pygame
import gameboard
import start

class DataEditorUI():
    
    def __init__(self, app):
        self.app = app
        self.save_button = start.Button(350,30,  gameboard.BLUE,  200, 150, "SAVE")
        
    def Draw(self, screen):
        self.save_button.Draw(screen, 60)
        
    def ProcessUiEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.save_button.isHighlighted(pygame.mouse.get_pos()):
                self.save_button.color = gameboard.PURPLE
            else:
                self.save_button.color = gameboard.BLUE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.PostMessage(messages.SaveMessage())   


class DataEditor():
    
    def __init__(self, app):
        self.app = app
        self.ui  = DataEditorUI(app)
        
    def Draw(self, screen):
        self.ui.Draw(screen)
        
    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)