from ui_utils import Colors

import ui_utils
import pygame
import board

class Scoreboard():

    def __init__(self, app):
        self.app     = app
        self.ui      = ScoreboardUI(app, 160, board.BoardUI.BOARD_HEIGHT+10)

    def Draw(self, screen):
        """Draw the scoreboard onto the pygame screen."""
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        """Process user interface events.
        
        This class does not handle any user interface events.
        """
        pass

class ScoreboardUI():

    def __init__(self, app, pos_x, pos_y):
        self.app    = app
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.width  = 700
        self.height = 40*5+6

    def Draw(self, screen):
        """Draw the scoreboard onto the pygame screen."""

        divider_width = 6

        col_width  = 140
        col1_start = self.pos_x
        xtext_offset = 10

        row_height = 40
        row1_start = self.pos_y
        ytext_offset = 7
        font = pygame.font.SysFont('Calibri', 25, True, False)

        # Background for the scoreboard
        boardRect = pygame.Rect([self.pos_x, self.pos_y, self.width, row_height*5+divider_width])
        pygame.draw.rect(screen, Colors.BLUE, boardRect)

        #Column dividers
        for col in range(6):
            x = self.pos_x + col*col_width
            y = self.pos_y
            pygame.draw.rect(screen, Colors.WHITE, [x, y, divider_width, self.height])
            pygame.draw.rect(screen, Colors.WHITE, [x, y, divider_width, self.height])

        #Column headers
        text = font.render('Round 1', True, Colors.WHITE)
        screen.blit(text, [col1_start+col_width+xtext_offset, row1_start+ytext_offset])
        text = font.render('Round 2', True, Colors.WHITE)
        screen.blit(text, [col1_start+2*col_width+xtext_offset, row1_start+ytext_offset])
        text = font.render('Total', True, Colors.WHITE)
        screen.blit(text, [col1_start+3*col_width+xtext_offset, row1_start+ytext_offset])
        text = font.render('Spin Tokens', True, Colors.WHITE)
        screen.blit(text, [col1_start+4*col_width+xtext_offset, row1_start+ytext_offset])

        #Row dividers
        for row in range(6):
            x = col1_start
            y = row1_start + row_height*row
            pygame.draw.rect(screen, Colors.WHITE, [x, y, self.width, divider_width])

        for i in range(self.app.num_players):
            y = row1_start + (i+1)*row_height + ytext_offset

            player_text = 'Player %i' % (i+1)
            x = col1_start + xtext_offset
            text = font.render(player_text, True, Colors.WHITE)
            screen.blit(text, [x, y])

            round1_text = '$%i' % self.app.players[i].playerRoundScore[0]
            text = font.render(round1_text, True, Colors.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            round2_text = '$%i' % self.app.players[i].playerRoundScore[1]
            text = font.render(round2_text, True, Colors.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            total_text = '$%i' % (self.app.players[i].finalScore())
            text = font.render(total_text, True, Colors.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            tokens_text = '%i' % self.app.players[i].playerTokenCount
            text = font.render(tokens_text, True, Colors.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            y = row1_start
            x += col_width

        if self.app.game_over:
            text = font.render('GAME OVER', True, Colors.WHITE)
            screen.blit(text, [10,450])

            if self.checkTie():
                text = font.render('Tie Game', True, Colors.WHITE)
                screen.blit(text, [10,510])
            else:
                text = font.render('Winner:', True, Colors.WHITE)
                screen.blit(text, [10,510])

                text = font.render('Player %i' % (self.findWinner()), True, Colors.WHITE)
                screen.blit(text, [10,540])

        else:
            text = font.render('Current Player', True, Colors.WHITE)
            screen.blit(text, [10,450])
            text = font.render('%i' % (self.app.cur_player_index+1), True, Colors.WHITE)
            screen.blit(text, [70,480])

            text = font.render('Current Round', True, Colors.WHITE)
            screen.blit(text, [10,510])
            text = font.render('%i' % (self.app.cur_round), True, Colors.WHITE)
            screen.blit(text, [70,540])

            text = font.render('Spins Remaining', True, Colors.WHITE)
            screen.blit(text, [10,570])
            text = font.render('%i' % (self.app.spinsRemaining), True, Colors.WHITE)
            screen.blit(text, [68,600])

    def checkTie(self):
        """Check if there is a tie."""
        max = self.app.players[0].finalScore()
        tie = False
        for i in range(self.app.num_players):
            if self.app.players[i].finalScore() == max and i is not 0:
                tie = True
            if self.app.players[i].finalScore() > max:
                max = self.app.players[i].finalScore()
                tie = False
        return tie

    def findWinner(self):
        """Find the palyer with the best score."""
        winner = 0
        max = self.app.players[0].finalScore()
        for i in range(self.app.num_players):
            if self.app.players[i].finalScore() > max:
                max = self.app.players[i].finalScore()
                winner = i
        return winner+1
