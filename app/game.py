import os
from utils import *
import pygame, sys, random # lib
clock = pygame.time.Clock() 
from pygame.locals import * 
from pygame import mixer
pygame.init() 

mixer.init()
pygame.display.set_caption('A vingança de Zeca Urubu') #o nome da janela

WINDOW_SIZE = (1000,600) #variavel pra guardar o tamanho da minha janela
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) #janela

player_walkR = [pygame.image.load('assets/zequinha1d.png'), pygame.image.load('assets/zequinha2d.png'), pygame.image.load('assets/zequinha3d.png'), pygame.image.load('assets/zequinha4d.png'), pygame.image.load('assets/zequinha5d.png'), pygame.image.load('assets/zequinha6d.png'), pygame.image.load('assets/zequinha7d.png'), pygame.image.load('assets/zequinha8d.png'), pygame.image.load('assets/zequinha9d.png'), pygame.image.load('assets/zequinha10d.png'), pygame.image.load('assets/zequinha11d.png'), pygame.image.load('assets/zequinha12d.png'), pygame.image.load('assets/zequinha13d.png'), pygame.image.load('assets/zequinha14d.png'), pygame.image.load('assets/zequinha15d.png')] #carrega a imagem do meu personagem
player_walkL = [pygame.image.load('assets/zequinha1e.png'), pygame.image.load('assets/zequinha2e.png'), pygame.image.load('assets/zequinha3e.png'), pygame.image.load('assets/zequinha4e.png'), pygame.image.load('assets/zequinha5e.png'), pygame.image.load('assets/zequinha6e.png'), pygame.image.load('assets/zequinha7e.png'), pygame.image.load('assets/zequinha8e.png'), pygame.image.load('assets/zequinha9e.png'), pygame.image.load('assets/zequinha10e.png'), pygame.image.load('assets/zequinha11e.png'), pygame.image.load('assets/zequinha12e.png'), pygame.image.load('assets/zequinha13e.png'), pygame.image.load('assets/zequinha14e.png'), pygame.image.load('assets/zequinha15e.png')]
player_jump = [pygame.image.load('assets/zequinhajumpd.png'), pygame.image.load('assets/zequinhajumpe.png')]
obstaculo_sprite = pygame.image.load('assets/obstaculo.png')
obstaculo1_sprite = pygame.image.load('assets/obstaculo1.jpg')
bg = pygame.image.load('assets/background.png')
startScreen = pygame.image.load('assets/startScreen.png')
jogar = pygame.image.load('assets/jogar.png')
instrucoes = pygame.image.load('assets/instrucoes.png')
sair = pygame.image.load('assets/sair.png')
gameOverScreen= pygame.image.load('assets/gameover.png')
gameOverPlayAgain= pygame.image.load('assets/gameoverPlayAgain.png')
gameOverSair= pygame.image.load('assets/gameoverSair.png')
last = "right"

pulo = False
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
walkCount = 0
wait = 0

player_location = [-3,536]
player_y_momentum = 1

player_rect = pygame.Rect(player_location[0],player_location[1],player_walkL[0].get_width(),player_walkL[0].get_height())#isso aqui eh pra tratar colisao

#variaveis pra meu obstaculo
array_rect = [0, 590]
minGap=250
maxGap=950
obstaculo_X1=900
obstaculo_Y=510
obstaculo_X2=random.randint(900+minGap, 900+maxGap)
obstaculo_X3=random.randint(obstaculo_X2+minGap, obstaculo_X2+maxGap)
lastObstacle=obstaculo_X3
speed=-0.05
posbgX = 0
#rectX = 900
#rectY = 300

def exit():
    pygame.quit()
    quit()

