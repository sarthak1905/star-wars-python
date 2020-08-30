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

#Colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)


class Enemy:

    def __init__(self):
        self.max_health = 3
        self.health = self.max_health
        self.show = False
        self.x = random.randint(50,MAXX-50)
        self.y = 25
        self.speedx = 5
        self.speedy = 1
    
    def SetImage(self,image):
        self.image = pygame.image.load(image)

    def DisplayEnemy(self,win):
        win.blit(self.image,(self.x,self.y))

    def MoveEnemy(self):
        self.x += self.speedx
        self.y += self.speedy 

    def CheckBoundaries(self):
        if self.x >= MAXX-64:
            self.x = MAXX-64
            self.speedx = -self.speedx
        elif self.x <= MINX:
            self.x = MINX
            self.speedx = -self.speedx

    def CheckCollision(self,X,Y):
        distance = math.sqrt((self.x-X)**2 + (self.y-Y)**2)
        if distance < 50:
            self.health -= 1
            return True
        else:
            return False
    def EnemyToEnemyCollison(self,enemy2):
        self.speedx = -self.speedx
        enemy2.speedx = -enemy2.speedx
    
    def CheckDeath(self):
        if self.health == 0:
            self.show = False
            self.x = random.randint(50,MAXX-50)
            self.y = 25
            self.health = self.max_health
            return True
        return False
    
    def LevelChange(self):
        self.health = 0 
        status = self.CheckDeath()

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

def Player_Display(screen,playerimg,x,y):
    screen.blit(playerimg,(x,y))

def Run_Game():

    #Initializing window, images 
    screen = Game_Display()
    playerimg = Player_Init()
    enemies =[]
    for i in range(5):
        enemies.append(Enemy())
        enemies[i].SetImage('images/alien' + str(i+1) +'.png')
    bgimg = pygame.image.load('images/background.png')
    bulletimg = pygame.image.load('images/ammo.png')

    #Live score display and Level display
    font = pygame.font.Font('freesansbold.ttf', 25)
    score_template = ' Score: '
    level_display = ' Level: '
    text_level = font.render(level_display, True, black, white)
    text = font.render(score_template, True, black, white)
    text_levelRect = text_level.get_rect()
    textRect = text.get_rect()
    level_rectx = MAXX/2
    level_recty = 15
    score_rectx = 40
    score_recty = 15
    text_levelRect.center = (level_rectx,level_recty)
    textRect.center = (score_rectx,score_recty)   

    #Initializing variables for player movement 
    playerX = MAXX/2 - 50
    playerY = MAXY-100
    changeX = 0
    normal_speed = 10

    death_delay=1

    #Initializing bullet movement variables
    bulletX = playerX
    bulletY = playerY-12
    bullet_speed = 15
    bullet_state = True
    bullet_show = False

    level = 1
    score = 0 

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
        
        display_enemies = score//100
        if display_enemies <= 4:
            for i in range(display_enemies+1):
                enemies[i].show = True
        else:
            for i in range(5):
                enemies[i].show = True

        #Change of location of player and enemy 
        playerX+=changeX

        for x in enemies:

            if x.show == True:
        
                x.MoveEnemy()

                #Checking if bullet has collided with enemy 
                collision = x.CheckCollision(bulletX,bulletY)
                if collision:
                    bulletY = playerY+32
                    bullet_show = False
                    bullet_state = True
                    score += 10
                    if x.CheckDeath():
                        score += 10
                
                x.CheckBoundaries()

                for y in enemies:

                    if y.show == True and y!=x:
                        inter_coll = x.CheckCollision(y.x,y.y)
                        if inter_coll:
                            x.EnemyToEnemyCollison(y)

        level_prev = level        
        level = score//100 + 1
        
        if level > level_prev:
            for x in enemies:
                if x.show == True:
                    x.LevelChange()

        #Checking if player hit end of game window
        if playerX>=MAXX-64:
            playerX = MAXX-64
        elif playerX<=MINX:
            playerX = MINX

        #If space bar was pressed, display the bullet 
        if bullet_show:
            Bullet_Display(screen,bulletimg,bulletX,bulletY)
            bulletY-=bullet_speed

        #Display Live Score
        text = font.render(score_template + str(score) + ' ', True, black, white)
        screen.blit(text,textRect)

        #Level Display
        text_level = font.render(level_display + str(level) + ' ', True, black, white)
        screen.blit(text_level,text_levelRect)

        #If bullet exits the screen
        if bulletY<=MINY and bullet_show:
            bulletY = playerY+32
            bullet_show = False
            bullet_state = True

        #If bullet hits the enemy 
        for x in enemies:
            if x.show == True:
                #Enemy Display 
                x.DisplayEnemy(screen)

        Player_Display(screen,playerimg,playerX,playerY)
        pygame.display.update()   

def main():
    Run_Game()

if __name__=="__main__":
    main()