import pygame, sys, random, pygame.mixer
import cPickle as pickle
from pygame.locals import *
from GameSprites import *
from GameCharacters import *
from GameEnemies import *
from PlayerClasses import *

#Colors   R    G   B
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)#CYAN
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255) #AQUA
INVISIBLE = (255, 255, 255, 255)

pygame.init()
DisplayWidth = 1024
DisplayHeight = 683
DISPLAYSURF = pygame.display.set_mode((DisplayWidth, DisplayHeight))
pygame.display.set_caption("Adventure Game")
FPS = 30
FPSCLOCK = pygame.time.Clock()

#imgs------------
guySwordImgs = ('characters/guySword0.png','characters/guySword1.png','characters/guySword2.png','characters/guySword3.png','characters/guySword4.png','characters/guySword5.png','characters/guySword6.png','characters/guySword7.png','characters/guySword8.png','characters/guySword9.png','characters/guySword10.png','characters/guySword11.png')
mapImg = ('items/map.png',)
coinImgs = ('items/coin0.png','items/coin1.png','items/coin2.png')
guyBroImgs = ('characters/guybro0.png','characters/guybro1.png','characters/guybro2.png','characters/guybro3.png','characters/guybro4.png','characters/guybro5.png','characters/guybro6.png')
guyBroNoWalk = (guyBroImgs[0],guyBroImgs[1],guyBroImgs[2],guyBroImgs[3],guyBroImgs[6])
evilGuyImgs = ('characters/evilGuy0.png','characters/evilGuy1.png','characters/evilGuy2.png','characters/evilGuy3.png','characters/evilGuy4.png','characters/evilGuy5.png')
orangeBroImgs = ('characters/newguy0.png','characters/newguy0.png','characters/newguy0.png','characters/newguy0.png','characters/newguy0.png')
orbImg = 'items/Orb.png'
healthOrbImg = 'items/RedOrb.png'
manaOrbImg = 'items/BlueOrb.png'
#sounds---------
coinSound = 'sounds/coin.wav'
painSound = 'sounds/pain.wav'
#controls---------
controls = {'left':pygame.K_a,'right':pygame.K_d,'up':pygame.K_w,'down':pygame.K_s,'inventory':pygame.K_e,'pause':K_ESCAPE,'interact':pygame.K_q,'attack':pygame.K_SPACE}                  
#fonts------------
interactionFont = pygame.font.Font(None, 24)
inventoryFont = pygame.font.Font(None, 32)
startFont = pygame.font.Font(None, 32)
startFont.set_underline(True)
#character sprite creations-----------
playerName = 'Ben' #String name for player
player=Player(playerName,700,500,guySwordImgs)#guy creation and starting (x,y) coords
#spriteGroups-----------------
allSprites = pygame.sprite.Group()
all_spriteblit = pygame.sprite.Group()
#mousePoints-------------------------
mousex = 0 #mouse x coordinate value
mousey = 0 #mouse y coordinate value

