import pygame
import sys
import time 
import random
from pygame.locals import *

# 初始化显示窗口以及颜色元素等
pygame.init()
fpsClock = pygame.time.Clock()

#定义显示层
playSurface = pygame.display.set_mode((640,480))
pygame.display.set_caption('Snack Go!')
image = pygame.image.load('game.ico')
pygame.display.set_icon(image)
#定义基本颜色
redColor = pygame.Color(255,0,0)
blockColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
greyColor = pygame.Color(150,150,150)
lightGrey =pygame.Color(220,220,220)

def gameOver(playSurface, score):
    #显示Game Over
    gameOverFront = pygame.font.Font('Arial.ttf', 72)
    gameOverSurf = gameOverFront.render('Game Over', True, greyColor)
    gameOverRect = gameOverSurf.get_rect()
    playSurface.blit(gameOverSurf, gameOverRect)

    #定义分数
    scoreFont = pygame.font.Font('Arial.ttf', 48)
    scoreSurf = scoreFont.render('Score: ' + str(score), True, greyColor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (320, 225)
    playSurface.blit(scoreSurf, scoreRect)
    pygame.display.flip()

    #5s后退出
    time.sleep(3)
    pygame.quit()
    sys.exit()

def gameStart():

    #初始位置
    snakePosition = [100, 100]
    snakeSegments = [[100,100], [80, 100], [60, 100]]
    raspberryPosition = [300, 300]
    raspberrySpawned = 1
    direction = 'right'
    changeDirection = direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == ord('d'):
                    changeDirection = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    changeDirection = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    changeDirection = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
            
            #判断是否输入了反方向
            if changeDirection == 'right' and not direction == 'left':
                direction = changeDirection
            if changeDirection == 'left' and not direction == 'right':
                direction = changeDirection
            if changeDirection == 'up' and not direction == 'down':
                direction = changeDirection
            if changeDirection == 'down' and not direction == 'up':
                direction = changeDirection
            
        #根据方向移动蛇头
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20
        snakeSegments.insert(0, list(snakePosition))

        #判断是否吃到树莓
        if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
            raspberrySpawned = 0
        else:
            snakeSegments.pop()

        #重新生成树莓
        if raspberrySpawned == 0:
            x = random.randrange(1, 32)
            y = random.randrange(1, 24)
            raspberryPosition = [int(x*20), int(y*20)]
            raspberrySpawned = 1
            score += 1
            
        #重新绘制图画
        playSurface.fill(blockColor)
        for position in snakeSegments[1:]:
            pygame.draw.rect(playSurface, whiteColor, Rect(position[0], position[1], 20, 20))
        pygame.draw.rect(playSurface, lightGrey, Rect(snakePosition[0], snakePosition[1], 20, 20))
        pygame.draw.rect(playSurface, redColor, Rect(raspberryPosition[0], raspberryPosition[1], 20, 20))
        pygame.display.flip()

        #判断死亡
        if snakePosition[0] > 620 or snakePosition[0] < 0: #左右边界
            gameOver(playSurface, score)
        if snakePosition[1] > 460 or snakePosition[1] < 0: #上下边界
            gameOver(playSurface, score)
        for snackBody in snakeSegments[1:]: #自环
            if snakePosition[0] == snackBody[0] and snakePosition[1] == snackBody[1]:
                gameOver(playSurface, score)

        #根据长度增加速度
        if len(snakeSegments) < 20:
            speed = 6 + len(snakeSegments)//4
        else:
            speed = 10 + len(snakeSegments)//3
        fpsClock.tick(speed)

gameStart()