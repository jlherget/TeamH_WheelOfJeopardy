from ui_utils import Button, Colors

import pygame
import ui_utils

class DataEditor():
    """Data editor captures and store the questions and answers that the user entered at the configuration screen."""

    def __init__(self, app):
        self.app = app
        self.ui  = DataEditorUI(app)

    def Draw(self, screen):
        """Draw the data editor onto the pygame screen."""
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        """Process user interface events."""
        self.ui.ProcessUiEvent(event)

class DataEditorUI():
    """Handles drawing the data editor user interface onto the pygame screen."""

    def __init__(self, app):
        self.app = app
        self.save_button = Button(350,30,  Colors.BLUE,  200, 150, "SAVE")
        
    def Draw(self, screen):
        """Draw the data editor onto the pygame screen."""
        self.save_button.Draw(screen, 60)

    def ProcessUiEvent(self, event):
        """Process user interface events."""
        # Color save button purple if the user hovers over it.
        # Otherwise color it blue
        if event.type == pygame.MOUSEMOTION:
            if self.save_button.isHighlighted(pygame.mouse.get_pos()):
                self.save_button.color = Colors.PURPLE
            else:
                self.save_button.color = Colors.BLUE

        # If user clicks on the save button, go back to the start screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.showStartScreen()