#interactions----------------------------------------------------------------------
def commonInteraction(x, y, name):
    interacting = True
    chat0 = '"How are you doing kind sir?"'
    chat1 = '"What a nice day!"'
    chat2 = '"Im so happy to be alive today!"'
    chat3 = '"You look like an adventurer!"'
    chat4 = '"I wish I could fly..."'
    chat5 = '"What a nice day!"'
    chat6 = '"I feel like I need to learn more phrases..."'
    chat7 = '"Hello!"'
    chat8 = '"I love this area!"'
    chats = (chat0, chat1, chat2, chat3, chat4, chat5, chat6, chat7, chat8)
    randomInt = random.randint(0,4)
    chatText = interactionFont.render(chats[randomInt],True,RED,WHITE)
    chatTextRect = chatText.get_rect()
    nameText = interactionFont.render(name,True,BLUE,WHITE)
    nameTextRect = nameText.get_rect()
    while interacting:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['interact']):
                    interacting = False
        if x < DisplayWidth/2:
            DISPLAYSURF.blit(chatText, (x,y-10))
            DISPLAYSURF.blit(nameText, (x,y-30))
        else:
            DISPLAYSURF.blit(chatText, (x-(chatTextRect.width-50),y-10))
            DISPLAYSURF.blit(nameText, (x-(nameTextRect.width-50),y-30))
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def forestGuardInteract(x, y, name):
    interacting = True
    chatLine = 0
    chat0 = '"It is too dangerous to enter this forest without a map!"'
    chat1 = ('"Wow you have a forest map?"', '"You must be a true adventurer!"')
    nameText = interactionFont.render(name,True,BLUE,WHITE)
    nameTextRect = nameText.get_rect()
    while interacting:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['interact']):
                    if chatLine == 1:
                        interacting = False
                    else:
                        chatLine = 1
        if player.searchInventory('forest map') == False:
            chatText = interactionFont.render(chat0,True,RED,WHITE)
            chatTextRect = chatText.get_rect()
            chatLine = 1
        else:
            chatText = interactionFont.render(chat1[chatLine],True,RED,WHITE)
            chatTextRect = chatText.get_rect()
        if x < DisplayWidth/2:
            DISPLAYSURF.blit(chatText, (x,y-10))
            DISPLAYSURF.blit(nameText, (x,y-30))
        else:
            DISPLAYSURF.blit(chatText, (x-(chatTextRect.width-50),y-10))
            DISPLAYSURF.blit(nameText, (x-(nameTextRect.width-50),y-30))
        FPSCLOCK.tick(FPS)
        pygame.display.update()

