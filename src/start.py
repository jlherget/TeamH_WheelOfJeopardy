from gameboard import Button

import pygame
import gameboard
import messages


class StartUI():
    
    def __init__(self, app):
        self.running = True
        self.app     = app
        self.start_button       = Button(350,30,  gameboard.BLUE,  200, 150, "START")
        self.numPlayers1_button = Button(40,210,  gameboard.GREEN, 260,  75, "Number Of Players: 1")
        self.numPlayers2_button = Button(40,300,  gameboard.BLUE,  260,  75, "Number Of Players: 2")
        self.numPlayers3_button = Button(40,390,  gameboard.BLUE,  260,  75, "Number Of Players: 3")
        self.numPlayers4_button = Button(40,480,  gameboard.BLUE,  260,  75, "Number Of Players: 4")
        self.edit_button        = Button(400,300, gameboard.BLUE,  250, 250, "Edit Questions/Answers")
        
    def Draw(self, screen):
        self.start_button.Draw(screen, 60)
        self.edit_button.Draw(screen, 40)
        self.numPlayers1_button.Draw(screen, 35)
        self.numPlayers2_button.Draw(screen, 35)
        self.numPlayers3_button.Draw(screen, 35)
        self.numPlayers4_button.Draw(screen, 35)
        
    def ProcessUiEvent(self, event):
        
        #Check to see if the mouse is moving. If so, highlight the button.
        # If the button is clicked, send a start message to the queue
        if event.type == pygame.MOUSEMOTION:
            if self.start_button.isHighlighted(pygame.mouse.get_pos()):
                self.start_button.color = gameboard.PURPLE
            else:
                self.start_button.color = gameboard.BLUE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If start button is pressed, send a StartMessage
            if self.start_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.PostMessage(messages.StartMessage(self.app.num_players, None))    
                
            # If the edit button is pressed, send a EditMessage
            if self.edit_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.PostMessage(messages.EditMessage())     
        
            # IF any of the number of players buttons are pressed, 
            # update the number of players and button colors
            if self.numPlayers1_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.num_players = 1
                self.numPlayers1_button.color = gameboard.GREEN
                self.numPlayers2_button.color = gameboard.BLUE
                self.numPlayers3_button.color = gameboard.BLUE
                self.numPlayers4_button.color = gameboard.BLUE
            if self.numPlayers2_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.num_players = 2
                self.numPlayers1_button.color = gameboard.BLUE
                self.numPlayers2_button.color = gameboard.GREEN
                self.numPlayers3_button.color = gameboard.BLUE
                self.numPlayers4_button.color = gameboard.BLUE
            if self.numPlayers3_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.num_players = 3
                self.numPlayers1_button.color = gameboard.BLUE
                self.numPlayers2_button.color = gameboard.BLUE
                self.numPlayers3_button.color = gameboard.GREEN
                self.numPlayers4_button.color = gameboard.BLUE
            if self.numPlayers4_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.num_players = 4
                self.numPlayers1_button.color = gameboard.BLUE
                self.numPlayers2_button.color = gameboard.BLUE
                self.numPlayers3_button.color = gameboard.BLUE
                self.numPlayers4_button.color = gameboard.GREEN

class Start():
    
    def __init__(self, app):
        self.app            = app
        self.main_list      = []
        self.firstCall      = True
        self.ui             = StartUI(app)
        self.ingestText()

    def PostMessage(self, message):
        self.queue.put(message)
        
    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)
        
    def Draw(self, screen):
        self.ui.Draw(screen)

    # Replace Category:
    # ------------------------------------------
    # num_cat: The category number to be replaced
    # c_list: The list new list of Category, Questions and Answers
    # This function simply replaces the current list of Categories, Questions, and Answers
    #	and writes the new main_list to the original text file in its original format  
    #   should be called whenever the user has saved a change to the questions/answers

    def replaceCategory(self, num_cat, c_list):
        if num_cat < 5:
            self.main_list[num_cat] = c_list
        else:
            pass
        textfile = "resources/category_question_answer.txt"
        f = open(textfile, "w")
        for list in self.main_list:
            for item in list:
                outstring=item+"\n"
                f.write(outstring)
        f.close()

    # Ingest Text:
    # ------------------------------------------
    # This function reads from the category_question_answer.txt file that is storing the 
    #    current Categories, questions, and answers. While it is reading the file, it is 
    #    sorting each category with its questions and answers into its own list, and then
    #    appending that to its master list. Should be called during the init of the class
    #    Text file format is as follows:
    #	 	Category: <Name of Category 1>
    #		<Question 1 of Category 1>
    #		<Answer 1 of Category 1>
    #		. . .
    #		<Answer 6 of Category 1>
    # 		Category: <Name of Category 2>
    # 		. . .

    def ingestText(self):
        temp_list = []
        textfile = "resources/category_question_answer.txt"
        f = open(textfile, "r")
        for line in f.readlines():
            if "Category:" in line:
                category = line.split("Category: ")
                if self.firstCall:
                    temp_list.append(category[len(category)-1].strip())
                    self.firstCall = False
                else:
                    self.main_list.append(temp_list)
                    temp_list = []
                    temp_list.append(category[len(category)-1].strip())
                self.firstCall = False
            else:
                temp_list.append(line.strip())
        f.close()
