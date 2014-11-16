import pygame, sys, random
from pygame.locals import *

class SpinningItem(pygame.sprite.Sprite):
    def __init__(self,name,x,y,ItemType,Images,sound=None,timeTarg=3):
        '''x: x coordinate of item, y: y coordinate of item
        timeTarg: int greater than or equal to zero -- closer to zero faster animation
        ItemType: dict object with string as key and quantity as value -- {'coin':1}
        Images: tuple of three animation images strings if animation wanted, tuple of one image string if no animation
        sound: a string name of a sound "sound.mp3"'''
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if len(Images)>1:
            self.i0 = pygame.image.load(Images[0]).convert_alpha()
            self.i1 = pygame.image.load(Images[1]).convert_alpha()
            self.i2 = pygame.image.load(Images[2]).convert_alpha()
            self.isSpin = True
        else:
            self.i0 = pygame.image.load(Images[0]).convert_alpha()
            self.isSpin = False
        self.timeTarget = timeTarg #must be int>=0 -- closer to zero is faster
        self.timeNum = 0
        self.currentImageNum = 0
        self.image = self.i0
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        self.itemType = ItemType
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None
    
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_rect(self):
        #print self.rect
        return self.rect

    def get_bottom(self):
        return self.rect.bottom

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_image(self):
        return self.image

    def get_itemType(self):
        return self.itemType

    def get_name(self):
        return self.name
    
    def newRect(self, newx, newy, newwidth, newheight):
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        self.rect.x = newx
        self.rect.y = newy
        self.rect.width = newwidth
        self.rect.height = newheight

    def playSound(self):
        if self.sound != None:
            self.sound.play()

    def pickUp(self):
        self.playSound()
        self.kill()
        return self.itemType
    
    def scaleSprite(self, ScaleVal):
        self.image = pygame.transform.scale(self.image, (int(self.rect.width*ScaleVal), int(self.rect.height*ScaleVal)))

    def update(self):
        if self.isSpin == True:
            self.timeNum+=1
            if self.timeNum > self.timeTarget:
                if self.currentImageNum==0:
                    self.front = True
                    self.currentImageNum=1
                elif self.currentImageNum==1 and self.front == True:
                    self.currentImageNum=2
                elif self.currentImageNum == 2:
                    self.currentImageNum=1
                    self.front = False
                else:
                    self.currentImageNum=0
                self.timeNum=0
            self.render()
        else:
            self.image = self.i0

    def render(self):
        if self.currentImageNum==0:
            self.image = self.i0
        elif self.currentImageNum==1 and self.front == True:
            self.image = self.i1
        elif self.currentImageNum == 2:
            self.image = self.i2
        else:
            self.image = pygame.transform.flip(self.i1, True, False)

        
class Wall(pygame.sprite.Sprite):
    def __init__(self,name,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface([width, height])
        #self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def get_name(self):
        return self.name

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_rect(self):
        return self.rect

    def get_bottom(self):
        return self.rect.bottom

    def get_top(self):
        return self.rect.top

    def get_left(self):
        return self.rect.left

    def get_right(self):
        return self.rect.right

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height
    

class fallingOrb(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, endPoint, energy, sound=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed = speed
        self.endPoint = endPoint
        self.energy = energy
        self.loadSound(sound)

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_rect(self):
        #print self.rect
        return self.rect

    def get_bottom(self):
        return self.rect.bottom

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_image(self):
        return self.image

    def loadSound(self, sound):
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None

    def playSound(self):
        if self.sound != None:
            self.sound.play()

    def moveSprite(self):
        self.rect.y+=self.speed
        num = random.random()
        if num<0.1:
            self.rect.x -= 1
        elif num>0.9:
            self.rect.x += 1
        if self.rect.y >= self.endPoint:
            self.kill()

    def update(self):
        self.moveSprite()

    def click(self, playerObj):
        self.playSound()
        self.kill()

class healthOrb(fallingOrb):    
    def click(self, playerObj):
        self.playSound()
        playerObj.addHealth(self.energy)
        self.kill()

class manaOrb(healthOrb):
    def click(self, playerObj):
        self.playSound()
        playerObj.addMana(self.energy)
        self.kill()

class randomOrb(healthOrb):
    def click(self, playerObj):
        self.playSound()
        randFloat = random.random()
        if randFloat > 0.5:
            playerObj.addHealth(self.energy)
        else:
            playerObj.addMana(self.energy)
        self.kill()
        
        
