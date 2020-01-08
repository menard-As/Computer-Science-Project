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
currentRoom = "room2,1.txt"
roomVert = 2
roomHorz = 1
moved = 50
shotted =  10
looked = 50
changedGun = 4
usedItem = 2


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
        self.health = 100
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
            
class grenadePickup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = grenadePickupICON
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,850)
        self.rect.y = random.randint(0,700)

    def update(self):
        self.kill()
    
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

player1 = player()
playerGroup.add(player1)
allSpritesGroup.add(playerGroup)
allButEnemyGroup.add(playerGroup)

projectionGroup = pygame.sprite.Group()


#////////////////////////////////////////////////////           MAIN PROGRAM           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


while done == False:
    if menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
        if mx > 267 and mx < 608 and my > 221 and my < 355:
            menu = False
        screen.blit(mainMenuIMG,(0,0))
    else:
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
            player1.equipWeapon(equippedWeapon)
            changeWeapon = False
        if weaponNo == 1:
            equippedWeapon = "MG"
            ammoUsing = mgAmmo
        elif weaponNo == 2:
            equippedWeapon = "STG"
            ammoUsing = stgAmmo
        elif weaponNo == 3:
            equippedWeapon = "CAR"
            ammoUsing = carAmmo
        elif weaponNo == 4:
            equippedWeapon = "SMG"
            ammoUsing = smgAmmo
    

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
            if shotgunCooldown == False and equippedWeapon == "STG" and stgAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                for shot in range(0,5):
                    myShotgunBullet = shotgunBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                    shotgunBulletGroup.add(myShotgunBullet)
                shotgunCooldown = True
                stgAmmo = stgAmmo - 1
            if carbineCooldown == False and equippedWeapon == "CAR" and carAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                myCarbineBullet = carbineBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                carbineBulletGroup.add(myCarbineBullet)
                carbineCooldown = True
                carAmmo = carAmmo - 1
            if smgCooldown == False and equippedWeapon == "SMG" and smgAmmo > 0:
                if shotted > 0:
                    shotted = shotted - 1
                mySmgBullet = smgBullet(player1.rect.x,player1.rect.y,xOffset,yOffset)
                smgBulletGroup.add(mySmgBullet)
                smgCooldown = True
                smgAmmo = smgAmmo - 1
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


        #Adding all bullets to one group
        bulletGroup.add(heavyTurretBulletGroup)
        bulletGroup.add(turretBulletGroup)
        bulletGroup.add(carbineBulletGroup)
        bulletGroup.add(shotgunBulletGroup)
        bulletGroup.add(smgBulletGroup)
        bulletGroup.add(mgBulletGroup)

        #Updating groups
        bulletGroup.update()
        grenadeGroup.update()
        turretGroup.update((player1.rect.x+23),(player1.rect.y+23))
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

        #Checking collisions : bullets & walls
        pygame.sprite.groupcollide(wallGroup,bulletGroup,False,True)

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
        
        #Drawing everything on screen
        screen.fill(BLACK)
        allSpritesGroup.draw(screen)
        if currentRoom == "room2,1.txt":
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
        if ammoUsing > 10 or equippedWeapon == "STG":
            screen.blit(myDisplayFont.render(str(ammoUsing),1,GREEN),(100,700))
        else:
            screen.blit(myDisplayFont.render(str(ammoUsing),1,RED),(100,700))
        screen.blit(grenadeICON,(10,650))
        screen.blit(myDisplayFont.render("HP: "+str(player1.health),1,GREEN),(780,700))
        screen.blit(myDisplayFont.render(str(grenadeCount),1,YELLOW),(50,650))
        screen.blit(myDisplayFont.render(equippedWeapon,1,RED),(10,700))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
