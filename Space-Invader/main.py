import pygame
import math
import random

from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('Space-Invader/assets/background.png')

#Background sound
mixer.music.load('Space-Invader/assets/background.wav')
mixer.music.play(-1) #-1 to play in a loop

#Title and Icon
pygame.display.set_caption("Game")
icon = pygame.image.load("Space-Invader/assets/game.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('Space-Invader/assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('Space-Invader/assets/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('Space-Invader/assets/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5

#Ready - You can't see the bullet on the screen
#Fire - The bullet is currently moving
bullet_state = "ready"  

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


#Game Loop
running = True
while running:
    #RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    #Backgound Image
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if Keystroke is pressed check whether its right, left, up or dowm
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            #if event.key == pygame.K_UP:
                #playerY_change = -5
            #if event.key == pygame.K_DOWN:
                #playerY_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Space-Invader/assets/laser.wav')
                    bullet_sound.play()
                    #Get the current x coordinates of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0


    #checking for boundary of spcaeship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736: #800-64
        playerX = 736

    #playerY += playerY_change
    #if playerY <= 0:
    #    playerY = 0
    #elif playerY >= 536:
    #    playerY = 536

    #enemy movement
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 440: #and enemyX[i] == playerX :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
    
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736: #800-64
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

            
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('Space-Invader/assets/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)
    
    pygame.display.update()