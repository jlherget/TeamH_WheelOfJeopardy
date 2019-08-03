import board
import ui_utils
import pygame

class Scoreboard():

    def __init__(self, app):
        self.app     = app
        self.ui      = ScoreboardUI(app, 0, board.BoardUI.BOARD_HEIGHT+10)

    def Draw(self, screen):
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        pass

class ScoreboardUI():

    def __init__(self, app, pos_x, pos_y):
        self.app    = app
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.width  = 700
        self.height = 40*5+6

    def Draw(self, screen):

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
        pygame.draw.rect(screen, ui_utils.PURPLE, boardRect)

        #Column dividers
        for col in range(6):
            x = self.pos_x + col*col_width
            y = self.pos_y
            pygame.draw.rect(screen, ui_utils.WHITE, [x, y, divider_width, self.height])
            pygame.draw.rect(screen, ui_utils.WHITE, [x, y, divider_width, self.height])

        #Column headers
        text = font.render('Round 1', True, ui_utils.WHITE)
        screen.blit(text, [col1_start+col_width+xtext_offset, row1_start+ytext_offset])
        text = font.render('Round 2', True, ui_utils.WHITE)
        screen.blit(text, [col1_start+2*col_width+xtext_offset, row1_start+ytext_offset])
        text = font.render('Total', True, ui_utils.WHITE)
        screen.blit(text, [col1_start+3*col_width+xtext_offset, row1_start+ytext_offset])
        text = font.render('Spin Tokens', True, ui_utils.WHITE)
        screen.blit(text, [col1_start+4*col_width+xtext_offset, row1_start+ytext_offset])

        #Row dividers
        for row in range(6):
            x = col1_start
            y = row1_start + row_height*row
            pygame.draw.rect(screen, ui_utils.WHITE, [x, y, self.width, divider_width])

        for i in range(self.app.num_players):
            y = row1_start + (i+1)*row_height + ytext_offset

            player_text = 'Player %i' % (i+1)
            x = col1_start + xtext_offset
            text = font.render(player_text, True, ui_utils.WHITE)
            screen.blit(text, [x, y])

            round1_text = '$%i' % self.app.players[i].playerRoundScore[0]
            text = font.render(round1_text, True, ui_utils.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            round2_text = '$%i' % self.app.players[i].playerRoundScore[1]
            text = font.render(round2_text, True, ui_utils.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            total_text = '$%i' % (self.app.players[i].finalScore())
            text = font.render(total_text, True, ui_utils.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            tokens_text = '%i' % self.app.players[i].playerTokenCount
            text = font.render(tokens_text, True, ui_utils.WHITE)
            x += col_width
            screen.blit(text, [x, y])

            y = row1_start
            x += col_width

        if self.app.game_over:
            text = font.render('GAME OVER', True, ui_utils.WHITE)
            screen.blit(text, [x,y+50])

            if self.checkTie():
                text = font.render('Tie Game', True, ui_utils.WHITE)
                screen.blit(text, [x,y+100])
            else:
                text = font.render('Winner:', True, ui_utils.WHITE)
                screen.blit(text, [x,y+100])

                text = font.render('Player %i' % (self.findWinner()), True, ui_utils.WHITE)
                screen.blit(text, [x+50,y+125])

        else:
            text = font.render('Current Player', True, ui_utils.WHITE)
            screen.blit(text, [x,y])
            text = font.render('%i' % (self.app.cur_player_index+1), True, ui_utils.WHITE)
            screen.blit(text, [x+50,y+15])

            text = font.render('Current Round', True, ui_utils.WHITE)
            screen.blit(text, [x,y+50])
            text = font.render('%i' % (self.app.cur_round), True, ui_utils.WHITE)
            screen.blit(text, [x+50,y+65])

            text = font.render('Spins Remainig', True, ui_utils.WHITE)
            screen.blit(text, [x,y+100])
            text = font.render('%i' % (self.app.spinsRemaining), True, ui_utils.WHITE)
            screen.blit(text, [x+50,y+115])

    def checkTie(self):
        max = self.app.players[0].finalScore()
        tie = False
        for i in range(self.app.num_players):
            if self.app.players[i].finalScore() == max:
                tie = True
            if self.app.players[i].finalScore() > max:
                max = self.app.players[i].finalScore()
                winner = i
                tie = False
        return tie

    def findWinner(self):
        winner = 0
        max = self.app.players[0].finalScore()
        for i in range(self.app.num_players):
            if self.app.players[i].finalScore() > max:
                max = self.app.players[i].finalScore()
                winner = i
        return winner+1