#levels--------------------------------------------------------------------------------------
projectiles = pygame.sprite.Group()
fallingObjs = pygame.sprite.Group()
#forestFront Objects--------
forestFrontItems = pygame.sprite.Group()
coin = SpinningItem('567a',200, 500, {'coin':1}, coinImgs, coinSound)
coin1 = SpinningItem('968b',220, 600, {'coin':1}, coinImgs, coinSound, 4)
forestFrontItems.add(coin, coin1)
forestFrontChars = pygame.sprite.Group()
guardbro = MovChar('Tim the Guard',700,450,(guyBroImgs[0],guyBroImgs[4],guyBroImgs[5],guyBroImgs[6]),forestGuardInteract,(300,450))
Bobbro = MovChar('Bob',100,580,orangeBroImgs,commonInteraction,(520,380))
normalGuy = Char('Dead Meat',500,470,orangeBroImgs,commonInteraction)
pauseBro = MovChar_Pauses('Ding Dong',600,600,guyBroImgs,commonInteraction,(890,520),2,100)
forestFrontChars.add(guardbro,Bobbro,normalGuy,pauseBro,)
forestFrontEnemies = pygame.sprite.Group()
forestFrontWalls = pygame.sprite.Group()
forestwall=Wall('e',0,480,DisplayWidth,1)
wall1=Wall('f',0,DisplayHeight+5,DisplayWidth,1)
forestFrontWalls.add(forestwall, wall1)
allSprites.add(forestFrontWalls,forestFrontItems,forestFrontChars,forestFrontEnemies)
def forestFront():
    background=pygame.image.load("backgrounds/forest.jpg").convert()
    moveX,moveY=0,0
    player.setLocation(forestFront)
    #Sprites
    projectiles.empty()
    fallingObjs.empty()
    all_spriteblit.empty()
    all_spriteblit.add(player,forestFrontItems,forestFrontChars,forestFrontEnemies)
    if player.searchInventory('forest map'):
        forestFrontWalls.remove(forestwall)
        guardTalk = False
    else:
        guardTalk = True
        forestFrontWalls.add(forestwall)
    while True:#maingameloop
        moveX, moveY = eventLoop(moveX, moveY,forestFrontWalls,forestFrontItems,forestFrontChars,forestFrontEnemies)
        createOrbs()
        if player.get_x() > DisplayWidth-90:
            player.newRect(10, player.get_y(), player.get_width(), player.get_height())
            space()
        if player.get_x() < 5:
            player.newRect(DisplayWidth-100, player.get_y(), player.get_width(), player.get_height())
            forest()
        if player.get_y() <= 485 and guardTalk == True:
            guardbro.interact()
            guardTalk = False
            moveX = 0
            moveY = 0
        if player.get_y() <= 400:
            house2D()
        updateSprites(moveX,moveY,forestFrontWalls,forestFrontItems,forestFrontChars,forestFrontEnemies)
        DISPLAYSURF.blit(background, (0,0))
        updateScreenText()
        SpriteBlit(all_spriteblit)
        projectiles.draw(DISPLAYSURF)
        fallingObjs.draw(DISPLAYSURF)
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        
#forest Objects--------
forestItems = pygame.sprite.Group()
coin = SpinningItem('124g',200, 600, {'coin':1}, coinImgs, coinSound)
coin1 = SpinningItem('968h',250, 600, {'coin':1}, coinImgs, coinSound)
coin2 = SpinningItem('345i',300, 600, {'coin':1}, coinImgs, coinSound, 4)
coin3 = SpinningItem('038j',350, 600, {'coin':1}, coinImgs, coinSound)
coin4 = SpinningItem('194k',400, 600, {'coin':1}, coinImgs, coinSound)
forestItems.add(coin, coin1, coin2, coin3, coin4)
forestChars = pygame.sprite.Group()
pauseBro = MovChar_Pauses('Din Din',600,480,guyBroImgs,commonInteraction,(130,535))
guybro1 = Char('Steve',130,500,guyBroNoWalk,commonInteraction, True)
forestChars.add(pauseBro,guybro1)
forestEnemies = pygame.sprite.Group()
forestWalls = pygame.sprite.Group()
wall=Wall('123m',0,480,DisplayWidth,1)
wall1=Wall('643n',0,DisplayHeight+5,DisplayWidth,1)
forestWalls.add(wall, wall1)
allSprites.add(forestItems,forestChars,forestWalls,forestEnemies)        
def forest():
    background=pygame.image.load("backgrounds/forest1.jpg").convert()
    moveX,moveY=0,0
    player.setLocation(forest)
    #Sprites
    projectiles.empty()
    fallingObjs.empty()
    all_spriteblit.empty()
    all_spriteblit.add(player,forestItems,forestChars,forestEnemies)
    while True:#maingameloop
        moveX, moveY = eventLoop(moveX, moveY,forestWalls,forestItems,forestChars,forestEnemies)
        createOrbs()
        if player.get_x() > DisplayWidth-90:
            player.newRect(10, player.get_y(), player.get_width(), player.get_height())
            forestFront()
        if player.get_x() < 5:
            player.newRect(DisplayWidth-100, player.get_y(), player.get_width(), player.get_height())
            space()
        updateSprites(moveX, moveY, forestWalls, forestItems, forestChars, forestEnemies)
        DISPLAYSURF.blit(background, (0,0))
        updateScreenText()
        SpriteBlit(all_spriteblit)
        projectiles.draw(DISPLAYSURF)
        fallingObjs.draw(DISPLAYSURF)
        FPSCLOCK.tick(FPS)
        pygame.display.update()

