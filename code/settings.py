#Settings Page

#libraries
import pygame, sys, os
import myLibrary as lib
import main
from pygame import mixer
import json
import time

pygame.init()

#code to start music, allows us to just pause or unpause

path = '/Users/mustafajaffar/Documents/GO/info/sponge.mp3'

mixer.init()
mixer.music.load(path)#../info/
mixer.music.set_volume(0.5)
mixer.music.play(-1)
mixer.music.pause()

#pygame.mixer.Channel(0).play(pygame.mixer.Sound('../info/song.mp3'))
#pygame.mixer.Channel(1).play(pygame.mixer.Sound('../info/click.mp3'))


#dictionary to hold icon state 

iconState = {'Elon':False,
            'Isaac':False,
            'Stewie':False,
            'Abe':False
            }


#get preselected icon
data = lib.loadJson('Settings.json')
chosenIcon = data[0]['icon']

if chosenIcon:
    iconState[chosenIcon] = True

def musicOn():
    mixer.music.unpause()
    return

def musicOff():
    mixer.music.pause()
    return

def backMain():

    #? change curr page state for account page so we can get acc data
    complete = False
    while not complete:
        try:
            data = lib.loadJson('currPage.json')
            data[0]['accPage'] = 'True'
            lib.storeJson(data, 'currPage.json')
            time.sleep(1) # using time.sleep so the client can have time to check the json file
            complete = True
        except:
            pass

    main.mainloop()
    return


def iconSet(name):
    
    for icon in iconState:
        if icon == name:
            iconState[icon] = True
        else:
            iconState[icon] = False

    data = lib.loadJson('Settings.json')
    data[0]['icon'] = name
    lib.storeJson(data, 'Settings.json')

    return

script_dir = sys.path[0]

bg_path = os.path.join(script_dir, '../info/images/backgrounds/Settings background.png')
bg = pygame.image.load(bg_path)

