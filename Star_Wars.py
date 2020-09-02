import pygame
import random
import math
import time
import sys

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
        self.lives = 3

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

    def CheckEnd(self):
        if self.y >= MAXY - 200:
            return True
        return False

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

    #Live score display, Level display and Lives Display
    font = pygame.font.Font('freesansbold.ttf', 25)
    score_template = ' Score: '
    level_display = ' Level: '
    lives_display = ' Lives: '
    text_level = font.render(level_display, True, black, white)
    text = font.render(score_template, True, black, white)
    text_lives = font.render(lives_display, True, black, white)
    text_levelRect = text_level.get_rect()
    textRect = text.get_rect()
    text_livesRect = text_lives.get_rect()
    level_rectx = MAXX/2
    level_recty = 15
    score_rectx = 40
    score_recty = 15
    lives_rectx = MAXX - 65
    lives_recty = 15
    text_levelRect.center = (level_rectx,level_recty)
    textRect.center = (score_rectx,score_recty)
    text_livesRect.center = (lives_rectx,lives_recty)   

    #Level Change Display
    font_l = pygame.font.Font('freesansbold.ttf', 40)
    message_l = ' LEVEL '
    text_l = font_l.render(message_l, True, red, black)
    text_lRect = text_l.get_rect()
    message_lx = MAXX/2
    message_ly = MAXY/2
    text_lRect.center = (message_lx,message_ly)

    #Game over display 
    font_c = pygame.font.Font('freesansbold.ttf', 40)
    message_c = ' Game Over! Your score was: '
    text_c = font_c.render(message_c, True, white, black)
    textRect_c = text_c.get_rect()
    messagex = MAXX/2
    messagey = MAXY/4
    textRect_c.center = (messagex, messagey)
    replay_quit_img = pygame.image.load('images/game_close.png')

    death_delay=1

    level = 1
    score = 0  

    running = True
    game_over = False
    play_again = False
    break_out = False
    level_change = False
    level_delay = 0

    while running:
        screen.fill((0,0,0))

        #Loading background
        screen.blit(bgimg,(0,0))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False

            if not game_over:
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
            
            else:
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse[0] in range(208,350) and mouse[1] in range(475,540):
                        break_out = True
                        play_again = True 
                        break
                    elif mouse[0] in range(454,605) and mouse[1] in range(475,540):
                        break_out = True
                        play_again = False
                        break

        if break_out:
            break
        
        if not game_over:

            if not level_change:

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
                        
                        if x.CheckEnd():
                            x.health = 0 
                            status = x.CheckDeath()
                            player.lives -= 1
                            if player.lives == 0:
                                game_over = True

                #Update Player coordinates
                player.UpdatePlayerX()

                #Update Level Change
                level_prev = level        
                level = score//100 + 1
                
                if level > level_prev:
                    for x in enemies:
                        if x.show == True:
                            x.LevelChange()
                    level_change = True
                    level_delay = 0

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

                #Lives Display
                text_lives = font.render(lives_display + str(player.lives) + ' ', True, black, white)
                screen.blit(text_lives,text_livesRect)

                #If bullet exits the screen
                player.CheckBulletBoundaries()

                for x in enemies:
                    if x.show == True:
                        #Enemy Display 
                        x.DisplayEnemy(screen)
                
                player.PlayerDisplay(screen)
            
            else:
                if level_delay < 50:
                    text_l = font.render(message_l + str(level) + ' ', True, red, black)
                    screen.blit(text_l,text_lRect)
                else:
                    level_change = False
                    level_delay = -1
                level_delay += 1

        else:
            screen.blit(bgimg,(0,0))
            text_c = font_c.render(message_c + str(score) + ' ', True, white, black)

            #Display final score
            screen.blit(text_c,textRect_c)

            #Display Play or Quit 
            screen.blit(replay_quit_img, (MAXX/5,2*MAXY/3))

            #Mouse coordinates
            mouse = pygame.mouse.get_pos()

        pygame.display.update()   
    
    if play_again:
        Run_Game()
    pygame.quit()
    sys.exit(0)

def main():
    Run_Game()

if __name__=="__main__":
    main()