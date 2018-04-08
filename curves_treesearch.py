# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 18:59:56 2018

@author: pranav
"""

import random
import sys
import time
import numpy as np
from math import *
import matplotlib.pyplot as plt

SPEED = 2       # frames per second setting
WINWIDTH = 1280  # width of the program's window, in pixels
WINHEIGHT = 720  # height in pixels
STEPSIZE = 10       # Stepsize of each move
PLAYERS = 1      # number of players
PLAYSIZE = 5 # size of player circle
TOL = 2     # tolerance in distination postion
BORDER = 15 # forbidden border around the chip
THETA = 10 # resolution of angle

BLACK = 0 
WHITE = 255 
GRAY = 150

def main():
    # main loop
    global SCREEN
    # SCREEN is the map
    SCREEN = np.zeros((WINWIDTH, WINHEIGHT), dtype = np.uint8)
    rungame()
    

class Player(object):
    # Class which can be used to generate random position and angle, to compute movement values and to draw player
    def __init__(self):
        self.running = True
        self.colour = None
        self.length = 200 #+ 200

    def start(self):
        # start position and direction
        self.x = 200 
        self.y = 600 
        self.angle = 0 
        
        # stop position and direction
        self.stop_x = 450
        self.stop_y = 600
        self.stop_angle = 0
        for i in range(3):
            delx = int(i * cos(radians(self.angle)))
            dely = int(i * sin(radians(self.angle)))
            SCREEN[self.stop_x - delx, self.stop_y - dely] = GRAY
            SCREEN[self.stop_x + delx, self.stop_y + dely] = GRAY
    
    def move(self):
        # computes current movement
        self.x += int(STEPSIZE * cos(radians(self.angle)))
        self.y += int(STEPSIZE * sin(radians(self.angle)))
        
    def actions(self):
        # allowed actions
        self.actions = [-1,0,1]
        
    def draw(self):
        # drawing players
        SCREEN[self.x - PLAYSIZE:self.x + PLAYSIZE, self.y - PLAYSIZE:self.y + PLAYSIZE] = WHITE

def DFS(length, player_t):
    i=0
    if length * STEPSIZE + TOL >= player_t[i].length:
        pass
    return
    
def rungame():
    global WINNER, SCORE
    WINNER = 0
    run = True
    players_running = PLAYERS
    SCORE = 0
    length = 0
    action = np.zeros(PLAYERS)
    # generating players
    player_t = []
    for i in range(PLAYERS):
        player_t.append(Player())
        player_t[i].start()
        player_t[i].draw()
    fig = plt.figure(1)
    im = plt.imshow(SCREEN.T)
    while run:
        length += 1
        for i in range(PLAYERS):  # loop for checking positions, drawing, moving and scoring for all players
            if player_t[i].running:
                player_t[i].angle = (player_t[i].angle + THETA * action[0]) % 360
                player_t[i].move()
                
                # checking if you collide and fail
                if (player_t[i].x > WINWIDTH - BORDER or player_t[i].x < BORDER or
                            player_t[i].y > WINHEIGHT - BORDER or player_t[i].y < BORDER or
                            SCREEN[player_t[i].x, player_t[i].y] == WHITE):
                    player_t[i].running = False
                    players_running = 0
                    SCORE -= 2
                
                # checking if the max length for this curve is reached
                elif length * STEPSIZE + TOL >= player_t[i].length: 
                    # note: the above condition might need to be modified if 
                    # the integer rounding off errors mess thigns up
                    player_t[i].running = False
                    players_running -= 1
                    
                    # check if the destination is correctly reached 
                    if (abs(player_t[i].x - player_t[i].stop_x) <= TOL and
                        abs(player_t[i].y - player_t[i].stop_y) <= TOL and
                        player_t[i].angle == player_t[i].stop_angle):
                        
                        SCORE += 1
                    else:
                        SCORE -= 1
                    
                player_t[i].draw()
                              
        # Determine the action to be taken from the agent
#        action = Agent(player_t, )
        
#        time.sleep(10)
        # checking if someone reach max length and win
        if players_running == 0:
            im.set_data(SCREEN.T)
            plt.draw()
            if SCORE > 0:
                WINNER = 1
            run = False
            players_running = PLAYERS
            for i in range(PLAYERS):
                player_t[i].start()
                player_t[i].running = True
            continue

        
if __name__ == '__main__':
    main()
