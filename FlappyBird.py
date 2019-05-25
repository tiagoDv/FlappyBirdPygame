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

class Bird(pygame.sprite.Sprite):
    # This represents the bird should be controlled by the player
    ''' 
    the bird can make it climb
    otherwise it  can sink (descends more than climb)
    it must pass through the pipe and between the pipe and for every pipe pisses one point is second
    
    x: bird X coordinate
    y: bird Y coordinate
    msec_to_climb: Bird.CLIMB_DURATION
    Constants:
        WIDTH
        HEIGHT
        SINK_SPEED

        CLIMB_SPEED
        CLIMB_DURATION : num of msec it takes for bird execute complete climb

    '''
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3

    def __init__(self,x,y,msec_to_climb,images):
        '''
            :param x: bird x coordinate
            :param y: bird y coordinate

            :param msec_to_climb: num if milli sec left to climb, when the complete ckimb last
            :param images: images is tuple containing image used by bird
        '''
        super(Bird,self).__init__()
        self.x,self.y = x,y
        self.msec_to_climb = msec_to_climb
        self.image_wingup,self.image_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)
    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown
        #get a bitmask for use in collision detection
        #bitmask exclude all the pixel in self.image with 

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
def frames_to_msec(frame,fps = FPS):
    return 1000.0 * frame/ fps
    ''' Convert frame to msec at specified rate '''
def msec_to_frames(milliseconds, fps = FPS):
    '''
    milliseconds : how many milliseconds to cionvert for frame
    fps: rate to use for conversion default FPS
    :param milliseconds
    :param fps:
    :return;
    '''
    return fps * milliseconds / 1000.0

def main():
    ''' main of program '''
    pygame.init()
    gameScreen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), 0)
    pygame.display.set_caption("Flappy Bird Pygame")
    clock = pygame.time.Clock()
    score_font = pygame.font.Font("fonts/FlappyBirdy.ttf",20)
    images = load_images()