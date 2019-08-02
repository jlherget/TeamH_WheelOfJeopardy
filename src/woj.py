import start
import queue
import pygame
import data_editor
import ui_utils
import gamescreen
import player


CAT_6 = 11
FREE_SPIN = 10
CAT_5 = 9
LOSE_TURN = 8
CAT_4 = 7
DOUBLE_SCORE = 6
CAT_3 = 5
BANKRUPT = 4
CAT_2 = 3
OPPONENT_CHOOSE_CAT = 2
CAT_1 = 1
CHOOSE_CAT = 0

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
        self.players        = [player.Player() for i in range(num_players)]
        self.cur_player_index = 0
        self.game_qset      = game_qset
        self.spinsRemaining = 50
        self.startRound(1)
    
    def startRound(self, round_num):
        self.cur_round = round_num
        self.game_screen.startRound(round_num, self.game_qset.getRound(round_num))

    def curPlayerTokenCount(self):
        """Reurn the number of tokens the current player has"""
        return self.players[self.cur_player_index].playerTokenCount
    
    def wheelResult(self, section):
        self.spinsRemaining -= 1

        if section == CAT_1:
            print("Category %i" % 1)
            self.game_screen.board.sendQuestion(0)
        elif section == CAT_2:
            print("Category %i" % 2)
            self.game_screen.board.sendQuestion(1)
        elif section == CAT_3:
            print("Category %i" % 3)
            self.game_screen.board.sendQuestion(2)
        elif section == CAT_4:
            print("Category %i" % 4)
            self.game_screen.board.sendQuestion(3)
        elif section == CAT_5:
            print("Category %i" % 5)
            self.game_screen.board.sendQuestion(4)
        elif section == CAT_6:
            print("Category %i" % 6)
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
            self.game_screen.board.playerSelectsCategory()
        elif section == OPPONENT_CHOOSE_CAT:
            print("Opponent choose cat section")
            self.game_screen.board.opponentSelectsCategory()
        elif section == DOUBLE_SCORE:
            print("Double score section")
            self.players[self.cur_player_index].doubleScore()
            self.nextPlayer()
            self.startNextTurn()
        elif section == BANKRUPT:
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
                self.players[self.cur_player_index].useToken()
            else:
                self.nextPlayer()
        self.startNextTurn()

    def roundEnd(self):
        """Process the end of a round"""
        if self.cur_round == 1:
            for p in self.players:
                p.roundEnd()
            self.startRound(2)
        else:
            self.gameEnd()

    def noQuestionsInCategory(self):
        self.game_screen.wheel.enableSpin()

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
