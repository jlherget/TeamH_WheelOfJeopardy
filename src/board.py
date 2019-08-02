import pygame
import ui_utils
from ui_utils import Button
import messages
from questionset import RoundSet

class BoardUI():
    NUM_COLS   = 6
    NUM_QROWS  = 5 # Not including categories row
    ROW_HEIGHT = 70
    COL_WIDTH  = 90
    COL_LINE_WIDTH = 4
    ROW_LINE_WIDTH = 4
    SEPARATOR_HEIGHT = 15

    QY_OFFSET = ROW_HEIGHT + SEPARATOR_HEIGHT

    BOARD_WIDTH   = COL_WIDTH * NUM_COLS
    BOARD_HEIGHT  = ROW_HEIGHT * (NUM_QROWS+1) + SEPARATOR_HEIGHT

    BASE_VALUE  = 200


    def __init__(self, parent, app, pos_x, pos_y):
        self.parent             = parent
        self.app                = app
        self.pos_x              = pos_x
        self.pos_y              = pos_y
        #Question Phase States:
        #   - 0: Board normal
        #   - 1: Show Question
        #   - 2: Show Answer
        #   - 3: Ask For Free Spin
        #   - 4: Choice Board
        #   - 5: Opponents Choice Board
        self.question_phase     = 0

        self.show_answer_button = Button(pos_x+60,pos_y+200,  ui_utils.YELLOW, 350, 100,
                                         "Show Answer")
        self.correct_button = Button(pos_x+60,pos_y+200,  ui_utils.YELLOW, 170, 100,
                                         "Correct!")
        self.incorrect_button = Button(pos_x+250,pos_y+200,  ui_utils.YELLOW, 170, 100,
                                         "Incorrect!")
        self.freespin_yes = Button(pos_x+60,pos_y+200,  ui_utils.YELLOW, 170, 100,
                                         "Yes!")
        self.freespin_no = Button(pos_x+250,pos_y+200,  ui_utils.YELLOW, 170, 100,
                                         "No!")
        self.cat1_button = Button(self.pos_x+60,self.pos_y+70,  ui_utils.YELLOW, 170, 100,
                                "None")
        self.cat2_button = Button(self.pos_x+250,self.pos_y+70,  ui_utils.YELLOW, 170, 100,
                                 "None")
        self.cat3_button = Button(self.pos_x+60,self.pos_y+200,  ui_utils.YELLOW, 170, 100,
                                "None")
        self.cat4_button = Button(self.pos_x+250,self.pos_y+200,  ui_utils.YELLOW, 170, 100,
                                 "None")
        self.cat5_button = Button(self.pos_x+60,self.pos_y+330,  ui_utils.YELLOW, 170, 100,
                                "None")
        self.cat6_button = Button(self.pos_x+250,self.pos_y+330,  ui_utils.YELLOW, 170, 100,
                                 "None")

    def Draw(self, screen):

        # Background for the questions
        boardRect = pygame.Rect([self.pos_x, self.pos_y, self.BOARD_WIDTH, self.BOARD_HEIGHT])
        pygame.draw.rect(screen, ui_utils.BLUE, boardRect)
        #Top line
        pygame.draw.rect(screen, ui_utils.BLACK, [self.pos_x, self.pos_y, self.BOARD_WIDTH, 5])

        if self.question_phase == 0:
            # Draw the lines between rows
            # Categories
            font = pygame.font.SysFont('Calibri', 16, True, False)
            for i in range(self.NUM_COLS+1):
                left    = self.pos_x + self.COL_WIDTH *i
                top     = self.pos_y
                width   = 5
                height  = self.ROW_HEIGHT
                pygame.draw.rect(screen, ui_utils.BLACK, [left, top, width, height])
                if i < self.NUM_COLS:
                    text = font.render(self.parent.qset.category[i].title, True, ui_utils.YELLOW)
                    screen.blit(text, [left+15, top+5.5])

            # Categories/questions seaparator
            pygame.draw.rect(screen, ui_utils.BLACK, [self.pos_x, self.pos_y + self.ROW_HEIGHT, self.BOARD_WIDTH + 5, self.SEPARATOR_HEIGHT])


            for i in range(self.NUM_QROWS+1):
                top     = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * i
                left    = self.pos_x
                width   = self.BOARD_WIDTH + 5
                height  = 5
                pygame.draw.rect(screen, ui_utils.BLACK, [left, top, width, height])

        # Draw the lines between columns
            for i in range(self.NUM_COLS+1):
                top     = self.pos_y + self.QY_OFFSET
                left    = self.pos_x + self.COL_WIDTH *i
                width   = 5
                height  = self.ROW_HEIGHT * self.NUM_QROWS
                pygame.draw.rect(screen, ui_utils.BLACK, [left, top, width, height])

            # Draw the dollar amounts that havent been revelead
            font = pygame.font.SysFont('Calibri', 25, True, False)
            for r in range(self.NUM_QROWS):
                for c  in range(self.NUM_COLS):
                    x = self.pos_x + self.COL_WIDTH*c + self.COL_WIDTH / 3
                    y = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * r + self.ROW_HEIGHT / 2.5
                    s = '${}'.format((r+1) * self.BASE_VALUE)
                    text = font.render(s, True, ui_utils.YELLOW)
                    if r > 4-self.parent.qset.category[c].q_count:
                        screen.blit(text, [x, y])

        elif self.question_phase == 1:
            font = pygame.font.SysFont('Calibri', 34, True, False)
            s = '{}'.format("Question:  " + self.parent.qa.question)
            text = font.render(s, True, ui_utils.YELLOW)
            screen.blit(text, [self.pos_x+15, self.pos_y+40])
            s = '{}'.format("Value:  $" + str(self.parent.qa.value))
            text = font.render(s, True, ui_utils.YELLOW)
            screen.blit(text, [self.pos_x+15, self.pos_y+80])
            self.show_answer_button.Draw(screen, 60)

        elif self.question_phase == 2:
            self.incorrect_button.Draw(screen, 30)
            self.correct_button.Draw(screen, 30)
            font = pygame.font.SysFont('Calibri', 34, True, False)
            s = '{}'.format("Answer:  " + self.parent.qa.answer)
            text = font.render(s, True, ui_utils.YELLOW)
            screen.blit(text, [self.pos_x+15, self.pos_y+20])

        elif self.question_phase == 3:
            self.freespin_yes.Draw(screen, 30)
            self.freespin_no.Draw(screen, 30)
            font = pygame.font.SysFont('Calibri', 34, True, False)
            text = font.render("Use Your Free Token?", True, ui_utils.YELLOW)
            screen.blit(text, [self.pos_x+15, self.pos_y+20])

        elif self.question_phase == 4 or self.question_phase == 5:
            font = pygame.font.SysFont('Calibri', 34, True, False)
            if self.question_phase == 4:
                text = font.render("Player Choose A Category!", True, ui_utils.YELLOW)
            else:
                text = font.render("Opponent Choose A Category!", True, ui_utils.YELLOW)
            screen.blit(text, [self.pos_x+15, self.pos_y+20])
            self.cat1_button = Button(self.pos_x+60,self.pos_y+70,  ui_utils.YELLOW, 170, 100,
                                      self.parent.qset.category[0].title)
            self.cat2_button = Button(self.pos_x+250,self.pos_y+70,  ui_utils.YELLOW, 170, 100,
                                      self.parent.qset.category[1].title)
            self.cat3_button = Button(self.pos_x+60,self.pos_y+185,  ui_utils.YELLOW, 170, 100,
                                      self.parent.qset.category[2].title)
            self.cat4_button = Button(self.pos_x+250,self.pos_y+185,  ui_utils.YELLOW, 170, 100,
                                      self.parent.qset.category[3].title)
            self.cat5_button = Button(self.pos_x+60,self.pos_y+300,  ui_utils.YELLOW, 170, 100,
                                      self.parent.qset.category[4].title)
            self.cat6_button = Button(self.pos_x+250,self.pos_y+300,  ui_utils.YELLOW, 170, 100,
                                      self.parent.qset.category[5].title)
            self.cat1_button.Draw(screen, 25)
            self.cat2_button.Draw(screen, 25)
            self.cat3_button.Draw(screen, 25)
            self.cat4_button.Draw(screen, 25)
            self.cat5_button.Draw(screen, 25)
            self.cat6_button.Draw(screen, 25)

    def ProcessUiEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.app.PostMessage(messages.RestartMessage())
            if event.key == pygame.K_2:
                self.app.PostMessage(messages.KillMessage())

        if self.question_phase == 1:
            if event.type == pygame.MOUSEMOTION:
                if self.show_answer_button.isHighlighted(pygame.mouse.get_pos()):
                    self.show_answer_button.color = ui_utils.PURPLE
                else:
                    self.show_answer_button.color = ui_utils.YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_answer_button.isHighlighted(pygame.mouse.get_pos()):
                    self.question_phase = 2

        elif self.question_phase == 2:
            if event.type == pygame.MOUSEMOTION:
                if self.correct_button.isHighlighted(pygame.mouse.get_pos()):
                    self.correct_button.color = ui_utils.PURPLE
                else:
                    self.correct_button.color = ui_utils.YELLOW
                if self.incorrect_button.isHighlighted(pygame.mouse.get_pos()):
                    self.incorrect_button.color = ui_utils.PURPLE
                else:
                    self.incorrect_button.color = ui_utils.YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.correct_button.isHighlighted(pygame.mouse.get_pos()):
                    self.app.questionResult(messages.QuestionsResultMessage(True, self.parent.qa.value, False, self.parent.questionsRemaining()))
                    self.question_phase = 0

                if self.incorrect_button.isHighlighted(pygame.mouse.get_pos()):
                    if self.app.curPlayerTokenCount() <= 0:
                        self.app.questionResult(messages.QuestionsResultMessage(False,self.parent.qa.value, False,  self.parent.questionsRemaining()))
                        self.question_phase = 0
                    else:
                        self.question_phase = 3
        elif self.question_phase == 3:
            if event.type == pygame.MOUSEMOTION:
                if self.freespin_yes.isHighlighted(pygame.mouse.get_pos()):
                    self.freespin_yes.color = ui_utils.PURPLE
                else:
                    self.freespin_yes.color = ui_utils.YELLOW
                if self.freespin_no.isHighlighted(pygame.mouse.get_pos()):
                    self.freespin_no.color = ui_utils.PURPLE
                else:
                    self.freespin_no.color = ui_utils.YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.freespin_yes.isHighlighted(pygame.mouse.get_pos()):
                    self.app.questionResult(messages.QuestionsResultMessage(False, self.parent.qa.value, True,  self.parent.questionsRemaining()))                   
                if self.freespin_no.isHighlighted(pygame.mouse.get_pos()):
                    self.app.questionResult(messages.QuestionsResultMessage(False ,self.parent.qa.value, False,  self.parent.questionsRemaining()))
                self.question_phase = 0
                    
        elif self.question_phase == 4 or self.question_phase == 5:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cat1_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.sendQuestion(0)
                if self.cat2_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.sendQuestion(1)
                if self.cat3_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.sendQuestion(2)
                if self.cat4_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.sendQuestion(3)
                if self.cat5_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.sendQuestion(4)
                if self.cat6_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.sendQuestion(5)

