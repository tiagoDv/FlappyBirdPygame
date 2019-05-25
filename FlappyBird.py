import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *

#Base variables
FPS = 60
ANIMATION_SPEED = 0.18
WIN_WIDTH = 284 * 2
WIN_HEIGHT = 512


def load_images():
    '''load images required by images and return dict of them
        what should it return?
        1. Background
        2. bird-wingup
        3 .bird-wingdown
        4. pipe-end
        5. pipe-body
    '''
    def load_image(img_file_name):
        '''
        :return the pygame image with specified filename
        :param img_file_name:
        :return:
         '''
        file_name = os.path.join('.','images',img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img
    return {
        'background': load_image('background.png'),
        'pipe-end': load_image('pipe_end.png'),
        'pipe-body': load_image('pipe_body.png'),
        'bird-wingup':load_image('bird_wing_up.png'),
        'bird-wingdown':load_image('bird_wing_down.png') 
    }


def main():
    ''' main of program '''
    pygame.init()
    gameScreen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), 0)
    pygame.display.set_caption("Flappy Bird Pygame")
    clock = pygame.time.Clock()
    score_font = pygame.font.Font("fonts/FlappyBirdy.ttf",20)
    images = load_images()