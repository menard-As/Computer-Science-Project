import pygame
import random
import sys
import math

#/////////////////////////////////////////////////////////           COLOURS           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


BLACK = (0,0,0)
GREY = (75,75,75)
WHITE = (255,255,255)
BLUE =(50,50,255)
YELLOW = (255,255,0)
GREEN = (150,200,0)
LIGHTBLUE = (50,175,236)
RED = (255,50,50)
SKINCOLOUR = (235,160,130)
COLOUR = (150,200,0)


#/////////////////////////////////////////////////////////         VARIABLES           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


pygame.init()
size = (900,750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("coursework")
done= False
clock = pygame.time.Clock()
direction = "Down"
move = False
stgTimer = 0
mgTimer = 0
carbTimer = 0
smgTimer = 0
grenadeTimer = 0
smgCooldown = False
machinegunCooldown = False
shotgunCooldown = False
carbineCooldown = False
grenadeCooldown = False
mgAmmo = 30
stgAmmo = 5
carAmmo = 20
smgAmmo = 35
equippedWeapon = "MG"
weaponNo = 1
grenadeCount = 5
myDisplayFont =  pygame.font.SysFont("Impact",40)
grenadeICON = pygame.image.load("grenadeICON.png")
grenadePickupICON = pygame.image.load("grenadepickupICON.png")
gPickupCount = 0
enemyPresent = False
menu = True
spawnMenu = False
spawnLevel = False
mainMenuIMG = pygame.image.load("MainMenu.png")
lvl1IMG = pygame.image.load("level1.png")
room = 1
mx = 0
my = 0
changeWeapon = False
currentRoom = "room3,5.txt"
roomVert = 2
roomHorz = 1
moved = 50
shotted =  10
looked = 50
pickedUped = 1
changedGun = 4
usedItem = 2
spawnBoss = False
alive = False
dedCounter = 100
spawnPlayer = False
ammoUsing = mgAmmo
equippedWeapon = 'MG'

#/////////////////////////////////////////////////////////           CLASSES           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class wall(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos):
        super().__init__()
        wallNum = random.randint(1,5)
        wallImage = "wall"+str(wallNum)+".png"
        self.image = pygame.image.load(wallImage)
        self.rect = self.image.get_rect()
        self.rect.x = xpos*50
        self.rect.y = ypos*50
        self.name = "Wall Man"

    def update(self):
        self.kill()

class door(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos):
        super().__init__()
        if xpos > 15 or xpos < 3:
            doorImage = "doorVert.png"
        else:
            doorImage = "doorHorz.png"
        self.image = pygame.image.load(doorImage)
        self.rect = self.image.get_rect()
        self.rect.x = xpos*50  
        self.rect.y = ypos*50
        self.name = "door man"

    def update(self):
        self.kil()

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "Yeetus Maximus"
        self.origImage = pygame.image.load("playerMG.png")
        self.image = self.origImage
        self.direction = "null"
        self.health = 90
        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.rect.y = 120
        self.xSpeed = 0
        self.ySpeed = 0
    
    def update(self,keyPressed):
        if keyPressed[pygame.K_a]:
            self.xSpeed  = -5
        elif keyPressed[pygame.K_d]:
            self.xSpeed = 5
        else:
            self.xSpeed = 0
        if keyPressed[pygame.K_w]:
            self.ySpeed  =-5
        elif keyPressed[pygame.K_s]:
            self.ySpeed = 5
        else:
            self.ySpeed = 0
        self.rect.x = self.rect.x + self.xSpeed
        self.rect.y = self.rect.y + self.ySpeed

    def getDirection(self):
        return(self.direction)

    def equipWeapon(self,weapon):
        self.origImage = pygame.image.load("player"+str(weapon)+".png")

    def rotate(self, angle):
        self.rectx = self.rect.x
        self.recty = self.rect.y
        self.image = pygame.transform.rotate(self.origImage, angle)
        self.rect = self.image.get_rect()
        self.rect.y = self.recty
        self.rect.x = self.rectx
        
class grenade(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,xOffset,yOffset,explosion):
        super().__init__()
        self.image = pygame.image.load("grenade.png")
        self.explosionIMG = explosion
        self.rect = self.image.get_rect()
        self.rect.x = playerX + 15
        self.rect.y = playerY + 23
        self.xSpeed = int(15*xOffset)
        self.ySpeed = int(15*yOffset)
        self.timer = 75
        self.name = "boomBoi"

    def update(self):
        self.timer = self.timer - 1
        if self.timer > 25:
            self.rect.x  = self.rect.x + self.xSpeed
            self.rect.y = self.rect.y + self.ySpeed
            self.xpos = self.rect.x - 100
            self.ypos = self.rect.y - 90
        elif self.timer == 25:
            self.kill()
            explosionGroup.add(self)
            self.image = self.explosionIMG
            self.rect = self.image.get_rect()
            self.rect.x = self.xpos
            self.rect.y = self.ypos
            self.timer  = self.timer -1
        elif self.timer < 25 and self.timer > 0:
            self.timer = self.timer -1
        elif self.timer <= 0:
            self.kill()

class healthPickup(pygame.sprite.Sprite):
    def __init__(self,X,Y):
        super().__init__()
        self.image = pygame.image.load('healthpickupICON.png')
        self.rect = self.image.get_rect()
        self.rect.x = 50*X
        self.rect.y = 50*Y

    def update(self):
        self.kill()

         
class grenadePickup(pygame.sprite.Sprite):
    def __init__(self,X,Y):
        super().__init__()
        self.image = grenadePickupICON
        self.rect = self.image.get_rect()
        self.rect.x = 50*X
        self.rect.y = 50*Y

    def update(self):
        self.kill()

class straightBullet(pygame.sprite.Sprite):
    def __init__(self,X,Y,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([3,3])
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = X
        self.rect.y = Y
        self.xSpeed = 20*xOffset
        self.ySpeed = 20*yOffset
        self.name = "mg"

    def update(self):
        self.rect.x  = self.rect.x + self.xSpeed
        self.rect.y = self.rect.y + self.ySpeed
    
class machineGunBullet(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([3,3])
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = playerX + 15
        self.rect.y = playerY + 23
        self.xSpread = random.randint(-1,1)
        self.ySpread = random.randint(-1,1)
        self.xSpeed = int((50*xOffset) + self.xSpread)
        self.ySpeed = int((50*yOffset) + self.ySpread)
        self.name = "mg"

    def update(self):
        if self.rect.x < 905 and self.rect.x  > 0 and self.rect.y > 0 and self.rect.y < 755:
            self.rect.x  = self.rect.x + self.xSpeed
            self.rect.y = self.rect.y + self.ySpeed
        else:
            self.kill()

class smgBullet(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([2,2])
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = playerX + 15
        self.rect.y = playerY + 23
        self.xSpread = random.randint(-2,2)
        self.ySpread = random.randint(-2,2)
        self.xSpeed = int((40*xOffset) + self.xSpread)
        self.ySpeed = int((40*yOffset) + self.ySpread)
        self.name = "smg"

    def update(self):
        if self.rect.x < 905 and self.rect.x  > 0 and self.rect.y > 0 and self.rect.y < 755:
            self.rect.x  = self.rect.x + self.xSpeed
            self.rect.y = self.rect.y + self.ySpeed
        else:
            self.kill()

class shotgunBullet(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = playerX + 15
        self.rect.y = playerY + 23
        self.xSpread = random.randint(-5,5)
        self.ySpread = random.randint(-5,5)
        self.xSpeed = int((35*xOffset) + self.xSpread)
        self.ySpeed = int((35*yOffset) + self.ySpread)
        self.name = "stg"

    def update(self):
        if self.rect.x < 905 and self.rect.x  > 0 and self.rect.y > 0 and self.rect.y < 755:
            self.rect.x  = self.rect.x + self.xSpeed
            self.rect.y = self.rect.y + self.ySpeed
        else:
            self.kill()

class carbineBullet(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([6,6])
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = playerX + 15
        self.rect.y = playerY + 23
        self.xSpeed = int(60*xOffset)
        self.ySpeed = int(60*yOffset)
        self.name = "crb"

    def update(self):
        if self.rect.x < 905 and self.rect.x  > 0 and self.rect.y > 0 and self.rect.y < 755:
            self.rect.x  = self.rect.x + self.xSpeed
            self.rect.y = self.rect.y + self.ySpeed
        else:
            self.kill()

class heavyTurret(pygame.sprite.Sprite):
    def __init__(self,xPos,yPos):
        super().__init__()
        self.origImage = pygame.image.load("heavyTurret.png")
        self.image = self.origImage
        self.rect = self.image.get_rect()
        self.health = 150
        self.rect.x = xPos*50  
        self.rect.y = yPos*50
        self.shotCooldown = 40
        self.deathTimer = 20
        self.setExplode = False
        self.alreadyExplode = False
        self.name = "turretMan"
        self.collide = False
        self.playerCollide = False

    def update(self,playerX,playerY):
        if self.health > 0:
            run = (self.rect.x + 20) - playerX
            rise = (self.rect.y + 20) - playerY
            adjacent = run
            opposite = rise
            if run<0:
                run = run*-1
            if rise<0:
                rise = rise*-1
            if self.rect.x >= playerX and self.rect.y <= playerY:
                xDirection = -1
                yDirection = 1
            elif self.rect.x >= playerX and self.rect.y >= playerY:
                xDirection = -1
                yDirection = -1
            elif self.rect.x <= playerX and self.rect.y >= playerY:
                xDirection = 1
                yDirection = -1
            elif self.rect.x <= playerX and self.rect.y <= playerY:
                xDirection = 1
                yDirection = 1
            xOffset = (run/(rise+run))*xDirection
            yOffset = (rise/(rise+run))*yDirection

            if self.shotCooldown == 0:
                myProjection = projection(self.rect.x, self.rect.y, xOffset, yOffset)
                self.playerCollide = False
                self.collide = False
                while self.playerCollide == False and self.collide == False:
                    if pygame.sprite.spritecollide(myProjection,allSpritesGroup,False):
                        for x in pygame.sprite.spritecollide(myProjection,allSpritesGroup,False):
                            if x.name == player1.name:
                                self.playerCollide = True
                            elif x.name != "turretMan":
                                self.collide = True
                    myProjection.update()

            if self.playerCollide == True:
                if adjacent != 0 and opposite != 0:
                    if adjacent  < 0:
                        adjacent = adjacent*-1
                    if opposite < 0:
                        opposite = opposite*-1
                    radAngle = math.atan(opposite/adjacent)
                    angle = int((radAngle/(2*math.pi))*360)
                else:
                    angle = 0
                if self.rect.x+25 > (player1.rect.x+15) and self.rect.y < (player1.rect.y+23):
                    angle = (270+angle)
                elif self.rect.x  > (player1.rect.x+15) and self.rect.y > (player1.rect.y+23):
                    angle = (270-angle)
                elif self.rect.x  < (player1.rect.x+15) and self.rect.y > (player1.rect.y+23):
                    angle = (90+angle)
                elif self.rect.x  < (player1.rect.x+15) and self.rect.y < (player1.rect.y+23):
                    angle = (90-angle)
                origX = self.rect.x
                origY = self.rect.y
                self.image = pygame.transform.rotate(self.origImage, angle)
                self.rect = self.image.get_rect()
                self.rect.x = origX
                self.rect.y = origY
                if self.shotCooldown == 0:
                    myShot = carbineBullet(self.rect.x,self.rect.y,xOffset,yOffset)
                    heavyTurretBulletGroup.add(myShot)
                    self.shotCooldown = 40
                    
            if self.shotCooldown != 0:
                self.shotCooldown = self.shotCooldown - 1
        else:
            if self.setExplode == False:
                self.kill()
                explosionGroup.add(self)
                origX = self.rect.x
                origY = self.rect.y
                self.image= pygame.image.load("turretExplosion.png")
                self.rect.x = origX - 15
                self.rect.y = origY - 10
                self.setExplode = True
            elif self.setExplode == True and self.deathTimer >0:
                self.deathTimer = self.deathTimer - 1
            else:
                self.kill()

    def damage(self,damage):
        self.health = self.health - damage

class turret(pygame.sprite.Sprite):
    def __init__(self,xPos,yPos):
        super().__init__()
        self.origImage = pygame.image.load("turret.png")
        self.image = self.origImage
        self.rect = self.image.get_rect()
        self.health = 80
        self.rect.x = xPos*50  
        self.rect.y = yPos*50
        self.shotCooldown = 10
        self.deathTimer = 20
        self.setExplode = False
        self.alreadyExplode = False
        self.name = "turretMan"
        self.collide = False
        self.playerCollide = False

    def update(self,playerX,playerY):
        if self.health > 0:
            run = (self.rect.x + 25) - playerX
            rise = (self.rect.y + 25) - playerY
            adjacent = run
            opposite = rise
            if run<0:
                run = run*-1
            if rise<0:
                rise = rise*-1
            if self.rect.x+25 >= playerX and self.rect.y+25 <= playerY:
                xDirection = -1
                yDirection = 1
            elif self.rect.x+25 >= playerX and self.rect.y+25 >= playerY:
                xDirection = -1
                yDirection = -1
            elif self.rect.x+25 <= playerX and self.rect.y+25 >= playerY:
                xDirection = 1
                yDirection = -1
            elif self.rect.x+25 <= playerX and self.rect.y+25 <= playerY:
                xDirection = 1
                yDirection = 1
            xOffset = (run/(rise+run))*xDirection
            yOffset = (rise/(rise+run))*yDirection

            if self.shotCooldown == 0:
                myProjection = projection(self.rect.x, self.rect.y, xOffset, yOffset)
                self.playerCollide = False
                self.collide = False
                while self.playerCollide == False and self.collide == False:
                    if pygame.sprite.spritecollide(myProjection,allSpritesGroup,False):
                        for x in pygame.sprite.spritecollide(myProjection,allSpritesGroup,False):
                            if x.name == player1.name:
                                self.playerCollide = True
                            elif x.name != "turretMan":
                                self.collide = True
                    myProjection.update()

            if self.playerCollide == True:
                if adjacent != 0 and opposite != 0:
                    if adjacent  < 0:
                        adjacent = adjacent*-1
                    if opposite < 0:
                        opposite = opposite*-1
                    radAngle = math.atan(opposite/adjacent)
                    angle = int((radAngle/(2*math.pi))*360)
                else:
                    angle = 0
                if self.rect.x+25 > (player1.rect.x+15) and self.rect.y < (player1.rect.y+23):
                    angle = (270+angle)
                elif self.rect.x  > (player1.rect.x+15) and self.rect.y > (player1.rect.y+23):
                    angle = (270-angle)
                elif self.rect.x  < (player1.rect.x+15) and self.rect.y > (player1.rect.y+23):
                    angle = (90+angle)
                elif self.rect.x  < (player1.rect.x+15) and self.rect.y < (player1.rect.y+23):
                    angle = (90-angle)
                origX = self.rect.x
                origY = self.rect.y
                self.image = pygame.transform.rotate(self.origImage, angle)
                self.rect = self.image.get_rect()
                self.rect.x = origX
                self.rect.y = origY
                if self.shotCooldown == 0:
                    myShot = machineGunBullet(self.rect.x,self.rect.y,xOffset,yOffset)
                    turretBulletGroup.add(myShot)
                    self.shotCooldown = 10
                    
            if self.shotCooldown != 0:
                self.shotCooldown = self.shotCooldown - 1
        else:
            if self.setExplode == False:
                self.kill()
                explosionGroup.add(self)
                origX = self.rect.x
                origY = self.rect.y
                self.image= pygame.image.load("turretExplosion.png")
                self.rect.x = origX - 15
                self.rect.y = origY - 10
                self.setExplode = True
            elif self.setExplode == True and self.deathTimer >0:
                self.deathTimer = self.deathTimer - 1
            else:
                self.kill()

    def damage(self,damage):
        self.health = self.health - damage

class boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.origImage = pygame.image.load("boss.png")
        self.image = self.origImage
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 300
        self.health = 5000
        self.oldHealth = 5000
        self.attackTimer = 0
        self.attackDone = True
        self.laserOn = False
        self.laserCount = 0
        self.laserTime = 0
        self.vibeCheck = 90
        self.originalVibe = 90
        self.vibration = 5
        self.vibe = 1
        self.spinTick = 0 

    def damage(self,damage):
        self.health = self.health - damage

    def update(self,playerX,playerY):
        if self.health < 0:
            self.kill()
        if self.attackTimer == 0:
            self.attackNo = random.randint(1,3)
            self.attackDone = False
            if self.health < 1500:
                self.attackTimer = 30
            elif self.health < 2500:
                self.attackTimer = 50
            elif self.health < 3500:
                self.attackTimer = 65
            elif self.health < 4500:
                self.attackTimer = 75
            else:
                self.attackTimer = 90
        elif self.attackTimer > 0 and self.attackDone == True:
            self.attackTimer = self.attackTimer - 1
            
        if self.attackNo == 1 and self.attackDone == False:
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,0.2,0.2)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,-0.2,0.2)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,-0.2,-0.2)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,0.2,-0.2)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,0.2,0)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,0,0.2)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,-0.2,0)
                turretBulletGroup.add(myBullet)
            for c in range (0,10):
                myBullet = shotgunBullet(self.rect.x+100,self.rect.y+100,0,-0.2)
                turretBulletGroup.add(myBullet)
            self.attackDone = True
            
        elif self.attackNo == 2 and self.attackDone == False:
            if self.health < 2000:
                self.laserCount = 3
            elif self.health < 3500:
                self.laserCount = 2
            else:
                self.laserCount = 1
            self.laserTime = self.attackTimer*0.9
            self.laserWindUp = self.laserTime*0.6
            self.laserOn = True
            self.attackDone = True
            self.playerPositionFound = False
            
        elif self.attackNo == 3 and self.attackDone == False:
            if self.spinTick == 0:
                self.xOffset = 0
                self.yOffset = 1
                self.xChange = 1
                self.yChange = -1
                myBullet = straightBullet(self.rect.x+100,self.rect.y+100,self.xOffset,self.yOffset)
                turretBulletGroup.add(myBullet)
                self.spinTick = self.spinTick + 1
            elif self.spinTick == 10:
                self.xOffset = self.xOffset + (0.1*self.xChange)
                self.yOffset = self.yOffset + (0.1*self.yChange)
                self.xChange = self.xChange*-1
                myBullet = straightBullet(self.rect.x+100,self.rect.y+100,self.xOffset,self.yOffset)
                turretBulletGroup.add(myBullet)
                self.spinTick = self.spinTick + 1
            elif self.spinTick == 20:
                self.xOffset = self.xOffset + (0.1*self.xChange)
                self.yOffset = self.yOffset + (0.1*self.yChange)
                self.yChange = self.yChange*-1
                myBullet = straightBullet(self.rect.x+100,self.rect.y+100,self.xOffset,self.yOffset)
                turretBulletGroup.add(myBullet)
                self.spinTick = self.spinTick + 1
            elif self.spinTick <= 40:
                self.xOffset = self.xOffset + (0.1*self.xChange)
                self.yOffset = self.yOffset + (0.1*self.yChange)
                myBullet = straightBullet(self.rect.x+100,self.rect.y+100,self.xOffset,self.yOffset)
                turretBulletGroup.add(myBullet)
                self.spinTick = self.spinTick + 1
            else:
                self.attackDone = True
                self.spinTick = 0
            

        if self.health < 1000 and self.oldHealth >= 1000:
            self.virbation =  15
            self.originalVibe = 10
            oldX = self.rect.x
            oldY = self.rect.y
            self.image = pygame.image.load("boss4.png")
            self.rect = self.image.get_rect()
            self.rect.x = oldX
            self.rect.y = oldY
        elif self.health < 2000 and self.oldHealth >= 2000:
            self.virbation =  10
            self.originalVibe = 30
            oldX = self.rect.x
            oldY = self.rect.y
            self.image = pygame.image.load("boss3.png")
            self.rect = self.image.get_rect()
            self.rect.x = oldX
            self.rect.y = oldY
        elif self.health < 3000 and self.oldHealth >= 3000:
            self.virbation = 10
            self.originalVibe = 50
            oldX = self.rect.x
            oldY = self.rect.y
            self.image = pygame.image.load("boss2.png")
            self.rect = self.image.get_rect()
            self.rect.x = oldX
            self.rect.y = oldY
        elif self.health < 4000 and self.oldHealth >= 4000:
            self.virbation =  5
            self.originalVibe = 70
            oldX = self.rect.x
            oldY = self.rect.y
            self.image = pygame.image.load("boss1.png")
            self.rect = self.image.get_rect()
            self.rect.x = oldX
            self.rect.y = oldY
    
        self.oldHealth = self.health

        
        if self.laserOn == True:
            if self.playerPositionFound == False:
                run = (self.rect.x + 100) - playerX
                rise = (self.rect.y + 100) - playerY
                if run<0:
                    run = run*-1
                if rise<0:
                    rise = rise*-1
                if self.rect.x+100 > playerX and self.rect.y+100 <= playerY:
                    xDirection = -1
                    yDirection = 1
                elif self.rect.x+100 >= playerX and self.rect.y+100 >= playerY:
                    xDirection = -1
                    yDirection = -1
                elif self.rect.x+100 < playerX and self.rect.y+100 >= playerY:
                    xDirection = 1
                    yDirection = -1
                elif self.rect.x+100 <= playerX and self.rect.y+100 <= playerY:
                    xDirection = 1
                    yDirection = 1
                self.xOffset = (run/(rise+run))*xDirection
                self.yOffset = (rise/(rise+run))*yDirection
                self.playerPositionFound = True
                print(self.xOffset)
                print(self.yOffset)
            if self.laserTime < self.laserWindUp:
                myLaser = laser(self.rect.x+90,self.rect.y+90,self.xOffset,self.yOffset)
                laserGroup.add(myLaser)
            else:
                myLaser = targetLaser(self.rect.x+95,self.rect.y+95,self.xOffset,self.yOffset)
                laserGroup.add(myLaser)
            self.laserTime = self.laserTime - 1
            if self.laserTime == 0:
                self.laserOn = False

        if self.vibeCheck == 0:
            self.rect.x = self.rect.x + (self.vibe*self.vibration)
            self.rect.y = self.rect.y + (self.vibe*self.vibration)
            self.vibe = self.vibe*-1
            self.vibeCheck = self.originalVibe
        else:
            self.vibeCheck = self.vibeCheck - 1
            