#space Objects--------
spaceItems = pygame.sprite.Group()
coin = SpinningItem('037o',400, 600, {'coin':1}, coinImgs, coinSound, 2)
coin1 = SpinningItem('739p',200,500, {'coin':1}, coinImgs, coinSound, 4)
mapitem = SpinningItem('819q',600,550, {'forest map':1}, mapImg)
spaceItems.add(coin, coin1, mapitem)
spaceChars = pygame.sprite.Group()
#guybro = WalkingCharacter('JOJO',(300,300),(500,420),guyBroImgs,commonInteraction,(60,130),1,2,True)
#spaceChars.add(guybro)
spaceEnemies = pygame.sprite.Group()
enemybro1 = PlayerChaser('BadGUY',600,555,evilGuyImgs)
enemybro2 = PlayerChaser('BadGurl',543,444,evilGuyImgs,30)
enemybro3 = PlayerChaser('BadG0l',543,474,evilGuyImgs,8,25,painSound)
enemybro4 = Enemy('Danger Dolan',500,500,(evilGuyImgs[0],evilGuyImgs[5],evilGuyImgs[1],evilGuyImgs[4]))
spaceEnemies.add(enemybro1,enemybro2,enemybro3,enemybro4)
spaceWalls = pygame.sprite.Group()
wall=Wall('378s',0,300,DisplayWidth,10)
spaceWalls.add(wall)
allSprites.add(spaceWalls,spaceItems,spaceChars,spaceEnemies)
def space():
    background=pygame.image.load("backgrounds/Space.jpg").convert()
    moveX,moveY=0,0
    player.setLocation(space)
    #Sprites
    projectiles.empty()
    fallingObjs.empty()
    all_spriteblit.empty()
    if len(spaceEnemies) == 0:
        enemybro6 = PlayerChaser('Bad88rl',543,424,evilGuyImgs)
        spaceEnemies.add(enemybro6)
        allSprites.add(spaceEnemies)
    all_spriteblit.add(player,spaceItems,spaceChars,spaceEnemies)
    while True:#maingameloop
        moveX, moveY = eventLoop(moveX,moveY,spaceWalls,spaceItems,spaceChars,spaceEnemies)
        createOrbs()
        if player.get_x() > DisplayWidth-90:
            player.newRect(10, 600, player.get_width(), player.get_height())
            forest()
        if player.get_x() < 5:
            player.newRect(DisplayWidth-100, 600, player.get_width(), player.get_height())
            forestFront()
        updateSprites(moveX, moveY, spaceWalls, spaceItems, spaceChars, spaceEnemies)
        DISPLAYSURF.blit(background, (0,0))
        updateScreenText()
        SpriteBlit(all_spriteblit)
        projectiles.draw(DISPLAYSURF)
        fallingObjs.draw(DISPLAYSURF)
        fillRed()
        FPSCLOCK.tick(FPS)
        pygame.display.update()
#house Objects--------
houseItems = pygame.sprite.Group()
houseChars = pygame.sprite.Group()
houseEnemies = pygame.sprite.Group()
houseWalls = pygame.sprite.Group()
wall=Wall('378s',0,600,DisplayWidth,20)
houseWalls.add(wall)
allSprites.add(houseWalls,houseItems,houseChars,houseEnemies)
def house2D():
    background=pygame.image.load("backgrounds/Space.jpg").convert()
    moveX,moveY=0,0
    gravity = 9.8
    player.setLocation(house2D)
    #Sprites
    projectiles.empty()
    fallingObjs.empty()
    all_spriteblit.empty()
    all_spriteblit.add(player)
    while True:#maingameloop
        moveX, moveY = eventLoop2D(moveX,moveY,gravity,houseWalls,houseItems,houseChars,houseEnemies)
        createOrbs()
        if player.get_x() > DisplayWidth-90:
            player.newRect(10, 600, player.get_width(), player.get_height())
            forest()
        if player.get_x() < 5:
            player.newRect(DisplayWidth-100, 600, player.get_width(), player.get_height())
            forestFront()
        updateSprites2D(moveX, moveY, spaceWalls, spaceItems, spaceChars, spaceEnemies)
        DISPLAYSURF.blit(background, (0,0))
        updateScreenText()
        SpriteBlit(all_spriteblit)
        projectiles.draw(DISPLAYSURF)
        fallingObjs.draw(DISPLAYSURF)
        fillRed()
        FPSCLOCK.tick(FPS)
        pygame.display.update()
                
#menus--------------------------------------------------------------------------------------
scroll = pygame.image.load("backgrounds/scroll.png").convert_alpha()
scroll = pygame.transform.scale(scroll, (844, 543))#scroll (width, height)
scrollX = 90#90 default
scrollY = 70#70 default
def inventoryMenu():
    '''displays inventory menus'''
    playerInv = player.get_inventory()
    invKeys = []
    if playerInv == {}:
        emptyInvMenu()
    else:
        for key in playerInv.keys():
            invKeys.append(key)
        if len(invKeys) <= 8:
            smallInvMenu(playerInv, invKeys)
        else:
            #invMenu(playerInv, invKeys)
            print 'not implemented'
            