(width, height) = (1100, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Settings')

#images
Username_img = pygame.image.load(os.path.join(script_dir, '../info/images/Settings buttons/username.png'))
Country_img = pygame.image.load(os.path.join(script_dir, '../info/images/Settings buttons/country.png'))
Icons_img = pygame.image.load(os.path.join(script_dir, '../info/images/Settings buttons/icons.png'))
Music_img = pygame.image.load(os.path.join(script_dir, '../info/images/Settings buttons/music.png'))
SoundOption_img = pygame.image.load(os.path.join(script_dir, '../info/images/Settings buttons/sound options.png'))
ButtonPress_img = pygame.image.load(os.path.join(script_dir, '../info/images/Settings buttons/button press.png'))
On_img = os.path.join(script_dir, '../info/images/Settings buttons/on button.png')
Off_img = os.path.join(script_dir, '../info/images/Settings buttons/off button.png')
Back_img = os.path.join(script_dir, '../info/images/Settings buttons/back.png')

    
#icon images, selected icon

Elon_on = os.path.join(script_dir, '../info/images/Settings buttons/elon on.png')
Isaac_on = os.path.join(script_dir, '../info/images/Settings buttons/isaac on.png')
Stewie_on = os.path.join(script_dir, '../info/images/Settings buttons/stewie on.png')
Abe_on = os.path.join(script_dir, '../info/images/Settings buttons/abe on.png')

#icon images, deselcted icon
Elon_off = os.path.join(script_dir, '../info/images/Settings buttons/elon off.png')
Isaac_off = os.path.join(script_dir, '../info/images/Settings buttons/isaac off.png')
Stewie_off = os.path.join(script_dir, '../info/images/Settings buttons/stewie off.png')
Abe_off = os.path.join(script_dir, '../info/images/Settings buttons/abe off.png')

#buttons

#music options
Music_on_btn = lib.Button(On_img, (340,600), musicOn) 
Music_off_btn = lib.Button(Off_img, (400, 600), musicOff)

#button noise options
Press_on_btn = lib.Button(On_img, (140,600), musicOn) 
Press_off_btn = lib.Button(Off_img, (200, 600), musicOff)

#back button
Back_btn = lib.Button(Back_img, (900,620), backMain)



#icon on buttons
Elon_on_btn = lib.Button(Elon_on, (520,120), iconSet, 'Elon')
Isaac_on_btn = lib.Button(Isaac_on, (780,120), iconSet, 'Isaac')
Stewie_on_btn = lib.Button(Stewie_on, (520,400), iconSet, 'Stewie')
Abe_on_btn = lib.Button(Abe_on, (780,400), iconSet, 'Abe')

#icon off buttons
Elon_off_btn = lib.Button(Elon_off, (520,120), iconSet, 'Elon')
Isaac_off_btn = lib.Button(Isaac_off, (780,120), iconSet, 'Isaac')
Stewie_off_btn = lib.Button(Stewie_off, (520,400), iconSet, 'Stewie')
Abe_off_btn = lib.Button(Abe_off, (780,400), iconSet, 'Abe')


def mainloop():

    (width, height) = (1100, 700)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Settings')

    data = lib.loadJson('Settings.json')
    currCountry = data[0]['country']
    currName = data[0]['username']

    #input boxes
    Username_input_box = lib.InputBox(100,120, 365,50, currName)
    Country_input_box = lib.InputBox(100, 340, 325,50, currCountry)
    input_boxes = [Username_input_box, Country_input_box]
    
    
    while True:

        screen.blit(bg, (0,0))


        
        #stores curr input boxes
        data = lib.loadJson('Settings.json')
        data[0]['username'] = Username_input_box.getText()
        data[0]['country'] = Country_input_box.getText()
        lib.storeJson(data, 'Settings.json')


        #dictionary to hold all icon options with state
        currIcons = {'Elon'  :[ iconState['Elon'],   Elon_on_btn,   Elon_off_btn],
                     'Isaac' :[ iconState['Isaac'],  Isaac_on_btn,  Isaac_off_btn],
                     'Stewie':[ iconState['Stewie'], Stewie_on_btn, Stewie_off_btn],
                     'Abe'   :[ iconState['Abe'],    Abe_on_btn,    Abe_off_btn]
                     }

        #putting the labels on screen
        screen.blit(Username_img, (30,20))
        screen.blit(Country_img, (40,250))
        screen.blit(Icons_img, (550,33))
        screen.blit(SoundOption_img, (35, 470))
        screen.blit(Music_img, (330, 550))
        screen.blit(ButtonPress_img, (80, 550))

        #putting the buttons on screen
        screen.blit(Music_on_btn.image, Music_on_btn.rect) # music options
        screen.blit(Music_off_btn.image, Music_off_btn.rect)
        screen.blit(Press_on_btn.image, Press_on_btn.rect) # press button options
        screen.blit(Press_off_btn.image, Press_off_btn.rect)
        
        screen.blit(Back_btn.image, Back_btn.rect) # back button

        onScreen = [] #holds all of the icon buttons in thier current state

        for option in currIcons:

            state = currIcons[option][0]
            
            if state: 
                screen.blit( currIcons[option][1].image, currIcons[option][1].rect)
                onScreen.append(currIcons[option][1])
            else:
                screen.blit(currIcons[option][2].image, currIcons[option][2].rect)
                onScreen.append(currIcons[option][2])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Music_on_btn.on_click(event)
                Music_off_btn.on_click(event)
                Press_on_btn.on_click(event)
                Press_off_btn.on_click(event)
                Back_btn.on_click(event)

                for option in onScreen:
                    option.on_click(event)

            for box in input_boxes:
                box.handle_event(event)
                
        for box in input_boxes:
            box.update()
            box.draw(screen)

        pygame.display.update()

    return
        
    
                
if __name__ == '__main__':
    mainloop()
else:
    pass


