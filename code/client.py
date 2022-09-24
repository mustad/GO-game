# python3 /Users/mustafajaffar/Documents/GO/code/client.py

import socket
import threading
import json
import myLibrary as lib
import time
import ast

nickname = input("enter name: ")

# holds the recieved and sent text from the client
writ = []
rec = []

# create client with tcp
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',14030))

path = '/Users/mustafajaffar/Documents/GO/code/'

# recieving text from server
def recieve():
    global nickname
    while True:
        try:
            # when the user gets a message from the server
            message = client.recv(1024).decode('ascii')
            print(message)
            if message == 'NICK':
                print('nick is working on client')
                client.send(nickname.encode('ascii'))
            
            #? if a new user has entered the new game
            elif message == 'extra player added':
                complete = False
                while not complete:
                    try:
                        with open(path + 'numPlayers.json', 'r') as file:
                            data = json.loads(file.read())
                        data[0]['numPlayers'] += 1
                        lib.storeJson(data, "numPlayers.json")
                        complete = True
                    except:
                        pass
            
            #? if server sent the data of the two players for the new game
            elif 'newGameData' in message:
                #? get the dicitonary part of the message and turn to dictionary
                gameData = message[11:]
                gameDataa = ast.literal_eval(gameData)
                #? continually try to get the data until we get it
                complete = False
                while not complete:
                    try:
                        with open(path + 'currGame.json', 'r') as file:
                            data = json.loads(file.read())
                        data[0]['user1'] = gameDataa['user1']
                        data[0]['user2'] = gameDataa['user2']
                        data[0]['icon1'] = gameDataa['icon1']
                        data[0]['icon2'] = gameDataa['icon2']
                        lib.storeJson(data, "currGame.json") # store data in currGame so board can proccess this
                        complete = True
                    except:
                        pass
            
            else:
                if message:
                    print(message)

        except:
            # if it doesnt happen we present the error
            print('error')
            client.close()
            break

# sending text to server
def write():
    
    while True:
        
        #? get the current page the user is on
        gottenPage = False
        while not gottenPage:
            try:
                with open(path + 'currPage.json', 'r') as file:
                    data = json.loads(file.read())
                newGame = data[0]['newGame']
                inGame = data[0]['inGame']
                loadGame = data[0]['loadGame']
                accPage = data[0]['accPage']
                gottenPage = True
            except:
                pass
        
        #? if user has selected board for new game
        if newGame == 'True':
            print('this user has queed up')
            print('new game section runs in go client')
            message = 'extra player added'
            client.send(message.encode('ascii'))
            print('message sent')

            with open(path + 'currPage.json', 'r') as file:
                data = json.loads(file.read())
            data[0]['newGame'] = 'False'
            lib.storeJson(data,"currPage.json")
        
        #? if user just finished entering info
        elif accPage == 'True':
            complete = False
            while not complete:
                try:
                    #? get the user data 
                    with open(path + 'Settings.json', 'r') as file:
                        data = json.loads(file.read())
                    userData = {"username": data[0]['username'],
                                "icon": data[0]['icon']}

                    #? put user data in acceptaple format and send it
                    userData = str(userData)
                    message = 'userData' + userData
                    message = message.encode('ascii')
                    client.send(message)

                    #? reset the account page and set is back to false
                    with open(path + 'currPage.json', 'r') as file:
                        data = json.loads(file.read())
                    data[0]['accPage'] = 'False'
                    lib.storeJson(data, 'currPage.json')
                    complete = True
                except:
                    pass
        
        else:
            pass


def running():

    # starting the recieve thread we can send and recieve at the same time
    recieve_thread = threading.Thread(target = recieve)
    recieve_thread.start()

    # starting the wrtie thread, we can send and recieve at the same time
    write_thread = threading.Thread(target = write)
    write_thread.start()

    return


if __name__ == '__main__':
    running()
    
else:
    pass
