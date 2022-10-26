import random
import math

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1000, 800))

# Background
backgroundImg = pygame.image.load("background.png")

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 450
playerY = 700
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

for e in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(50)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 700
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('santana.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (450, 450))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, e):
    screen.blit(enemyImg[e], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((150, 21, 200))
    # Background Image
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed, check whether it's right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -4
        if event.key == pygame.K_RIGHT:
            playerX_change = 4
        if event.key == pygame.K_LCTRL:
            if bullet_state == "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                # Get the current x coordinate of the spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 935:
        playerX = 935

    # Enemy Movement
    for e in range(num_of_enemies):

        # Game Over
        if enemyY[e] == 200:
            for j in range(num_of_enemies):
                enemyY[e] = 2000
                game_over_text()
                break
        enemyX[e] += enemyX_change[e]
        if enemyX[e] <= 0:
            enemyX_change[e] = 2
            enemyY[e] += enemyY_change[e]
        elif enemyX[e] >= 945:
            enemyX_change[e] = -2
            enemyY[e] += enemyY_change[e]

        # Collision
        collision = isCollision(enemyX[e], enemyY[e], bulletX, bulletY)
        if collision:
            bullet_Sound = mixer.Sound('explosion.wav')
            bullet_Sound.play()
            bulletY = 700
            bullet_state = "ready"
            score_value += 1
            enemyX[e] = random.randint(0, 735)
            enemyY[e] = random.randint(50, 150)

        enemy(enemyX[e], enemyY[e], e)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 700
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textY, textY)
    pygame.display.update()