def emptyInvMenu():
    EmptyText = inventoryFont.render('Inventory is Empty... Go find some stuff!!', True, BLACK)
    HeaderText = inventoryFont.render('--Inventory--', True, BLACK)
    xcoord = 212
    ycoord = 150
    Open = True
    while Open:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['inventory']):
                    Open = False
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        DISPLAYSURF.blit(HeaderText, (xcoord,ycoord))
        DISPLAYSURF.blit(EmptyText, (xcoord,ycoord+50))
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def smallInvMenu(playerInv, invKeys):
    HeaderText = inventoryFont.render('--Inventory--', True, BLACK)
    xcoord = 212
    ycoord = 150
    Open = True
    selectNum = 0
    while Open:
        ycoord = 150
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['inventory']):
                    Open = False
                if (event.key==controls['up']):
                    if selectNum > 0:
                        selectNum -= 1
                    else:
                        selectNum = len(invKeys)-1
                if (event.key==controls['down']):
                    if selectNum < len(invKeys)-1:
                        selectNum += 1
                    else:
                        selectNum = 0
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        DISPLAYSURF.blit(HeaderText, (xcoord,ycoord))
        ycoord += 50
        for key in invKeys:
            if invKeys[selectNum] == key:
                itemtext = startFont.render(key + '---' + str(playerInv[key]), True, BLACK)
            else:
                itemtext = inventoryFont.render(key + '---' + str(playerInv[key]), True, BLACK)
            DISPLAYSURF.blit(itemtext, (xcoord,ycoord))
            ycoord += 40
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def invMenu(playerInv, invKeys):
    HeaderText = inventoryFont.render('--Inventory--', True, BLACK)
    uparrow = inventoryFont.render('^', True, BLACK)
    downarrow = inventoryFont.render('v', True, BLACK)
    xcoord = 212
    ycoord = 150
    Open = True
    selectNum = 0
    selectrange = (0,8)
    while Open:
        ycoord = 150
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['inventory']):
                    Open = False
                if (event.key==controls['up']):
                    if selectNum > selectrange[0]:
                        selectNum -= 1
                    else:
                        if selectrange[0] > 0:
                            selectNum -= 1
                            selectrange = (selectrange[0]-1,selectrange[1]-1)
                        else:
                            selectNum = len(invKeys)-1
                            selectrange = (len(invKeys)-8,len(invKeys))
                if (event.key==controls['down']):
                    if selectNum < selectrange[1]:
                        selectNum += 1
                    else:
                        if selectrange[1] < len(invKeys)-1:
                            selectNum += 1
                            selectrange = (selectrange[0]+1,selectrange[1]+1)
                        else:
                            selectrange = (0,8)
                            selectNum = 0
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        DISPLAYSURF.blit(HeaderText, (xcoord,ycoord))
        ycoord += 25
        if selectrange[0] > 0:
            DISPLAYSURF.blit(uparrow, (xcoord,ycoord))
        ycoord += 25
        for keyNum in range(selectrange[0],selectrange[1]):
            key = invKeys[keyNum]
            if invKeys[selectNum] == key:
                itemtext = startFont.render(key + '---' + str(playerInv[key]), True, BLACK)
            else:
                itemtext = inventoryFont.render(key + '---' + str(playerInv[key]), True, BLACK)
            DISPLAYSURF.blit(itemtext, (xcoord,ycoord))
            ycoord += 40
        if selectrange[1] < len(invKeys):
            DISPLAYSURF.blit(downarrow, (xcoord,ycoord))
        print invKeys
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def StartMenu():
    background=pygame.image.load("backgrounds/forest.jpg").convert()
    New = True
    xcoord = 212
    Toptext = inventoryFont.render('The Game - use arrow keys and space bar', True, BLACK)
    loadingFail = False
    while True:
        ycoord = 150
        DISPLAYSURF.blit(background, (0,0))
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['up']):
                    New = True
                if (event.key==controls['down']):
                    New = False
                if (event.key==K_SPACE):
                    if New == True:
                        newGameStartLocation()
                    else:
                        try:
                            importGame()
                        except:
                            loadingFail = True
                            New = True
                            print('Save files not found. Make sure the save files are saved as c:\GuyGameSpriteSave and c:\GuyGamePlayerSave')
        if New == True:
            Newtext = startFont.render('New Game!', True, BLACK)
            Loadtext = inventoryFont.render('Load Game!', True, BLACK)
        else:
            Newtext = inventoryFont.render('New Game!', True, BLACK)
            Loadtext = startFont.render('Load Game!', True, BLACK)
        if loadingFail:
            Loadtext = inventoryFont.render('Save files not found. Try a new game.', True, BLACK)
            New = True
        DISPLAYSURF.blit(Toptext, (xcoord,ycoord))
        ycoord += 50
        DISPLAYSURF.blit(Newtext, (xcoord,ycoord))
        ycoord += 50
        DISPLAYSURF.blit(Loadtext, (xcoord,ycoord))
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def pauseMenu():
    inScreen = True
    xcoord = 212
    selection = 0
    PauseHeadText = inventoryFont.render('Paused -- Press escape to return to game', True, BLACK)
    menuTexts = ['Save Game', 'Load Game', 'Exit Game']
    while inScreen:
        ycoord = 150
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['up']):
                    if selection <= 0:
                        selection = 2
                    else:
                        selection -= 1
                if (event.key==controls['down']):
                    if selection >= 2:
                        selection = 0
                    else:
                        selection += 1
                if (event.key==K_SPACE):
                    inScreen = False
                if (event.key==controls['pause']):
                    return
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        DISPLAYSURF.blit(PauseHeadText, (xcoord,ycoord))
        ycoord += 50
        for text in menuTexts:
            if menuTexts.index(text) == selection:
                YesText = startFont.render(text, True, BLACK)
                DISPLAYSURF.blit(YesText, (xcoord,ycoord))
                ycoord += 50
            else:
                NoText = inventoryFont.render(text, True, BLACK)
                DISPLAYSURF.blit(NoText, (xcoord,ycoord))
                ycoord += 50
        FPSCLOCK.tick(FPS)
        pygame.display.update()         
    if selection == 0:
        saveMenu()
    elif selection == 1:
        shittyLoadMssg()
    else:
        pygame.quit()
        sys.exit()

