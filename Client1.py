import socket
import time

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
            print(f"game {index} started!")
            while True:
                rounds += 1
                print(f"round number :{rounds}")
                wanted_column = input("Please enter the number of column you would like to put in:")
                client_socket.send(wanted_column.encode(FORMAT))

                time.sleep(1)

                data = client_socket.recv(1024).decode(FORMAT)  # Receiving winner/ column from computer

                if data == "yellow" or data == "red":
                    if data == "yellow":
                        won_by_yellow += 1
                    else:
                        won_by_red += 1
                    print(f"the game was finished in {rounds} rounds, the winner of game # {index + 1} was {data}")
                    print(f"the current score is {won_by_red} - {won_by_yellow}")
                    rounds_per_match.append(rounds)
                    rounds = 0
                    break
                else:
                    print(f"[RECEIVED DATA] computer pick: {data}\n")  # Printing recieved data from server
        if won_by_red > won_by_yellow:
            print("you won total match!")
        elif won_by_yellow == won_by_red:
            print("match was concluded at a tie !")
        else:
            print("computer won total match!")

        rounds_average = sum(rounds_per_match) / len(rounds_per_match)
        print(f"this game rounds average was {rounds_average}")


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
