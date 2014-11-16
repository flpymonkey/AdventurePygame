import pygame, sys, random
from pygame.locals import *
from VectorClass import Vector

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, x, y, images, health=10, attackDamage=5, sound=None):
        '''images: 4 image string tuple
            images is (stand, stand2, attack stand, stun stand)'''
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.loadImages(images)
        self.currentImageNum = 0
        self.image = self.i0
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.realWidth = self.rect.width
        self.realHeight = self.rect.height
        self.playerX = self.rect.x
        self.playerY = self.rect.y
        self.picDelay = 20
        self.picNum = self.picDelay
        self.left = False
        self.stunned = False
        self.stunDelay = 10
        self.stunNum = self.stunDelay
        self.attacking = False
        self.attackDelay = 40
        self.attackNum = self.attackDelay
        self.attackAni = self.attackDelay/2
        self.health=health
        self.attackDamage = attackDamage
        self.loadSound(sound)

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

    def get_image(self):
        return self.image

    def loadSound(self, sound):
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None
        
    def loadImages(self, images):
        '''images: 4 image string tuple
            images is (stand, stand2, attack stand, stun stand)'''
        self.i0 = pygame.image.load(images[0]).convert_alpha()
        self.i1 = pygame.image.load(images[1]).convert_alpha()
        self.i2 = pygame.image.load(images[2]).convert_alpha()
        self.i3 = pygame.image.load(images[3]).convert_alpha()
        self.images = (self.i0,self.i1,self.i2,self.i3)

    def playSound(self):
        if self.sound != None:
            self.sound.play()

    def scaleSprite(self, ScaleVal):
        self.image = pygame.transform.scale(self.image, (int(self.realWidth*ScaleVal), int(self.realHeight*ScaleVal)))
        imageRect = self.image.get_rect()
        imageRect.bottom = self.rect.bottom
        imageRect.left = self.rect.left
        self.rect = imageRect

    def update(self):
        self.isStunned()
        self.isAttacking()
        self.isLeft()
        self.chooseImageNum()
        self.render()

    def render(self):
        self.image = self.images[self.currentImageNum]
        if self.left:
            self.image = pygame.transform.flip(self.image, True, False)

    def chooseImageNum(self):
        if self.stunned:
            self.currentImageNum = 3
        elif self.attacking and self.attackNum < self.attackAni:
            self.currentImageNum = 2
        else:
            if self.picNum >= self.picDelay:
                self.picNum = 0
                if self.currentImageNum == 0:
                    self.currentImageNum = 1
                else:
                    self.currentImageNum = 0
            else:
                self.picNum += 1
            
    def inflictDamage(self, damage, knockBack):
        self.playSound()
        if self.health - damage > 0:
            self.health -= damage
            self.stunNum = 0
        else:
            self.kill()

    def collPlayer(self):
        if self.attacking == False:
            self.attackNum = 0
            return self.attackDamage
        else:
            return 0

    def isAttacking(self):
        if self.attackNum >= self.attackDelay:
            self.attacking = False
        else:
            self.attacking = True
            self.attackNum += 1
        
    def isLeft(self):
        if self.playerX < self.rect.centerx:
            self.left = True
        else:
            self.left = False
        
    def isStunned(self):
        if self.stunNum >= self.stunDelay:
            self.stunned = False
        else:
            self.stunned = True
            self.stunNum += 1
        
    def recievePlayerCoords(self, xCoord, yCoord):
        self.playerX = xCoord
        self.playerY = yCoord


