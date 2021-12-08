import socket
import time
import game

NONE = '.'
RED = 'R'
YELLOW = 'Y'
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client():
    client_socket.connect((HOST, PORT))  # Connecting to server's socket
    welcome = client_socket.recv(1024).decode(FORMAT)
    if str(welcome) == "hello":
        print("there are too many users connected to the server at the time.")
        exit()
    else:
        print(f"[SERVER MESSAGE] {welcome}")
    wanted_mode = input("game mode: exit  (1), computer (2), PvP (3) ")  # receives from the user the mode of game
    client_socket.send(wanted_mode.encode(FORMAT))

    if int(wanted_mode) == 1:  # if the mode was 1 we close the client socket
        client_socket.close()  # Closing client's connection with server (<=> closing socket)
        print("\n[CLOSING CONNECTION] client closed socket!")

    elif int(wanted_mode) == 2:  # if the mode was 2 we play vs computer
        wanted_difficulty = input("difficulty:(1) easy, (2) hard")  # the user chooses difficulty
        client_socket.send(wanted_difficulty.encode(FORMAT))
        num_of_games = get_games()  # gets the amount of games that will need to be won to complete a match.
        client_socket.send(str(num_of_games).encode(FORMAT))
        won_by_red = 0  # variables to count
        won_by_yellow = 0
        rounds = 0
        rounds_per_match = []
        for index in range(num_of_games):  # runs for each game
            g = game.Game()
            print(f"game {index} started!")
            while True:
                rounds += 1
                g.printBoard()
                print(f"round number :{rounds}")
                wanted_column = input("Please enter the number of column you would like to put in:")
                client_socket.send(wanted_column.encode(FORMAT))
                w_c = g.insert(int(wanted_column), RED)
                if w_c:  # if we received a winner from the game
                    won_by_red += 1
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(
                        f"the game was finished in {rounds} rounds, the winner of game # {str(index + 1)} was {w_c}")  # update about who won the game and in how many rounds
                    print(
                        f"the current score is {won_by_red} - {won_by_yellow}")  # updates the current score of the game so far.
                    print(f" that game covered {round(g.get_percentage_board(), 2)} of the board ")
                    results = g.get_highest()
                    print(
                        f" in that game the highest column was {results[1]} and it was of height {(-1) * int(results[0])}")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    rounds_per_match.append(rounds)
                    rounds = 0  # sets the rounds counter back to 0
                    break  # if the game had a winner we break the while loop and go on to the next match.
                else:
                    g.printBoard()
                    print("computers turn:")

                    time.sleep(1)

                    computer_choice = client_socket.recv(1024).decode(FORMAT)  # Receiving winner/ column from computer
                    w = g.insert(int(computer_choice), YELLOW)
                    if w:  # if we received a winner from the game
                        won_by_yellow += 1
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print(
                            f"the game was finished in {rounds} rounds, the winner of game # {str(index + 1)} was {w}")  # update about who won the game and in how many rounds
                        print(
                            f"the current score is {won_by_red} - {won_by_yellow}")  # updates the current score of the game so far.
                        print(f" that game covered {round(g.get_percentage_board(), 2)} of the board ")
                        results = g.get_highest()
                        print(
                            f" in that game the highest column was {results[1]} and it was of height {(-1) * int(results[0])}")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        rounds_per_match.append(rounds)
                        rounds = 0  # sets the rounds counter back to 0
                        break  # if the game had a winner we break the while loop and go on to the next match.
                    else:
                        print(
                            f"[RECEIVED DATA] computer pick: {computer_choice}\n")  # Printing recieved data from server
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if won_by_red > won_by_yellow:
            print("you won total match!")
        elif won_by_yellow == won_by_red:
            print("match was concluded at a tie !")
        else:
            print("computer won total match!")

        rounds_average = sum(rounds_per_match) / len(rounds_per_match)
        print(f"this game rounds average was {rounds_average}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def get_games():  # receives the amount of games wanted to be played
    multiplier = 1
    while True:
        games_to_win = input("how many games are needed to win 1-5 (if you choose other u will be timed out)")
        if int(games_to_win) < 1 or int(games_to_win) > 5:
            print(f"wrong input now you wait for {10 * multiplier} seconds ")
            time.sleep(10 * multiplier)
            multiplier *= 2
        else:
            return int(games_to_win)


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")
