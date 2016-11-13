import pygame, sys, time, random
from pygame.locals import *
import random
from random import randint
from sys import exit

pygame.init()

#Definição de cores
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (190, 190, 190)

#Criar tela
DISPLAYSURF = pygame.display.set_mode((800,600))
SURFACE_RECT = DISPLAYSURF.get_rect()
pygame.display.set_caption('PyPong')

#Criar texto
def makeText(text, colorfront, sizefont, centerx, centery):
    FONT = pygame.font.Font('bitman.ttf', sizefont)
    TEXT = FONT.render(text, True, colorfront)
    OBJ = TEXT.get_rect()
    OBJ.center = (centerx, centery)
    DISPLAYSURF.blit(TEXT, OBJ)

#Criar objetos
def makeObject(posx, posy, width, height, color):
    pygame.draw.rect(DISPLAYSURF, color, [posx, posy, width, height])

#Criar circulos
def makeCircle(x, y):
    center = int(x), int(y)
    pygame.draw.circle(DISPLAYSURF, WHITE, center, 8, 0)

#Criar butões
def makeButton(msg, fontsize, posx,posy,width,height,inactivecolor, activecolor, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if posx + width > mouse[0] > posx and posy + height > mouse[1] > posy:
        makeObject(posx, posy, width, height, activecolor)
        if click[0] == 1 and action != None:
            action()
    else:
        makeObject(posx, posy, width, height, inactivecolor)

    makeText(msg, BLACK, fontsize, (posx + (width/2)), (posy + (height/2)))

#Criar layout padrão
def layout():
    makeObject(10, 20, 780, 10, WHITE)
    makeObject(10, 570, 780, 10, WHITE)
    makeObject(397, 38,  6, 15, WHITE)
    makeObject(397, 68,  6, 15, WHITE)
    makeObject(397, 98,  6, 15, WHITE)
    makeObject(397, 128, 6, 15, WHITE)
    makeObject(397, 158, 6, 15, WHITE)
    makeObject(397, 188, 6, 15, WHITE)
    makeObject(397, 218, 6, 15, WHITE)
    makeObject(397, 248, 6, 15, WHITE)
    makeObject(397, 278, 6, 15, WHITE)
    makeObject(397, 308, 6, 15, WHITE)
    makeObject(397, 338, 6, 15, WHITE)
    makeObject(397, 368, 6, 15, WHITE)
    makeObject(397, 398, 6, 15, WHITE)
    makeObject(397, 428, 6, 15, WHITE)
    makeObject(397, 458, 6, 15, WHITE)
    makeObject(397, 488, 6, 15, WHITE)
    makeObject(397, 518, 6, 15, WHITE)
    makeObject(397, 548, 6, 15, WHITE)

#Criar pause e unpause
pause = False
def unpause():
    global pause
    pause = False
def paused():
    makeText('PAUSED', WHITE, 50, 400, 300)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        makeButton('RESUME',       15, 315, 400, 170, 20, WHITE, GRAY,unpause)
        makeButton('MAIN MENU', 15, 315, 430, 170, 20, WHITE, GRAY, pypong_intro)
        pygame.display.update()

#Criar menu inicial
def pypong_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BLACK)

        TITLE = makeText('PYPONG',                  WHITE, 60, 400, 150)
        CREDITS = makeText('2016 - Pygame', WHITE, 15, 400, 200)

        makeObject(10, 20, 780, 10, WHITE)
        makeObject(10, 570, 780, 10, WHITE)

        makeButton("CLASSIC",      20, 275, 300, 250, 30, WHITE, GRAY, pypong_classic)
        makeButton("DOUBLE",       20, 275, 350, 250, 30, WHITE, GRAY)
        makeButton("MULTI BALL",   20, 275, 400, 250, 30, WHITE, GRAY, pypong_multiball)
        makeButton("CANNON",       20, 275, 450, 250, 30, WHITE, GRAY)
        makeButton("INSTRUCTIONS", 10, 315, 530, 170, 20, WHITE, GRAY, pypong_instructions)

        pygame.display.update()

#Criar tela de instruções
def pypong_instructions():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BLACK)
        makeObject(10, 20, 780, 10, WHITE)
        makeObject(10, 570, 780, 10, WHITE)

        makeText('Instructions:',             WHITE, 30, 400, 150)
        makeText('     W/S - moves Player 1', WHITE, 20, 400, 250)
        makeText('UP/DOWN - moves Player 2',  WHITE, 20, 400, 300)
        makeText('  PAUSE - pause game',      WHITE, 20, 400, 350)

        makeButton("MAIN MENU", 10, 315, 530, 170, 20, WHITE, GRAY, pypong_intro)

        pygame.display.update()

#Criar placar
def score(player1_score,player2_score):
    score1 = makeText(str(player1_score),WHITE, 40, 50, 70)
    score2 = makeText(str(player2_score),WHITE, 40, 750, 70)

