#  new game page

import pygame, sys, os
import myLibrary as lib
import main
import board
from pygame import mixer
import json
import time




# dictionary if option is chosen or not
optionChosen = {
    'Beginner': False,
    'Intermediate': False,
    'Advanced': False,
    'Master': False
    }

#functions

def backMain():

    for mode in optionChosen:
        optionChosen[mode] = False
    
    main.mainloop()
    return 

def runBoard():
    global optionChosen

    #? changes the curr page state to new game to process changes
    changeMade = False
    while not changeMade:
        try:
            data = lib.loadJson('currPage.json')
            data[0]['newGame'] = 'True'
            lib.storeJson(data, 'currPage.json')
            changeMade = True
        except:
            pass

    #? set the chosen board size in newSize to run board of chosen size
    for button in optionChosen:
        if optionChosen[button]:
            if button == 'Beginner':
                size = 9
            elif button == 'Intermediate':
                size = 13
            elif button == 'Advanced':
                size = 17
            else:
                size = 19
    data = lib.loadJson('newSize.json')
    data[0]['size'] = size
    lib.storeJson(data, 'newSize.json') 

    #? does not run until 2 players chosen bew board
    players = 0
    while players < 2:
        try:
            data = lib.loadJson('numPlayers.json')
            players = data[0]['numPlayers']
        except:
            pass

    board.mainloop()
    return


def chosenMode(difficulty): # function to change all the other states to false
    
    for option in optionChosen: 
        if option == difficulty:
            optionChosen[option] = not optionChosen[option] # the 'not' allows for deselection, so user is not forced'
        else:
            optionChosen[option] = False
    
    return


script_dir = sys.path[0]

#backround
bg_path = os.path.join(script_dir, '../info/images/backgrounds/Settings background.png')
bg = pygame.image.load(bg_path)
(width, height) = (1100, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('NewGame')


#button images
Beginner_img = os.path.join(script_dir, '../info/images/NewGame buttons/black beginner.png')
Intermediate_img = os.path.join(script_dir, '../info/images/NewGame buttons/black intermediate.png')
Advanced_img = os.path.join(script_dir, '../info/images/NewGame buttons/black advanced.png')
Master_img = os.path.join(script_dir, '../info/images/NewGame buttons/black master.png')
redBeginner_img = os.path.join(script_dir, '../info/images/NewGame buttons/red beginner.png')
redIntermediate_img = os.path.join(script_dir, '../info/images/NewGame buttons/red intermediate.png')
redAdvanced_img = os.path.join(script_dir, '../info/images/NewGame buttons/red advanced.png')
redMaster_img = os.path.join(script_dir, '../info/images/NewGame buttons/red master.png')
Back_img = os.path.join(script_dir, '../info/images/NewGame buttons/back.png')

#go button images
off_go = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/grey go.png'))
on_go = os.path.join(script_dir, '../info/images/NewGame buttons/red go.png')

#title image
NewGame_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/new game.png'))

#black number imgs
black_9_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/black 9x9.png'))
black_13_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/black 13x13.png'))
black_17_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/black 17x17.png'))
black_19_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/black 19x19.png'))

#red number imgs
red_9_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/red 9x9.png'))
red_13_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/red 13x13.png'))
red_17_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/red 17x17.png'))
red_19_img = pygame.image.load(os.path.join(script_dir, '../info/images/NewGame buttons/red 19x19.png'))


#buttons

#black buttons
Beginner_btn = lib.Button(Beginner_img, (50,200), chosenMode, 'Beginner')
Intermediate_btn = lib.Button(Intermediate_img, (260,185), chosenMode, 'Intermediate')
Advanced_btn = lib.Button(Advanced_img, (555,170), chosenMode, 'Advanced')
Master_btn = lib.Button(Master_img, (835,175), chosenMode, 'Master')

#red buttons
redBeginner_btn = lib.Button(redBeginner_img, (50,197), chosenMode, 'Beginner')
redIntermediate_btn = lib.Button(redIntermediate_img, (275,205), chosenMode, 'Intermediate')
redAdvanced_btn = lib.Button(redAdvanced_img, (600,190), chosenMode, 'Advanced')
redMaster_btn = lib.Button(redMaster_img, (795,175), chosenMode, 'Master')

#back button
Back_btn = lib.Button(Back_img, (900, 620), backMain)

#on go button
Go_btn = lib.Button(on_go, (400,500), runBoard)


def mainloop():

    
    #backround and screen generating
    bg_path = os.path.join(script_dir, '../info/images/backgrounds/Settings background.png')
    bg = pygame.image.load(bg_path)
    (width, height) = (1100, 700)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('NewGame')

    currMode = 0

    while True:

        ifChosen = False #if a difficulty has been chosen, True = red go button present instead of grey go
        
        

        # dict to hold every button and num with black/red, first entity in array shows whether red is should appear (true) or black (false)
        optionButtons ={'Beginner'    :[optionChosen['Beginner'],     Beginner_btn,     redBeginner_btn,     [black_9_img, (100,260)] ,  [red_9_img, (100,260)], 9],
                        'Intermediate':[optionChosen['Intermediate'], Intermediate_btn, redIntermediate_btn, [black_13_img,(310,250)] ,  [red_13_img,(345,240)], 13],
                        'Advanced'    :[optionChosen['Advanced'],     Advanced_btn,     redAdvanced_btn,     [black_17_img,(630,260)] ,  [red_17_img,(630,255)], 17], 
                        'Master'      :[optionChosen['Master'],       Master_btn,       redMaster_btn,       [black_19_img,(815,240)] ,  [red_19_img,(830,245)], 19]
                        }

        screen.blit(bg, (0,0))# background

        currOptions = [] # to hold current buttons to show on screen in real time
        currNum = [] # num to show based off of currOptions buttons

        #all on screen Buttons 
        
        #back button
        screen.blit(Back_btn.image, Back_btn.rect) 

        #placing option buttons on screen
        for button in optionButtons:
            
            chosen = optionButtons[button][0]

            if chosen: # if chosen is true, therefore selected by user
                screen.blit( optionButtons[button][2].image, optionButtons[button][2].rect)
                currOptions.append(optionButtons[button][2]) # put button in array to easily process when pressed
                currNum.append(optionButtons[button][4]) # corresponding number
                ifChosen = True

                
                """ data = lib.loadJson('newSize.json')
                data[0]['size'] = optionButtons[button][5]
                lib.storeJson(data, 'newSize.json')  """
                
            else: # deselcted by user
                screen.blit( optionButtons[button][1].image, optionButtons[button][1].rect)
                currOptions.append(optionButtons[button][1])
                currNum.append(optionButtons[button][3])


        if ifChosen:
            #red go button
            screen.blit(Go_btn.image, Go_btn.rect)
        else:
            #off go image
            screen.blit(off_go, (400,500))

        
        
        #all on screen images
        
        #placing numbers on screen, looping thru all active nums
        for number,pos in currNum:
            screen.blit(number, pos)

        #new game title
        screen.blit(NewGame_img, (300,30))
        
        #button press processing
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Back_btn.on_click(event)

                #option buttons
                for button in currOptions:
                    button.on_click(event)

                if ifChosen:
                    Go_btn.on_click(event)

        

        pygame.display.update()

    return



if __name__ == '__main__':
    mainloop()
else:
    pass
