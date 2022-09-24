# boardgame

# libraries
import pygame, sys, os
import myLibrary as lib
import main
from pygame import mixer
import json
import copy

#consts
myfont = pygame.font.SysFont('Comic Sans MS', 30)

#functions

def saveGame():
    return

def Quit():
    print('quitting')
    main.mainloop()
    return

ifSafe = False
def checkCaptured(row,col,board,player):

    global ifSafe 

    if row >= len(board) or col >= len(board) or row <= -1 or col <= -1 or board[row][col] == 0 or board[row][col] == -1 * ( (player^3) + 1) or board[row][col] == 0: # if we are out of bounds or if we see an empty position
        ifSafe = True                                                                                                                         # we know that the current stone is not captured
        return

    elif board[row][col] == player: #if we meet the current players stone stone or if this position is empty

        board[row][col] = -1 * (player + 1) # make the position checked with -1  
        checkCaptured(row + 1, col, board, player) # recurse over all 4 other position directly next to it
        checkCaptured(row - 1, col, board, player)
        checkCaptured(row, col + 1, board, player)
        checkCaptured(row, col - 1, board, player)

    elif board[row][col] == player ^ 3:
        board[row][col] == -1 * ( (player^3) + 1)

    return


ifMoved = False
turn = 0

def PlaceStone(pos):

    global turn
    global ifMoved

    row = pos[0]
    col = pos[1]
    board = pos[2]

    
    if turn % 2 == 0:
        if board[row][col] == 0 or board[row][col] == -3:
            board[row][col] = 1
            turn += 1
            ifMoved = True

    else:
        if board[row][col] == 0 or board[row][col] == -2:
            board[row][col] = 2
            turn += 1
            ifMoved = True

    return



script_dir = sys.path[0]

bg_path = os.path.join(script_dir, '../info/images/Board buttons/game background.png')
bg = pygame.image.load(bg_path)

(width, height) = (1300, 780)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Board')

#images
NameBox_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/name box.png'))
BlueBar_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/bar.png'))
Flag_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/surrender.png'))
Menu_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/menu.png'))
ChatBox_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/chat box.png'))
Board19_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/19 board.png'))
Board9_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/9 board.png'))
Board13_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/13 board.png'))
Board17_img = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/17 board.png'))

#icons
Elon = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/elon.png'))
Isaac = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/isaac.png'))
Abe = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/abe.png'))
Stewie = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/stewie.png'))

#stones for each board size
black9 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/black 9.png'))
white9 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/white 9.png'))
black13 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/black 13.png'))
white13 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/white 13.png'))
black17 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/black 17.png'))
white17 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/white 17.png'))
black19 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/black 19.png'))
white19 = pygame.image.load(os.path.join(script_dir, '../info/images/Board buttons/white 19.png'))

# save quit button images
save_img = os.path.join(script_dir, '../info/images/Board buttons/save.png')
quit_img = os.path.join(script_dir, '../info/images/Board buttons/quit.png')

#posititon image
dot_img = os.path.join(script_dir, '../info/images/Board buttons/dot.png')


#placing board corner, [x coord of first dot, y coord of first dot],
#[x diff for each dot, y diff for each dot], board img, the stone size for the board,
#offset for each stone
boardInfo = {
    'board 19': [(35,175), [47, 190], [31, 30], Board19_img, [black19, white19], [-5, -6],   [-4, -3]],
    'board 9' : [(35,168), [61, 198], [63, 67], Board9_img,  [black9,  white9],  [-19, -21], [-17, -18]],
    'board 13': [(28,163), [55, 200], [42, 44], Board13_img, [black13, white13], [-6, -7],   [0, -2]],
    'board 17': [(35,163), [47, 180], [34, 34], Board17_img, [black13, white13], [-6, -8],   [-2, -5]]
    }



ifMoved = False

