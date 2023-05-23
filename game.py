# import modules
import pygame
import sys
import math
import mysql.connector as sq
from pygame import mixer

# intialise pygame
pygame.init()

# screen dimensions
res = (600, 200)

# create screen
screen = pygame.display.set_mode(res)

# title, icon, background
pygame.display.set_caption('Car Crash')

icon = pygame.image.load('F:\\Vinaya\\Python Projects\\Car Crash\\Media\\icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('F:\\Vinaya\\Python Projects\\Car Crash\\Media\\background.png')

# mysql
con = sq.connect(host = 'localhost', user = 'root', passwd = 'Vinaya@2003', database = 'CarCrash')
cursor = con.cursor()

# background music
mixer.music.load('F:\\Vinaya\\Python Projects\\Car Crash\\Media\\background.mp3')
mixer.music.play(-1)

JumpSound = mixer.Sound('F:\Vinaya\Python Projects\Car Crash\Media\jump.wav')
LevelUpSound = mixer.Sound('F:\Vinaya\Python Projects\Car Crash\Media\LevelUp.wav')
GameOverSound = mixer.Sound('F:\Vinaya\Python Projects\Car Crash\Media\GameOver.wav')

# player
PlayerImg = pygame.image.load('F:\\Vinaya\\Python Projects\\Car Crash\\Media\\player.png')

''' player movement coordinates '''
PlayerX = 60
PlayerY = 138
PlayerChangeX = 0
PlayerChangeY = 30

''' checks whether car is up or down
    when spacebar is pressed & when required to bring car down '''
PlayerState = 'down'  

def player(x,y):
    screen.blit(PlayerImg, (x,y))

''' records the X coordinate of obstacle
    when spacebar is pressed
    used to determine the distance after which the car should be brought down'''
UpDist = -1000

# obstacle
ObstacleImg = pygame.image.load('F:\\Vinaya\\Python Projects\\Car Crash\\Media\\obstacle.png')

''' obstacle movement coordinates '''
ObstacleX = 576
ObstacleY = 155
ObstacleChangeX = 0.1
ObstacleChangeY = 0

def obstacle(x,y):
    screen.blit(ObstacleImg, (x,y))

# collision
''' uses 2D geometry dist betw 2 points eqn d = ((x2-x1)^2 + (y2-y1)^2)^(1/2)
    to check whether dist betn car and obstacle is less than 47 pixels

    47 is an arbitrary value chosen after some observations '''

def collision():
    if math.hypot(PlayerX - ObstacleX, PlayerY - ObstacleY) < 47:
        return True
    else:
        return False

# score

''' keeps track of score '''
ScoreVal = 0

Font = pygame.font.Font('freesansbold.ttf', 24)

def DisplayScore():
    score = Font.render('Score : '+str(ScoreVal), True, (0, 0, 0))
    screen.blit(score, (10,0))

# level

''' keeps track of level '''
LevelVal = 1

''' equal to ScoreVal *most of the time*
    keeps track of when to increase the level according to the score '''
LevelScore = 0

def DisplayLevel():
    score = Font.render('Level : '+str(LevelVal), True, (0, 0, 0))
    screen.blit(score, (490,0))

# highscore
qry = 'SELECT highscore FROM scoreboard'
cursor.execute(qry)
''' keeps track of highscore '''
HighScoreVal = cursor.fetchone()[0]

def DisplayHighScore():
    highscore = Font.render('High Score : '+str(HighScoreVal), True, (0, 0, 0))
    screen.blit(highscore, (215,0))

# end game
EndFont = pygame.font.Font('freesansbold.ttf', 50)
end = EndFont.render('Game Over', True, (225, 0, 0))

def GameOver():
    screen.blit(end, (150,75))

#main loop
running = True

while running:

    # event check
    for event in pygame.event.get():

        # exit loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # player movement
        ''' when spacebar pressed, car is down,
            car moves up'''
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if PlayerState == 'down':
                    UpDist = ObstacleX
                    PlayerY -= PlayerChangeY 
                    PlayerState = 'up'
                    JumpSound.play()
            
    # background color
    screen.fill((225, 225, 225))

    # background image
    screen.blit(background, (0,0))

    # player movement
    ''' return down after jump
        when the obstacle has passed a certain distance '''
    
    if PlayerState == 'up':
        if UpDist - ObstacleX >= 150:
            PlayerY += PlayerChangeY
            PlayerState = 'down'
            UpDist = -1000

        elif UpDist == -1000:
            PlayerY += PlayerChangeY
            PlayerState = 'down'
        

    # obstacle movement
    ''' move obstacle towards left '''
    
    ObstacleX -= ObstacleChangeX

    ''' when hits 0,
        disappear &
        increase score by 1 '''
    
    if ObstacleX <= -25:
        UpDist = 600
        ObstacleX = 600
        ScoreVal += 1
        LevelScore = ScoreVal

    # cloud movement
    ''' illusion of car movement'''

    # game over
    ''' when collision func returns True,
        displays game over text
        game ends '''
    
    ###############################################
    ''' ERROR : LOOP BREAKS DOWN, UNABLE TO EXIT '''
    ###############################################
    
    collide = collision()
    
    if collide:
        GameOver()
        mixer.music.fadeout(2000)
        GameOverSound.play()
        running = False

    # level up
    ''' every time score increases by 5,
        level increases by 1 &
        obstacle speed increases by 0.3

        LevelScore changed so that
        levels do not keep increasing rapidly
        as until ScoreVal increases by 1
        it will remain divisible by 5'''
    
    if LevelScore%5 == 0 and LevelScore != 0:
        LevelScore = 0
        ObstacleChangeX += 0.03
        LevelVal += 1
        LevelUpSound.play()

    # highscore up
    ''' if current score greater than highscore
        increase and display new highscore simultaneously '''
    
    if ScoreVal>HighScoreVal:
        qry = f'UPDATE scoreboard SET highscore = {ScoreVal} WHERE highscore = {HighScoreVal}'
        cursor.execute(qry)
        con.commit()
        HighScoreVal = ScoreVal
        DisplayHighScore()
        
    # motion
    ''' call functions to display player and obstacle '''
    
    player(PlayerX, PlayerY)
    obstacle(ObstacleX, ObstacleY)

    # display score, level, highscore
    ''' call functions to display score, level, highscore '''
    
    DisplayScore()
    DisplayLevel()
    DisplayHighScore()

    # update screen
    pygame.display.update()

# loop to quit after game over
while not running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

# future scope
''' ERROR AFTER COLLISION : LOOP BREAKS DOWN, CANNOT EXIT GAME '''

''' add multiple obstacles
    implications : make sure obstacles do not overlap
                   arrive too close together such that impossible to jump '''

''' 2 or more obstacles together
    implications : increase jump distance for all/ select obstacles '''

''' enter name for highscore '''

# attribution
'''
backgound music
Sci-Fi Dramatic Theme by Twisterium | https://www.twisterium.com/
Music promoted by https://www.chosic.com/
Licensed under Creative Commons: Attribution 3.0 Unported (CC BY 3.0)
https://creativecommons.org/licenses/by/3.0/
'''

'''
sound effects
Mixkit Sound Effects Free License
'''
 
'''
icon image
<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
'''
 
'''
player image
<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
'''

'''
obstacle image
<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
'''

'''
background image
<a href="https://www.freepik.com/free-photos-vectors/abstract">Abstract vector created by upklyak - www.freepik.com</a>
'''

