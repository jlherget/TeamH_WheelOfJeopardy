from ui_utils import Button

import pygame
import ui_utils
import messages
from questionset import GameSet, RoundSet, CategorySet

class StartUI():

    def __init__(self, parent, app):
        self.running = True
        self.app     = app
        self.parent  = parent
        self.start_button       = Button(350,30,  ui_utils.BLUE,  200, 150, "START")
        self.numPlayers1_button = Button(40,210,  ui_utils.GREEN, 260,  75, "1")
        self.numPlayers2_button = Button(40,300,  ui_utils.BLUE,  260,  75, "2")
        self.numPlayers3_button = Button(40,390,  ui_utils.BLUE,  260,  75, "3")
        self.numPlayers4_button = Button(40,480,  ui_utils.BLUE,  260,  75, "4")
        self.edit_button        = Button(400,300, ui_utils.BLUE,  420, 100, "Edit Questions/Answers")
        self.num_players        = 1

    def Draw(self, screen):
        font = pygame.font.SysFont('arial', 35)
        text = font.render("Number of Players", 1, (0,0,0))
        screen.blit(text, (40 , 150))

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
                self.start_button.color = ui_utils.PURPLE
            else:
                self.start_button.color = ui_utils.BLUE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If start button is pressed, send a StartMessage
            if self.start_button.isHighlighted(pygame.mouse.get_pos()):
                gameSet = self.parent.ingestText()
                self.app.startGame(self.num_players, gameSet)

            # If the edit button is pressed, send a EditMessage
            if self.edit_button.isHighlighted(pygame.mouse.get_pos()):
                self.app.PostMessage(messages.EditMessage())

            # If any of the number of players buttons are pressed,
            # update the number of players and button colors
            if self.numPlayers1_button.isHighlighted(pygame.mouse.get_pos()):
                self.num_players = 1
                self.numPlayers1_button.color = ui_utils.GREEN
                self.numPlayers2_button.color = ui_utils.BLUE
                self.numPlayers3_button.color = ui_utils.BLUE
                self.numPlayers4_button.color = ui_utils.BLUE
            if self.numPlayers2_button.isHighlighted(pygame.mouse.get_pos()):
                self.num_players = 2
                self.numPlayers1_button.color = ui_utils.BLUE
                self.numPlayers2_button.color = ui_utils.GREEN
                self.numPlayers3_button.color = ui_utils.BLUE
                self.numPlayers4_button.color = ui_utils.BLUE
            if self.numPlayers3_button.isHighlighted(pygame.mouse.get_pos()):
                self.num_players = 3
                self.numPlayers1_button.color = ui_utils.BLUE
                self.numPlayers2_button.color = ui_utils.BLUE
                self.numPlayers3_button.color = ui_utils.GREEN
                self.numPlayers4_button.color = ui_utils.BLUE
            if self.numPlayers4_button.isHighlighted(pygame.mouse.get_pos()):
                self.num_players = 4
                self.numPlayers1_button.color = ui_utils.BLUE
                self.numPlayers2_button.color = ui_utils.BLUE
                self.numPlayers3_button.color = ui_utils.BLUE
                self.numPlayers4_button.color = ui_utils.GREEN

class Start():

    def __init__(self, app):
        self.app            = app
        self.main_list      = []
        self.firstCall      = True
        self.ui             = StartUI(self, app)

    def Draw(self, screen):
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)


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
    #		<Answer 5 of Category 1>
    # 		Category: <Name of Category 2>
    # 		. . .

    def ingestText(self):
        textfile = "resources/category_question_answer.txt"
        f = open(textfile, "r")
        gameSet = GameSet()

        # Go through both rounds
        for r in range(2):
            roundSet = RoundSet()

            # Go through 6 categories per round
            for cat in range(6):
                line = f.readline()
                category = line.split("Category: ")[1].strip()

                catSet = CategorySet(category)

                # Go through 5 quesitons per category
                for q in range(5):
                    question_text = f.readline().strip()
                    answer_text   = f.readline().strip()
                    catSet.addQuestionAndAnswer(question_text, answer_text)
                roundSet.addCategory(catSet)
            gameSet.addRound(roundSet)
        f.close()
        return gameSet