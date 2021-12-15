import random
import socket
import threading
import game

NONE = '-'
RED = 'R'
YELLOW = 'Y'
HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 60000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


# Function that handles a single client connection
# Operates like an echo-server
def handle_client1(conn, addr):
    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address
    mode_to_run = conn.recv(1024).decode(FORMAT)  # gets from client the mode of game
    if int(mode_to_run) == 1:  # if 1 just leaves.
        print("\n[CLIENT DISCONNECTED] on address: ", addr)

    elif int(mode_to_run) == 2:  # if 2 we play vs computer
        difficulty = conn.recv(1024).decode(FORMAT)  # get difficulty
        games_to_win = conn.recv(1024).decode(FORMAT)  # gets num of game to win
        for index in range(int(games_to_win)):  # runs on all games.
            g = game.Game()
            while True:
                g.printBoard()
                client_column = conn.recv(1024).decode(FORMAT)  # received column from user
                print(f"Received from client column wanted #{client_column}")
                w_c = g.insert(int(client_column), RED)
                if w_c:
                    break
                print("computers turn:")
                if int(difficulty) == 1:
                    computer_column = random.randint(0, 6)
                else:
                    computer_column = get_smart_column(g)

                conn.send(str(computer_column).encode(FORMAT))

                w = g.insert(int(computer_column), YELLOW)
                if w:
                    break



def get_smart_column(game):  # receives the input column of the computer by looking for another yellow
    l = list(range(7))
    random.shuffle(l)
    for column in l:
        c = game.board[column]
        if c[0] == NONE:
            i = -1
            while c[i] != NONE:
                i -= 1
            if c[i + 1] == YELLOW:
                return column
    while True:
        column = random.randint(0, 6)
        c = game.board[column]
        if c[0] == NONE:
            return column


def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections
    while True:
        if threading.activeCount() == 1:  # Checking if no clients connected to the server client in total
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working
        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
        if threading.active_count() <= 5:
            connection.send("hello there".encode(FORMAT))
            thread = threading.Thread(target=handle_client1, args=(connection, address))  # Creating new Thread object.
            thread.start()  # Starting the new thread (<=> handling new client)
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")
        else:
            print("too many Clients are logged in try again later.")
            connection.send("hello".encode(FORMAT))
            connection.close()


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket

    print("[STARTING] server is starting...")
    start_server()

    print("THE END!")
