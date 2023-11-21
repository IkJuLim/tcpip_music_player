import multiprocessing
import socket
import threading
from start_music import start_music


class Client:
    prev_music = ""
    current_music = ""
    next_music = ""
    current_command = ""

    def set_music(self, prev_music, current_music, next_music):
        self.prev_music = prev_music
        self.current_music = current_music
        self.next_music = next_music

    def get_prev_music(self):
        return self.prev_music

    def get_current_music(self):
        return self.current_music

    def get_next_music(self):
        return self.next_music

    def set_command(self, command):
        self.current_command = command

    def get_command(self):
        return self.current_command


def send(sock, client):
    print('Thread send() Start\n')
    while True:
        message = str(input())
        command = message[:4]
        if command == "list":
            send_list(sock)
        elif command == "prev":
            prev_cmd(sock, client)
        elif command == "play":
            play_cmd(sock, client, message[5:])
        elif command == "next":
            next_cmd(sock, client)
        elif command == "stop":
            stop_cmd(client)
        elif command == "help":
            display_cmd()
        else:
            bad_request()


def send_list(sock):
    sock.send("list".encode(FORMAT))


def prev_cmd(sock, client):
    send_play(sock, client.get_prev_music())


def play_cmd(sock, client, music):
    send_play(sock, music)


def next_cmd(sock, client):
    send_play(sock, client.get_next_music())


def send_play(sock, music):
    sock.send(("play " + music).encode(FORMAT))


def stop_cmd(client):
    global music_process
    music_process.terminate()


def display_cmd():
    print("commands : \n" +
          "list         : Display play list\n" +
          "prev         : Play previous music on play list\n" +
          "play <name>  : Play music that you choosed\n" +
          "next         : Play next music on play list\n" +
          "stop         : Stop music\n" +
          "help         : Display all commands")


def bad_request():
    print("bad request\n" +
          "commands : \n" +
          "list         : Display play list\n" +
          "prev         : Play previous music on play list\n" +
          "play <name>  : Play music that you choosed\n" +
          "next         : Play next music on play list\n" +
          "stop         : Stop music\n" +
          "help         : Display all commands")


def recv(sock, client):
    print('Thread recv() Start\n')
    while True:
        message = sock.recv(SIZE)
        print(message)
        message = message.decode(FORMAT)
        command = message[:4]
        if command == "list":
            print(message[5:])
        elif command == "play":
            music = message[5:].split(" ")
            client.set_music(music[0], music[1], music[2])
            recv_file(sock, client)


def recv_file(sock, client):
    file_data = b""

    while True:
        data = sock.recv(SIZE)
        print(data)
        if data == "<END>".encode():
            break
        file_data = file_data + data
        sock.send("Data received".encode())

    global music_process
    music_process = multiprocessing.Process(target=start_music, args=(file_data, ))
    music_process.start()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SERVER = input("IP:")
    PORT = int(input("PORT:"))

    ADDR = (SERVER, PORT)

    FORMAT = "utf-8"
    SIZE = 32768
    sock.connect(ADDR)

    print(f'Connecting to {SERVER}:{PORT}')
    client = Client()
    beep_data = open("./src/beep_sound.wav", "rb").read()
    global music_process
    music_process = multiprocessing.Process(target=start_music, args=(beep_data, ))
    music_process.start()

    sendthread = threading.Thread(target=send, args=(sock, client,))
    sendthread.start()

    recvthread = threading.Thread(target=recv, args=(sock, client,))
    recvthread.start()
