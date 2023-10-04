import socket
import threading
import pickle
from util import *

def bs_server_main():

   
    host = socket.gethostname()
    port = 5000  

    serverSock = socket.socket()  

    serverSock.bind((host, port))
    firstClientThread, secondClientThread = spawn_clients()

    clientConns = connect_clients(serverSock)
    boards = recv_board(clientConns)
    winner = play_game(clientConns, boards)

    print("Game over, player {} wins".format(winner))

    clientConns[0].close()
    clientConns[1].close()


def play_game(clientConns, boards):

    player = 0

    while True:

        clientConns[player].send("ur turn".encode())

        handle_move(clientConns, player, boards)

        # print boards
        print("Player 0 board")
        boards[0].print_board()
        print("Player 1 board")
        boards[1].print_board()
        # check for win condition
        if boards[(player + 1)%2].all_ships_sunk() is True:

            clientConns[player].send("game over u win".encode())
            clientConns[(player + 1)%2].send("game over u lose".encode())
            
            return player
        
        if player == 0:
            player = 1
        else:
            player = 0




def handle_move(clientConns, player, boards):

    data = clientConns[player].recv(4096)
    coordGuess = pickle.loads(data)
    boards[(player + 1)%2].handle_coord_guess(coordGuess)


    

    
    
def recv_board(clientConns):

    dataOne = clientConns[0].recv(4096)
    dataTwo = clientConns[1].recv(4096)

    boardPlayerOne = pickle.loads(dataOne)
    boardPlayerTwo = pickle.loads(dataTwo)

    boards = []
    boards.append(boardPlayerOne)
    boards.append(boardPlayerTwo)
    
    
    return boards

def connect_clients(serverSock):


    serverSock.listen(2)
    
    conns = []
    numClients = 0
    
    while numClients < 2:
        conn, address = serverSock.accept()

        numClients += 1
        conns.append(conn)
    return conns
    
def spawn_clients():

    firstClientThread = threading.Thread(target = bs_client, args=(0,))
    secondClientThread = threading.Thread(target = bs_client, args=(1,))
    firstClientThread.start()
    secondClientThread.start()
    
    return firstClientThread, secondClientThread


def client_play(clientSock):

    clientBoard = Board(10,10)
    clientSock.send(pickle.dumps(clientBoard))

    
    while True:
        serverMsg = clientSock.recv(4096).decode()
        

        if serverMsg == "game over u lose":
            return "lose :("
        if serverMsg == "game over u win":
            return "win :D"

        if serverMsg == "ur turn":
            xGuess = rand.randint(0,9)
            yGuess = rand.randint(0,9)
            clientSock.send(pickle.dumps((xGuess,yGuess)))
        

def bs_client(clientNumber):
    
    host = socket.gethostname()
    port = 5000 

    clientSock = socket.socket() 
    clientSock.connect((host, port))  

    result = client_play(clientSock)

    clientSock.close()

def main():
    bs_server_main()


if __name__ == '__main__':
    main()



