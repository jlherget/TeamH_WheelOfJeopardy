from decimal     import Decimal
from ui_utils    import Button, Colors
from questionset import RoundSet
from enum        import Enum
from timer       import Timer
from timeit import default_timer as timer

import pygame
import time

class Phase(Enum):
    """Question phase states."""

    NORMAL          = 0
    SHOW_QUESTION   = 1
    SHOW_ANSWER     = 2
    ASK_SPIN_TOKEN  = 3
    PLAYER_CHOICE   = 4
    OPPONENT_CHOICE = 5
    ANIMATION       = 6

class BoardUI():
    """Handles drawing the board onto the pygame screen."""

    NUM_COLS         = 6
    NUM_QROWS        = 5 # Not including categories row
    ROW_HEIGHT       = 70
    COL_WIDTH        = 90
    COL_LINE_WIDTH   = 4
    ROW_LINE_WIDTH   = 4
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

        self.show_answer_button = Button(pos_x+60,  pos_y+200, Colors.YELLOW, 350, 100, "Show Answer")
        self.correct_button     = Button(pos_x+60,  pos_y+200, Colors.YELLOW, 170, 100, "Correct!")
        self.incorrect_button   = Button(pos_x+250, pos_y+200, Colors.YELLOW, 170, 100, "Incorrect!")
        self.freespin_yes       = Button(pos_x+60,  pos_y+200, Colors.YELLOW, 170, 100, "Yes!")
        self.freespin_no        = Button(pos_x+250, pos_y+200, Colors.YELLOW, 170, 100, "No!")
        self.cat1_button        = Button(pos_x+60,   pos_y+70, Colors.YELLOW, 170, 100, "None")
        self.cat2_button        = Button(pos_x+250,  pos_y+70, Colors.YELLOW, 170, 100, "None")
        self.cat3_button        = Button(pos_x+60,  pos_y+200, Colors.YELLOW, 170, 100, "None")
        self.cat4_button        = Button(pos_x+250, pos_y+200, Colors.YELLOW, 170, 100, "None")
        self.cat5_button        = Button(pos_x+60,  pos_y+330, Colors.YELLOW, 170, 100, "None")
        self.cat6_button        = Button(pos_x+250, pos_y+330, Colors.YELLOW, 170, 100, "None")

        #Animation Variables
        self.timerInit          = False
        self.timerStart         = timer()
        self.animate            = False
        self.animate_left       = 0
        self.animate_top        = 0
        self.animate_width      = 0
        self.animate_height     = 0
        self.flash_done         = False

        # Sounds
        #self.incorrect_sound = pygame.mixer.Sound("resources/wrong.wav")
        #self.correct_sound   = pygame.mixer.Sound("resources/correct.wav")

    def DrawBoardBackground(self, screen):
        """Draw the background of the board."""

        boardRect = pygame.Rect([self.pos_x, self.pos_y, self.BOARD_WIDTH, self.BOARD_HEIGHT])
        pygame.draw.rect(screen, Colors.BLUE, boardRect)
        pygame.draw.rect(screen, Colors.BLACK, [self.pos_x, self.pos_y, self.BOARD_WIDTH, 5])

    def DrawNormal(self, screen):
        """Draw the board while in the Normal phase."""

        # Categories
        font = pygame.font.SysFont('Calibri', 16, True, False)
        for i in range(self.NUM_COLS+1):
            left    = self.pos_x + self.COL_WIDTH *i
            top     = self.pos_y
            width   = 5
            height  = self.ROW_HEIGHT
            pygame.draw.rect(screen, Colors.BLACK, [left, top, width, height])
            if i < self.NUM_COLS:
                text = font.render(self.parent.qset.category[i].title, True, Colors.YELLOW)
                screen.blit(text, [left+15, top+5.5])

        # Categories/questions seaparator
        pygame.draw.rect(screen, Colors.BLACK, [self.pos_x, self.pos_y + self.ROW_HEIGHT, self.BOARD_WIDTH + 5, self.SEPARATOR_HEIGHT])
        for i in range(self.NUM_QROWS+1):
            top     = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * i
            left    = self.pos_x
            width   = self.BOARD_WIDTH + 5
            height  = 5
            pygame.draw.rect(screen, Colors.BLACK, [left, top, width, height])

        # Draw the lines between columns
        for i in range(self.NUM_COLS+1):
            top     = self.pos_y + self.QY_OFFSET
            left    = self.pos_x + self.COL_WIDTH *i
            width   = 5
            height  = self.ROW_HEIGHT * self.NUM_QROWS
            pygame.draw.rect(screen, Colors.BLACK, [left, top, width, height])

        # Draw the dollar amounts that havent been revelead
        font = pygame.font.SysFont('ComicSans', 25, True, False)
        for r in range(self.NUM_QROWS):
            for c  in range(self.NUM_COLS):
                x = self.pos_x + self.COL_WIDTH*c + self.COL_WIDTH / 3
                y = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * r + self.ROW_HEIGHT / 2.5
                s = '${}'.format((r+1) * self.BASE_VALUE * self.app.cur_round)
                text = font.render(s, True, Colors.YELLOW)
                if r > 4-self.parent.qset.category[c].q_count:
                    screen.blit(text, [x, y])
 
    def flashQuestion(self, screen):
        offset = 5
        animate_width  = self.animate_right  - self.animate_left
        animate_height = self.animate_bottom - self.animate_top
        time_elapsed = self.parent.timer.time_elapsed()
        if time_elapsed < 0.2:
            pygame.draw.rect(screen, Colors.YELLOW, [self.animate_left+offset, self.animate_top+offset, animate_width-offset, animate_height-offset])
        elif time_elapsed < 0.4:
            pass
        elif time_elapsed < 0.6:
            pygame.draw.rect(screen, Colors.YELLOW, [self.animate_left+offset, self.animate_top+offset, animate_width-offset, animate_height-offset])
        elif time_elapsed < 0.8:
            pass
        elif time_elapsed < 1.0:
            pygame.draw.rect(screen, Colors.YELLOW, [self.animate_left+offset, self.animate_top+offset, animate_width-offset, animate_height-offset])
        elif time_elapsed < 1.2:
            pass
        elif time_elapsed < 1.4:
            pygame.draw.rect(screen, Colors.YELLOW, [self.animate_left+offset, self.animate_top+offset, animate_width-offset, animate_height-offset])
        elif time_elapsed < 1.6:
            pass
        elif time_elapsed < 1.8:
            pygame.draw.rect(screen, Colors.YELLOW, [self.animate_left+offset, self.animate_top+offset, animate_width-offset, animate_height-offset])
        elif time_elapsed < 2.0:
            pass
        else:
            max_y  = self.pos_y + self.BOARD_HEIGHT + 15
            max_x  = self.pos_x + self.BOARD_WIDTH + 5

            # Checks for which sides of the rectangle are still moving from question to screen edge.
            leftCheck   = True  # Is the left side of the rectangle still moving?
            rightCheck  = True  # Is the right side of the rectangle still moving?
            topCheck    = True  # Is the top side of the rectangle still moving?
            bottomCheck = True  # Is the bottom side of the rectangle still moving?

            # We want to hit the sides by the end of the timer
            perc_time_remaining = (2.5 - time_elapsed) / 0.5
            animate_left   = self.pos_x + (self.animate_left   - self.pos_x) * perc_time_remaining
            animate_top    = self.pos_y + (self.animate_top    - self.pos_y) * perc_time_remaining # Calculate the current top side
            animate_right  = max_x - (max_x  - self.animate_right) * perc_time_remaining
            animate_bottom = max_y - (max_y  - self.animate_bottom) * perc_time_remaining

            if animate_left <= self.pos_x:
                leftCheck = False
                animate_left = self.pos_x

            if animate_top <= self.pos_y:
                topCheck = False
                animate_top = self.pos_y

            if animate_right >= max_x:
                rightCheck = False
                animate_right = max_x
                
            if animate_bottom >= max_y:
                bottomCheck = False
                animate_bottom = max_y
            
            animate_width  = animate_right - animate_left
            animate_height = animate_bottom - animate_top

            pygame.draw.rect(screen, Colors.YELLOW, [animate_left, animate_top, animate_width, animate_height])
            if not leftCheck and not rightCheck and not topCheck and not bottomCheck:
                self.parent.question_phase = Phase.SHOW_QUESTION
                self.parent.qset.category[self.parent.curr_question[0]].q_count -= 1
                self.parent.timer.start(10) # 10 second timer to answer the question

    def DrawShowQuestion(self, screen):
        """Draw the board while in the SHOW_QUESTION phase."""

        lineSpace = 25
        lineWrapped = 0 

        timeLeft = self.parent.timer.time_left()
        timeLeft = max(timeLeft, 0) # Minimum of 0 seconds left for printing

        remainder = True
        if len(self.parent.qa.question) % 25 == 0:
            remainder = False
        
        lineWrapped = 0

        font = pygame.font.SysFont('Calibri', 34, True, False)
        s = "Timer: %.2f Seconds Left!"  % timeLeft
        text = font.render(s, True, Colors.YELLOW)
        screen.blit(text, [self.pos_x+15, self.pos_y+30])

        questionWords = self.parent.qa.question.split(" ")
        printLines = []

        lineWrite = ""
        for word in questionWords:
            lineWrite += (word + " ")
            if len(lineWrite) >= 25:
                if lineWrapped < 6:
                    printLines.append(lineWrite)
                    lineWrite = ""
                    lineWrapped += 1
                else:
                    remainder = True
        if remainder:
            printLines.append(lineWrite)
            lineWrapped += 1

        lineNum = 0
        for line in printLines:
            if lineNum == 0:        
                s = "Question: %s" % line
                text = font.render(s, True, Colors.YELLOW)
                screen.blit(text, [self.pos_x+15, self.pos_y+80])
                lineNum += 1
            else:
                s = line
                text = font.render(s, True, Colors.YELLOW)
                screen.blit(text, [self.pos_x+20, self.pos_y+80+(lineSpace*lineNum)])
                lineNum += 1

        s = "Value: $%i" % self.parent.qa.value
        text = font.render(s, True, Colors.YELLOW)
        screen.blit(text, [self.pos_x+15, self.pos_y+100+(lineSpace*lineNum)])

        self.show_answer_button = Button(self.pos_x+60,  self.pos_y+140+(lineSpace*lineNum), Colors.YELLOW, 350, 100, "Show Answer")
        self.show_answer_button.Draw(screen, 60)

    def DrawShowAnswer(self, screen):
        font = pygame.font.SysFont('Calibri', 34, True, False)
        lineWrapped = 0
        lineSpace = 25

        remainder = True
        if len(self.parent.qa.question) % 25 == 0:
            remainder = False
        questionWords = self.parent.qa.answer.split(" ")
        printLines = []

        lineWrite = ""
        for word in questionWords:
            lineWrite += (word + " ")
            if len(lineWrite) >= 25:
                if lineWrapped < 6:
                    printLines.append(lineWrite)
                    lineWrite = ""
                    lineWrapped += 1
                else:
                    remainder = True
        if remainder:
            printLines.append(lineWrite)
            lineWrapped += 1


        lineNum = 0
        for line in printLines:
            if lineNum == 0:
                s = "Answer: %s" % line
                text = font.render(s, True, Colors.YELLOW)
                screen.blit(text, [self.pos_x+15, self.pos_y+20])
                lineNum += 1
            else:
                s = line
                text = font.render(s, True, Colors.YELLOW)
                screen.blit(text, [self.pos_x+20, self.pos_y+20+(lineSpace*lineNum)])
                lineNum += 1

        """Draw the board while in the SHOW_ANSWER phase."""
        self.incorrect_button.Draw(screen, 30)
        self.correct_button.Draw(screen, 30)

    def DrawAskSpinToken(self, screen):
        """Draw the board while in the ASK_SPIN_TOKEN phase."""
        self.freespin_yes.Draw(screen, 30)
        self.freespin_no.Draw(screen, 30)
        font = pygame.font.SysFont('Calibri', 34, True, False)
        text = font.render("Use Your Free Token?", True, Colors.YELLOW)
        screen.blit(text, [self.pos_x+15, self.pos_y+20])

    def DrawChooseCategory(self, screen, player_choose):
        """Draw the board while in the OPPONENT_CHOOSE or PLAYER_CHOOSE phase."""

        font = pygame.font.SysFont('Calibri', 34, True, False)
        s = "Player Choose a Category!"
        if not player_choose:
            s = "Opponent Choose A Category!"
        text = font.render(s, True, Colors.YELLOW)
        screen.blit(text, [self.pos_x+15, self.pos_y+20])
        self.cat1_button = Button(self.pos_x+60,self.pos_y+70,  Colors.YELLOW, 170, 100,
                                  self.parent.qset.category[0].title)
        self.cat2_button = Button(self.pos_x+250,self.pos_y+70,  Colors.YELLOW, 170, 100,
                                  self.parent.qset.category[1].title)
        self.cat3_button = Button(self.pos_x+60,self.pos_y+185,  Colors.YELLOW, 170, 100,
                                  self.parent.qset.category[2].title)
        self.cat4_button = Button(self.pos_x+250,self.pos_y+185,  Colors.YELLOW, 170, 100,
                                  self.parent.qset.category[3].title)
        self.cat5_button = Button(self.pos_x+60,self.pos_y+300,  Colors.YELLOW, 170, 100,
                                  self.parent.qset.category[4].title)
        self.cat6_button = Button(self.pos_x+250,self.pos_y+300,  Colors.YELLOW, 170, 100,
                                  self.parent.qset.category[5].title)
        self.cat1_button.Draw(screen, 25)
        self.cat2_button.Draw(screen, 25)
        self.cat3_button.Draw(screen, 25)
        self.cat4_button.Draw(screen, 25)
        self.cat5_button.Draw(screen, 25)
        self.cat6_button.Draw(screen, 25)

    def startAnimation(self):
        self.animate_top     = self.pos_y + self.QY_OFFSET + (self.ROW_HEIGHT * (self.parent.curr_question[1]))
        self.animate_left    = self.pos_x + (self.COL_WIDTH * self.parent.curr_question[0])
        self.animate_bottom  = self.animate_top + self.ROW_HEIGHT
        self.animate_right   = self.animate_left + self.COL_WIDTH

    def ProcessUiEvent(self, event):
        # Special event keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.app.restart()
            if event.key == pygame.K_2:
                self.app.kill()

        if self.parent.question_phase == Phase.SHOW_QUESTION:
            if event.type == pygame.MOUSEMOTION:
                if self.show_answer_button.isHighlighted(pygame.mouse.get_pos()):
                    self.show_answer_button.color = Colors.PURPLE
                else:
                    self.show_answer_button.color = Colors.YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_answer_button.isHighlighted(pygame.mouse.get_pos()):
                    self.parent.question_phase = Phase.SHOW_ANSWER

        elif self.parent.question_phase == Phase.SHOW_ANSWER:
            if event.type == pygame.MOUSEMOTION:
                if self.correct_button.isHighlighted(pygame.mouse.get_pos()):
                    self.correct_button.color = Colors.PURPLE
                else:
                    self.correct_button.color = Colors.YELLOW
                if self.incorrect_button.isHighlighted(pygame.mouse.get_pos()):
                    self.incorrect_button.color = Colors.PURPLE
                else:
                    self.incorrect_button.color = Colors.YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.correct_button.isHighlighted(pygame.mouse.get_pos()):
                    self.app.questionResult(True, self.parent.qa.value, False, self.parent.questionsRemaining())
                    self.parent.question_phase = Phase.NORMAL
                    #self.correct_sound.play()

                if self.incorrect_button.isHighlighted(pygame.mouse.get_pos()):
                    #self.incorrect_sound.play()
                    if self.app.curPlayerTokenCount() <= 0:
                        self.app.questionResult(False, self.parent.qa.value, False,  self.parent.questionsRemaining())
                        self.parent.question_phase = Phase.NORMAL
                    else:
                        self.parent.question_phase = Phase.ASK_SPIN_TOKEN
        elif self.parent.question_phase == Phase.ASK_SPIN_TOKEN:
            if event.type == pygame.MOUSEMOTION:
                if self.freespin_yes.isHighlighted(pygame.mouse.get_pos()):
                    self.freespin_yes.color = Colors.PURPLE
                else:
                    self.freespin_yes.color = Colors.YELLOW

                if self.freespin_no.isHighlighted(pygame.mouse.get_pos()):
                    self.freespin_no.color = Colors.PURPLE
                else:
                    self.freespin_no.color = Colors.YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.freespin_yes.isHighlighted(pygame.mouse.get_pos()):
                    self.app.questionResult(False, self.parent.qa.value, True,  self.parent.questionsRemaining())
                if self.freespin_no.isHighlighted(pygame.mouse.get_pos()):
                    self.app.questionResult(False ,self.parent.qa.value, False,  self.parent.questionsRemaining())
                self.parent.question_phase = Phase.NORMAL

        elif self.parent.question_phase == Phase.PLAYER_CHOICE or self.parent.question_phase == Phase.OPPONENT_CHOICE:
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
        self.app             = app
        self.qa              = QASet("", "", -1)
        self.ui              = BoardUI(self, app, 320, 0)
        self.qset            = RoundSet()
        self.roundNum        = 0
        self.timer           = Timer()
        self.question_phase  = Phase.NORMAL
        self.curr_question = [0,0]
        self.animate_x       = 0
        self.animate_y       = 0

    def startRound(self, roundNum, round_qset):
        self.qset     = round_qset
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
            if category.q_count > 0:
                q_pos    = 5-category.q_count
                self.curr_question = [section, q_pos]
                question = category.question[q_pos]
                answer   = category.answer[q_pos]
                value = (q_pos+1)*200*self.roundNum
                self.displayQuestion(question, answer, value)
            else:
                # Shouldn't happen
                print("Out of questions, spinning again!")
                self.app.noQuestionsInCategory()
        else:
            print("Bad category %i" % section)

    def opponentSelectsCategory(self):
        self.question_phase = Phase.OPPONENT_CHOICE

    def playerSelectsCategory(self):
        self.question_phase = Phase.PLAYER_CHOICE

    def displayQuestion(self, q_text, q_answer, value):
        self.qa = QASet(q_text, q_answer, value)
        self.question_phase = Phase.ANIMATION
        self.timer.start(2.5) # Start 2.5 second animation timer
        self.ui.startAnimation()

    def Draw(self, screen):

        # Draw the background first.
        self.ui.DrawBoardBackground(screen)

        # Change what is drawn based on the phase
        if self.question_phase == Phase.NORMAL:
            self.ui.DrawNormal(screen)
        elif self.question_phase == Phase.SHOW_QUESTION:

            # Start the timer if it hasn't already been started
            timeLeft = self.timer.time_left()
            if timeLeft <= 0:
                if self.app.curPlayerTokenCount() <= 0:
                    self.app.questionResult(False, self.qa.value, False, self.questionsRemaining())
                    self.question_phase = Phase.NORMAL
                else:
                    self.question_phase = Phase.ASK_SPIN_TOKEN

            self.ui.DrawShowQuestion(screen)
        elif self.question_phase == Phase.SHOW_ANSWER:
            self.ui.DrawShowAnswer(screen)
        elif self.question_phase == Phase.ASK_SPIN_TOKEN:
            self.ui.DrawAskSpinToken(screen)
        elif self.question_phase == Phase.PLAYER_CHOICE or self.question_phase == Phase.OPPONENT_CHOICE:
            player_choose = True if self.question_phase == Phase.PLAYER_CHOICE else False
            self.ui.DrawChooseCategory(screen, player_choose)
        elif self.question_phase == Phase.ANIMATION:
            self.ui.DrawNormal(screen) # Start with a normal screen, then add animations on top
            self.processAnimation(screen)
        else:
            # Invalid question_phase
            pass

    def processAnimation(self, screen):
        time_left = self.timer.time_left()
        if time_left <= 0:
            self.question_phase = Phase.SHOW_QUESTION
            self.qset.category[self.curr_question[0]].q_count -= 1
            self.timer.start(10) # 10 second timer to answer the question
        else:
            self.ui.flashQuestion(screen)     

    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)
