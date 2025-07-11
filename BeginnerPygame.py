import pygame
import random
import math
from pygame import mixer # to to add background music

# if you want an image, you can go ton flaticon.com and you should go for 64 bites
# initialize the pygame , also if you wanna make it fance press , ctrl + alt + l
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
Background = pygame.image.load("Assets/space.png")

# title and icon
pygame.display.set_caption("Awesome")
icon = pygame.image.load('Assets/spaceship_red.png')
pygame.display.set_icon(icon)

# player, scale and rotate
Player = pygame.image.load('Assets/spaceship_yellow.png')
playerIMG = pygame.transform.rotate(pygame.transform.scale(Player, (55, 40)), 180)
playerX = 370
playerY = 480  # if you input some number that is lower like "30" it will appear on the top (idk why)
playerX_change = 0

# enemy, also append is used to add a value to a list/array
Enemy = []
EnemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 7

# background sound
mixer.music.load("Assets/Kevin MacLeod Investigations.mp3")
mixer.music.play(-1)  # play on loop, idk why.
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) # if you want more font, go to www.dafont.com
textX = 10
textY = 550

for i in range(num_of_enemy):
   Enemy = pygame.image.load('Assets/spaceship_red.png')
   EnemyIMG.append(pygame.transform.rotate(pygame.transform.scale(Enemy, (55, 40)), 0))
   enemyX.append(random.randint(20, 730))
   enemyY.append(random.randint(50, 150))
   enemyX_change.append(0.1)
   enemyY_change.append(15)

# bullet
# Ready - You can't see the bullet on the screen
# fire - THe bullet is currently moving
bullet = pygame.image.load("Assets/bullet.png.png")
bulletIMG = pygame.transform.rotate(pygame.transform.scale(bullet, (34, 20)), 0)
bulletX = 0
bulletY = 480
bulletY_change = 0.3
bullet_state = "ready"

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200,250))


def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))  # that str i called type casting
    screen.blit(score, (x,y))

# keyboard input & key pressed events
def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyIMG[i], (x, y))


def fire_bullets(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY,2))  # the equation is D(distance) = √(x2-x1)^2 + (y2-y1)^2
    if distance < 27:  # pixels
        return True  # if the distance < 27. we're gonna call is_collision
    else:
        return False

# we have to open the file
run = True
while run:
    # make sure that color can go into the infinite while loop
    screen.fill((255, 255, 255))  # (RGB) red, green, blue the max is 255
    screen.blit(Background, (0, 0))
    # you could go to google to see RGB colors
    for event in pygame.event.get():  # getting all the events
        if event.type == pygame.QUIT:  # check if event is quit or not
            run = False
        if event.type == pygame.KEYDOWN:  # checked if any key on the keyboard is pressed
            if event.key == pygame.K_a:  # this is for movement. "a" is left
                playerX_change -= 0.3
            if event.key == pygame.K_d:
                playerX_change += 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound("Assets/Gun+Silencer.mp3")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullets(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # you need to put it in this player while loop so it can every frame it won't disappear
    # playerY -= 0.1  # if it decrease the value, it will go up
    playerX += playerX_change
    if playerX <= 20:
        playerX = 20  # if you do something like 10 (not changing the top) iut will go back to the beginning
    if playerX >= 730:  # this is actually making a new one, not prevents the boundaries
        playerX = 730  # if we choose 800, it will a part of spaceship out of the boundaries

    for i in range(num_of_enemy):
        # game over
        if enemyY[i] > 300:
            for j in range(num_of_enemy):
                enemyY[j] = 2000  # below the screen
            game_over_text()
            break  # break out of the loop

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 20:
            enemyX_change[i] += 0.1  # example 5 = 5+0.2 = 5.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] -= 0.1  # this is going down, if "-=" then it's going up
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # True or False
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(20, 730)
            enemyY[i] = random.randint(50, 150)
            collision_sound = mixer.Sound("Assets/Grenade+1.mp3")
            collision_sound.play()
        enemy(enemyX[i], enemyY[i], i)

    # bullet redo
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet movement
    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullets(bulletX, bulletY)

    show_score(textX, textY)
    player(playerX, playerY)  # you have to put it after screen fill so it can go in, cuz it's first
    # also we need display update so if we add something, it can get updated in while loop
    pygame.display.update()

# we have to close the file (event)
# you press something keys, moving your mouse that is an event
# close button is a quit event in python

'''if __name__ == "__main__":
    main()'''
# you could use that but you have to use a function to call it, you have to make a main() function
# on top of the while loop
