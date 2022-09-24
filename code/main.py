#Main Menu

#libraries
import pygame
import sys, os
import myLibrary as lib
import settings
import newGame
import loadGame

pygame.init()
is_initialized = pygame.get_init()

#functions

def run1():
    print('this is not running')

def runNewGame():
    newGame.mainloop()
    return

def runLoadGame():
    loadGame.mainloop()
    return

def Quit():
    pygame.display.quit()
    pygame.quit()

def runSettings():
    settings.mainloop()
    return

script_dir = sys.path[0]

bg_path = os.path.join(script_dir, '../info/images/backgrounds/MainMenu background.png')
bg = pygame.image.load(bg_path)

(width, height) = (1300, 790)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Main Menu')

#buttons
Title_img = os.path.join(script_dir, '../info/images/MainMenu buttons/title.png')
Title_btn = lib.Button(Title_img, (120,40), run1)

NewGame_img = os.path.join(script_dir, '../info/images/MainMenu buttons/newgame.png')
NewGame_btn = lib.Button(NewGame_img, (145,180), runNewGame)

LoadGame_img = os.path.join(script_dir, '../info/images/MainMenu buttons/loadgame.png')
LoadGame_btn = lib.Button(LoadGame_img, (135, 260), runLoadGame)

Account_img = os.path.join(script_dir, '../info/images/MainMenu buttons/account.png')
Account_btn = lib.Button(Account_img, (180,340), runSettings)

Quit_img = os.path.join(script_dir, '../info/images/MainMenu buttons/quit.png')
Quit_btn = lib.Button(Quit_img, (220, 410), Quit)


def mainloop():

    while True:
        screen.blit(bg, (0, 0))
        
        screen.blit(Title_btn.image, Title_btn.rect)
        
        screen.blit(NewGame_btn.image, NewGame_btn.rect)
        screen.blit(LoadGame_btn.image, LoadGame_btn.rect)
        screen.blit(Account_btn.image, Account_btn.rect)
        screen.blit(Quit_btn.image, Quit_btn.rect)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                Title_btn.on_click(event)
                
                NewGame_btn.on_click(event)
                LoadGame_btn.on_click(event)
                Account_btn.on_click(event)
                Quit_btn.on_click(event)
                    
            pygame.display.flip()

            

if __name__ == '__main__':
    mainloop()
else:
    pass
