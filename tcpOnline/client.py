import socket
import threading

# gets username from users end 
nickname = raw_input('name: ')

# holds the recieved and sent text from the client
writ = []
rec = []

# create client with tcp
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',12902))

# recieving text from server
def recieve():
    while True:
        try:
            # when the user gets a message from the server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
                
        except:
            # if it doesnt happen we present the error
            print('error')
            client.close()
            break

# sending text to server
def write():
    while True:
        message = raw_input('enter: ')
        client.send(message.encode('ascii'))

# starting the recieve thread we can send and recieve at the same time
recieve_thread = threading.Thread(target = recieve)
recieve_thread.start()

# starting the wrtie thread, we can send and recieve at the same time
write_thread = threading.Thread(target = write)
write_thread.start()