def shittyLoadMssg():
    LoadDecide = True
    LoadText = inventoryFont.render("restart game and choose 'load game' at start screen", True, BLACK)
    LoadText2 = inventoryFont.render("Press esc to return to game", True, BLACK)
    while LoadDecide:
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['pause']):
                    return        
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        DISPLAYSURF.blit(LoadText, (170,150))
        DISPLAYSURF.blit(LoadText2, (170,200))
        FPSCLOCK.tick(FPS)
        pygame.display.update() 
        
def saveMenu():
    inScreen = True
    save = False
    xcoord = 212
    SaveGameHeadText = inventoryFont.render('Save the game?', True, BLACK)
    while inScreen:
        ycoord = 150
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.KEYDOWN):
                if (event.key==controls['up']):
                    save = True
                if (event.key==controls['down']):
                    save = False
                if (event.key==K_SPACE):
                    inScreen = False
        if save == True:
            Yestext = startFont.render('Yes!', True, BLACK)
            Notext = inventoryFont.render('No!', True, BLACK)
        else:
            Yestext = inventoryFont.render('Yes!', True, BLACK)
            Notext = startFont.render('No!', True, BLACK)
        DISPLAYSURF.blit(scroll, (scrollX,scrollY))
        DISPLAYSURF.blit(SaveGameHeadText, (xcoord,ycoord))
        ycoord += 50
        DISPLAYSURF.blit(Yestext, (xcoord,ycoord))
        ycoord += 50
        DISPLAYSURF.blit(Notext, (xcoord,ycoord))
        FPSCLOCK.tick(FPS)
        pygame.display.update()
    if save == True:
        saveGame()  
       
