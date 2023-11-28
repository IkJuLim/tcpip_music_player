import socket
import os
import threading
import time

print_lock = threading.Lock()


def send(conn, message):
    print('Thread Send Start')
    command = message[:4]
    print(message)
    print(message[:4])
    print(message[5:])
    if command == "list":
        send_list(conn)
    elif command == "play":
        music = message[5:]
        print(music)
        send_play(conn, music)


def recv(conn):
    print('Thread Recv() Start\n')
    while True:
        message = conn.recv(SIZE).decode(FORMAT)
        print(f"RECEIVE([{SERVER}:{PORT}]{message})")
        send(conn, message)


def send_list(conn):
    files = os.listdir("../../Desktop/music_dir")
    cnt = 1
    message = "list|"
    for file in files:
        message = message + str(cnt) + " : " + os.path.splitext(os.path.basename(file))[0] + "\n"
        cnt = cnt + 1
    conn.send(message.encode(FORMAT))


def send_play(conn, music):
    files = os.listdir("../../Desktop/music_dir")
    filenames = []
    for file in files:
        filenames.append(os.path.splitext(os.path.basename(file))[0])
    if music not in filenames:
        return
    index = filenames.index(music)
    prev_music = filenames[index - 1]
    next_music = filenames[index + 1]
    message = "play|" + prev_music + "|" + music + "|" + next_music
    print(message)
    conn.send(message.encode(FORMAT))
    time.sleep(0.1)

    file_path = "./music_dir/" + music + ".wav"
    with open(file_path, "rb") as file:
        while True:
            data = file.read(SIZE)
            if not data:
                break
            conn.send(data)
            msg = conn.recv(SIZE).decode()
            print(msg)
    conn.send("<END>".encode(FORMAT))
    print("Done......")
    file.close()


if __name__ == '__main__':
    PORT = 6060

    SERVER = socket.gethostbyname(socket.gethostname())

    ADDR = (SERVER, PORT)
    print(f"※STARTING※\nserver is starting......\nserver adress : {SERVER}:{PORT}\n")

    SIZE = 32768
    FORMAT = "utf-8"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    server.listen()
    print(f"※LISTENING※\nserver is listening on {SERVER}\n")

    while True:
        conn, addr = server.accept()

        print(f"※NEW CONNECTION※\n{str(addr)} connected.")

        recvthread = threading.Thread(target=recv, args=(conn, ))
        recvthread.start()
