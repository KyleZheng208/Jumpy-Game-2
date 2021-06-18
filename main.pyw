# Imports
import pygame
from pygame import mixer
import random
import time

pygame.init()

#################################################

# The screen
screen = pygame.display.set_mode((800, 300))

#################################################

# Sprites and Sounds

# Music
music = mixer.Sound('music.mp3')
music.set_volume(0.1)
music.play(-1)

# Function to generate sprites
def generate(x, y, entity):
    screen.blit(entity, (x, y))

# Font
font = pygame.font.Font('freesansbold.ttf', 27)


# Score
score = 0
textX = 10
textY = 10

def show_score(x, y):
    # Rendering the text
    scoreText = font.render("Score: " + str(score), True, (0, 0, 0))
    # Drawing the text
    screen.blit(scoreText, (x, y))


# Lives
lives = 3
liveX = 10
liveY = 40

def show_lives(x, y):
    # Rendering the text
    liveText = font.render("Lives: " + str(lives), True, (0, 0, 0))
    # Drawing the text
    screen.blit(liveText, (x, y))



# Game Over
text2X = 325
text2Y = 50

def over(x, y):
    # Rendering the text
    overText = font.render("GAME OVER", True, (0, 0, 0))
    # Drawing the text
    screen.blit(overText, (x, y))


# Player
global playerX
playerImg = pygame.image.load('player.png')
playerRect = playerImg.get_rect()
playerY = 201
playerX = 25
playerXrateRight = 0
playerXrateLeft = 0
playerYrate = 0
v = 16
m = 0.2
jump = False

# Player Movment
def move(rate, rate2):
    global playerX
    if playerX > -1 and playerX < 776:
        playerX += rate
        playerX -= rate2
    if playerX < -1:
        playerX = 0
    if playerX > 776:
        playerX = 775


# Short Wall
sWallImg = pygame.image.load('shortWall.png')
sWallRect = sWallImg.get_rect()
sWallX = 3000
sWallY = 190



# Normal Wall
wallImg = pygame.image.load('wall.png')
wallRect = wallImg.get_rect()
wallX = 3000
wallY = 170


# Tall Wall
tWallImg = pygame.image.load('tallWall.png')
tWallRect = tWallImg.get_rect()
tWallX = 3000
tWallY = 160


# Hole
holeImg = pygame.image.load('hole.png')
holeRect = holeImg.get_rect()
holeX = 3000
holeY = 250

# Random Generation Stuff
ObstacleImgs = [holeImg, sWallImg, wallImg, tWallImg]
ObstacleX = [holeX, sWallX, wallX, tWallX]
ObstacleY = [holeY, sWallY, wallY, tWallY]
onScreen = [0, 1, 2, 3]
goal = 0
randObstacle = random.randint(0, 3)

# Icon and Caption
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Jumpy Game 2")

# Background
titleScreenImg = pygame.image.load('titleScreen.png')
bg = pygame.image.load('bg.png')


#################################################

# Main Game Loop
hit = False
running = False
run = True
var = True
while run:
    # Title Screen
    if running == False:
        screen.blit(titleScreenImg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                titleScreenImg = bg
                running = True
            if event.type == pygame.QUIT:
                run = False
                running = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
            if event.type == pygame.KEYDOWN and var == True:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerXrateRight = 8.5
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerXrateLeft = 8.5
                if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE and jump == False:
                    jumpS = mixer.Sound('step.mp3')
                    jumpS.set_volume(0.5)
                    jumpS.play()
                    jump = True
            if event.type == pygame.KEYUP and var == True:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerXrateRight = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerXrateLeft = 0
        
        # Jumping
        if jump and var == True:
            F =(1 / 2)*m*(v**2)
            playerY-= F
            v = v-1
            if v<0:
                m =-0.2
            if v == -17:
                land = mixer.Sound('land.mp3')
                land.set_volume(0.5)
                land.play()
                jump = False
                v = 16
                m = 0.2

        screen.fill((0, 0, 0))
        playerRect.x = playerX
        playerRect.y = playerY
        holeRect.x = holeX
        holeRect.y = holeY
        sWallRect.x = sWallX
        sWallRect.y = sWallY
        wallRect.x = wallX
        wallRect.y = wallY
        tWallRect.x = tWallX
        tWallRect.y = tWallY
        generate(0, 0, bg)
        move(playerXrateRight, playerXrateLeft)

        # Random Generation
        for obstacle in onScreen:
            generate(ObstacleX[obstacle], ObstacleY[obstacle], ObstacleImgs[obstacle])
            playerRect.x = playerX
            playerRect.y = playerY
            holeRect.x = holeX
            holeRect.y = holeY
        
        generate(playerX, playerY, playerImg)
        if playerX >= 775:
            jump = False
            v = 16
            m = 0.2
            playerY = 201
            score += 1
            playerX = 50
            sWallX = holeX - random.randint(-500, 50)
            wallX = holeX - random.randint(-500, 50)
            tWallX = holeX - random.randint(-500, 50)
            holeX = random.randint(200, 650)
            ObstacleX = [holeX, sWallX, wallX, tWallX]
            generate(0, 0, bg)
            for obstacle in onScreen:
                generate(ObstacleX[obstacle], ObstacleY[obstacle], ObstacleImgs[obstacle])
            show_score(textX, textY)
            show_lives(liveX, liveY)
            generate(playerX, playerY, playerImg)
            pygame.display.update()
            time.sleep(1.5)

        # Collision
        if playerRect.colliderect(holeRect) or playerRect.colliderect(wallRect) or playerRect.colliderect(tWallRect) or playerRect.colliderect(sWallRect):
            jump = False
            v = 16
            m = 0.2
            playerY = 201
            slap = mixer.Sound('slap.wav')
            slap.set_volume(0.5)
            slap.play()
            lives -= 1
            score += 1
            playerX = 50
            sWallX = random.randint(200, 650)
            wallX = random.randint(200, 650)
            tWallX = random.randint(200, 650)
            holeX = random.randint(200, 650)
            ObstacleX = [holeX, sWallX, wallX, tWallX]
            generate(0, 0, bg)
            for obstacle in onScreen:
                generate(ObstacleX[obstacle], ObstacleY[obstacle], ObstacleImgs[obstacle])
            show_lives(liveX, liveY)
            show_score(textX, textY)
            generate(playerX, playerY, playerImg)
            pygame.display.update()
            if lives > 0:
                time.sleep(1.5)

        # Game Over
        if lives == 0:
            music.set_volume(0)
            over(text2X, text2Y)
            var = False
            hit = True
            running = False
            break

        show_score(textX, textY)
        show_lives(liveX, liveY)
        pygame.time.delay(20)
        pygame.display.update()
    if hit == True:
        over(text2X, text2Y)
        show_score(textX, textY)
        show_lives(liveX, liveY)
    pygame.display.update()