#other functions-----------------------------------------------------
def eventLoop(moveX, moveY,walls,items,chars,enemies):
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            pygame.quit()
            sys.exit()
        if (event.type==pygame.KEYDOWN):
            if (event.key==controls['left']):
                moveX = -6
            if (event.key==controls['right']):
                moveX = 6
            if (event.key==controls['up']):
                moveY = -5
            if (event.key==controls['down']):
                moveY = 5
            if (event.key==controls['inventory']):
                moveX=0
                moveY=0
                inventoryMenu()
            if (event.key==controls['pause']):
                moveX=0
                moveY=0
                pauseMenu()
            if event.key==controls['interact'] and player.get_interactionnear() == True:
                moveX=0
                moveY=0
                player.playerInteract()
            if event.key==controls['attack']:
                player.swordAttack(chars,enemies)
        if event.type==pygame.KEYUP:
            if (event.key==controls['left']):
                moveX=0
            if (event.key==controls['right']):
                moveX=0
            if (event.key==controls['up']):
                moveY=0
            if (event.key==controls['down']):
                moveY=0
        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouseButtons = pygame.mouse.get_pressed()
            mouseEvent(mousex, mousey, mouseButtons, enemies)
    return moveX, moveY

def eventLoop2D(moveX,moveY,gravity,walls,items,chars,enemies):
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            pygame.quit()
            sys.exit()
        if (event.type==pygame.KEYDOWN):
            if (event.key==controls['left']):
                moveX = -6
            if (event.key==controls['right']):
                moveX = 6
            #if (event.key==controls['up']):
               # moveY = -5
            #if (event.key==controls['down']):
               # moveY = 5
            if (event.key==controls['inventory']):
                moveX=0
                moveY=0
                inventoryMenu()
            if (event.key==controls['pause']):
                moveX=0
                moveY=0
                pauseMenu()
            if event.key==controls['interact'] and player.get_interactionnear() == True:
                moveX=0
                moveY=0
                player.playerInteract()
            if event.key==controls['attack']:
                player.swordAttack(chars,enemies)
        if event.type==pygame.KEYUP:
            if (event.key==controls['left']):
                moveX=0
            if (event.key==controls['right']):
                moveX=0
            if (event.key==controls['up']):
                moveY=0
            if (event.key==controls['down']):
                moveY=0
        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouseButtons = pygame.mouse.get_pressed()
            mouseEvent(mousex, mousey, mouseButtons, enemies)
    moveY = gravity
    return moveX, moveY

def mouseEvent(mousex, mousey, mouseButtons, enemies):
    if mouseButtons[0] == 1:
        for obj in fallingObjs:
            if mousex in range(obj.get_x(), obj.get_width()+obj.get_x()) and mousey in range(obj.get_y(), obj.get_height()+obj.get_y()):
                obj.click(player)  ##need better way to use orbs
    if mouseButtons[2] == 1:
        player.fireBallAttack(mousex, mousey, projectiles)

def fillRed():
    if player.get_red():
        s = pygame.Surface((DisplayWidth,DisplayHeight), pygame.SRCALPHA)   # per-pixel alpha
        s.fill((200,0,0,50))                         # notice the alpha value in the color
        DISPLAYSURF.blit(s, (0,0))

def createOrbs():
    randFloat = random.random()
    if randFloat<= 0.01:
        randFloat = random.random()
        randX = random.randint(30,DisplayWidth-50)
        if randFloat <= 0.8:
            orb = randomOrb(randX,0,orbImg,random.randint(1,4),DisplayHeight-200,1)
            fallingObjs.add(orb)
        elif randFloat <= 0.9:
            orb = healthOrb(randX,0,healthOrbImg,random.randint(1,4),DisplayHeight-200,10)
            fallingObjs.add(orb)
        else:
            orb = manaOrb(randX,0,manaOrbImg,random.randint(1,4),DisplayHeight-200,10)
            fallingObjs.add(orb)
    
