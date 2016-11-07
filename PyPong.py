import pygame, sys, time
from random import randint
from pygame.locals import *
from FGAme import *

pygame.init()

#Definição de cores
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (190, 190, 190)

#Criar display
SIZE = SIZE_WIDTH, SIZE_HEIGHT = 800, 600
DISPLAYSURF = pygame.display.set_mode(SIZE)
SURFACE_RECT = DISPLAYSURF.get_rect()
pygame.display.set_caption('PyPong')

#Clock
clock = pygame.time.Clock()

def things(thingposx, thingposy, thingwidth, thingheight, color):
    pygame.draw.rect(DISPLAYSURF, color, [thingposx, thingposy, thingwidth, thingheight])

#Carregando imagem e criando bola
BALLIMG = pygame.image.load('qicone.png')
def ball(ballx, bally):
    DISPLAYSURF.blit(BALLIMG, (ballx, bally))

#Necessário para messa_display
def text_obj(text, font):
    textsurface = font.render(text, True, WHITE)
    return textsurface, textsurface.get_rect()

#Mostrar texto na tela
def message_display(text):
    LARGETEXT = pygame.font.Font('bitman.ttf', 60)
    TEXTSURF, TEXT_RECT = text_obj(text, LARGETEXT)
    TEXT_RECT.center = ((SIZE_WIDTH/2), (SIZE_HEIGHT/2))
    DISPLAYSURF.blit(TEXTSURF, TEXT_RECT)

    pygame.display.update()

    time.sleep(5) #Tempo antes do jogo retornar ao game_loop automaticamente
    game_loop()

#Função de parada
def crash():
    message_display('Game Over')

# -----------------//-------------
#Ball Stuff
UPLEFT = 0
DOWNLEFT = 1
UPRIGHT = 2
DOWNRIGHT = 3

#Paddle stuff
PADDLE_SPEED = 10
UP1 = False
DOWN1 = False
NO_MOVEMENT1 = True
UP2 = False
DOWN2 = False
NO_MOVEMENT2 = True

