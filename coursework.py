import pygame
import random
import sys


#/////////////////////////////////////////////////////////           COLOURS           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


BLACK = (0,0,0)
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
level = 1
mx = 0
my = 0


#/////////////////////////////////////////////////////////           CLASSES           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class wall(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos):
        super().__init__()
        self.image = pygame.Surface([50,50])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = xpos*50
        self.rect.y = ypos*50

    def update(self):
        self.kil()

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("playerMGLeft.png")
        self.direction = "null"
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 20

    def update(self,keyPressed):
        if keyPressed[pygame.K_a]:
            self.rect.x = self.rect.x - 5
            self.direction = "Left"
        if keyPressed[pygame.K_d]:
            self.rect.x = self.rect.x +5
            self.direction = "Right"
        if keyPressed[pygame.K_w]:
            self.rect.y = self.rect.y - 5
            self.direction = "Up"
        if keyPressed[pygame.K_s]:
            self.rect.y = self.rect.y + 5
            self.direction = "Down"

    def getDirection(self):
        return(self.direction)

    def equipWeapon(self,weapon,direction):
        self.currentImage = "player"+str(weapon)+direction+".png"
        self.image = pygame.image.load(self.currentImage)
    
class grenade(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,direction,explosion):
        super().__init__()
        self.image = pygame.image.load("grenade.png")
        self.explosionIMG = explosion
        self.rect = self.image.get_rect()
        self.xspeed = 10
        self.yspeed = 5
        self.rect.x = playerX
        self.rect.y = playerY
        self.direction = direction
        self.timer = 75

    def update(self):
        self.timer = self.timer - 1
        if self.timer > 25:
            if self.direction == "Left":
                self.rect.x = self.rect.x - self.xspeed
            elif self.direction == "Right":
                self.rect.x = self.rect.x + self.xspeed
            elif self.direction == "Up":
                self.rect.y = self.rect.y - self.yspeed
            elif self.direction == "Down":
                self.rect.y = self.rect.y + self.yspeed
            self.xpos = self.rect.x - 100
            self.ypos = self.rect.y - 90 
        elif self.timer < 25 and self.timer > 1:
            self.image = self.explosionIMG
            self.rect = self.image.get_rect()
            self.rect.x = self.xpos
            self.rect.y = self.ypos
        elif self.timer == 0:
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
    def __init__(self,playerX,playerY,direction):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        if direction == "Left":
            self.rect.x = playerX
            self.rect.y = playerY+ 10
        if direction == "Right":
            self.rect.x = playerX+ 50
            self.rect.y = playerY+ 10
        if direction == "Up":
            self.rect.x = playerX+ 30
            self.rect.y = playerY
        if direction == "Down":
            self.rect.x = playerX+ 10
            self.rect.y = playerY+ 50
        self.direction = direction
        self.spread = random.randint(-1,1)

    def update(self):
        if self.rect.x > -5 and self.direction == "Left":
            self.rect.x = self.rect.x - 20
            self.rect.y = self.rect.y + self.spread
        elif self.rect.x < 1250 and self.direction == "Right":
            self.rect.x = self.rect.x + 20
            self.rect.y = self.rect.y + self.spread
        elif self.rect.y > -5 and self.direction == "Up":
            self.rect.y = self.rect.y - 20
            self.rect.x = self.rect.x + self.spread
        elif self.rect.y < 750 and self.direction == "Down":
            self.rect.y = self.rect.y + 20
            self.rect.x = self.rect.x + self.spread
        else:
            self.kill()

class smgBullet(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,direction):
        super().__init__()
        self.image = pygame.Surface([3,3])
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        if direction == "Left":
            self.rect.x = playerX + 10
            self.rect.y = playerY+ 10
        if direction == "Right":
            self.rect.x = playerX+ 50
            self.rect.y = playerY+ 10
        if direction == "Up":
            self.rect.x = playerX+ 25
            self.rect.y = playerY + 10
        if direction == "Down":
            self.rect.x = playerX+ 10
            self.rect.y = playerY+ 50
        self.direction = direction
        self.spread = random.randint(-2,2)

    def update(self):
        if self.rect.x > -5 and self.direction == "Left":
            self.rect.x = self.rect.x - 15
            self.rect.y = self.rect.y + self.spread
        elif self.rect.x < 1250 and self.direction == "Right":
            self.rect.x = self.rect.x + 15
            self.rect.y = self.rect.y + self.spread
        elif self.rect.y > -5 and self.direction == "Up":
            self.rect.y = self.rect.y - 15
            self.rect.x = self.rect.x + self.spread
        elif self.rect.y < 750 and self.direction == "Down":
            self.rect.y = self.rect.y + 15
            self.rect.x = self.rect.x + self.spread
        else:
            self.kill()