class laser(pygame.sprite.Sprite):
    def __init__(self,X,Y,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([50,50])
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.rect.x = X
        self.rect.y = Y
        self.xSpeed = int(60*xOffset)
        self.ySpeed = int(60*yOffset)
        self.name = "lsrS"

    def update(self):
        self.rect.x = self.rect.x + self.xSpeed
        self.rect.y = self.rect.y + self.ySpeed


class targetLaser(pygame.sprite.Sprite):
    def __init__(self,X,Y,xOffset,yOffset):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = X
        self.rect.y = Y
        self.xSpeed = int(30*xOffset)
        self.ySpeed = int(30*yOffset)
        self.name = "lsrW"

    def update(self):
        self.rect.x = self.rect.x + self.xSpeed
        self.rect.y = self.rect.y + self.ySpeed

class projection(pygame.sprite.Sprite):
    def __init__(self,X,Y,xSpeed,ySpeed):
        super().__init__()
        self.image = pygame.Surface([1,1])
        self.rect = self.image.get_rect()
        self.rect.x = X
        self.rect.y = Y
        self.xSpeed = xSpeed*5
        self.ySpeed = ySpeed*5

    def update(self):
        self.rect.x = self.rect.x + self.xSpeed
        self.rect.y = self.rect.y + self.ySpeed
            
            
#////////////////////////////////////////////////////         SPRITE GROUPS            \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


hPickupGroup = pygame.sprite.Group()
gPickupGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
allSpritesGroup = pygame.sprite.Group()
shotgunBulletGroup = pygame.sprite.Group()
mgBulletGroup = pygame.sprite.Group()
carbineBulletGroup = pygame.sprite.Group()
smgBulletGroup = pygame.sprite.Group()
grenadeGroup = pygame.sprite.Group()
grenadePickupGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
turretGroup = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()
doorGroup = pygame.sprite.Group()
heavyTurretBulletGroup = pygame.sprite.Group()
turretBulletGroup = pygame.sprite.Group()
allButEnemyGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()
laserGroup = pygame.sprite.Group()

projectionGroup = pygame.sprite.Group()


#////////////////////////////////////////////////////           MAIN PROGRAM           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


while done == False:
    if menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
        if mx > 250 and mx < 615 and my > 250 and my < 450:
            menu = False
            alive = True
            spawnPlayer = False
        screen.blit(mainMenuIMG,(0,0))
        
    elif alive == True:
        if spawnPlayer == False:
            player1 = player()
            playerGroup.add(player1)
            spawnPlayer = True
        if player1.health <= 0:
            alive = False
            player1.kill()
        if spawnLevel == False:
            wallGroup.update()
            f =open(currentRoom)
            yCounter = 0
            xCounter = 0
            for line in f:
                for letter in line:
                    if letter == "w":
                        myWall = wall(xCounter,yCounter)
                        wallGroup.add(myWall)
                    elif letter == "d":
                        myDoor = door(xCounter,yCounter)
                        doorGroup.add(myDoor)
                    elif letter == "t":
                        myTurret = turret(xCounter,yCounter)
                        turretGroup.add(myTurret)
                    elif letter == "h":
                        myTurret = heavyTurret(xCounter,yCounter)
                        turretGroup.add(myTurret)
                    elif letter == 'g':
                        myPickup = grenadePickup(xCounter,yCounter)
                        gPickupGroup.add(myPickup)
                    elif letter == 'e':
                        myPickup = healthPickup(xCounter,yCounter)
                        hPickupGroup.add(myPickup)
                    xCounter = xCounter + 1
                xCounter = 0
                yCounter = yCounter + 1
            spawnLevel = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    changeWeapon = True
                    if changedGun > 0:
                        changedGun = changedGun - 1
                elif event.key == pygame.K_u:
                    myEnemy = turret()
                    enemyGroup.add(myEnemy)
        keyPressed = pygame.key.get_pressed()
        
        #Rotating the player to look at mouse
        mx, my = pygame.mouse.get_pos()
        opposite = (my-(player1.rect.y+23))
        adjacent = (mx - (player1.rect.x+15))

        if moved == 0 and looked > 0:
            looked = looked-1
        
        if adjacent != 0 and opposite != 0:
            if adjacent  < 0:
                adjacent = adjacent*-1
            if opposite < 0:
                opposite = opposite*-1
            radAngle = math.atan(opposite/adjacent)
            angle = int((radAngle/(2*math.pi))*360)
        else:
            angle = 0
        if mx > (player1.rect.x+15) and my < (player1.rect.y+23):
            player1.rotate(270+angle)
        elif mx > (player1.rect.x+15) and my > (player1.rect.y+23):
            player1.rotate(270-angle)
        elif mx < (player1.rect.x+15) and my > (player1.rect.y+23):
            player1.rotate(90+angle)
        elif mx < (player1.rect.x+15) and my < (player1.rect.y+23):
            player1.rotate(90-angle)

        #Changing weapon
        if changeWeapon == True:
            if weaponNo == 4:
                weaponNo = 1
            else:
                weaponNo = weaponNo + 1
                
            if weaponNo == 1:
                equippedWeapon = "MG"
                ammoUsingUsing = mgAmmo
            elif weaponNo == 2:
                equippedWeapon = "STG"
                ammoUsing = stgAmmo
            elif weaponNo == 3:
                equippedWeapon = "CAR"
                ammoUsing = carAmmo
            elif weaponNo == 4:
                equippedWeapon = "SMG"   
                ammoUsing = smgAmmo
                
            player1.equipWeapon(equippedWeapon)
            changeWeapon = False
    
    

        #Shooting & reloading weapons
        if keyPressed[pygame.K_SPACE]:
            run = (player1.rect.x+15) - mx
            rise = (player1.rect.y + 23) - my
            if run<0:
                run = run*-1
            if rise<0:
                rise = rise*-1

            if mx > (player1.rect.x+15) and my < (player1.rect.y+23):
                xDirection = 1
                yDirection = -1
            elif mx > (player1.rect.x+15) and my > (player1.rect.y+23):
                xDirection = 1
                yDirection = 1
            elif mx < (player1.rect.x+15) and my > (player1.rect.y+23):
                xDirection = -1
                yDirection = 1
            elif mx < (player1.rect.x+15) and my < (player1.rect.y+23):
                xDirection = -1
                yDirection = -1
    
            xOffset = (run/(rise+run))*xDirection
            yOffset = (rise/(rise+run))*yDirection
            
            if machinegunCooldown == False and equippedWeapon == "MG" and mgAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                myBullet = machineGunBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                mgBulletGroup.add(myBullet)
                machinegunCooldown = True
                mgAmmo = mgAmmo - 1
                ammoUsing = mgAmmo
            if shotgunCooldown == False and equippedWeapon == "STG" and stgAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                for shot in range(0,5):
                    myShotgunBullet = shotgunBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                    shotgunBulletGroup.add(myShotgunBullet)
                shotgunCooldown = True
                stgAmmo = stgAmmo - 1
                ammoUsing = stgAmmo
            if carbineCooldown == False and equippedWeapon == "CAR" and carAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                myCarbineBullet = carbineBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                carbineBulletGroup.add(myCarbineBullet)
                carbineCooldown = True
                carAmmo = carAmmo - 1
                ammoUsing = carAmmo
            if smgCooldown == False and equippedWeapon == "SMG" and smgAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                mySmgBullet = smgBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                smgBulletGroup.add(mySmgBullet)
                smgCooldown = True
                smgAmmo = smgAmmo - 1
                ammoUsing = smgAmmo
        if keyPressed[pygame.K_r]:
            if equippedWeapon ==  "MG":
                mgAmmo = 30
            elif equippedWeapon == "STG":
                stgAmmo = 5
            elif equippedWeapon == "CAR":
                carAmmo = 20
            elif equippedWeapon == "SMG":
                smgAmmo = 35
            
        if shotgunCooldown == True:
            if stgTimer == 40:
                shotgunCooldown = False
                stgTimer = 0
            else:
                stgTimer = stgTimer + 1
        if machinegunCooldown == True:
            if mgTimer == 5:
                machinegunCooldown = False
                mgTimer = 0
            else:
                mgTimer = mgTimer + 1
        if carbineCooldown == True:
            if carbTimer == 20:
                carbineCooldown = False
                carbTimer = 0
            else:
                carbTimer = carbTimer + 1
        if smgCooldown == True:
            if smgTimer == 2:
                smgCooldown = False
                smgTimer = 0
            else:
                smgTimer = smgTimer + 1

        #Grenades
        if keyPressed[pygame.K_g] and grenadeCooldown == False and grenadeCount > 0:
            usedItem = usedItem - 1
            run = (player1.rect.x+15) - mx
            rise = (player1.rect.y + 23) - my
            if run<0:
                run = run*-1
            if rise<0:
                rise = rise*-1
            if mx > (player1.rect.x+15) and my < (player1.rect.y+23):
                xDirection = 1
                yDirection = -1
            elif mx > (player1.rect.x+15) and my > (player1.rect.y+23):
                xDirection = 1
                yDirection = 1
            elif mx < (player1.rect.x+15) and my > (player1.rect.y+23):
                xDirection = -1
                yDirection = 1
            elif mx < (player1.rect.x+15) and my < (player1.rect.y+23):
                xDirection = -1
                yDirection = -1
    
            xOffset = (run/(rise+run))*xDirection
            yOffset = (rise/(rise+run))*yDirection
            
            myGrenade = grenade(player1.rect.x,player1.rect.y,xOffset,yOffset,pygame.image.load("explosion.png"))
            grenadeGroup.add(myGrenade)
            grenadeCooldown = True
            grenadeCount = grenadeCount - 1
        if grenadeCooldown == True:
            if grenadeTimer == 30:
                grenadeCooldown = False
                grenadeTimer = 0
            else:
                grenadeTimer = grenadeTimer + 1


        #SpawnBoss
        if currentRoom == 'room3,5.txt':
            if spawnBoss == False:
                myBoss = boss()
                allSpritesGroup.add(myBoss)
                spawnBoss = True
            if myBoss.health > 0:
                myBoss.update(player1.rect.x+23,player1.rect.y+23)


        
        #Adding all bullets to one group
        bulletGroup.add(heavyTurretBulletGroup)
        bulletGroup.add(turretBulletGroup)
        bulletGroup.add(carbineBulletGroup)
        bulletGroup.add(shotgunBulletGroup)
        bulletGroup.add(smgBulletGroup)
        bulletGroup.add(mgBulletGroup)
        
        #Updating groups
        laserGroup.update()
        bulletGroup.update()
        grenadeGroup.update()
        turretGroup.update((player1.rect.x),(player1.rect.y))
        enemyGroup.add(turretGroup)
        
        for e in enemyGroup:
            if pygame.sprite.spritecollide(e,mgBulletGroup,True):
                e.damage(20)
            if pygame.sprite.spritecollide(e,carbineBulletGroup,True):
                e.damage(35)
            if pygame.sprite.spritecollide(e,shotgunBulletGroup,True):
                e.damage(20)
            if pygame.sprite.spritecollide(e,smgBulletGroup,True):
                e.damage(15)
            if pygame.sprite.spritecollide(e,explosionGroup,False):
                if e.alreadyExplode == False:
                    e.damage(75)
                    e.alreadyExplode = True
        
        #Moving player
        if keyPressed[pygame.K_w] or keyPressed[pygame.K_a] or keyPressed[pygame.K_s] or keyPressed[pygame.K_d]:
            if moved > 0:
                moved = moved-1
            playerGroup.update(keyPressed)
            move == True
            direction = player1.getDirection()

        #Checking collisions : player and door
        if pygame.sprite.spritecollide(player1,doorGroup,False) and keyPressed[pygame.K_e]:
            if player1.rect.x > 800:
                roomHorz = roomHorz + 1
                player1.rect.x = player1.rect.x - 760
            elif player1.rect.x < 150:
                roomHorz = roomHorz - 1
                player1.rect.x = player1.rect.x + 760
            if player1.rect.y < 100:
                roomVert = roomVert - 1
                player1.rect.y = player1.rect.y + 610
            elif player1.rect.y > 650:
                roomVert = roomVert + 1
                player1.rect.y = player1.rect.y - 610
            currentRoom =  "room"+str(roomVert)+","+str(roomHorz)+".txt"
            spawnLevel = False
            
        #Checking collisions : player & walls
        if pygame.sprite.spritecollide(player1,wallGroup,False):
            if player1.xSpeed == 5:
                player1.rect.x = player1.rect.x - 5
            if player1.xSpeed == -5:
                player1.rect.x = player1.rect.x + 5
            if player1.ySpeed == 5:
                player1.rect.y = player1.rect.y - 5
            if player1.ySpeed == -5:
                player1.rect.y = player1.rect.y +  5

        #checking collisions : grenadePickups and Player
        if pygame.sprite.spritecollide(player1,gPickupGroup,True):
            if grenadeCount != 5:
                grenadeCount = grenadeCount + 1
                
            if pickedUped == 1:
                pickedUped = -69

        #checking collisions : healthPickups and Player
        if pygame.sprite.spritecollide(player1,hPickupGroup,True):
            if player1.health < 50:
                player1.health = player1.health + 50
            else:
                player1.health = 100
                
            if pickedUped == 1:
                pickedUped = -69
                

        #Checking collisions : bullets & walls
        pygame.sprite.groupcollide(wallGroup,bulletGroup,False,True)

        #checking collisiosns : boss
        if currentRoom == 'room3,5.txt':
            if pygame.sprite.spritecollide(myBoss,mgBulletGroup,True):
                myBoss.damage(20)
            if pygame.sprite.spritecollide(myBoss,carbineBulletGroup,True):
                myBoss.damage(35)
            if pygame.sprite.spritecollide(myBoss,shotgunBulletGroup,True):
                myBoss.damage(20)
            if pygame.sprite.spritecollide(myBoss,smgBulletGroup,True):
                myBoss.damage(15)
        
        #checking collisions : laser 
        pygame.sprite.groupcollide(wallGroup,laserGroup,False,True)
        if pygame.sprite.spritecollide(player1,laserGroup,False):
            for e in pygame.sprite.spritecollide(player1,laserGroup,False):
                if e.name == 'lsrS':
                    player1.health = player1.health-1
        
        #Checking collisions : grenades & walls
        if pygame.sprite.groupcollide(grenadeGroup,wallGroup,False,False):
            for i in pygame.sprite.groupcollide(grenadeGroup,wallGroup,False,False):
                gHorzProjection = projection(i.rect.x+10,i.rect.y-i.ySpeed,5,5)
                gVertProjection = projection(i.rect.x-i.xSpeed,i.rect.y+10,5,5)
                if pygame.sprite.spritecollide(gHorzProjection,wallGroup,False):
                    i.xSpeed = i.xSpeed*-1
                if pygame.sprite.spritecollide(gVertProjection,wallGroup,False):
                    i.ySpeed = i.ySpeed*-1

        #damaging player
        if pygame.sprite.spritecollide(player1,turretBulletGroup,True):
            player1.health = player1.health - 10
        if pygame.sprite.spritecollide(player1, heavyTurretBulletGroup,True):
            player1.health = player1.health - 25
            
        #Sprite groups
        for w in explosionGroup:
            if w.name == "boomBoi":
                w.update()
            elif w.name == "turretMan":
                w.update(0,0)

        allSpritesGroup.add(hPickupGroup)
        allSpritesGroup.add(gPickupGroup)
        allSpritesGroup.add(laserGroup)
        allSpritesGroup.add(explosionGroup)
        allSpritesGroup.add(turretBulletGroup)
        allSpritesGroup.add(enemyGroup)
        allSpritesGroup.add(heavyTurretBulletGroup)
        allSpritesGroup.add(grenadeGroup)
        allSpritesGroup.add(grenadePickupGroup)
        allSpritesGroup.add(bulletGroup)
        allSpritesGroup.add(wallGroup)
        allSpritesGroup.add(doorGroup)
        allButEnemyGroup.add(turretBulletGroup)
        allButEnemyGroup.add(heavyTurretBulletGroup)
        allButEnemyGroup.add(grenadeGroup)
        allButEnemyGroup.add(grenadePickupGroup)
        allButEnemyGroup.add(bulletGroup)
        allButEnemyGroup.add(wallGroup)
        allButEnemyGroup.add(doorGroup)
        allSpritesGroup.add(playerGroup)
        allButEnemyGroup.add(playerGroup)
        
        #Drawing everything on screen
        screen.fill(BLACK)
        allSpritesGroup.draw(screen)
        if currentRoom == "room2,1.txt":
            spawnBoss = False
            if moved > 0 and shotted > 0 and looked > 0 and changedGun > 0 and usedItem > 0:
                screen.blit(myDisplayFont.render("Move with the",1,RED),(330,80))
                screen.blit(pygame.image.load("moveKeys.png"),(565,60))
                screen.blit(myDisplayFont.render("YOU",1,RED),(110,60))
            elif moved == 0 and shotted > 0 and looked > 0 and changedGun > 0 and usedItem > 0:
                screen.blit(myDisplayFont.render("Look using the mouse",1,RED),(330,80))
                screen.blit(pygame.image.load("mouse.png"),(720,70))
            elif moved == 0 and shotted > 0 and looked == 0 and changedGun > 0 and usedItem > 0:
                screen.blit(myDisplayFont.render("Shoot with",1,RED),(330,80))
                screen.blit(pygame.image.load("spaceKey.png"),(550,60))
                screen.blit(myDisplayFont.render("Reload with",1,RED),(330,180))
                screen.blit(pygame.image.load("rKey.png"),(600,160))
                screen.blit(myDisplayFont.render("AMMO",1,RED),(80,550))
                screen.blit(pygame.image.load("arrowDown.png"),(120,610))
            elif moved == 0 and shotted == 0 and looked == 0 and changedGun > 0 and usedItem > 0:
                screen.blit(myDisplayFont.render("Change weapon with ",1,RED),(330,80))
                screen.blit(pygame.image.load("changeGunKey.png"),(720,60))
                screen.blit(myDisplayFont.render("Weapon",1,RED),(280,700))
                screen.blit(pygame.image.load("arrowLeft.png"),(180,710))
            elif moved == 0 and shotted == 0 and looked == 0 and changedGun == 0 and usedItem > 0:
                screen.blit(myDisplayFont.render("Use item",1,RED),(500,80))
                screen.blit(pygame.image.load("useItem.png"),(400,60))
                screen.blit(myDisplayFont.render("Item Type + Count",1,RED),(200,650))
                screen.blit(pygame.image.load("arrowLeft.png"),(100,660))
            elif moved == 0 and shotted == 0 and looked == 0 and changedGun == 0 and usedItem == 0 and pickedUped > 0:
                screen.blit(myDisplayFont.render("Run into pickups to get more",1,RED),(310,50))
                screen.blit(myDisplayFont.render("Items health or ammo.",1,RED),(310,100))
            else:
                screen.blit(myDisplayFont.render("You are ready, to go through the",1,RED),(320,80))
                screen.blit(myDisplayFont.render("door get close to it and press E",1,RED),(320,120))
        elif currentRoom == "room3,5.txt":
            screen.blit(myDisplayFont.render("Boss Health : " + str(myBoss.health),1,RED),(300,50))

        
        if ammoUsing > 10 or equippedWeapon == "STG":
            screen.blit(myDisplayFont.render(str(ammoUsing),1,GREEN),(100,700))
        else:
            screen.blit(myDisplayFont.render(str(ammoUsing),1,RED),(100,700))
        screen.blit(myDisplayFont.render("HP: "+str(player1.health),1,GREEN),(780,700))
        screen.blit(grenadeICON,(10,650))
        screen.blit(myDisplayFont.render(str(grenadeCount),1,YELLOW),(50,650))
        screen.blit(myDisplayFont.render(equippedWeapon,1,RED),(10,700))
    elif alive == False:
        if dedCounter == 0:
            menu = True
            currentRoom = "room2,1.txt."
        else:
            screen.fill(BLACK)
            screen.blit(myDisplayFont.render("YOU DIED",10,RED),(200,300))
            dedCounter = dedCounter - 1
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
