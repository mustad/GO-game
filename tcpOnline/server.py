
# python /Users/mustafajaffar/Documents/GO/tcpOnline/server.py

import threading
import socket


host = '127.0.0.1' # local host
port = 12902 # the port ill be using

# creating the server with tcp layer and binding it with max
# attempts until rejecting new connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

# holds the usernames
clients = []
nicknames = []

# commands recienved from each players 
commands = {'black': [],
            'white': []}

turn = 0

# distributing the message to all clients/users
def broadcast(message):
    global turn

    # all clients get the message 
    for client in clients: #black client first, then white
        client.send(message)

    # if it was blacks message, we add it to blacks message queue
    if turn % 2 == 0:
        commands['black'].append(message.decode('ascii'))
        
    # if it was white who sent message, we send it to white qeueu
    else:
        commands['white'].append(message.decode('ascii'))
        
    print(commands)
    turn += 1
    
def handle(client):
    while True:
        try:
            # as long as we get a conneciton, we broadcast it to all clients
            message = client.recv(1024)
            broadcast(message)

        except:
            # if the client exits, we remove the client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('this man has left'.encode('ascii'))
            nicknames.remove(nickname)
            break

# accept people connecting to server and 
def recieve():
    while True:
        # when user connects
        client, address = server.accept()
        print("connected with", address)

        # add client to the server and into the usernames and client list
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        commands[nickname] = []

        joined = nickname + ' joined'
        broadcast(joined.encode('ascii'))

        # create a new thread for the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()
        






            