class Paddle(pygame.sprite.Sprite):
    def __init__(self, player_number):

        pygame.sprite.Sprite.__init__(self)

        self.player_number = player_number
        self.image = pygame.Surface([10, 100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 8

        if self.player_number == 1:
            self.rect.centerx = DISPLAYSURF.get_rect().left
            self.rect.centerx += 10
        elif self.player_number == 2:
            self.rect.centerx = DISPLAYSURF.get_rect().right
            self.rect.centerx -= 10
        self.rect.centery = DISPLAYSURF.get_rect().centery

    def move(self):

        if self.player_number == 1:
            if (UP1 == True) and (self.rect.y > 5):
                self.rect.y -= self.speed
            elif (DOWN1 == True) and (self.rect.bottom < WINDOW_HEIGHT - 5):
                self.rect.y += self.speed
            elif (NO_MOVEMENT1 == True):
                pass

        if self.player_number == 2:
            if (UP2 == True) and (self.rect.y > 5):
                self.rect.y -= self.speed
            elif (DOWN2 == True) and (self.rect.bottom < WINDOW_HEIGHT - 5):
                self.rect.y += self.speed
            elif (NO_MOVEMENT2 == True):
                pass



class Block(pygame.sprite.Sprite):

    def __init__(self):
        #super(Block, self).__init__()#Super function
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SURFACE_RECT.centerx
        self.rect.centery = SURFACE_RECT.centery
        self.direction = randint(0, 3) ############################
        self.speed = 4

    def move(self):
        if self.direction == UPLEFT:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        elif self.direction == UPRIGHT:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        elif self.direction == DOWNLEFT:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        elif self.direction == DOWNRIGHT:
            self.rect.x += self.speed
            self.rect.y += self.speed

    def change_direction(self):
        if self.rect.y < 0 and self.direction == UPLEFT:
            self.direction = DOWNLEFT
        if self.rect.y < 0 and self.direction == UPRIGHT:
            self.direction = DOWNRIGHT
        if self.rect.y > SURFACE_RECT.bottom and self.direction == DOWNLEFT:
            self.direction = UPLEFT
        if self.rect.y > SURFACE_RECT.bottom and self.direction == DOWNRIGHT:
            self.direction = UPRIGHT

a_block = Block()
b_block = Block()
paddle1 = Paddle(1)
paddle2 = Paddle(2)

#Criando jogo
def game_loop():
    playery1 = playery2 = 260
    playermove1 = playermove2 = 0

    GAMEXIT = False
    while not GAMEXIT:
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playermove2 = -5
                elif event.key == pygame.K_DOWN:
                    playermove2 = 5
                elif event.key == ord('w'):
                    playermove1 = -5
                elif event.key == ord('s'):
                    playermove1 = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playermove1 = playermove2 = 0

        playery1 = playery1 + playermove1
        playery2 = playery2 + playermove2

        DISPLAYSURF.fill(BLACK)

        things(10, playery1, 20, 80, WHITE)#PLayer1
        things(760, playery2, 20, 80, WHITE)#Player2

        things(10,20,780,10, WHITE)#Barra superior

        if playery1 > SIZE_HEIGHT-80 or playery1 <0 or playery2 > SIZE_HEIGHT-80 or playery2 <0:
            crash() #mostrar mensagem de game over

        block_group = pygame.sprite.RenderPlain(a_block, b_block, paddle1, paddle2)
        block_group.draw(DISPLAYSURF)

        a_block.move()
        a_block.change_direction()
        b_block.move()
        b_block.change_direction()

        pygame.display.update()
        clock.tick(30)


#Criação de botão
def button(msg,posx,posy,width,height,inactivecolor, activecolor, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if posx + width > mouse[0] > posx and posy + height > mouse[1] > posy:
        pygame.draw.rect(DISPLAYSURF, activecolor, (posx, posy, width, height))
        if click[0] == 1 and action!= None:
            action()
            """if action == "classic":
                pygame.quit()
            elif action == "multiball":
                game_loop_multiball()"""
    else:
        pygame.draw.rect(DISPLAYSURF, inactivecolor, (posx, posy, width, height))

    MEDIUMFONT = pygame.font.Font('bitman.ttf', 20)
    TEXT = MEDIUMFONT.render(msg, True, BLACK)
    TEXT_RECT = TEXT.get_rect()
    TEXT_RECT.center = ((posx + (width/2)), (posy + (height/2)))
    DISPLAYSURF.blit(TEXT, TEXT_RECT)

#Crianção do menu inicial
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        DISPLAYSURF.fill(BLACK)
        FONT = pygame.font.Font('bitman.ttf', 60)
        NAME = FONT.render('PYPONG', True, WHITE, BLACK)
        NAME_RECT = NAME.get_rect()
        NAME_RECT.center = (400, 150)
        DISPLAYSURF.blit(NAME, NAME_RECT)

        pygame.draw.rect(DISPLAYSURF, WHITE, (10,20,780,10))
        pygame.draw.rect(DISPLAYSURF, WHITE, (10, 570, 780, 10))

        button("CLASSIC", 275, 300, 250, 30, WHITE, GRAY)
        button("DOUBLE", 275, 350, 250, 30, WHITE, GRAY)
        button("MULTI BALL", 275, 400, 250, 30, WHITE, GRAY, game_multi)
        button("CANNON", 275, 450, 250, 30, WHITE, GRAY)

        pygame.display.update()

def game_multiball():

    DISPLAYSURF.fill(GRAY)
    pygame.display.set_caption('PyPong - MultiBall')

def game_multi():
    world = World(background='black')
    world.add.margin(1, color='black')
    centrebar = world.add(draw.AABB(shape=(10, 490), pos=(400, 300), color='white'))
    upbar = world.add.aabb(shape=(760, 10), pos=(400, 580), mass = 'inf', color='white')
    downbar = world.add.aabb(shape=(760, 10), pos=(400, 20), mass = 'inf', color='white')
    ball = world.add.circle(15, pos=(500, 360), color='red', vel=vel.random_fast())
    ball_2 = world.add.circle(15, pos=(500,400), color='white', vel=vel.random_fast())
    ball_3 = world.add.circle(15, pos=(500, 440), color='yellow', vel=vel.random_fast())
    p1 = world.add.aabb(shape=(20, 120), pos=(30, 300), mass='1000000000', color='red')
    p2 = world.add.aabb(shape=(20, 120), pos=(770, 300), mass='1000000000', color='white')
    on('long-press', 'w').do(p1.move, 0, 5)
    on('long-press', 's').do(p1.move, 0, -5)
    on('long-press', 'up').do(p2.move, 0, 5)
    on('long-press', 'down').do(p2.move, 0, -5)
    pause = world.listen('key-down', 'space', function=world.toggle_pause)

    run()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update() and run()

game_intro()
