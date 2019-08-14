from wheel    import Section
from ui_utils import Colors, SCREEN_SIZE

import start
import pygame
import data_editor
import gamescreen
import player


class WoJ():
    """This class will run the game. 
    
    It instantiates the other classes and stores game state information. This class receives events 
    from the other subsystems and handles them appropriately. The main class is also responsible for
    keeping track of the current screen being displayed to the user.  It will be in charge of reading
    UI events (such as clicking buttons) off of the event queue and sending the events to the correct 
    subsystem.

    """

    def __init__(self):
        pygame.init()
        self.running            = True          # Set to false to close the application.
        self.num_players        = 1             # Number of players in the game.
        self.spinsRemaining     = 0             # Number of spins remaining in the round.
        self.cur_round          = 0             # Current round number. 1 Based.
        self.players            = []            # List of player objects for the current game.
        self.game_over          = False         # Flag to indicate the game has ended.

        # Set mode before creating the WoJ screens
        self.screen             = pygame.display.set_mode(SCREEN_SIZE) # pygame screen object to draw on

        self.start_screen       = start.Start(self)             # StartScreen
        self.game_screen        = gamescreen.GameScreen(self)   # GameScreen (contains Board, Wheel, and Scoreboard)
        self.editor_screen      = data_editor.DataEditor(self)  # DataEditor

        self.current_screen     = self.start_screen     # Current screen to display. Initialize to start screen.

    
    def run(self):
        """Starts the application.
        
        Starts the infinite loop while the application is running.
        Event time through the loop will attempt to pull events
        off the event queue and execute the approach action.

        Args:
            None
        Return:
            None.

        """

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
            self.screen.fill(Colors.GRAY)

            # Draw the current screen
            self.current_screen.Draw(self.screen)

            # Draw moving logo
            teamHLogo.draw( self.screen )

            # Draw the new screen
            pygame.display.flip()

            # Draw at 60Hz
            clock.tick(60)

    def showDataEdtior(self):
        """Sets the current screen to the data editor.
        
        The data editor screen will be shown until another screen is selected to be shown,
        typically the start screen.

        """
        self.current_screen = self.editor_screen

    def showStartScreen(self):
        """Sets the current screen to the start screen.
        
        The start screen will be shown until another screen is selected to be shown, 
        typically either when the game starts or the data editor screen is shown.

        """
        self.current_screen = self.start_screen
        self.game_over      = False

    def startGame(self, num_players, game_qset):
        """Starts the game.
        
        Initializes the players, the board, and the wheel.
        The first player’s turn starts immediately after initialization.
        
        Args:
            num_players: Number of players. Integer. Range: [1,4]
            game_qset:   GameSet object that holds all the questions
                         and answers for the game.
        Returns:
            None.
        
        """
        self.current_screen = self.game_screen
        self.num_players    = num_players
        self.players        = [player.Player() for i in range(num_players)]
        self.cur_player_index = 0
        self.game_qset      = game_qset
        self.startRound(1)

    def startRound(self, round_num):
        """Start the round.

        Initialize the game screen elements with the next round of data.

        Args:
            round_num - The round number. Integer. Range [1,2].

        """
        self.game_screen.wheel.enableSpin()
        self.cur_round = round_num
        self.game_screen.startRound(round_num, self.game_qset.getRound(round_num-1))
        self.spinsRemaining = 50

    def curPlayerTokenCount(self):
        """Get the number of free spin tokens the current player has.
        
        Args:
            None
        Return:
            Number of free spin tokens the current player has.
        
        """
        return self.players[self.cur_player_index].playerTokenCount

    def wheelResult(self, section):
        """Accept the result of the wheel landing on a section. 
        
        Each section may be handled differently.
        
        Args:
            section - The section the board landed one. Section object.
        
        """
        self.spinsRemaining -= 1

        if section == Section.CAT_1:
            print("Category %i" % 1)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(0)

        elif section == Section.CAT_2:
            print("Category %i" % 2)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(1)

        elif section == Section.CAT_3:
            print("Category %i" % 3)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(2)

        elif section == Section.CAT_4:
            print("Category %i" % 4)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(3)
            
        elif section == Section.CAT_5:
            print("Category %i" % 5)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(4)

        elif section == Section.CAT_6:
            print("Category %i" % 6)
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.sendQuestion(5)

        elif section == Section.FREE_SPIN:
            print("Free spin section")
            self.players[self.cur_player_index].grantSpinToken()
            self.nextPlayer()
            self.startNextTurn()

        elif section == Section.LOSE_TURN:
            print("Lose turn section")
            if self.curPlayerTokenCount() > 0:
                self.game_screen.board.qa.value = 0
                self.game_screen.board.ui.question_phase = 3
            else:
                self.nextPlayer()
                self.startNextTurn()

        elif section == Section.CHOOSE_CAT:
            print("Player choose category section")
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.playerSelectsCategory()

        elif section == Section.OPPONENT_CHOOSE_CAT:
            print("Opponent choose cateogry section")
            self.game_screen.wheel.disableSpin()
            self.game_screen.board.opponentSelectsCategory()

        elif section == Section.DOUBLE_SCORE:
            print("Double score section")
            self.players[self.cur_player_index].doubleScore()
            self.nextPlayer()
            self.startNextTurn()

        elif section == Section.BANKRUPT:
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
        """Change current player to the next player.

        If current player is the last player, move to the first player

        """
        self.cur_player_index = (self.cur_player_index + 1) % self.num_players

    def startNextTurn(self):
        """Start the next turn by allowing the player to spin the wheel.

        If there are no spins remaining, end the round, which may end the
        game.

        """
        if self.spinsRemaining <= 0:
            self.roundEnd()
        else:
            self.game_screen.wheel.enableSpin()

    def questionResult(self, answered_correctly, net_amount, free_token_used, questions_left):
        """Accept the result of the user answering a question.
        
        If the player answered correctly, the question value is added to the player’s score and they may spin again.
        If the player answers incorrectly, the question value is deducted from the player’s score. 
            If the player used a spin token, they may spin again.
            Otherwise, play moves to the next player.
        If there are no questions remaining, the round ends.

        Args:
            answered_correctly - True indicates player answered the question correctly.
            net_amount         - Value of the question.
            free_token_used    - Indicate player used a free spin token if they answered incorrectly.
            question_left      - Indicates number of quesitons left on the board.
        Returns:
            None

        """
        if answered_correctly:
            self.players[self.cur_player_index].addPoints(net_amount)
        else:
            self.players[self.cur_player_index].addPoints(-net_amount)
            if free_token_used:
                self.players[self.cur_player_index].useSpinToken()
            else:
                self.nextPlayer()

        if questions_left <= 0:
            self.roundEnd()
        else:
            self.startNextTurn()

    def roundEnd(self):
        """Process the end of a round.
        
        The end of the first round starts the second round.
        Otherwise, the game is over.
        
        """
        end_of_round = pygame.mixer.Sound("resources/endofround.wav")
        end_of_round.play()

        if self.cur_round == 1:
            for p in self.players:
                p.roundEnd()
            self.startRound(2)
        else:
            self.gameEnd()

    def noQuestionsInCategory(self):
        """Handle when the selected category has no questions left.

        Instead of receiving a quesiton result, the category that was selected
        has no questions left. In this case, the current player is allowed to
        spin again. If there are no spins left in the round, the round ends.

        """
        print("NO QUESTIONS REMAINING IN CATEGORY - Spin Again")
        self.startNextTurn()

    def gameEnd(self):
        """End the game.

        User is no longer allowed to spin the wheel.

        """
        self.game_screen.wheel.disableSpin()
        self.game_over = True
        print("Game over")

    def kill(self):
        """Completely close the application.

        Termiantes the infinite loop.

        """
        self.running = False
        print("KILLING APP")

    def restart(self):
        """Return to the start screen."""
        self.current_screen = self.start_screen
        self.game_over = False
        print("RESTATING APP")

    @staticmethod
    def main():
        """Start the Wheel of Jeopardy application"""
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