class shotgunBullet(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,direction):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        if direction == "Left":
            self.rect.x = playerX
            self.rect.y = playerY+ 10
        if direction == "Right":
            self.rect.x = playerX+ 50
            self.rect.y = playerY+ 10
        if direction == "Up":
            self.rect.x = playerX+ 30
            self.rect.y = playerY
        if direction == "Down":
            self.rect.x = playerX+ 10
            self.rect.y = playerY+ 50
        self.direction = direction
        self.spread = random.randint(-3,3)

    def update(self):
        if self.rect.x > -5 and self.direction == "Left":
            self.rect.x = self.rect.x - 10
            self.rect.y = self.rect.y + self.spread
        elif self.rect.x < 1250 and self.direction == "Right":
            self.rect.x = self.rect.x + 10
            self.rect.y = self.rect.y + self.spread
        elif self.rect.y > -5 and self.direction == "Up":
            self.rect.y = self.rect.y - 10
            self.rect.x = self.rect.x + self.spread
        elif self.rect.y < 750 and self.direction == "Down":
            self.rect.y = self.rect.y + 10
            self.rect.x = self.rect.x + self.spread
        else:
            self.kill()

class carbineBulletHorz(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,direction):
        super().__init__()
        self.image = pygame.Surface([20,5])
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        if direction == "Left":
            self.rect.x = playerX
            self.rect.y = playerY+ 10
        if direction == "Right":
            self.rect.x = playerX+ 50
            self.rect.y = playerY+ 10
        self.direction = direction

    def update(self):
        if self.rect.x > -5 and self.direction == "Left":
            self.rect.x = self.rect.x - 40
        elif self.rect.x < 1250 and self.direction == "Right":
            self.rect.x = self.rect.x + 40
        else:
            self.kill()

class carbineBulletVert(pygame.sprite.Sprite):
    def __init__(self,playerX,playerY,direction):
        super().__init__()
        self.image = pygame.Surface([5,20])
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        if direction == "Up":
            self.rect.x = playerX+ 30
            self.rect.y = playerY
        if direction == "Down":
            self.rect.x = playerX+ 10
            self.rect.y = playerY+ 50
        self.direction = direction
        
    def update(self):
        if self.rect.y > -5 and self.direction == "Up":
            self.rect.y = self.rect.y - 40
        elif self.rect.y < 750 and self.direction == "Down":
            self.rect.y = self.rect.y + 40
        else:
            self.kill()

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30,30])
        self.rect = self.image.get_rect()
        self.image.fill(SKINCOLOUR)
        self.health = 80
        self.rect.x = 300
        self.rect.y = 300

    def update(self,damage):
        self.health = self.health - damage
        if self.health < 0:
            self.kill()

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
wallGroup = pygame.sprite.Group()
player1 = player()
playerGroup.add(player1)
allSpritesGroup.add(playerGroup)


#////////////////////////////////////////////////////           MAIN PROGRAM           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


