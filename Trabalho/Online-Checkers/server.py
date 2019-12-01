import socket
from _thread import *
import pickle
import time
from checkers import *
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.0.107"
port = 5005
server_ip = socket.gethostbyname(server)

try:
	s.bind((server, port))

except socket.error as e:
	print(str(e))

s.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0: Checker()}




def threaded_client(conn, game):
	global pos, games, currentId, connections

	
	name = None
	bo = games[game]

	if connections % 2 == 0:
		currentId = "x"
		turn = 0
	else:
		currentId = "o"
		

	bo.start_user = currentId
	
		# Pickle the object and send it to the server
	data_string = pickle.dumps(bo)

	if currentId == "o":
		bo.ready = True
		#bo.user= "s"
		bo.startTime = time.time()

	conn.send(data_string)
	connections += 1

	while True:
		if game not in games:
			break

		try:
			d = conn.recv(8192 * 3)
			data = d.decode("utf-8")
			if not d:
				break
			else:
				if data.count("select") > 0:
					all = data.split(" ")
					row = int(all[1])
					col = int(all[2])
					#color = all[3]
					#print("id",currentId)
					bo.evaluate_click(row, col)
					#print(col,row)

				if data == "winner x":
					bo.winner = "x"
					print("[GAME] Player o won the game", game)
				if data == "winner o":
					bo.winner = "o"
					print("[GAME] Player x won the game", game)


				if data.count("name") == 1:
					name = data.split(" ")[1]
					if currentId == "o":
						bo.p2Name = name
					elif currentId == "x":	
						bo.p1Name = name

					#print("Recieved board fros", currentId, "in game", game)

				if bo.ready:
					if bo.user == bo.start_user:
						if(time.time()-bo.startTime >=1):
							bo.time1-=1
							bo.startTime = time.time()

						bo.time2 = 30
					else:
						if(time.time()-bo.startTime >=1):
						
							bo.time2-=1
							bo.startTime = time.time()

						bo.time1 = 30 

				sendData = pickle.dumps(bo)
					#print("Sending board to player", currentId, "in game", game)

			conn.sendall(sendData)

		except Exception as e:
			print(e)
		
	connections -= 1
	try:
		del games[game]
		print("[GAME] Game", game, "ended")
	except:
		pass
	print("[DISCONNECT] Player", name, "left game", game)
	conn.close()



while True:
	if connections < 6:
		conn, addr = s.accept()
		g = -1
		print("[CONNECT] New connection")

		for game in games.keys():
			if games[game].ready == False:
				g=game

		if g == -1:
			try:
				g = list(games.keys())[-1]+1
				
				games[g] = Checker()
			except:
				g = 0
				
				games[g] = Checker()


		print("[DATA] Number of Connections:", connections+1)
		print("[DATA] Number of Games:", len(games))

		start_new_thread(threaded_client, (conn,g))
