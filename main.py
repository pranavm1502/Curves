import random
import sys
import time
import pygame
import pygame.gfxdraw

from menu import *

from math import *
from pygame.locals import *

SPEED = 2       # frames per second setting
WINWIDTH = 1280  # width of the program's window, in pixels
WINHEIGHT = 720  # height in pixels
RADIUS = 10       # radius of the circles
PLAYERS = 1      # number of players
playerSize = 5 # size of player circle
len_tol = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
P1COLOUR = RED
P2COLOUR = GREEN
P3COLOUR = BLUE


def main():
    # main loop
    global FPS_CLOCK, SCREEN, DISPLAYSURF, MY_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    DISPLAYSURF = pygame.Surface(SCREEN.get_size())
    pygame.display.set_caption('Curves!')
    # pygame.mixer.music.load('test.mp3')
    # pygame.mixer.music.play(-1, 0.0)
    MY_FONT = pygame.font.SysFont('bauhaus93', 37)

    while True:
        start_screen()
        rungame()
        gameover()


class Player(object):
    # Class which can be used to generate random position and angle, to compute movement values and to draw player
    def __init__(self):
        self.running = True
        self.colour = None
        self.length = 200 + 200

    def start(self):
        # start position and direction
        self.x = 200 #random.randrange(50, WINWIDTH - 165)
        self.y = 600 #random.randrange(50, WINHEIGHT - 50)
        self.angle = 0 #random.randrange(0, 360)
        
        # stop position and direction
        self.stop_x = 450
        self.stop_y = 600
        self.stop_angle = 0
    
    def move(self):
        # computes current movement
        self.x += int(RADIUS * cos(radians(self.angle)))
        self.y += int(RADIUS * sin(radians(self.angle)))

    def draw(self):
        # drawing players
        pygame.gfxdraw.aacircle(DISPLAYSURF, self.x, self.y, playerSize, self.colour)
        pygame.gfxdraw.filled_circle(DISPLAYSURF, self.x, self.y, playerSize, self.colour)


def rungame():
    global WINNER, SCORE
    DISPLAYSURF.fill(BLACK)
    pygame.draw.aaline(DISPLAYSURF, WHITE, (WINWIDTH-115, 0), (WINWIDTH-115, WINHEIGHT))
    WINNER = 0
    first = True
    run = True
    players_running = PLAYERS
    SCORE = 0
    length = 0
    largePenalty = -10
    # generating players
    player1 = Player()
    player2 = Player()
    player3 = Player()
    player_t = [player1, player2, player3]
    for i in range(PLAYERS):
        player_t[i].start()

    while run:
        # checking how many players are needed running
        if PLAYERS < 3:
            player3.running = False

        # initializing players colours
        player1.colour = P1COLOUR
        player2.colour = P2COLOUR
        player3.colour = P3COLOUR

        length += 1
        for i in range(PLAYERS):  # loop for checking positions, drawing, moving and scoring for all players
            if player_t[i].running and players_running >= 1:
                player_t[i].angle = player_t[i].angle % 360
                player_t[i].move()
                
                # checking if you collide and fail
                if (player_t[i].x > WINWIDTH-125 or player_t[i].x < 3 or
                            player_t[i].y > WINHEIGHT-3 or player_t[i].y < 3 or
                            DISPLAYSURF.get_at((player_t[i].x, player_t[i].y)) != BLACK):
                    player_t[i].running = False
                    players_running = 0
                    SCORE = LargePenalty
                
                # checking if the max length for this curve is reached
                if length * RADIUS + len_tol >= player_t[i].length: 
                    # note: the above condition might need to be modified if 
                    # the integer rounding off errors mess thigns up
                    player_t[i].running = False
                    players_running -= 1
                    
                    # check if the destination is correctly reached 
                    if (abs(player_t[i].x - player_t[i].stop_x) <= len_tol and
                        abs(player_t[i].y - player_t[i].stop_y) <= len_tol and
                        player_t[i].angle == player_t[i].stop_angle):
                        
                        SCORE += 1
                    else:
                        SCORE -= 1
                    
                player_t[i].draw()
                              

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
        

        # steering
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.angle -= 10
        if keys[pygame.K_RIGHT]:
            player1.angle += 10
        if keys[pygame.K_a]:
            player2.angle -= 10
        if keys[pygame.K_s]:
            player2.angle += 10
        if keys[pygame.K_k]:
            player3.angle -= 10
        if keys[pygame.K_l]:
            player3.angle += 10

        # drawing scores
        length_disp(length, [player1.x, player1.y, player1.angle], P1COLOUR)

        # drawing all on the screen
        SCREEN.blit(DISPLAYSURF, (0, 0))
        pygame.display.update()

        # checking if someone reach max length and win
        if players_running == 0:
            if SCORE > 0:
                WINNER = 1
            run = False
            pygame.time.wait(1000)
#            DISPLAYSURF.fill(BLACK)
            pygame.draw.aaline(DISPLAYSURF, WHITE, (WINWIDTH-115, 0), (WINWIDTH-115, WINHEIGHT))
            first = True
            players_running = PLAYERS
            for i in range(PLAYERS):
                player_t[i].start()
                player_t[i].running = True
            continue

        if first:  # if the game starts, wait some time
            pygame.time.wait(1500)
            first = False

        FPS_CLOCK.tick(SPEED)


def start_screen():
    # initializing menu, getting number of players after choosing game mode
    global PLAYERS
    menu = Menu(['1 Player', '3 Players', 'Help', 'Exit'])
    menu.init(SCREEN)
    menu.draw()
    PLAYERS = menu.start()


def length_disp(length, xy, colour1):
    # drawing scores
    colour0 = WHITE
    len_msg = MY_FONT.render("L: " + str(length), 1, colour0, BLACK)
    len1_msg = MY_FONT.render("x: " + str(xy[0]), 1, colour1, BLACK)
    len2_msg = MY_FONT.render("y: " + str(xy[1]), 1, colour1, BLACK)
    len3_msg = MY_FONT.render("a: " + str(xy[2]), 1, colour1, BLACK)
    DISPLAYSURF.blit(len_msg, (WINWIDTH - 110, WINHEIGHT/10))
    DISPLAYSURF.blit(len1_msg, (WINWIDTH - 108, WINHEIGHT/10 + 40))
    DISPLAYSURF.blit(len2_msg, (WINWIDTH - 108, WINHEIGHT/10 + 80))
    DISPLAYSURF.blit(len3_msg, (WINWIDTH - 108, WINHEIGHT/10 + 120))


def gameover():
    # drawing winner/s and waiting for key press
    if WINNER == 1:
        end_msg = "Good job." 
    else:
        end_msg = "Try again. Your score is " + str(SCORE)
    end_msg_render = MY_FONT.render(end_msg, 1, WHITE, BLACK)
    SCREEN.blit(end_msg_render, ((WINWIDTH - MY_FONT.size(end_msg)[0]) / 2, WINHEIGHT/5))
    pygame.display.update()
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                else:
                    end = False
        FPS_CLOCK.tick(10)


if __name__ == '__main__':
    main()
