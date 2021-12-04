import random
import socket
import threading
import game


NONE = '.'
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

        won_by_red = 0  # variables
        won_by_yellow = 0
        rounds = 0
        rounds_per_match = []
        for index in range(int(games_to_win)):  # runs on all games.
            g = game.Game()
            turn = RED
            while True:
                rounds += 1
                g.printBoard()

                client_column = conn.recv(1024).decode(FORMAT)  # received column from user
                print(f"Received from client column wanted #{client_column}")
                w_c = g.insert(int(client_column), RED)
                if w_c:  # if we received a winner from the game
                    if w_c == YELLOW:  # if yellow we update
                        won_by_yellow += 1
                    else:  # else its red
                        won_by_red += 1

                    print(
                        f"the game was finished in {rounds} rounds, the winner of game # {str(index + 1)} was {w_c}")  # update about who won the game and in how many rounds
                    print(
                        f"the current score is {won_by_red} - {won_by_yellow}")  # updates the current score of the game so far.
                    rounds_per_match.append(rounds)
                    rounds = 0  # sets the rounds counter back to 0
                    winner_message = "yellow" if w_c == YELLOW else "red"  # sets who won to send back to user.

                    conn.send(winner_message.encode(FORMAT))  # sends the message back to the user.
                    break  # if the game had a winner we break the while loop and go on to the next match.
                else:
                    g.printBoard()
                    print("computers turn:")
                    if int(difficulty) == 1 or rounds == 1:
                        computer_column = random.randint(0, 6)
                    else:
                        computer_column = get_smart_column(g)

                    w = g.insert(int(computer_column), YELLOW)

                    if w:  # if we received a winner from the game
                        if w == YELLOW:  # if yellow we update
                            won_by_yellow += 1
                        else:  # else its red
                            won_by_red += 1

                        print(
                            f"the game was finished in {rounds} rounds, the winner of game # {str(index + 1)} was {w}")  # update about who won the game and in how many rounds
                        print(
                            f"the current score is {won_by_red} - {won_by_yellow}")  # updates the current score of the game so far.
                        rounds_per_match.append(rounds)
                        rounds = 0  # sets the rounds counter back to 0
                        winner_message = "yellow" if w == YELLOW else "red"  # sets who won to send back to user.

                        conn.send(winner_message.encode(FORMAT))  # sends the message back to the user.
                        break  # if the game had a winner we break the while loop and go on to the next match.
                    else:
                        conn.send(str(computer_column).encode(FORMAT))  # if no winner was elected we just send the column that was selected by computer.
        if won_by_red > won_by_yellow:
            print("you won total match!")
        elif won_by_yellow == won_by_red:
            print("match was concluded at a tie !")
        else:
            print("computer won total match!")
        rounds_average = sum(rounds_per_match) / len(rounds_per_match)
        print(f"this game rounds average was {rounds_average}")
        print(f" that game covered {round(g.get_percentage_board(),2) } of the board ")
        results = g.get_highest()
        print(f" in that game the highest column was {results[1]} and it was of height {(-1) * int(results[0])}")


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
    column = random.randint(0, 6)
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