#Criar jogo multi bolas
def pypong_multiball():
    global pause
    #Parâmetros bola e jogadores
    ball_x, ball_y = 400, 300
    ball2_x, ball2_y = 410, 310
    player1_x, player1_y = 10, 255
    player2_x, player2_y = 775, 255
    playermove1, playermove2 = 0, 0
    clock = pygame.time.Clock()
    player1_score = player2_score = 0
    speed_x, speed_y = randint(200, 300), randint(200, 300)
    speed2_x, speed2_y = randint(200, 300), randint(200, 300)
    time_passed = clock.tick(60)#clock tick update the clock
    time_sec = time_passed / 10000.0
    quadrant = random.choice([1, 2, 3, 4])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    playermove2 = -1
                elif event.key == K_DOWN:
                    playermove2 = 1
                elif event.key == ord('w'):
                    playermove1 = -1
                elif event.key == ord('s'):
                    playermove1 = 1
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    playermove1 = playermove2 = 0
                if event.key == ord('w') or event.key == ord('s'):
                    playermove1 = playermove2 = 0

        player1_y += playermove1
        player2_y += playermove2

        #Limites jogador-layout
        if player1_y >= 480:
            player1_y = 480
        elif player1_y <= 30:
            player1_y = 30
        if player2_y >= 480:
            player2_y = 480
        elif player2_y <= 30:
            player2_y = 30

        # Movimentos da bola
        if quadrant == 1:
            ball_x += (speed_x * time_sec)
            ball_y += (speed_y * time_sec)
            ball2_x -= (speed2_x * time_sec)
            ball2_y -= (speed2_y * time_sec)
        if quadrant == 2:
            ball_x -= (speed_x * time_sec)
            ball_y -= (speed_y * time_sec)
            ball2_x += (speed2_x * time_sec)
            ball2_y += (speed2_y * time_sec)
        if quadrant == 3:
            ball_x += (speed_x * time_sec)
            ball_y -= (speed_y * time_sec)
            ball2_x -= (speed2_x * time_sec)
            ball2_y += (speed2_y * time_sec)
        if quadrant == 4:
            ball_x -= (speed_x * time_sec)
            ball_y += (speed_y * time_sec)
            ball2_x += (speed2_x * time_sec)
            ball2_y -= (speed2_y * time_sec)

        #Limites bola-layout
        if ball_y <= 32.5:
            speed_y = -speed_y
            ball_y = 32.5
        elif ball_y >= 567.5:
            speed_y = -speed_y
            ball_y = 567.5
        if ball2_y <= 32.5:
            speed2_y = -speed2_y
            ball2_y = 32.5
        elif ball2_y >= 567.5:
            speed2_y = -speed2_y
            ball2_y = 567.5

        # Detectando colisões bola-jogador
        if ball_x <= player1_x + 15:
            if ball_y >= player1_y + 15 and ball_y <= player1_y + 90:
                ball_x = 25
                speed_x = -speed_x
        if ball_x >= player2_x:
            if ball_y >= player2_y and ball_y <= player2_y + 90:
                ball_x = 775
                speed_x = -speed_x
        if ball2_x <= player1_x + 15:
            if ball2_y >= player1_y + 15 and ball2_y <= player1_y + 90:
                ball2_x = 25
                speed2_x = -speed2_x
        if ball2_x >= player2_x:
            if ball2_y >= player2_y and ball2_y <= player2_y + 90:
                ball2_x = 775
                speed2_x = -speed2_x

        # Realizando contagem de pontos
        if ball_x < 23:
            player2_score += 1
            ball_x, ball_y = 400, 300
        elif ball_x >= 777:
            player1_score += 1
            ball_x, ball_y = 400, 300
        if ball2_x < 23:
            player2_score += 1
            ball2_x, ball2_y = 400, 300
        elif ball2_x >= 777:
            player1_score += 1
            ball2_x, ball2_y = 400, 300

        DISPLAYSURF.fill(BLACK)
        layout()

        score(player1_score, player2_score)#Placar
        makeCircle(ball_x, ball_y)#Bola 1
        makeCircle(ball2_x, ball2_y)#Bola 2
        makeObject(player1_x, player1_y, 15, 90, WHITE)#Player 1
        makeObject(player2_x, player2_y, 15, 90, WHITE)#Player 2

        # Checando o vencedor
        if player1_score >=10 or player2_score >=10:
            if player1_score >= 10:
                makeText('PLAYER 1', WHITE, 30, 200, 230)
                makeText('WINS',     WHITE, 30, 200, 270)
                makeText('PLAYER 2', WHITE, 30, 600, 230)
                makeText('LOSES',    WHITE, 30, 600, 270)
                makeText('Total Score: ' + str(player1_score), WHITE, 15, 200, 320)
                makeText('Total Score: ' + str(player2_score), WHITE, 15, 600, 320)
            elif player2_score >= 10:
                makeText('PLAYER 2',  WHITE, 30, 600, 230)
                makeText('WINS',      WHITE, 30, 600, 270)
                makeText('PLAYER 1',  WHITE, 30, 200, 230)
                makeText('LOSES',     WHITE, 30, 200, 270)
                makeText('Total Score: ' + str(player1_score), WHITE, 15, 200, 320)
                makeText('Total Score: ' + str(player2_score), WHITE, 15, 600, 320)
            ball_x, ball_y = 400, 300
            ball2_x, ball2_y = 400, 300
            makeButton("PLAY AGAIN", 10, 315, 500, 170, 20, WHITE, GRAY, pypong_multiball)
            makeButton("MAIN MENU",  10, 315, 530, 170, 20, WHITE, GRAY, pypong_intro)

        pygame.display.update()


