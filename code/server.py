
# python3 /Users/mustafajaffar/Documents/GO/code/server.py

import threading
import socket
import myLibrary as lib
import json
import ast
import time

host = '127.0.0.1' # local host
port = 14030 # the port ill be using

# creating the server with tcp layer and binding it with max
# attempts until rejecting new connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

# holds the usernames and thier data
clients = []
nicknames = []
usernames = []
#? for users icons
userIcons = {}

# commands recienved from each players 
commands = {}
turn = 0

#? game queue to be able to match players

games = []
numPlayers = 0

# distributing the message to all clients/users
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    global numPlayers
    global usernames
    global userIcons

    while True:
        try:
            # as long as we get a message, we broadcast it to all clients
            message = client.recv(1024)
            message = message.decode('ascii')

            #? tell all other clients to increase the number of waiting users
            
            if message == 'extra player added':
                numPlayers += 1
                print(numPlayers)
                message1 = 'extra player added'
                message1 = message1.encode('ascii')
                broadcast(message1)

            #? if two new users, send user dtaa tto the clients
            if numPlayers == 2:
                gameData = {'user1': usernames[0],
                            'user2': usernames[1],
                            'icon1': userIcons[usernames[0]],
                            'icon2': userIcons[usernames[1]]
                            }
                gameData = str(gameData)
                #? add command word so client knows what data this is
                message2 = 'newGameData' + gameData
                message2 = message2.encode('ascii')
                broadcast(message2)

                #? make numPlayers = 0 as this will stop the infinite loop
                numPlayers = 0
            
            #? if the clients has sent userData, store it
            if message[:8] == 'userData':
                userData = ast.literal_eval(message[8:])
                usernames.append(userData['username'])
                userIcons[ userData['username'] ] = userData['icon']
                print(usernames)
                print(userIcons)

        except:
            # if the client exits, we remove the client
            index = clients.index(client)
            #clients.remove(client)
            #client.close()
            nickname = nicknames[index]
            #broadcast('this man has left'.encode('ascii'))
            #nicknames.remove(nickname)
            pass

# accept people connecting to server and 
def recieve():
    while True:
        # when user connects

        client, address = server.accept()
        print("connected with", address)
        print('the client is', clients)

        # add client to the server and into the usernames and client list
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        joined = nickname + 'joined'
        broadcast(joined.encode('ascii'))
        client.send(joined.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()
lsof -n -i

