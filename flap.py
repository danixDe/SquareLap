import pygame
from sys import exit
import random

pygame.init()
window = pygame.display.set_mode((480,640))
clock = pygame.time.Clock()
pygame.display.set_caption('squarelap')

square = pygame.Rect(120,300,20,20)

gravity =0
game_active=True
start_time = 0


def randopipe():
    fixedgap= random.randint(80,200)
    x=720
    w=random.randint(10,50)
    h1=random.randint(90,400)
    
    pipetop = pygame.Rect(x,0,w,h1)
    pipebot = pygame.Rect(x,h1+fixedgap,w,640-h1-fixedgap)
    
    return pipetop,pipebot

pixyfont = pygame.font.Font('font/pixeltype.ttf',50)
score=0

pipes = [randopipe()]




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active and event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active=True
            square.y = 300
            pipes = [randopipe()]
            score = 0
            gravity=0
            start_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]and game_active:
        gravity = -9
    
    window.fill('black')
    if game_active:

        gravity+=0.5
        square.y+=gravity

        newpipes = []
        for pipetop,pipebot in pipes:
            pipetop.x-=5
            pipebot.x-=5

            if pipetop.right>0:
                newpipes.append((pipetop,pipebot))
            if pipetop.right < 480 and len(newpipes) == len(pipes):
                newpipes.append(randopipe())
        
        pipes = newpipes
        
        
        if pipes and square.left > pipes[0][0].right:
            score+=1
            pipes.pop(0)
        scoresurf = pixyfont.render(str(score), False, '#FF0800')
        scorect = scoresurf.get_rect(center = (240,30))
            
        
        
        if square.y>620:
            square.y=620
            game_active=False

        pygame.draw.rect(window, 'white', square)
        for pipetop,pipebot in pipes:
            pygame.draw.rect(window, 'white', pipetop)
            pygame.draw.rect(window, 'white', pipebot)
        pygame.draw.rect(window, 'black', scorect)
        window.blit(scoresurf,scorect)
        for pipetop, pipebot in pipes:
            if square.colliderect(pipetop) or square.colliderect(pipebot):
                game_active = False
        
    else:
        window.fill('white')    
        gameover = pixyfont.render('GAME OVER!', False,'#660066')
        gameoverect = gameover.get_rect(center = (240,320))

        window.blit(gameover,gameoverect)
    pygame.display.update()
    clock.tick(60)
