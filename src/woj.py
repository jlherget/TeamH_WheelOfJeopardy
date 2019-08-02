import start
import queue
import pygame
import data_editor
import ui_utils
import gamescreen

CAT_1 = 0
CAT_2 = 1
CAT_3 = 3
CAT_4 = 4
CAT_5 = 5
CAT_6 = 6
FREE_SPIN = 7
LOSE_TURN = 8
CHOOSE_CAT = 9
OPPONENT_CHOOSE_CAT = 10
DOUBLE_SCORE = 11
BANKRUPT = 12

class WoJ():

    def __init__(self):
        pygame.init()
        self.queue              = queue.Queue()
        self.running            = True
        self.num_players        = 1
        self.spins_remaining    = 0
        self.cur_round          = 0
        self.players            = []
        
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

    def showDataEdtior(self):
        self.current_screen = self.editor_screen

    def showStartScreen(self):
        self.current_screen = self.start_screen

    def startGame(self, num_players, game_qset):
        """Start the game with the given question/answer set and the number of players"""
        self.current_screen = self.game_screen
        self.num_players    = num_players
        self.game_qset      = game_qset
        self.spinsRemaining = 50
        self.startRound(1)
    
    def startRound(self, round_num):
        self.cur_round = round_num
        self.game_screen.startRound(round_num, self.game_qset.getRound(round_num))

    def curPlayerTokenCount(self):
        """Reurn the number of tokens the current player has"""
        #return cur_player.spinTokens;
        return 0;
    
    def wheelResult(self, section):
        self.spinsRemaining -= 1

        if section >= CAT_1 and section <= CAT_6:
            print("Category %i section" % section)
            #self.game_screen.selectCategory(section)
        elif section == FREE_SPIN:
            print("Free spin section")
            #self.cur_player.grantSpinToken()
        elif section == LOSE_TURN:
            print("Lose turn section")
            if self.curPlayerTokenCount() > 0:
                #self.game_screen.askToUseToken()
                pass
        elif section == CHOOSE_CAT:
            print("Choose cat section")
            #self.game_screen.playerSelectsCategory()
        elif section == OPPONENT_CHOOSE_CAT:
            print("Opponent choose cat section")
            #self.game_screen.opponentSelectsCategory()
        elif section == DOUBLE_SCORE:
            print("Double score section")
            #self.cur_player.scoreDouble()
        elif section == BANKRUPT:
            print("Bankrupt section")
            #self.cur_player.bankrupt()
        else:
            print("Error! Invalid section %i" % section)
            pass

    def selectedCategory(self, cat):
        """The user's category choice has been selected"""
        #self.game_screen.selectCategory(section)
        pass

    def questionResult(self, result):
        if result.answeredCorrectly:
            #self.cur_player.addScore(result.value)
            pass
        else:
            self.cur_player.addScore(-result.value)
            if result.usedToken:
                #self.cur_player.useToken()
                pass
            else:
                self.cur_player_index = self.cur_player_index % self.num_players
                self.cur_player = self.players[self.cur_player_index]

    def roundEnd(self):
        """Process the end of a round"""
        if self.cur_round == 1:
            for player in self.players:
                #player.roundEnd()
                pass
            self.startRound(2)
        else:
            self.gameEnd()

    def gameEnd(self):
        print("Game over")


    @staticmethod
    def main():
        app = WoJ()
        app.run()
        pygame.quit()

    def PostMessage(self, message):
        self.queue.put(message)

if __name__ == '__main__':
    WoJ.main()