def game_over():
    fd = os.open(PATH, os.O_RDWR)
    green_leds_on(fd, True) 
    red_leds_on(fd, False)   
    intro = True
    global player_location, obstaculo_X1, obstaculo_Y, obstaculo_X2, obstaculo_X3, lastObstacle, speed, posbgX, array_rect
    global player_rect, player_y_momentum, walkCount, air_timer, vertical_momentum, moving_left
    global moving_right, pulo, player_location, minGap, maxGap
    sprites_screen2 = [1, 0, 0]
    while intro:
        pos3 = pygame.mouse.get_pos()[0]
        pos4 = pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                player_location = [-3, 536] 
                obstaculo_X1=900
                obstaculo_Y=510
                obstaculo_X2=random.randint(900+minGap, 900+maxGap)
                obstaculo_X3=random.randint(obstaculo_X2+minGap, obstaculo_X2+maxGap)
                lastObstacle=obstaculo_X3
                pulo = False
                moving_right = False
                moving_left = False
                vertical_momentum = 0
                air_timer = 0
                walkCount = 0
                minGap=250
                maxGap=950

                player_y_momentum = 1

                player_rect = pygame.Rect(player_location[0],player_location[1],player_walkL[0].get_width(),player_walkL[0].get_height())#isso aqui eh pra tratar colisao

                array_rect = [0, 590]
                speed=-0.05
                posbgX = 0
            if((pos3 >= 305 and pos3 <= 691) and (pos4 >= 367 and pos4 <= 440)):
                sprites_screen2[1] = 1
                sprites_screen2[0] = 0
                sprites_screen2[2] = 0
            elif((pos3 >= 305 and pos3 <= 691) and (pos4 >= 456 and pos4 <= 529)):
                sprites_screen2[1] = 0
                sprites_screen2[0] = 0
                sprites_screen2[2] = 1
            else: 
                sprites_screen2[1] = 0
                sprites_screen2[0] = 1
                sprites_screen2[2] = 0

            if (event.type == pygame.MOUSEBUTTONUP) and (pos3 >= 305 and pos3 <= 691) and (pos4 >= 367 and pos4 <= 440):
                game_loop()
            if (event.type == pygame.MOUSEBUTTONUP) and (pos3 >= 305 and pos3 <= 691) and (pos4 >= 456 and pos4 <= 529):
                exit()

            if sprites_screen2[0]: screen.blit(gameOverScreen, (0,0))
            if sprites_screen2[1]: screen.blit(gameOverPlayAgain, (0,0))
            if sprites_screen2[2]: screen.blit(gameOverSair, (0,0))
        pygame.display.update()