def updateScreenText():
    if player.get_interactionnear() == True:
        interactNearText = interactionFont.render('Interact with %s'  %(player.interactList[0].get_name()),True,RED)
        DISPLAYSURF.blit(interactNearText,(5, 5))
    healthNum = player.get_health()
    manaNum = player.get_mana()
    healthText = interactionFont.render('Health: %s'  %(healthNum),True,RED)
    DISPLAYSURF.blit(healthText,(DisplayWidth-100, 5))
    manaText = interactionFont.render('Mana: %s'  %(manaNum),True,BLUE)
    DISPLAYSURF.blit(manaText,(DisplayWidth-100, 29))
    
def updateSprites(moveX, moveY, Walls, Items, Chars, Enemies, DivideNum=800.0):
    '''updates all sprites including player'''
    for sprite in fallingObjs:
        sprite.update()
    for sprite in projectiles:
        sprite.update(Enemies)
    for sprite in all_spriteblit:
        if sprite.get_name() == playerName:
            sprite.update(moveX, moveY, Walls, Items, Chars, Enemies)
        else:
            sprite.update()
        ScaleNum = 1.0-((DisplayHeight-sprite.get_bottom())/DivideNum)#DivideNum is Float that changes view of screen
        sprite.scaleSprite(ScaleNum)

def updateSprites2D(moveX, moveY, Walls, Items, Chars, Enemies):
    '''updates all sprites including player'''
    for sprite in fallingObjs:
        sprite.update()
    for sprite in projectiles:
        sprite.update(Enemies)
    for sprite in all_spriteblit:
        if sprite.get_name() == playerName:
            sprite.update(moveX, moveY, Walls, Items, Chars, Enemies)
        else:
            sprite.update()
 
def SpriteBlit(spriteGroup):
    '''blits all sprites to screen in order of lowest rect.bottom to highest rect.bottom (uses layers)
    spriteGroup: all sprites on level to be blitted to screen'''
    FinalLayerBlit = pygame.sprite.LayeredUpdates()
    bottoms = []
    layerNum = 0
    for sprite in spriteGroup:
        bottoms.append(sprite.get_bottom())
    bottoms = sorted(bottoms, key=int)
    for bottom in bottoms:
        for sprite in spriteGroup:
            if sprite.get_bottom() == bottom:
                FinalLayerBlit.add(sprite, layer=layerNum)
                layerNum += 1
    ##print FinalLayerBlit.wsprites()
    FinalLayerBlit.draw(DISPLAYSURF)
    FinalLayerBlit.empty()

def importGame():
    allNames = loadAllNames(r'c:\GuyGameSpriteSave')
    for sprite in allSprites:
        if sprite.get_name() not in allNames:
            sprite.kill()
    playerTraits = importPlayer(r'c:\GuyGamePlayerSave')
    player.newRect(playerTraits[0],playerTraits[1],player.get_width(),player.get_height())
    player.newInventory(playerTraits[2])
    player.setHealth(playerTraits[4])
    player.setMana(playerTraits[5])
    player.setLocation(playerTraits[3])
    player.get_location()()

def saveGame():
    allNames = []
    for sprite in allSprites:
        allNames.append(sprite.get_name())
    playerTraits = (player.get_x(),player.get_y(),player.get_inventory(),player.get_location(),player.get_health(),player.get_mana())
    saveobject(playerTraits, r'c:\GuyGamePlayerSave') 
    saveobject(allNames, r'c:\GuyGameSpriteSave')
        
def saveobject(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
       
def importPlayer(filename):
    with open(filename, 'rb') as input:
        playerTraits = pickle.load(input)
    #print player
    return playerTraits

def loadAllNames(filename):
    with open(filename, 'rb') as input:
        allNames = pickle.load(input)
    return allNames

#start location----------------
newGameStartLocation = forestFront
#start game-----------------
StartMenu()
