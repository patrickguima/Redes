
import subprocess
import sys



import pygame
import os
import time
from client import Network
import pickle
pygame.font.init()


rect = (113,113,525,525)

turn = "x"
WIDTH = 700
HEIGHT = 700

def menu_screen(win, name):
	global bo, chessbg
	run = True
	offline = False

	while run:
	
		win.fill([0,0,0])
		small_font = pygame.font.SysFont("comicsans", 50)
		click = small_font.render("Click To Play", 1, (255, 0, 0))
		
		if offline:
			off = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
			win.blit(off, (width / 2 - off.get_width() / 2, 500))
			click = small_font.render("", 1, (0, 0, 0))
	   
		win.blit(click, (width / 2 - click.get_width() / 2, 500))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				offline = False
				try:
					bo = connect()
					run = False
					main()
					break
				except:
					print("Server Offline")
					offline = True


	
def redraw_gameWindow(win, bo, p1, p2, color, ready):
	#bo.draw(win, color)
	#bo.draw(win)
	win.fill([0,0,0])

	formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
	formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
	if int(p1%60) < 10:
		formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
	if int(p2%60) < 10:
		formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

	font = pygame.font.SysFont("comicsans", 25)
	if bo.ready:
		try:
			txt = font.render(bo.p1Name + "\'s Time: " + str(formatTime2), 1, (255, 255, 255))
			txt2 = font.render(bo.p2Name + "\'s Time: " + str(formatTime1), 1, (255,255,255))
		except Exception as e:
			print(e)
		win.blit(txt, (720,70))
		win.blit(txt2, (720, 100))

	

	
	if not bo.ready:
		show = "Waiting for Player"
		font = pygame.font.SysFont("comicsans", 80)
		txt = font.render(show, 1, (255, 0, 0))
		win.blit(txt, (width/2 - txt.get_width()/2, 300))
	else:
		txt = font.render("Press q to Quit", 1, (255, 255, 255))
		win.blit(txt, (720, 10))
	
		font = pygame.font.SysFont("comicsans", 30)
		if color == "x":
			txt3 = font.render("YOU ARE RED", 1, (255, 0, 0))
			win.blit(txt3, ((width-100) - txt3.get_width() / 2, 40))
		
		else:
			txt3 = font.render("YOU ARE BLACK", 1, (255, 0, 0))
			win.blit(txt3, ((width-100)  - txt3.get_width() / 2, 40))

		if color==bo.user:
			txt3 = font.render("YOUR TURN", 0, (255, 0, 0))
			win.blit(txt3, ((width-100) - txt3.get_width() / 2, 680))
		else:
			txt3 = font.render("THEIR TURN", 1, (255, 0, 0))
			win.blit(txt3, ((width-100) - txt3.get_width() / 2, 680))
		txt4 = font.render("SCORE", 1, (255, 0, 0))
		txt5 = font.render("RED " + str(bo.scoreP1), 1, (255, 0, 0))
		txt6 = font.render("BLACK " + str(bo.scoreP2), 1, (255, 0, 0))
		win.blit(txt4, ((width-100) - txt3.get_width() / 2, 200))
		win.blit(txt5, ((width-100) - txt3.get_width() / 2, 250))
		win.blit(txt6, ((width-100) - txt3.get_width() / 2, 280))
		bo.draw(win)
	pygame.display.flip()


def end_screen(win, text):
	win.fill([0,0,0])
	pygame.font.init()
	font = pygame.font.SysFont("comicsans", 80)
	txt = font.render(text,1, (255,0,0))
	win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
	pygame.display.update()

	pygame.time.set_timer(pygame.USEREVENT+1, 3000)

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				run = False
			elif event.type == pygame.KEYDOWN:
				run = False
			elif event.type == pygame.USEREVENT+1:
				run = False


def click(pos):
	
	x = pos[0]
	y = pos[1]
	if rect[0] < x < rect[0] + rect[2]:
		if rect[1] < y < rect[1] + rect[3]:
			divX = x - rect[0]
			divY = y - rect[1]
			i = int(divX / (rect[2]/8))
			j = int(divY / (rect[3]/8))
			return i, j

	return -1, -1


def connect():
	global n
	n = Network()
	return n.board
def board_to_string(board):
	string_board = ""
	for b in board:
		for x in b:
			string_board +=x

	print(string_board)
def get_clicked_column(mouse_pos):
	x = mouse_pos[0]
	for i in range(1, 8):
		if x < i * WIDTH / 8:
			return i - 1
	return 7

def get_clicked_row(mouse_pos):
	y = mouse_pos[1]
	for i in range(1, 8):
		if y < i * HEIGHT / 8:
			return i - 1
	return 7

def main():
	global turn, bo, name

	color = bo.start_user
	
	count = 0
	reconnect = True

	
	bo = n.send("name " + name)
	print(color)
	clock = pygame.time.Clock()
	run = True

	while run:
		
		p1Time = bo.time1
		p2Time = bo.time2
		if count == 60:
			bo = n.send("get")
			count = 0
		else:
			count += 1
		clock.tick(30)

		try:
			
			redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
			
			
		except Exception as e:
			print(e)
			end_screen(win, "Other player left")
			run = False
			break



		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				reconnect = False
				if color == "x":
					bo = n.send("winner o")
				else:
					bo = n.send("winner x")
				run = False 
				quit()
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					reconnect=False
					if color == "x":
						bo = n.send("winner o")
					else:
						bo = n.send("winner x")
			if event.type == pygame.MOUSEBUTTONUP:
				if color == bo.user and bo.ready:
					#print("OI")
					mouse_x, mouse_y = pygame.mouse.get_pos()
			
					row, column = get_clicked_row(pygame.mouse.get_pos()), get_clicked_column(pygame.mouse.get_pos())

					bo = n.send("select " + str(row) + " " + str(column))	

	
		if p1Time <= 0:
			bo = n.send("winner x")
		elif p2Time <= 0:
				bo = n.send("winner o")


		if bo.winner == "x":
			if color=="x":

				end_screen(win, "You Win")
			else:
				end_screen(win, "You Lost")
			run = False
		elif bo.winner == "o":
			if color=="o":
				end_screen(win, "You Win")
			else:
				end_screen(win, "You Lost")
			run = False

	n.disconnect()
	bo = 0
	if reconnect:
		menu_screen(win,name)


name = input("Please type your name: ")
#name = "patrick"
width = 900
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Checkers Game")
menu_screen(win, name)
