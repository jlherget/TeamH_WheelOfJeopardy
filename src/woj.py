import start
import pygame
import data_editor
import ui_utils
import gamescreen
import player

# Define the sectors. This is the order of the categories
# in the wheel image.
CAT_6               = 11
FREE_SPIN           = 10
CAT_5               = 9
LOSE_TURN           = 8
CAT_4               = 7
DOUBLE_SCORE        = 6
CAT_3               = 5
BANKRUPT            = 4
CAT_2               = 3
OPPONENT_CHOOSE_CAT = 2
CAT_1               = 1
CHOOSE_CAT          = 0

class WoJ():

    def __init__(self):
        pygame.init()
        self.running            = True
        self.num_players        = 1
        self.spinsRemaining     = 0
        self.cur_round          = 0             # 1 Based
        self.players            = []
        self.game_over          = False

        # Set mode before creating the WoJ screens
        self.screen             = pygame.display.set_mode(ui_utils.SCREEN_SIZE)

        self.start_screen       = start.Start(self)
        self.game_screen        = gamescreen.GameScreen(self)
        self.editor_screen      = data_editor.DataEditor(self)

        self.current_screen     = self.start_screen

    
    def run(self):
        jeopardy_sound = pygame.mixer.Sound("resources/Jeopardy_Music.wav")
        jeopardy_sound.play()
        # This sets the name of the window
        pygame.display.set_caption('Wheel of Jeopardy')
        clock = pygame.time.Clock()
        print("After Start, Press 1 to Restart, Press 2 to Kill")
        teamHLogo = logo( 10, 650, 50, 50, 830 )

        while self.running:

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

            # Draw moving logo
            teamHLogo.draw( self.screen )

            # Draw the new screen
            pygame.display.flip()

            # Draw at 60Hz
            clock.tick(60)

    def showDataEdtior(self):
        self.current_screen = self.editor_screen

    def showStartScreen(self):
        self.current_screen = self.start_screen
        self.game_over = False

    def startGame(self, num_players, game_qset):
        """Start the game with the given question/answer set and the number of players"""
        self.current_screen = self.game_screen
        self.num_players    = num_players
        self.players        = [player.Player() for i in range(num_players)]
        self.cur_player_index = 0
        self.game_qset      = game_qset
        self.startRound(1)

    def startRound(self, round_num):
        self.game_screen.wheel.enableSpin()
        self.cur_round = round_num
        self.game_screen.startRound(round_num, self.game_qset.getRound(round_num-1))
        self.spinsRemaining = 2

    def curPlayerTokenCount(self):
        """Reurn the number of tokens the current player has"""
        return self.players[self.cur_player_index].playerTokenCount

    def wheelResult(self, section):
        self.spinsRemaining -= 1

        if section == CAT_1:
            print("Category %i" % 1)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(0)
        elif section == CAT_2:
            print("Category %i" % 2)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(1)
        elif section == CAT_3:
            print("Category %i" % 3)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(2)
        elif section == CAT_4:
            print("Category %i" % 4)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(3)
        elif section == CAT_5:
            print("Category %i" % 5)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(4)
        elif section == CAT_6:
            print("Category %i" % 6)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(5)
        elif section == FREE_SPIN:
            print("Free spin section")
            self.players[self.cur_player_index].grantSpinToken()
            self.nextPlayer()
            self.startNextTurn()
        elif section == LOSE_TURN:
            print("Lose turn section")
            if self.curPlayerTokenCount() > 0:
                self.game_screen.board.qa.value = 0
                self.game_screen.board.ui.question_phase = 3
            else:
                self.nextPlayer()
                self.startNextTurn()
        elif section == CHOOSE_CAT:
            print("Choose cat section")
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.playerSelectsCategory()
        elif section == OPPONENT_CHOOSE_CAT:
            print("Opponent choose cat section")
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.opponentSelectsCategory()
        elif section == DOUBLE_SCORE:
            print("Double score section")
            self.players[self.cur_player_index].doubleScore()
            self.nextPlayer()
            self.startNextTurn()
        elif section == BANKRUPT:
            bankrupt_sound = pygame.mixer.Sound("resources/bankrupt.wav")
            bankrupt_sound.play()
            print("Bankrupt section")
            self.players[self.cur_player_index].bankrupt()
            self.nextPlayer()
            self.startNextTurn()
        else:
            print("Error! Invalid section %i" % section)
            pass

    def nextPlayer(self):
        self.cur_player_index = (self.cur_player_index + 1) % self.num_players

    def startNextTurn(self):
        if self.spinsRemaining <= 0:
            self.roundEnd()
        else:
            self.game_screen.wheel.enableSpin()

    def questionResult(self, result):
        if result.getResult():
            self.players[self.cur_player_index].addPoints(result.getNetAmount())
        else:
            self.players[self.cur_player_index].addPoints(-result.getNetAmount())
            if result.getFreeTokenUsed():
                self.players[self.cur_player_index].useSpinToken()
            else:
                self.nextPlayer()
        self.startNextTurn()

    def roundEnd(self):
        """Process the end of a round"""
        
        end_of_round = pygame.mixer.Sound("resources/endofround.wav")
        end_of_round.play()
        if self.cur_round == 1:
            for p in self.players:
                p.roundEnd()
            self.startRound(2)
        else:
            self.gameEnd()

    def noQuestionsInCategory(self):
        print("NO QUESTIONS REMAINING IN CATEGORY - Spin Again")
        self.game_screen.wheel.enableSpin()


    def gameEnd(self):
        self.game_screen.wheel.disableSpin()
        self.game_over = True
        print("Game over")

    def kill(self):
        self.running = False
        print("KILLING APP")

    def restart(self):
        self.current_screen = self.start_screen
        self.game_over = False
        print("RESTATING APP")

    @staticmethod
    def main():
        app = WoJ()
        app.run()
        pygame.quit()

class logo( object ):

    teamH = pygame.transform.scale(pygame.image.load("resources/logo.png"), [60,50])

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = 5

    def draw(self, screen):
        self.move()
        screen.blit(self.teamH,(self.x,self.y) )

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel

            else:
                self.vel = self.vel * -1

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel

            else:
                self.vel = self.vel * -1

if __name__ == '__main__':
    WoJ.main()