def redrawGameWindow():
    global walkCount
    if walkCount+1 >= 75:
        walkCount = 0
    
    if (moving_left) and (pulo == False):
        screen.blit(player_walkL[walkCount//5], (player_location[0], player_location[1]))
        walkCount += 1
    elif (moving_right) and (pulo == False):
        screen.blit(player_walkR[walkCount//5], (player_location[0], player_location[1]))
        walkCount += 1
    elif pulo:
        if last == "right":
            screen.blit(player_jump[0], (player_location[0], player_location[1]))
        if last == "left":
            screen.blit(player_jump[1], (player_location[0], player_location[1]))
    else:
        if last == "right":
            screen.blit(player_walkR[0], (player_location[0], player_location[1]))
        if last == "left":
            screen.blit(player_walkL[0], (player_location[0], player_location[1]))
    pygame.display.update()

#novo evento pra aumentar a velocidade
increase_speed = pygame.USEREVENT+1
pygame.time.set_timer(increase_speed,1000)

def game_loop(): # famoso loop infinito 
    fd = os.open(PATH, os.O_RDWR)       
    global posbgX, obstaculo_Y, obstaculo_X1, obstaculo_X2,obstaculo_X3, moving_right, moving_left, vertical_momentum, speed, array_rect, obstaculo_sprite, obstaculo1_sprite
    global player_location, player_rect, pulo, walkCount, last, wait, minGap, maxGap, lastObstacle

    green_leds_on(fd, False)
    while 1:
        clock.tick(60) #fpszada
        screen.blit(bg, (posbgX,0))
        screen.blit(bg, (posbgX+1000,0))
        screen.blit(obstaculo_sprite, (obstaculo_X1, obstaculo_Y))
        screen.blit(obstaculo_sprite, (obstaculo_X2, obstaculo_Y))
        screen.blit(obstaculo_sprite, (obstaculo_X3, obstaculo_Y))

        if posbgX > -1000:
            posbgX -= 1
        else:
            posbgX = 0
    
        #printando meu obstaculo
        test_rect2 = pygame.Rect(array_rect[0], array_rect[1], 1000, 10)
        obstaculo1= pygame.Rect(obstaculo_X1, obstaculo_Y, obstaculo_sprite.get_width(), obstaculo_sprite.get_height())
        obstaculo2= pygame.Rect(obstaculo_X2, obstaculo_Y, obstaculo_sprite.get_width(), obstaculo_sprite.get_height())
        obstaculo3= pygame.Rect(obstaculo_X3, obstaculo_Y, obstaculo_sprite.get_width(), obstaculo_sprite.get_height())

        if moving_right == True:
            if player_location[0] < 1000:
                player_location[0] += 4
            else:
                player_location[0] = 1000
        if moving_left == True:
            if player_location[0] > 0:
                player_location[0] -= 4
            else:
                player_location[0] = 0
        player_location[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum > 5:
            vertical_momentum = 4
        
        player_rect.x = player_location[0] # atualizando as "fronteiras" do personagem
        player_rect.y = player_location[1] # atualizando as "fronteiras" do personagem
        
        #atualiza a posição do obstaculo
        obstaculo1
        obstaculo_X1+=speed
        obstaculo_X2+=speed
        obstaculo_X3+=speed
        lastObstacle+=speed

        if (obstaculo_X1<-60):
            obstaculo_X1=random.uniform(lastObstacle+minGap, lastObstacle+maxGap)
            lastObstacle=obstaculo_X1

        if (obstaculo_X2<-60):
            obstaculo_X2=random.uniform(lastObstacle+minGap, lastObstacle+maxGap)
            lastObstacle=obstaculo_X2

        if (obstaculo_X3<-60):
            obstaculo_X3=random.uniform(lastObstacle+minGap, lastObstacle+maxGap)
            lastObstacle=obstaculo_X3

        #colisão com o chão
        if player_rect.colliderect(test_rect2):
            player_location[1] = array_rect[1]-player_walkL[0].get_height()
            pulo = False

        #colisão com o livro    
        if player_rect.colliderect(obstaculo1):
            #player_location[1] = obstaculo_Y-player_walkL[0].get_height()
            pulo = False
            game_over()
        
        if player_rect.colliderect(obstaculo2):
            #player_location[1] = obstaculo_Y-player_walkL[0].get_height()
            pulo = False
            game_over()
        
        if player_rect.colliderect(obstaculo3):
            #player_location[1] = obstaculo_Y-player_walkL[0].get_height()
            pulo = False
            game_over()

        for event in pygame.event.get(): #isso aqui fica esperando os eventos

            button = read_button(fd)    

            #eventozinho pra aumentar a velocidade
            if event.type == increase_speed:
                if event.type == increase_speed:
                    speed -= 0.1
                    minGap += 6
                    maxGap += 6
                    

            if event.type == QUIT: #se a pessoa saiu
                pygame.quit() 
                sys.exit()
            
            #qnd clica nas setinhas
            if BUTTONS_OPTIONS[button] != "OFF": 
                if (BUTTONS_OPTIONS[button] == "RIGHT"):
                    moving_right = True
                    last = "right"
                elif (BUTTONS_OPTIONS[button] == "LEFT"):
                    moving_left = True
                    last = "left"
                elif (BUTTONS_OPTIONS[button] == "UP") and (pulo == False):
                    pulo = True
                    if air_timer < 6:
                        vertical_momentum = -8
                else:
                    moving_left = False
                    moving_right = False
                    walkCount = 0
            if BUTTONS_OPTIONS[button] == "OFF":
                if (last == "right"):
                    moving_right = False
                elif (last == "left"):
                    moving_left = False
                else:
                    moving_left = False
                    moving_right = False
                    walkCount = 0

        redrawGameWindow()

def game_intro():
    fd = os.open(PATH, os.O_RDWR)  
    red_leds_on(fd, True)    
    green_leds_on(fd, True)
    intro = True
    sprites_screen = [1, 0, 0, 0]
    while intro:
        button = read_button(fd)

        pos1 = pygame.mouse.get_pos()[0]
        pos2 = pygame.mouse.get_pos()[1]
        #pressed = pygame.mouse.get_pressed()
        # for event in pygame.event.get():
        #     print('for')
        #     #print(event)
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     if((pos1 >= 358 and pos1 <= 605) and (pos2 >= 312 and pos2 <= 366)):
        #         sprites_screen[1] = 1
        #         sprites_screen[0] = 0
        #         sprites_screen[2] = 0
        #         sprites_screen[3] = 0
        #     elif((pos1 >= 358 and pos1 <= 605) and (pos2 >= 393 and pos2 <= 443)):
        #         sprites_screen[1] = 0
        #         sprites_screen[0] = 0
        #         sprites_screen[2] = 1
        #         sprites_screen[3] = 0
        #     elif((pos1 >= 358 and pos1 <= 605) and (pos2 >= 473 and pos2 <= 527)):
        #         sprites_screen[1] = 0
        #         sprites_screen[0] = 0
        #         sprites_screen[2] = 0
        #         sprites_screen[3] = 1
        #     else: 
        #         sprites_screen[1] = 0
        #         sprites_screen[0] = 1
        #         sprites_screen[2] = 0
        #         sprites_screen[3] = 0

        if BUTTONS_OPTIONS[button] == "START":
            game_loop()
        # if (event.type == pygame.MOUSEBUTTONUP) and (pos1 >= 358 and pos1 <= 605) and (pos2 >= 393 and pos2 <= 443):
        #     print('JongaDeus\n')
        # if (event.type == pygame.MOUSEBUTTONUP) and (pos1 >= 358 and pos1 <= 605) and (pos2 >= 473 and pos2 <= 527):
        #     exit()

        if sprites_screen[0] : screen.blit(startScreen, (0,0))
        if sprites_screen[1] : screen.blit(jogar, (0,0))
        if sprites_screen[2] : screen.blit(instrucoes, (0,0))
        if sprites_screen[3] : screen.blit(sair, (0,0))
        pygame.display.update()
        clock.tick(15)
game_intro()
#game_loop()