class PlayerChaser(Enemy):
    def __init__(self, name, x, y, images, health=10, attackDamage=5, sound=None, moveSpeed=3):
        '''images: 5 image string tuple
            images is (stand, stand attack, left ft step, right ft step, stun stand)'''
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.loadImages(images)
        self.currentImageNum = 0
        self.image = self.i0
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.trueX = x
        self.trueY = y
        self.realWidth = self.rect.width
        self.realHeight = self.rect.height
        self.playerX = self.rect.x
        self.playerY = self.rect.y
        self.target = (self.playerX, self.playerY)
        self.realSpeed = moveSpeed # Real movement speed of the sprite
        self.moveSpeed = moveSpeed # movement speed of the sprite
        self.left = False
        self.stunned = False
        self.stunDelay = 10
        self.stunNum = self.stunDelay
        self.attacking = False
        self.attackDelay = 40
        self.attackNum = self.attackDelay
        self.attackAni = self.attackDelay/2
        self.stepDelay = 10
        self.stepNum = self.stepDelay
        self.health=health
        self.attackDamage = attackDamage
        self.loadSound(sound)

    def loadImages(self, images):
        '''images: 5 image string tuple
            images is (stand, stand attack, left ft step, right ft step, stun stand)'''
        self.i0 = pygame.image.load(images[0]).convert_alpha()
        self.i1 = pygame.image.load(images[1]).convert_alpha()
        self.i2 = pygame.image.load(images[2]).convert_alpha()
        self.i3 = pygame.image.load(images[3]).convert_alpha()
        self.i4 = pygame.image.load(images[4]).convert_alpha()
        self.images = (self.i0,self.i1,self.i2,self.i3,self.i4)

    def update(self):
        self.isStunned()
        self.isAttacking()
        self.moveSprite()
        self.chooseImageNum()
        self.render()

    def direction(self, target):
        '''
        Function:
            takes total distance from sprite
            to the sprites target
            (gets direction to move)
        Returns:
            a normalized vector
        Parameters:
            - self
            - target
                x,y coordinates of the sprites target
                can be any x,y coorinate pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        if self.target: # if the sprite has a target
            position = Vector(self.rect.x, self.rect.y) # create a vector from x,y value
            target = Vector(target[0], target[1]) # and one from the target x,y
            self.dist = target - position # get total distance between target and position
            direction = self.dist.normalize() # normalize so its constant in all directions
            return direction

    def distance_check(self, dist):
        '''
        Function:
            tests if the total distance from the
            sprite to the target is smaller than the
            ammount of distance that would be normal
            for the sprite to travel
            (this lets the sprite know if it needs
            to slow down. we want it to slow
            down before it gets to it's target)
        Returns:
            bool
        Parameters:
            - self
            - dist
                this is the total distance from the
                sprite to the target
                can be any x,y value pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        dist_x = dist[0] ** 2 # gets absolute value of the x distance
        dist_y = dist[1] ** 2 # gets absolute value of the y distance
        t_dist = dist_x + dist_y # gets total absolute value distance
        speed = self.moveSpeed ** 2 # gets aboslute value of the speed
        if t_dist < (speed): # read function description above
            return True

    def moveSprite(self):
        '''
        Function:
            gets direction to move then applies
            the distance to the sprite.center
            ()
        Parameters:
            - self
        '''    
        if self.stunned == False and self.attackNum >= self.attackAni:
            self.limitSpeed()
            self.target = (self.playerX, self.playerY)
            oldx = self.rect.x
            oldy = self.rect.y
            self.dir = self.direction(self.target) # get direction
            if self.dir: # if there is a direction to move
                if self.distance_check(self.dist): # if we need to stop
                    self.rect.x = self.target[0] # center the sprite on the target
                    self.rect.y = self.target[1]
                else: # if we need to move normal
                    self.trueX += (self.dir[0] * self.moveSpeed) # calculate speed from direction to move and speed constant
                    self.trueY += (self.dir[1] * self.moveSpeed)
                    self.rect.x = round(self.trueX) # apply values to sprite rect
                    self.rect.y = round(self.trueY)
            self.isLeft(oldx, oldy)

    def chooseImageNum(self):
        if self.stunned:
            self.currentImageNum = 4
        elif self.attacking and self.attackNum < self.attackAni:
            self.currentImageNum = 1
        else:
            if self.stepNum >= self.stepDelay:
                self.stepNum = 0
                if self.currentImageNum == 2:
                    self.currentImageNum = 3
                else:
                    self.currentImageNum = 2
            else:
                self.stepNum += 1

    def inflictDamage(self, damage, knockBack):
        self.playSound()
        if self.health - damage > 0:
            self.health -= damage
            self.trueX += knockBack
            self.rect.x += knockBack
            self.stunNum = 0
        else:
            self.kill()

    def limitSpeed(self):
        if self.rect.y < 360 and self.realSpeed - 3 > 0:
            self.moveSpeed = self.realSpeed - 3
        elif self.rect.y < 430 and self.realSpeed - 2 > 0:
            self.moveSpeed = self.realSpeed - 2
        elif self.rect.y < 500 and self.realSpeed - 1 > 0:
            self.moveSpeed = self.realSpeed - 1
        else:
            self.moveSpeed = self.realSpeed

    def isLeft(self, oldx, oldy):
        if oldx > self.rect.x:
            self.left = True
        elif oldx < self.rect.x:
            self.left = False

        



        
        
        
        
    
        

    
