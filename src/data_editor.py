from ui_utils import Button

import messages
import pygame
import ui_utils

class DataEditor():
    
    def __init__(self, app):
        self.app = app
        self.ui  = DataEditorUI(app)
    
    def Draw(self, screen):
        self.ui.Draw(screen)
        
    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)

class DataEditorUI():
    
    def __init__(self, app):
        self.app = app
        self.save_button = Button(350,30,  ui_utils.BLUE,  200, 150, "SAVE")
        
    def Draw(self, screen):
        self.save_button.Draw(screen, 60)
        
    def ProcessUiEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.save_button.isHighlighted(pygame.mouse.get_pos()):
                self.save_button.color = ui_utils.PURPLE
            else:
                self.save_button.color = ui_utils.BLUE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.PostMessage(messages.SaveMessage())