def pypong_classic():
    global pause
    # Parâmetros bola e jogadores
    ball_x, ball_y = 400, 300
    player1_x, player1_y = 10, 255
    player2_x, player2_y = 775, 255
    playermove1, playermove2 = 0, 0
    clock = pygame.time.Clock()
    player1_score = player2_score = 0
    speed_x, speed_y = randint(200, 300), randint(200, 300)
    time_passed = clock.tick(60)  # clock tick update the clock
    time_sec = time_passed / 10000.0
    quadrant = random.choice([1, 2, 3, 4])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    playermove2 = -1
                elif event.key == K_DOWN:
                    playermove2 = 1
                elif event.key == ord('w'):
                    playermove1 = -1
                elif event.key == ord('s'):
                    playermove1 = 1
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    playermove1 = playermove2 = 0
                if event.key == ord('w') or event.key == ord('s'):
                    playermove1 = playermove2 = 0

        player1_y += playermove1
        player2_y += playermove2

        # Limites jogador-layout
        if player1_y >= 480:
            player1_y = 480
        elif player1_y <= 30:
            player1_y = 30
        if player2_y >= 480:
            player2_y = 480
        elif player2_y <= 30:
            player2_y = 30

        # Movimentos da bola
        if quadrant == 1:
            ball_x += (speed_x * time_sec)
            ball_y += (speed_y * time_sec)
        if quadrant == 2:
            ball_x -= (speed_x * time_sec)
            ball_y -= (speed_y * time_sec)
        if quadrant == 3:
            ball_x += (speed_x * time_sec)
            ball_y -= (speed_y * time_sec)
        if quadrant == 4:
            ball_x -= (speed_x * time_sec)
            ball_y += (speed_y * time_sec)

        # Limites bola-layout
        if ball_y <= 32.5:
            speed_y = -speed_y
            ball_y = 32.5
        elif ball_y >= 567.5:
            speed_y = -speed_y
            ball_y = 567.5

        # Detectando colisões bola-jogador
        if ball_x <= player1_x + 15:
            if ball_y >= player1_y + 15 and ball_y <= player1_y + 90:
                ball_x = 25
                speed_x = -speed_x
        if ball_x >= player2_x:
            if ball_y >= player2_y and ball_y <= player2_y + 90:
                ball_x = 775
                speed_x = -speed_x

        # Realizando contagem de pontos
        if ball_x < 23:
            player2_score += 1
            ball_x, ball_y = 400, 300
        elif ball_x >= 777:
            player1_score += 1
            ball_x, ball_y = 400, 300

        DISPLAYSURF.fill(BLACK)
        layout()

        score(player1_score, player2_score)  # Placar
        makeCircle(ball_x, ball_y)  # Bola 1
        makeObject(player1_x, player1_y, 15, 90, WHITE)  # Player 1
        makeObject(player2_x, player2_y, 15, 90, WHITE)  # Player 2

        # Checando o vencedor
        if player1_score >= 10 or player2_score >= 10:
            if player1_score >= 10:
                makeText('PLAYER 1', WHITE, 30, 200, 230)
                makeText('WINS', WHITE, 30, 200, 270)
                makeText('PLAYER 2', WHITE, 30, 600, 230)
                makeText('LOSES', WHITE, 30, 600, 270)
                makeText('Total Score: ' + str(player1_score), WHITE, 15, 200, 320)
                makeText('Total Score: ' + str(player2_score), WHITE, 15, 600, 320)
            elif player2_score >= 10:
                makeText('PLAYER 2', WHITE, 30, 600, 230)
                makeText('WINS', WHITE, 30, 600, 270)
                makeText('PLAYER 1', WHITE, 30, 200, 230)
                makeText('LOSES', WHITE, 30, 200, 270)
                makeText('Total Score: ' + str(player1_score), WHITE, 15, 200, 320)
                makeText('Total Score: ' + str(player2_score), WHITE, 15, 600, 320)
            ball_x, ball_y = 400, 300
            ball2_x, ball2_y = 400, 300
            makeButton("PLAY AGAIN", 10, 315, 500, 170, 20, WHITE, GRAY, pypong_multiball)
            makeButton("MAIN MENU", 10, 315, 530, 170, 20, WHITE, GRAY, pypong_intro)

        pygame.display.update()


pypong_intro()