class QASet():
    def __init__(self, question, answer, value):
        self.question = question
        self.answer = answer
        self.value = value

class Board():
    def __init__(self, app):
        self.running = True
        self.app     = app
        self.qa      = QASet("", "", -1)
        self.ui      = BoardUI(self, app, 320, 0)
        self.qset    = RoundSet()
        self.roundNum = 0

    def startRound(self, roundNum, round_qset):
        self.qset = round_qset
        self.roundNum = roundNum

    def questionsRemaining(self):
        total_q_count = 0
        for cat in self.qset.category:
            total_q_count += cat.q_count
        return total_q_count

    def sendQuestion(self, section):
        #Not a choice question
        if section < 6:
            category = self.qset.category[section]

            #Check to see if questions are left
            print(category.q_count)
            if category.q_count > 0:
                q_pos    = 5-category.q_count
                question = category.question[q_pos]
                answer   = category.answer[q_pos]
                value = (q_pos+1)*200*self.roundNum
                self.qset.category[section].q_count -= 1
                self.displayQuestion(question, answer, value)
            else:
                # Shouldn't happen
                print("Out of questions, spinning again!")
                self.app.noQuestionsInCategory()
        else:
            print("Bad category %i" % section)

    def opponentSelectsCategory(self):
        self.ui.question_phase = 5

    def playerSelectsCategory(self):
        self.ui.question_phase = 4
 
    def displayQuestion(self, q_text, q_answer, value):
        self.qa = QASet(q_text, q_answer, value)
        self.ui.question_phase = 1

    def Draw(self, screen):
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)
