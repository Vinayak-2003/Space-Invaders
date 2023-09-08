import pygame
from pygame import mixer
import random
import math


#initialize pygame(imp)
pygame.init()

#creating a screen
screen = pygame.display.set_mode((1200,700))                                       #(width,height)

#Background
background = pygame.image.load('images/space.jpg')

#background sound
mixer.music.load('music/background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")                                        #title
icon = pygame.image.load('images/ufo.png')                                          #icon
pygame.display.set_icon(icon)


#player(spaceship)
playerShip = pygame.image.load('images/spaceShip.png')                              #adding spaceship 
playerX = 570
playerY = 550
playerX_change = 0

def player(x,y):                                                                    #calling player's spaceship
    screen.blit(playerShip, (x,y))


#Enemies
alienG = []
alienGX = []
alienGY = []
alienGX_change = [0.3]
alienGY_change = [40]
num_of_alienG = 4

alienB = pygame.image.load('images/alienB.png')                                     #Enemy 1
alienBX = random.randint(0,1135)
alienBY = random.randint(50,300)
alienBX_change = 0.3
alienBY_change = 40

for i in range(num_of_alienG):
    alienG.append(pygame.image.load('images/alienG.png'))                                     #Enemy 2
    alienGX.append(random.randint(0,1135))
    alienGY.append(random.randint(50,300))
    alienGX_change.append(0.3)
    alienGY_change.append(40)

alienV = pygame.image.load('images/alienV.png')                                     #Enemy 3
alienVX = random.randint(0,1135)
alienVY = random.randint(50,300)
alienVX_change = 0.3
alienVY_change = 40

#---------Bullet----------#
    #ready --> you can't see the bullet on the screen
    #fire  --> the bullet is currently moving
    
bullet = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 550
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

#font
score = 0
font = pygame.font.Font('freesansbold.ttf',50)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',100)

def show_score(tx,ty):
    scoreDisplay = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(scoreDisplay , (tx,ty))

def game_over_text():
    gameOver = font.render('GAME OVER', True, (255,255,255))
    screen.blit(gameOver , (600,350))


#defining enemy function
def alienBlue(bx,by):                                                               #adding enemy 1
    screen.blit(alienB, (bx,by))

def alienGreen(gx,gy,i):                                                              #adding enemy 2
    screen.blit(alienG[i], (gx,gy))

def alienViolet(vx,vy):                                                             #adding enemy 3
    screen.blit(alienV, (vx,vy))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet , (x+16 , y+10))

def isCollisionB(alienBX,alienBY,bulletX,bulletY):
    distanceB = math.sqrt((math.pow(alienBX-bulletX,2)) + (math.pow(alienBY-bulletY,2)))
    if distanceB < 27:
        return True
    else:
        return False
    
def isCollisionG(alienGX,alienGY,bulletX,bulletY):
    distanceG = math.sqrt((math.pow(alienGX-bulletX,2)) + (math.pow(alienGY-bulletY,2)))
    if distanceG < 27:
        return True
    else:
        return False
    
def isCollisionV(alienVX,alienVY,bulletX,bulletY):
    distanceV = math.sqrt((math.pow(alienVX-bulletX,2)) + (math.pow(alienVY-bulletY,2)))
    if distanceV < 27:
        return True
    else:
        return False

#closing or ending of the window
running = True
while running:

    screen.fill((0,0,0))

    #background
    screen.blit(background , (0,0))

    for event in pygame.event.get():                                                #for quiting the window using cross
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('music/laser.wav')                   #adding sound to collision
                    bullet_sound.play()

                    bulletX = playerX                           #get the current xcoordinate of spaceship
                    fire_bullet(bulletX , bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


#changing left or right as directed by keyboard
    playerX += playerX_change                                                       

    if playerX <= 0:
        playerX = 0
    elif playerX >= 1136:
        playerX = 1136

#------------------Enemy movement-----------------------#
    alienBX += alienBX_change

    if alienBX <= 0:
        alienBX_change = 0.3
        alienBY += alienBY_change
    if alienBX >= 1136:
        alienBX_change = -0.3
        alienBY += alienBY_change

    for i in range(num_of_alienG):

        alienGX[i] += alienGX_change[i]
        if alienGX[i] <= 0:
            alienGX_change[i] = 0.3
            alienGY[i] += alienGY_change[i]
        elif alienGX[i] >= 1136:
            alienGX_change[i] = -0.3
            alienGY[i] += alienGY_change[i]

        collisionG = isCollisionG(alienGX[i],alienGY[i],bulletX,bulletY)
        if collisionG:
            explosion_sound = mixer.Sound('music/explosion.wav')                   #adding sound to collision
            explosion_sound.play()
            bulletY = 550
            bullet_state = 'ready'
            score += 5
            alienGX[i] = random.randint(0,1135)
            alienGY[i] = random.randint(50,300)

        alienGreen(alienGX[i] , alienGY[i], i)


    alienVX += alienVX_change

    if alienVX <= 0:
        alienVX_change = 0.3
        alienVY += alienVY_change
    if alienVX >= 1136:
        alienVX_change = -0.3
        alienVY += alienVY_change

    if bulletY <= 0:                                                               #multiple bullets
        bulletY = 550
        bullet_state = 'ready'

    #bullet movement
    if bullet_state == 'fire':
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

    #collision
    collisionB = isCollisionB(alienBX,alienBY,bulletX,bulletY)
    if collisionB:
        explosion_sound = mixer.Sound('music/explosion.wav')                   #adding sound to collision
        explosion_sound.play()
        bulletY = 550
        bullet_state = 'ready'
        score += 5
        alienBX = random.randint(0,1135)
        alienBY = random.randint(50,300)
        

    collisionV = isCollisionV(alienVX,alienVY,bulletX,bulletY)
    if collisionV:
        explosion_sound = mixer.Sound('music/explosion.wav')                   #adding sound to collision
        explosion_sound.play()
        bulletY = 550
        bullet_state = 'ready'
        score += 5
        alienVX = random.randint(0,1135)
        alienVY = random.randint(50,300)

#calling spaceShip
    player(playerX , playerY)

#calling enemies
    alienBlue(alienBX , alienBY)
    alienViolet(alienVX , alienVY)
    show_score(textX , textY)


    pygame.display.update()                 #things which have to show infinitely(imp )