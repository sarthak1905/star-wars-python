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

class Player:

    def __init__(self):
        self.x = MAXX/2 - 50
        self.y = MAXY - 100
        self.speed = 10
        self.changeX = 0 
        self.bulletX = self.x
        self.bulletY = self.y-12
        self.bullet_speed = 15
        self.bullet_state = True
        self.bullet_show = False
    
    def SetImage(self):
        self.playerimg = pygame.image.load('images/player.png')
        self.bulletimg = pygame.image.load('images/ammo.png')
    
    def BulletDisplay(self,win):
        win.blit(self.bulletimg,(self.bulletX,self.bulletY))
    
    def PlayerDisplay(self,win):
        win.blit(self.playerimg,(self.x,self.y))
    
    def CheckBoundaries(self):
        if self.x >= MAXX-64:
            self.x = MAXX-64
        elif self.x <= MINX:
            self.x = MINX
    
    def CheckBulletBoundaries(self):
        if self.bulletY <= MINY and self.bullet_show:
            self.bulletY = self.y + 32
            self.bullet_show = False
            self.bullet_state = True
    
    def UpdatePlayerX(self):
        self.x += self.changeX
    
    def ShootBullet(self):
        self.bulletX = self.x + 17
        self.bulletY = self.y + 32
        self.bullet_show = True
        self.bullet_state = False     

    def BulletCollision(self):
        self.bulletY = self.y + 32
        self.bullet_show = False
        self.bullet_state = True

    def MoveBullet(self):
        self.bulletY -= self.bullet_speed   

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

def Game_Display():
    screen = pygame.display.set_mode((MAXX,MAXY))
    pygame.display.set_caption("Star Wars 1.0")
    icon = pygame.image.load('images/gameicon.png')
    pygame.display.set_icon(icon)
    return screen

def Run_Game():

    #Initializing window, images 
    screen = Game_Display()
    player = Player()
    enemies =[]
    for i in range(5):
        enemies.append(Enemy())
        enemies[i].SetImage('images/alien' + str(i+1) +'.png')

    bgimg = pygame.image.load('images/background.png')

    player.SetImage()

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

    death_delay=1

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
                    player.changeX = -player.speed
                if event.key==pygame.K_RIGHT:
                    player.changeX = player.speed

                #If space bar pressed for shooting bullet
                if event.key==pygame.K_SPACE and player.bullet_state:
                    player.ShootBullet()
            
            #If key is released, for player movement 
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    player.changeX = 0
        
        display_enemies = score//100
        if display_enemies <= 4:
            for i in range(display_enemies+1):
                enemies[i].show = True
        else:
            for i in range(5):
                enemies[i].show = True

        for x in enemies:

            if x.show == True:
        
                x.MoveEnemy()

                #Checking if bullet has collided with enemy 
                collision = x.CheckCollision(player.bulletX,player.bulletY)
                if collision:
                    player.BulletCollision()
                    score += 10
                    if x.CheckDeath():
                        score += 10
                
                x.CheckBoundaries()

                for y in enemies:

                    if y.show == True and y!=x:
                        inter_coll = x.CheckCollision(y.x,y.y)
                        if inter_coll:
                            x.EnemyToEnemyCollison(y)

        #Update Player coordinates
        player.UpdatePlayerX()

        level_prev = level        
        level = score//100 + 1
        
        if level > level_prev:
            for x in enemies:
                if x.show == True:
                    x.LevelChange()

        #Checking if player hit end of game window
        player.CheckBoundaries()

        #If space bar was pressed, display the bullet 
        if player.bullet_show:
            player.BulletDisplay(screen)
            player.MoveBullet()

        #Display Live Score
        text = font.render(score_template + str(score) + ' ', True, black, white)
        screen.blit(text,textRect)

        #Level Display
        text_level = font.render(level_display + str(level) + ' ', True, black, white)
        screen.blit(text_level,text_levelRect)

        #If bullet exits the screen
        player.CheckBulletBoundaries()

        #If bullet hits the enemy 
        for x in enemies:
            if x.show == True:
                #Enemy Display 
                x.DisplayEnemy(screen)

        player.PlayerDisplay(screen)
        pygame.display.update()   

def main():
    Run_Game()

if __name__=="__main__":
    main()