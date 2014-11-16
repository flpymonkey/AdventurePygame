import pygame, sys, random
from pygame.locals import *
from GameSprites import *
from VectorClass import Vector

#powerImgs--------------------------------------------
fireBall = 'items/fireBall.png'

class Player(pygame.sprite.Sprite):
    def __init__(self,name,x,y,images):
        '''images = 12 images
            images is (faceright stand, stand attack, leftft step, rightft step, leftft stepAttack, rightft stepAttack,
            faceleft stand, stand attack, rightft step, leftft step, rightft stepAttack, leftft stepAttack)'''
        pygame.sprite.Sprite.__init__(self)
        self.loadImages(images)
        self.name = name
        self.timeTarget = 7
        self.timeNum = 0
        self.currentImageNum = 0
        self.image = self.i0
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.RealWidth = self.rect.width
        self.RealHeight = self.rect.height
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        self.left = False
        self.down = False
        self.leftStep = False
        self.moving = False
        self.inventory = {}#items in inventory
        self.location = None
        self.interactnear = False
        self.interactList = []
        self.attackTime = 5
        self.attackNum = 0
        self.attacking = False
        self.maxHealth = 100 #implement with potions
        self.health = self.maxHealth #starting health player has
        self.maxMana = 100
        self.mana = self.maxMana
        self.red = False#whether screen is filed red or not
        self.redDelay = 5
        self.redNum = self.redDelay

    def get_name(self):
        return self.name
        
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_bottom(self):
        return self.rect.bottom

    def get_rect(self):
        #print self.rect
        return self.rect

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_image(self):
        return self.image

    def get_inventory(self):
        return self.inventory

    def get_interactionnear(self):
        return self.interactnear

    def get_location(self):
        return self.location

    def get_attacking(self):
        return self.attacking

    def get_mana(self):
        return self.mana

    def get_health(self):
        return self.health

    def get_red(self):
        return self.red

    def addHealth(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health -= (self.health-self.maxHealth)
        
    def addMana(self, amount):
        self.mana += amount
        if self.mana > self.maxMana:
            self.mana -= (self.mana-self.maxMana)

    def setHealth(self, health):
        self.health = health

    def setMana(self, mana):
        self.mana = mana

    def inflictDamage(self, amount):
        self.health -= abs(amount)
        if self.red == False:
            self.redNum = 0
        if self.health < 0:
            print 'Game Over...'

    def fireBallAttack(self, attackGoalx, attackGoaly, projectiles):
        '''projectiles-- a sprite group containing all level projectiles'''
        if self.mana >= 10:#Mana system needs fixing for multiple powers ----- FIXXXX MEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
            deadlyBall = fireBall(self.rect.centerx,self.rect.centery,attackGoalx,attackGoaly)
            projectiles.add(deadlyBall)
            self.mana -= 10

    def swordAttack(self, chars, enemies):
        if self.attacking == False:
            self.attacking = True
            if self.left == False:#Attack block placed relative to picture must be adjusted if character picture is changed!! FIX MEEEEEEEEE
                killerBlock = attackBlock(self.rect.right-10,self.rect.y+30,10,5)
                killerBlock.update(False,chars,enemies)
            else:
                killerBlock = attackBlock(self.rect.x,self.rect.y+30,10,5)
                killerBlock.update(True,chars,enemies)

    def setLocation(self, location):
        self.location = location

    def loadImages(self, images):
        '''Images: 12 image string tuple
            Images is (faceright stand, stand attack, leftft step, rightft step, leftft stepAttack, rightft stepAttack,
            faceleft stand, stand attack, rightft step, leftft step, rightft stepAttack, leftft stepAttack)'''
        self.i0 = pygame.image.load(images[0]).convert_alpha()
        self.i1 = pygame.image.load(images[1]).convert_alpha()
        self.i2 = pygame.image.load(images[2]).convert_alpha()
        self.i3 = pygame.image.load(images[3]).convert_alpha()
        self.i4 = pygame.image.load(images[4]).convert_alpha()
        self.i5 = pygame.image.load(images[5]).convert_alpha()
        self.i6 = pygame.image.load(images[6]).convert_alpha()
        self.i7 = pygame.image.load(images[7]).convert_alpha()
        self.i8 = pygame.image.load(images[8]).convert_alpha()
        self.i9 = pygame.image.load(images[9]).convert_alpha()
        self.i10 = pygame.image.load(images[10]).convert_alpha()
        self.i11 = pygame.image.load(images[11]).convert_alpha()
        self.images = (self.i0,self.i1,self.i2,self.i3,self.i4,self.i5,self.i6,self.i7,self.i8,self.i9,self.i10,self.i11)

    def newRect(self, newx, newy, newwidth, newheight):
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        self.rect.x = newx
        self.rect.y = newy
        self.rect.width = newwidth
        self.rect.height = newheight
        #print self.rect
        
    def scaleSprite(self, ScaleVal):
        self.image = pygame.transform.scale(self.image, (int(self.RealWidth*ScaleVal), int(self.RealHeight*ScaleVal)))
        imageRect = self.image.get_rect()
        imageRect.bottom = self.rect.bottom
        imageRect.left = self.rect.left
        self.rect = imageRect   
        
    def Left(self, isleft):
        self.left = isleft
        
    def moveSprite(self, Xmove, Ymove, walls, items, chars, enemies):
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        self.rect.x += Xmove
        self.checkLeft()
        self.collCheckWallX(walls)
        self.rect.y += Ymove
        self.checkDown()
        self.collCheckWallY(walls)
        self.checkMovement()
        self.collCheckItem(items)
        self.collCheckInteract(chars)
        self.collCheckEnemies(enemies)
        
    def collCheckWallX(self, Walls):#check collision of wall Xaxis
        collisionList = pygame.sprite.spritecollide(self, Walls, False)
        for collision in collisionList:
            if self.left == False:
                self.rect.right = collision.get_left()
            else:
                self.rect.left = collision.get_right()
                
    def collCheckWallY(self, Walls):#check collision of wall Yaxis
        collisionList = pygame.sprite.spritecollide(self, Walls, False)
        for collision in collisionList:
            if self.down == True:
                self.rect.bottom = collision.get_top()
            else:
                self.rect.top = collision.get_bottom()
        
    def collCheckItem(self, Items):
        collisionList = pygame.sprite.spritecollide(self, Items, True)
        for collision in collisionList:
            item = collision.pickUp()
            self.updateInventory(item)

    def collCheckInteract(self, interacts):
        self.interactList = pygame.sprite.spritecollide(self, interacts, False)
        if len(self.interactList) > 0:
            self.interactnear = True
        else:
            self.interactnear = False

    def collCheckEnemies(self, enemies):
        playerZone = playerBlock(self.rect.x+34,self.rect.y,20,self.rect.height)        #Must be adjusted with new player image-- FIX MEEEEE
        collisionList = pygame.sprite.spritecollide(playerZone, enemies, False)
        for collision in collisionList:
            damage = collision.collPlayer()
            if damage > 0:
                self.inflictDamage(damage)

    def broadcastCoords(self,chars,enemies):
        for sprite in chars:
            sprite.recievePlayerCoords(self.rect.centerx-20, self.rect.y)
        for sprite in enemies:
            sprite.recievePlayerCoords(self.rect.centerx-20, self.rect.y)
                
    def update(self, moveX, moveY, Walls, Items, Chars, Enemies):
        self.moveSprite(moveX, moveY, Walls, Items, Chars, Enemies)
        self.broadcastCoords(Chars,Enemies)
        self.timeNum+=1
        if self.timeNum > self.timeTarget:
            self.stepChange()
            self.timeNum = 0
        if self.attacking == True:
            if self.attackNum <= self.attackTime:
                self.attackNum += 1
            else:
                self.attacking = False
                self.attackNum = 0
        self.isRed()
        self.chooseImageNum()
        self.render()


    def chooseImageNum(self):
        if self.moving == False:
            if self.left == False:
                if self.attacking == False:
                    self.currentImageNum = 0
                else:
                    self.currentImageNum = 1
            else:
                if self.attacking == False:
                    self.currentImageNum = 6
                else:
                    self.currentImageNum = 7
        else:
            if self.left == False:
                if self.leftStep == False:
                    if self.attacking == False: 
                        self.currentImageNum = 3
                    else:
                        self.currentImageNum = 5
                else:
                    if self.attacking == False:
                        self.currentImageNum = 2
                    else:
                        self.currentImageNum = 4
            else:
                if self.leftStep == False:
                    if self.attacking == False: 
                        self.currentImageNum = 8
                    else:
                        self.currentImageNum = 10
                else:
                    if self.attacking == False: 
                        self.currentImageNum = 9
                    else:
                        self.currentImageNum = 11

    def stepChange(self):
        if self.leftStep == False:
            self.leftStep = True
        else:
            self.leftStep = False

    def isRed(self):
        if self.redNum >= self.redDelay:
            self.red = False
        else:
            self.redNum += 1
            self.red = True

    def checkMovement(self):
        if self.oldx == self.rect.x and self.oldy == self.rect.y:
            self.moving = False
        else:
            self.moving = True

    def checkLeft(self):
        if self.oldx > self.rect.x:
            self.left = True
        elif self.oldx < self.rect.x:
            self.left = False

    def checkDown(self):
        if self.oldy > self.rect.y:
            self.down = False
        elif self.oldy < self.rect.y:
            self.down = True
        
    def playerInteract(self):
        if self.interactnear == True:
            self.interactList[0].interact()
                
    def render(self):
        self.image = self.images[self.currentImageNum]

    def adjustCurrentImg(self, adjustment):
        self.image = adjustment
        self.rect = self.image.get_rect()

    def updateInventory(self, item):
        for key in item.keys():
            if key in self.inventory:
                self.inventory[key] += item[key]
            else:
                self.inventory = dict(self.inventory.items() + item.items())

    def emptyInventory(self):
        self.inventory = {}

    def newInventory(self, inventory):
        self.inventory = inventory

    def searchInventory(self, itemStr):
        if itemStr in self.inventory:
            return True
        else:
            return False


class attackBlock(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,damageOnHit=4,knockBackonHit=20):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.damageOnHit = damageOnHit
        self.knockBackonHit = knockBackonHit

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_rect(self):
        return self.rect

    def update(self, left, chars, enemies):
        collisionList = pygame.sprite.spritecollide(self, chars, False)
        collisionList += pygame.sprite.spritecollide(self, enemies, False)
        #print str(collisionList)
        for collision in collisionList:
            if left == True:
                collision.inflictDamage(self.damageOnHit, -self.knockBackonHit)
            else:
                collision.inflictDamage(self.damageOnHit, self.knockBackonHit)
        self.kill()

class fireBall(pygame.sprite.Sprite):
    def __init__(self,x,y,targetx,targety,damageOnHit=2,knockBackonHit=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('items/fireBall.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.trueY = y
        self.trueX = x
        self.rect.center = (self.trueX, self.trueY) # set starting position
        self.speed = 20 # movement speed of the sprite
        self.target = (targetx,targety)
        self.damageOnHit = damageOnHit
        self.knockBackonHit = knockBackonHit

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_rect(self):
        return self.rect

    def destroy(self):
        self.sprite.kill()


    def update(self, enemies):
        self.collCheck(enemies)
        self.moveSprite()
        

    def collCheck(self, enemies):
        collisionList = pygame.sprite.spritecollide(self, enemies, False)
        #print str(collisionList)
        if len(collisionList) > 0:
            for collision in collisionList:
                collision.inflictDamage(self.damageOnHit, -self.knockBackonHit)
            self.kill()

    def scaleSprite(self, ScaleVal):
        self.image = pygame.transform.scale(self.image, (int(self.RealWidth*ScaleVal), int(self.RealHeight*ScaleVal)))
        imageRect = self.image.get_rect()
        imageRect.bottom = self.rect.bottom
        imageRect.left = self.rect.left
        self.rect = imageRect
        
    def get_direction(self, target):
        '''
        Function:
            takes total distance from sprite.center
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
        if self.target: # if the square has a target
            position = Vector(self.rect.centerx, self.rect.centery) # create a vector from center x,y value
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
        speed = self.speed ** 2 # gets aboslute value of the speed

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
        
        self.dir = self.get_direction(self.target) # get direction
        if self.dir: # if there is a direction to move
            
            if self.distance_check(self.dist): # if we need to stop
                self.rect.center = self.target # center the sprite on the target
                self.kill()
                
            else: # if we need to move normal
                self.trueX += (self.dir[0] * self.speed) # calculate speed from direction to move and speed constant
                self.trueY += (self.dir[1] * self.speed)
                self.rect.center = (round(self.trueX),round(self.trueY)) # apply values to sprite.center

        

class playerBlock(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
