# load game page

import pygame, sys, os
import myLibrary as lib
import main
from pygame import mixer
import json
import board

#initialisions
script_dir = sys.path[0]
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 45)
#pygame.font.init(), maybe type pip install pygame --update

#CONST 
BAR_SPACE = 60 # space between each bar in y

#functions
def runGame(gameNum):

    global gameInfo
    
    #? get username of our user
    data = lib.loadJson('Settings.json')
    user1 = data[0]['username']

    #? get the all other information
    data = lib.loadJson('currGame.json')
    data[0]['user1'] = gameInfo[gameNum][0]
    data[0]['user2'] = gameInfo[gameNum][0]
    data[0]['board'] = gameInfo[gameNum][3]
    lib.storeJson(data,'currGame.json')

    #? load the board page where it reads from the curr game file
    board.mainloop()
    
    return

def backMain():
    main.mainloop()
    return


#images

opponent_img = pygame.image.load(os.path.join(script_dir, '../info/images/LoadGame buttons/opponent.png'))
size_img = pygame.image.load(os.path.join(script_dir, '../info/images/LoadGame buttons/size.png'))
turn_img = pygame.image.load(os.path.join(script_dir, '../info/images/LoadGame buttons/turn.png'))
bar_img = pygame.image.load(os.path.join(script_dir, '../info/images/LoadGame buttons/game bar.png'))
Back_img = os.path.join(script_dir, '../info/images/Settings buttons/back.png')

#button images

go_img = os.path.join(script_dir, '../info/images/LoadGame buttons/go.png') 
Back_img = os.path.join(script_dir, '../info/images/Settings buttons/back.png')

#back button
Back_btn = lib.Button(Back_img, (900,620), backMain)

##processing##

#get all present games
data = lib.loadJson('SavedGames.json')
amount = len(data) #number of games
gameInfo = [] # holds opponent, size, turn, board

if amount != 0:
    for game in data:
        opponent = game['opponent']
        size = game['size']
        turn = game['turn']
        board = game['board']
        gameInfo.append([opponent, size, turn, board])



#get all text (eg opponent) in label
labels = []

for game in gameInfo:
    opponent_label = myfont.render(game[0], False, (0, 0, 0))
    size_label = myfont.render(game[1], False, (0, 0, 0))
    turn_label = myfont.render(game[2], False, (0, 0, 0))
    labels.append([opponent_label, size_label, turn_label])
    
    
amount = len(data) #number of games
goButtons = []

for gameNum in range(amount):
    button = lib.Button(go_img , (900,200 + 60 * gameNum), runGame, gameNum)
    goButtons.append(button)


def mainloop():

    #backround and screen generating
    bg_path = os.path.join(script_dir, '../info/images/backgrounds/Settings background.png')
    bg = pygame.image.load(bg_path)
    (width, height) = (1100, 700)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LoadGame')

    while True:

        screen.blit(bg, (0,0)) # background
        screen.blit(opponent_img, (70,100))
        screen.blit(size_img, (470,100))
        screen.blit(turn_img, (670,105))
        screen.blit(Back_btn.image, Back_btn.rect) # back button

        #show bars onscreen
        for num in range(amount):
            screen.blit(bar_img, (70, 200 + num * 60))

   
        #show information on screen
        for gameNum in range(amount): 
            screen.blit(labels[gameNum][0], (100, 215 + gameNum * 60))
            screen.blit(labels[gameNum][1], (500, 215 + gameNum * 60))
            screen.blit(labels[gameNum][2], (700, 215 + gameNum * 60))

        #show go buttons on screen
        for button in goButtons:
            screen.blit(button.image, button.rect)



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Back_btn.on_click(event)

                for button in goButtons:
                    button.on_click(event)
                
                

        pygame.display.update()



if __name__ == '__main__':
    mainloop()
else:
    pass
