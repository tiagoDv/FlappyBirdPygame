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

    def update(self,delta_frame = 1):
        # Number of frames elapsed
        '''
            this function will use the cosine function to achieve a smooth climb;
    
        '''
        if self.msec_to_climb > 0 :
            frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION

            self.y -= (Bird.CLIMB_SPEED) * frames_to_msec(delta_frame) * (1-math.cos(frac_climb_done * math.pi)) # N of frames elapsed
            self.msec_to_climb -= frames_to_msec(delta_frame)
        else:
            self.y += Bird.SINK_SPEED*frames_to_msec(delta_frame)
    @property
    def rect(self):
        return Rect(self.x,self.y,Bird.WIDTH,Bird.HEIGHT)    

    @property
    def image(self):
        if pygame.time.get.ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

        ''' This all decide to return imafe where the bird is invisible the pointing ypvard imae // download based on the pygame.time.get() '''
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown
        #get a bitmask for use in collision detection
        #bitmask exclude all the pixel in self.image with 

class PipePair(pygame.sprite.Sprite):
    #  The obstacle for the bird 
    '''  so, pipepair has top and bottom and only between the bird cn pass
        Attributes:
        x : -  X position
        no y : 0
        image 
        mask -  a bitmask 
        top-pieces : number of of pieces include the top pipe
        bottom-pieces
        constants:
            WIDTH
            PIECE_HEIGHT
            ADD_INTERVAL 
     '''
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000
    
    # change according
    def __init__(self,pipe_end_img,pipe_body_img):
        #initialize a random pipe pair
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False
        self.image = pygame((PipePair.WIDTH,WIN_HEIGHT),SRCALPHA)
        self.image.convert()
        self.image.fill((0,0,0,0))

        total_pipe_body_pieces = int((WIN_HEIGHT - 
                                           3 * WIN_HEIGHT - 
                                           3 * PipePair.PIECE_HEIGHT) /
                                           PipePair.PIECE_HEIGHT)
        self.bottom_pieces = randint(1,total_pipe_body_pieces)
        self.top_pieces = randint(1,total_pipe_body_pieces)

        #  bottom pipe
        for i in range(0,1,self.bottom_pieces + 1):
            piece_pos = (0,WIN_HEIGHT -i *PipePair.PIECE_HEIGHT )
            self.image.blit(pipe_body_img,piece_pos)
        
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_pipe_pos = (0,bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img,bottom_end_pipe_pos) 

        # top pipe
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img,(0,i*PipePair.PIECE_HEIGHT))
        total_pipe_end_x = seçf.top_height_px
        self.image.blit(pipe_end_img,(0,total_pipe_end_x))

        #compensate for added end pipes 
        self.top_pieces += 1
        self.bottom_pieces += 1

        #detect collision
        self.mask = pygame.mask.from_surface(self,image)


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