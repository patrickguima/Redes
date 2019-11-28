import pygame
import math
import random
import time
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN = (150, 255, 150)
#GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)
TRANS    = (   1,   2,   3)

# CONSTANTS:
WIDTH = 700
HEIGHT = 700
MARK_SIZE = 50

table = pygame.image.load('images/tabuleiro.png')
table = pygame.transform.scale(table,[705,705])
piece_player1 = pygame.image.load('images/red.png')
piece_player1 = pygame.transform.scale(piece_player1,[80,80])
piece_player2 = pygame.image.load('images/black.png')
piece_player2 = pygame.transform.scale(piece_player2,[100,100])

piece_player1_crown = pygame.image.load('images/red_crown.png')
piece_player1_crown = pygame.transform.scale(piece_player1_crown,[80,80])
piece_player2_crown = pygame.image.load('images/black_crown.png')
piece_player2_crown = pygame.transform.scale(piece_player2_crown,[100,100])



class Checker:
	"""class to keep track of the status of the game."""
	def __init__(self):
		"""
		Start a new game with an empty board
		"""
		self.ready = False

		self.last = None
		self.copy = True
		self.p1Name = "Player 1"
		self.p2Name = "Player 2"
		self.turn = 0
		self.start_user = "x"
		self.user = "x"
		self.time1 = 30
		self.time2 = 30
		self.storedTime1 = 30
		self.storedTime2 = 30
		self.winner = None
		self.startTime = time.time()
		self.scoreP1 = 0
		self.scoreP2 = 0
		self.status = 'playing'
		#self.turn = random.randrange(2)
		self.players = ['x','o']
		self.players_colors = ['Red','Black']
		self.selected_token = None
		self.jumping = False
		pygame.display.set_caption("%s's turn" % self.players_colors[self.turn % 2])
		
		self.game_board = [['x','-','x','-','x','-','x','-'],
							['-','x','-','x','-','x','-','x'],
							['x','-','x','-','x','-','x','-'],
							['-','-','-','-','-','-','-','-'],
							['-','-','-','-','-','-','-','-'],
							['-','o','-','o','-','o','-','o'],
							['o','-','o','-','o','-','o','-'],
							['-','o','-','o','-','o','-','o']]

		#self.game_board = [['-','-','-','-','-','-','-','-'],
		#					['-','-','-','-','-','-','-','-'],
		#					['-','-','-','-','-','-','x','-'],
		#					['-','-','-','-','-','-','-','-'],
		#					['-','-','-','-','-','-','-','-'],
		#					['-','o','-','o','-','o','-','o'],
		#					['o','-','o','-','o','-','o','-'],
		#				['-','o','-','o','-','o','-','o']]

	def evaluate_click(self, row,column,color):
		"""
		Select a token if none is selected.
		Move token to a square if it is a valid move.
		Start a new game if the game is over.
		"""
		if self.status == 'playing':
			#row, column = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
			if self.selected_token:
				move = self.is_valid_move(self.players[self.turn % 2], self.selected_token, row, column)
				if move[0]:
					self.play(self.players[self.turn % 2], self.selected_token, row, column, move[1])
				elif row == self.selected_token[0] and column == self.selected_token[1]:
					self.selected_token = None
					if self.jumping:
						self.jumping = False
						self.next_turn()
				else:
					print ('invalid move')
			else:
				if self.game_board[row][column].lower() == self.players[self.turn % 2]:
					self.selected_token = [row, column]
		elif self.status == 'game over':
			self.__init__()

	def is_valid_move(self, player, token_location, to_row, to_col):
		"""
		Check if clicked location is a valid square for player to move to.
		"""
		from_row = token_location[0]
		from_col = token_location[1]
		token_char = self.game_board[from_row][from_col]
		if self.game_board[to_row][to_col] != '-':
			return False, None
		if (((token_char.isupper() and abs(from_row - to_row) == 1) or (player == 'x' and to_row - from_row == 1) or
			 (player == 'o' and from_row - to_row == 1)) and abs(from_col - to_col) == 1) and not self.jumping:
			return True, None
		if (((token_char.isupper() and abs(from_row - to_row) == 2) or (player == 'x' and to_row - from_row == 2) or
			 (player == 'o' and from_row - to_row == 2)) and abs(from_col - to_col) == 2):
			jump_row = int((to_row - from_row) / 2 + from_row)
			jump_col = int((to_col - from_col) / 2 + from_col)
			print("comeu")
			print("row col",jump_row,jump_col)
			if self.user =="x":
				self.scoreP1 +=1
			else:
				self.scoreP2+=1
			if self.game_board[jump_row][jump_col].lower() not in [player, '-']:
				return True, [jump_row, jump_col]
		return False, None

	def play(self, player, token_location, to_row, to_col, jump):
		"""
		Move selected token to a particular square, then check to see if the game is over.
		"""
		from_row = token_location[0]
		from_col = token_location[1]
		token_char = self.game_board[from_row][from_col]
		self.game_board[to_row][to_col] = token_char
		self.game_board[from_row][from_col] = '-'
		if (player == 'x' and to_row == 7) or (player == 'o' and to_row == 0):
			self.game_board[to_row][to_col] = token_char.upper()
		if jump:
			self.game_board[jump[0]][jump[1]] = '-'
			self.selected_token = [to_row, to_col]
			self.jumping = True
		else:
			self.selected_token = None
			self.next_turn()
		self.winner = self.check_winner()
		winner = None
		if winner is None:
			pygame.display.set_caption("%s's turn" % self.players_colors[self.turn % 2])
		elif winner == 'draw':
			pygame.display.set_caption("It's a stalemate! Click to start again")
			self.status = 'game over'
		else:
			pygame.display.set_caption("%s wins! Click to start again" % winner)
			self.status = 'game over'

	def next_turn(self):
		self.turn += 1
		pygame.display.set_caption("%s's turn" % self.players_colors[self.turn % 2])

		if self.user == "x":
				self.user = "o"
		else:
			self.user ="x"

	def check_winner(self):
		"""
		check to see if someone won, or if it is a draw.
		"""
		x = sum([row.count('x') + row.count('X') for row in self.game_board])
		if x == 0:
			return 'o'
		o = sum([row.count('o') + row.count('O') for row in self.game_board])
		if o == 0:
			return 'x'
		if x == 1 and o == 1:
			return 'draw'
		return None

	def draw(self,screen):
		"""
		Draw the game board and the X's and O's.
		"""
		for i in range(9):
			pygame.draw.line(screen, BLACK, [i * WIDTH / 8, 0], [i * WIDTH / 8, HEIGHT], 5)
			pygame.draw.line(screen, BLACK, [0, i * HEIGHT / 8], [WIDTH, i * HEIGHT / 8], 5)
		font = pygame.font.SysFont('Calibri', MARK_SIZE, False, False)
		screen.blit(table,(WIDTH/2 -352,HEIGHT/2 -353))
		for r in range(len(self.game_board)):
			for c in range(len(self.game_board[r])):
				mark = self.game_board[r][c]
				if self.players[self.turn % 2] == mark.lower():
					color = YELLOW
				else:
					color = WHITE
				if self.selected_token:
					if self.selected_token[0] == r and self.selected_token[1] == c:
						color = RED
						
				if mark != '-':
					mark_text = font.render(self.game_board[r][c], True, color)
					x = WIDTH / 8 * c + WIDTH / 16
					y = HEIGHT / 8 * r + HEIGHT / 16
					if color ==RED:
						pygame.draw.rect(screen,
							 GREEN,
							 [x-85/2,
								y-87/2,
							 87,
							  87])


					screen.blit(mark_text, [x - mark_text.get_width()/ 2, y - mark_text.get_height() / 2])
					if mark =='x':
						screen.blit(piece_player1, [x - mark_text.get_width()-40/ 2, y - mark_text.get_height() -10/ 2])
					if mark =='X':
						screen.blit(piece_player1_crown, [x - mark_text.get_width()-40/ 2, y - mark_text.get_height() -10/ 2])
					if mark == 'o':
						screen.blit(piece_player2, [x - mark_text.get_width()-55/ 2, y - mark_text.get_height() -30/ 2])
					if mark == 'O':
						screen.blit(piece_player2_crown, [x - mark_text.get_width()-55/ 2, y - mark_text.get_height() -30/ 2])

		pygame.display.update()