def mainloop():

    global ifSafe
    global ifMoved

    turn = 0
    changeTurn = 0

    bg_path = os.path.join(script_dir, '../info/images/Board buttons/background 2.png')
    bg = pygame.image.load(bg_path)

    (width, height) = (1300, 780)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Board')

    #save and quit buttons
    save_btn = lib.Button(save_img, (1150,300), saveGame)
    quit_btn = lib.Button(quit_img, (1140,420), Quit)

    #fetching the new boardsize
    while True:
        try:
            data = lib.loadJson('newSize.json')
            size = data[0]['size']
            break
        except:
            pass

    boardSize = 'board ' + str(size)

    #? setting up the board

    #? getting data from the current game folder, either loaded or new
    data = lib.loadJson('currGame.json')
    if data[0]['boardState'] == 0:
        #setting up board for stones, 0 = empty, 1 = black, 2 = white
        boardState = [[0]*size for i in range(size)]
        boardPos = [[0]*size for i in range(size)]
        buttonsArr = [[0]*size for i in range(size)]

        # setting up board with buttons
        startX = boardInfo[boardSize][1][0]
        startY = boardInfo[boardSize][1][1]

        #creating buttons for each position
        for row in range(size):
            for col in range(size):
                currX = startX + (row *  boardInfo[boardSize][2][0])
                currY = startY + (col *  boardInfo[boardSize][2][1])
                boardPos[row][col] = [currX,currY]
                buttonsArr[row][col] = lib.Button(dot_img, (currX, currY), PlaceStone, [row,col,boardState] )
    
    # putting names into renderable font to put on screen
    username1 = str(data[0]['user1'])
    username2 = str(data[0]['user2'])
    name1 = myfont.render(username1 + ' - black', False, (0, 0, 0))
    name2 = myfont.render(username2, False, (0, 0, 0))

    #? fetching the icons
    icon1 = data[0]['icon1']
    icon2 = data[0]['icon2']
    
    while True:
        
        screen.blit(bg, (0,0))
        
        # images on screen
        screen.blit(BlueBar_img, (0,0))
        screen.blit( boardInfo[boardSize][3], boardInfo[boardSize][0])
        screen.blit(NameBox_img, (30,10))
        screen.blit(NameBox_img, (950,10))

        #blitsing names on screen
        if changeTurn % 2 == 0:
            name1 = myfont.render(username1 + ' - black', False, (0, 0, 0))
            name2 = myfont.render(username2, False, (0, 0, 0))
        else:
            name1 = myfont.render(username1, False, (0, 0, 0))
            name2 = myfont.render(username2 + ' - white', False, (0, 0, 0)) 

        screen.blit(name1, (200,60))
        screen.blit(name2, (1000,60))

        #blits save and quit on screen
        screen.blit(save_btn.image, save_btn.rect)
        screen.blit(quit_btn.image, quit_btn.rect)

        #icons on screen, 30,15 for left user and 1130,15 for right user
        screen.blit(Abe, (1130,15))
        screen.blit(Elon, (30,14))
        
        # pos buttons on screen
        for row in range(size):
            for col in range(size):
                currPos = buttonsArr[row][col]
                screen.blit( currPos.image, currPos.rect)

        #validaiton check each taken position for captured stones
        if ifMoved == True:

            changeTurn += 1

            for row in range(size):
                for col in range(size):
                    currState = boardState[row][col]
                    temp = copy.deepcopy(boardState)
                    
                    top = [0 for i in range(size+2)]
                    bottom = [0 for i in range(size+2)]
                    
                    if currState == 1 or currState == 2:
                        

                        for cell in range(size):
                            if temp[0][cell] == currState:
                                top[cell+1] = currState ^ 3
                                #print('yes', 0, cell)

                            if temp[size-1][cell] == currState:
                                bottom[cell+1] = currState ^ 3
                                #print('yes')



                        for cell in range(0,size):
                            if temp[cell][0] == currState:
                                temp[cell].insert(0, currState ^ 3)
                            else:
                                temp[cell].insert(0, 0)

                            if temp[cell][size] == currState:
                                temp[cell].insert(size+1, currState ^ 3)
                            else:
                                temp[cell].insert(size+1, 0)

                            
                            

                        temp.insert(0,top)
                        temp.insert(size+1,bottom)

                        
                        
                        ifSafe = False

                        
                        
                        checkCaptured(row+1,col+1,copy.deepcopy(temp),currState)

                        if not ifSafe:
                            boardState[row][col] = -1 * (currState + 1) 
            
            ifMoved = False

            
                                
        #get right size stone for board
        blackStone = boardInfo[boardSize][4][0]
        whiteStone = boardInfo[boardSize][4][1]

        for row in range(size):
            for col in range(size):

                #get the offset for each stone so they can be positioned correctly as i used the
                #dots positions to place the stones 
                stoneX = boardPos[row][col][0]
                stoneY = boardPos[row][col][1]

                if boardState[row][col] == 0:
                    pass
                
                elif boardState[row][col] == 1:

                    #re align the stones
                    XOffset = boardInfo[boardSize][5][0]
                    YOffset = boardInfo[boardSize][5][1]
                    stoneX += XOffset
                    stoneY += YOffset
                    
                    pos = (stoneX,stoneY)
                    screen.blit(blackStone, pos)
                    
                elif boardState[row][col] == 2:

                    XOffset = boardInfo[boardSize][6][0]
                    YOffset = boardInfo[boardSize][6][1]
                    stoneX += XOffset
                    stoneY += YOffset

                    pos = (stoneX,stoneY)
                    screen.blit(whiteStone, pos)
                    
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                save_btn.on_click(event)
                quit_btn.on_click(event)

                for row in range(size):
                    for col in range(size):
                        currPos = buttonsArr[row][col]
                        currPos.on_click(event)
    
        pygame.display.update()

    return
   


if __name__ == '__main__':
    mainloop()
else:
    pass



        
