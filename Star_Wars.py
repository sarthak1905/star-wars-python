import pygame
import random
import math
import time

pygame.init()

#Defining window borders 
MAXX = 800
MAXY = 600
MINX = 0
MINY = 0

def Player_Init():
    playerimg = pygame.image.load('images/player.png')
    return playerimg

def Game_Display():
    screen = pygame.display.set_mode((MAXX,MAXY))
    pygame.display.set_caption("Star Wars 1.0")
    icon = pygame.image.load('images/gameicon.png')
    pygame.display.set_icon(icon)
    return screen

def Bullet_Display(screen,bulletimg,x,y):
    screen.blit(bulletimg,(x,y))

def Enemy_Display(screen,enemyimg,x,y):
    screen.blit(enemyimg,(x,y))

def Player_Display(screen,playerimg,x,y):
    screen.blit(playerimg,(x,y))

def If_Collison(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
    if distance < 50:
        return True
    else:
        return False

def Run_Game():

    #Initializing window, images 
    screen = Game_Display()
    playerimg = Player_Init()
    enemyimg1 = pygame.image.load('images/alien1.png')
    enemyimg2 = pygame.image.load('images/alien2.png')
    enemyimg3 = pygame.image.load('images/alien3.png')
    enemyimg4 = pygame.image.load('images/alien4.png')
    enemyimg5 = pygame.image.load('images/alien5.png')
    bgimg = pygame.image.load('images/background.png')
    bulletimg = pygame.image.load('images/ammo.png')

    #Initializing variables for player movement 
    playerX = MAXX/2 - 50
    playerY = MAXY-100
    changeX = 0
    normal_speed = 10

    #Initializing enemy movement variables
    enemy_speedH = 5
    enemy_speedV = 1
    enemyX = random.randint(50,MAXX-50)
    enemyX_change = enemy_speedH
    enemyY_change = enemy_speedV
    enemyY = 50
    enemy_health = 3
    dead = False
    death_delay=1

    #Initializing bullet movement variables
    bulletX = playerX
    bulletY = playerY-12
    bullet_speed = 15
    bullet_state = True
    bullet_show = False

    running = True
    while running:
        screen.fill((0,0,0))

        #Loading background
        screen.blit(bgimg,(0,0))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False

            #If key is pressed
            if event.type==pygame.KEYDOWN:

                #Player movement with arrow keys
                if event.key==pygame.K_LEFT:
                    changeX = -normal_speed
                if event.key==pygame.K_RIGHT:
                    changeX = normal_speed

                #If space bar pressed for shooting bullet
                if event.key==pygame.K_SPACE and bullet_state:
                    bulletX = playerX + 17
                    bullletY = playerY + 32
                    bullet_show = True
                    bullet_state = False
            
            #If key is released, for player movement 
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    changeX = 0
        
        #Change of location of player and enemy 
        playerX+=changeX
        enemyX += enemyX_change
        enemyY += enemyY_change

        #If bullet hits the enemy 
        if dead:
            if death_delay>100:
                dead=False
                death_delay=1
                Enemy_Display(screen,enemyimg1,enemyX,enemyY)

            #Delaying respawn of enemy     
            death_delay+=1
        else:
            #Enemy Display 
            Enemy_Display(screen,enemyimg1,enemyX,enemyY)
        
        #Checking if player hit end of game window
        if playerX>=MAXX-64:
            playerX = MAXX-64
        elif playerX<=MINX:
            playerX = MINX
        
        #Checking if enemy hit end of game window
        if enemyX>=MAXX-64:
            enemyX = MAXX-64
            enemyX_change=-enemy_speedH
        elif enemyX<=MINX:
            enemyX = MINX
            enemyX_change = enemy_speedH

        #If space bar was pressed, display the bullet 
        if bullet_show:
            Bullet_Display(screen,bulletimg,bulletX,bulletY)
            bulletY-=bullet_speed

        #If bullet exits the screen
        if bulletY<=MINY and bullet_show:
            bulletY = playerY+32
            bullet_show = False
            bullet_state = True
        
        #Checking if bullet has collided with enemy 
        collision = If_Collison(enemyX,enemyY,bulletX,bulletY)
        if collision:
            enemy_health -= 1
            bulletY = playerY+32
            bullet_show = False
            bullet_state = True
            if enemy_health==0:
                dead=True
                enemyX = random.randint(50,MAXX-50)
                enemyY=50
                enemy_health=3
        Player_Display(screen,playerimg,playerX,playerY)
        pygame.display.update()   

def main():
    Run_Game()

if __name__=="__main__":
    main()