while done == False:
    if menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
            #checks the mouse to see if the user has clicked on a button
                mx, my = pygame.mouse.get_pos()
                print(mx)
                print(my)
        if mx > 267 and mx < 608 and my > 221 and my < 355:
            menu = False
        print(menu)
        screen.blit(mainMenuIMG,(0,0))
    else:
        if spawnLevel == False:
            if level == 1:
                f =open("level1.txt","r")
            elif level == 2:
                f = open("level2.txt","r")
            yCounter = 0
            xCounter = 0
            for line in f:
                for letter in line:
                    if letter == "w":
                        myWall = wall(xCounter,yCounter)
                        wallGroup.add(myWall)
                    xCounter = xCounter + 1
                xCounter = 0
                yCounter = yCounter + 1
            spawnLevel = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if weaponNo == 4:
                        weaponNo = 1
                    else:
                        weaponNo = weaponNo + 1
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_w] or keyPressed[pygame.K_a] or keyPressed[pygame.K_s] or keyPressed[pygame.K_d]:
            playerGroup.update(keyPressed)
            move == True
            direction = player1.getDirection()
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
        if keyPressed[pygame.K_SPACE] and machinegunCooldown == False and equippedWeapon == "MG" and mgAmmo > 0:
            myBullet = machineGunBullet(player1.rect.x,player1.rect.y,direction)
            mgBulletGroup.add(myBullet)
            machinegunCooldown = True
            mgAmmo = mgAmmo - 1
        if keyPressed[pygame.K_SPACE] and shotgunCooldown == False and equippedWeapon == "STG" and stgAmmo > 0:
            for c in range(0,10):
                myShotgunBullet = shotgunBullet(player1.rect.x,player1.rect.y,direction)
                shotgunBulletGroup.add(myShotgunBullet)
            shotgunCooldown = True
            stgAmmo = stgAmmo - 1
        if keyPressed[pygame.K_SPACE] and carbineCooldown == False and equippedWeapon == "CAR" and carAmmo > 0:
            if direction == "Up" or direction == "Down":
                myCarbineBullet = carbineBulletVert(player1.rect.x,player1.rect.y,direction)
            elif direction == "Left" or direction == "Right":
                myCarbineBullet = carbineBulletHorz(player1.rect.x,player1.rect.y,direction)
            carbineBulletGroup.add(myCarbineBullet)
            carbineCooldown = True
            carAmmo = carAmmo - 1
        if keyPressed[pygame.K_SPACE] and smgCooldown == False and equippedWeapon == "SMG" and smgAmmo > 0:
            mySmgBullet = smgBullet(player1.rect.x,player1.rect.y,direction)
            smgBulletGroup.add(mySmgBullet)
            smgCooldown = True
            smgAmmo = smgAmmo - 1
        if keyPressed[pygame.K_g] and grenadeCooldown == False and grenadeCount > 0:
            myGrenade = grenade(player1.rect.x,player1.rect.y,direction,pygame.image.load("explosion.png"))
            grenadeGroup.add(myGrenade)
            grenadeCooldown = True
            grenadeCount = grenadeCount - 1
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
        if grenadeCooldown == True:
            if grenadeTimer == 30:
                grenadeCooldown = False
                grenadeTimer = 0
            else:
                grenadeTimer = grenadeTimer + 1
        #if gPickupCount < 5:
                #for c in range(1,5-gPickupCount):
               #myPickup = grenadePickup()
              #grenadePickupGroup.add(myPickup)
                #gPickupCount = gPickupCount + 1
        #pickupGrenade = pygame.sprite.spritecollideany(player1,grenadePickupGroup)
        #if pickupGrenade:                       
            #pickupGrenade.update()
            #gPickupCount = gPickupCount - 1
           # if grenadeCount < 5:
           # grenadeCount = grenadeCount + 1
        if keyPressed[pygame.K_u]:
            myEnemy = enemy()
            enemyGroup.add(myEnemy)
        player1.equipWeapon(equippedWeapon,direction)
        bulletGroup.add(carbineBulletGroup)
        bulletGroup.add(shotgunBulletGroup)
        bulletGroup.add(smgBulletGroup)
        bulletGroup.add(mgBulletGroup)
        bulletGroup.update()
        grenadeGroup.update()
        if pygame.sprite.groupcollide(smgBulletGroup,enemyGroup,True,False):
            enemyGroup.update(10)
        if pygame.sprite.groupcollide(carbineBulletGroup,enemyGroup,True,False):
            enemyGroup.update(25)
        if pygame.sprite.groupcollide(mgBulletGroup,enemyGroup,True,False):
            enemyGroup.update(20)
        if pygame.sprite.groupcollide(shotgunBulletGroup,enemyGroup,True,False):
            enemyGroup.update(40)
        if pygame.sprite.groupcollide(grenadeGroup,enemyGroup,False,False):
            enemyGroup.update(80)
        if pygame.sprite.spritecollide(player1,wallGroup,False):
            if player1.direction == "Left":
                player1.rect.x = player1.rect.x + 5
            elif player1.direction == "Right":
                player1.rect.x = player1.rect.x - 5
            elif player1.direction == "Up":
                player1.rect.y = player1.rect.y + 5
            elif player1.direction == "Down":
                player1.rect.y = player1.rect.y - 5
        pygame.sprite.groupcollide(wallGroup,bulletGroup,False,True)
        if pygame.sprite.groupcollide(grenadeGroup,wallGroup,False,False):
            for i in pygame.sprite.groupcollide(grenadeGroup,wallGroup,False,False):
                i.xspeed = 0
                i.yspeed = 0
        allSpritesGroup.add(enemyGroup)
        allSpritesGroup.add(grenadeGroup)
        allSpritesGroup.add(grenadePickupGroup)
        allSpritesGroup.add(bulletGroup)
        allSpritesGroup.add(wallGroup)
        #if level == 1:
           # screen.blit(lvl1IMG,(0,0))
        screen.fill(BLACK)
        screen.blit(grenadeICON,(10,650))
        screen.blit(myDisplayFont.render(str(grenadeCount),1,YELLOW),(50,650))
        screen.blit(myDisplayFont.render(equippedWeapon,1,RED),(10,700))
        if ammoUsing > 10 or equippedWeapon == "STG":
            screen.blit(myDisplayFont.render(str(ammoUsing),1,GREEN),(100,700))
        else:
            screen.blit(myDisplayFont.render(str(ammoUsing),1,RED),(100,700))
        allSpritesGroup.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
