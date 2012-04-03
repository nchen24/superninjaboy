import pygame, os, sys
from pygame.locals import *

###############################
# Constants for image loading #
###############################
IDLE1 = "../assets/idle.gif"
FALL1 = "../assets/fall.gif"
JUMP1 = "../assets/jump.gif"
WALK1 = "../assets/walking_1.gif"
WALK2 = "../assets/walking_2.gif"
WALK3 = "../assets/walking_3.gif"
WALK4 = "../assets/walking_4.gif"
RUNN1 = "../assets/running_1.gif"
RUNN2 = "../assets/running_2.gif"
RUNN3 = "../assets/running_3.gif"
RUNN4 = "../assets/running_4.gif"
SLID1 = "../assets/wall_slide.gif"
PLAT1 = "../assets/platform1.png"
SS = "../assets/sprite_sheet_colors_fixed.png"



IDLE_L = (0,25,10,24)
FALL_L = (134,25,18,24) 
JUMP_L = (118,25,15,24) 
WALK_L = ((11,25,13,24),(25,25,8,24),(34,25,10,24),(45,25,12,24))
RUNN_L = ((58,25,16,24),(75,25,11,24),(87,25,11,24),(99,25,18,24))
SLID_L = (153,25,11,24)

IDLE_R = (0,0,10,24)
FALL_R = (134,0,18,24)
JUMP_R = (118,0,15,24)
WALK_R = ((11,0,13,24),(25,0,8,24),(34,0,10,24),(45,0,12,24)) 
RUNN_R = ((58,0,16,24),(75,0,11,24),(87,0,11,24),(99,0,18,24))
SLID_R = (153,0,11,24)




###################
# Other constants #
###################
#ONEFRAME  = 20
ONEFRAME = 11
JUMPLIMIT = 50
SPRINTMOD = 2



class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

#################
# Player Sprite #
#################

class Player(pygame.sprite.Sprite):
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__(self, screen, x, y):

        self.ss = spritesheet(SS)
        self.WALK_RIGHT = []
        self.WALK_LEFT = []
        self.RUNN_RIGHT = []
        self.RUNN_LEFT = []

        #Load two images into an array, their transparent bit is (255, 255, 255)
        self.WALK_RIGHT = self.ss.images_at(WALK_R, colorkey=-1)
        self.WALK_LEFT  = self.ss.images_at(WALK_L, colorkey=-1)

        self.RUNN_RIGHT = self.ss.images_at(RUNN_R, colorkey=-1)
        self.RUNN_LEFT  = self.ss.images_at(RUNN_L, colorkey=-1)

        self.JUMP_RIGHT = self.ss.image_at(JUMP_R,  colorkey = -1)
        self.JUMP_LEFT  = self.ss.image_at(JUMP_L,  colorkey = -1)

        self.IDLE_RIGHT = self.ss.image_at(IDLE_R,  colorkey=-1)
        self.IDLE_LEFT  = self.ss.image_at(IDLE_L,  colorkey=-1)
        
        self.FALL_RIGHT = self.ss.image_at(FALL_R,  colorkey=-1)
        self.FALL_LEFT  = self.ss.image_at(FALL_L,  colorkey=-1)

        self.SLID_RIGHT = self.ss.image_at(SLID_R,  colorkey=-1)
        self.SLID_LEFT  = self.ss.image_at(SLID_L,  colorkey=-1)


        self.direction = "Right"
        self.whichIdle()

        self.screen = screen
        self.x   = x
        self.y   = y
        self.dx  = 0
        self.dy  = 0

        #self.ddx = .1
        self.ddx = .5
        self.ddy = 0

        #self.dx_max = .8
        #self.dy_max = .8
        self.dx_max = 2
        self.dy_max = 2


        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.bottom = pygame.Rect((self.x + 2,(self.y + self.image_h - 5)), (self.image_w - 4, 5))

        # pygame.Rect takes ((start_x, start_y), (width, height))[EXPERIMENTAL]
        self.boundwidth = 5
        self.left = pygame.Rect((self.x, self.y), (self.boundwidth, self.image_h-self.boundwidth))
        self.right = pygame.Rect((self.x + self.image_w - self.boundwidth, self.y), (self.boundwidth, self.image_h - self.boundwidth))

        self.alive = True
        self.jumped = False
        self.canJump = True
        self.apex = False # True if the player has reached the max jump height
        self.jumptimer = 0
        self.movetimer = 0
        self.runtimer  = 0
        self.onplat = False
        self.onwall = False
        self.contact_side = None

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self, pressed, screenDimensions):
        if pressed['Space'] == True and not(self.jumped) and not(self.apex) and self.canJump == True:
            self.onplat = False
            if self.jumptimer > JUMPLIMIT:
                self.apex = True
                self.canJump = False
            else:
                self.jumptimer += 1

            self.whichJump()
            #self.dy = -.8
            self.dy = -2

        elif self.onplat == False and self.onwall == False:
            self.whichFall()
            #self.dy = .8
            self.dy = 2

        else:
            self.whichIdle()
            self.dy = 0
            self.jumped = False
            self.apex = False
            self.jumptimer = 0
        
        if pressed['Left'] == True:
            self.direction = "Left"
            if pressed['Shift'] == True: 
                if abs(self.dx) < SPRINTMOD*self.dx_max:
                    self.dx = self.dx - self.ddx
            else:
                if abs(self.dx) > self.dx_max:
                    self.dx = -self.dx_max
                if abs(self.dx) < self.dx_max:
                    self.dx = self.dx - self.ddx
            if pressed ['Right'] == True:
                self.dx = 0 
            elif pressed ['Space'] == False:
                if self.dy == 0:
                    if pressed['Shift'] == True:
                        self.whichRun()
                    else:
                        self.whichWalk()

        elif pressed['Right'] == True:
            self.direction = "Right"
            if pressed['Shift'] == True:
                if abs(self.dx) < SPRINTMOD*self.dx_max:
                    self.dx = self.dx + self.ddx
            else:
                if abs(self.dx) > self.dx_max:
                    self.dx = self.dx_max
                if abs(self.dx) < self.dx_max:
                    self.dx = self.dx + self.ddx
            if pressed ['Left'] == True:
                self.dx = 0 
            elif pressed ['Space'] == False:
                if self.dy == 0:
                    if pressed['Shift'] == True:
                        self.whichRun()
                    else:
                        self.whichWalk()
        else:
            self.dx = 0



        if self.onwall == True and self.onplat == False:
            self.whichSlide()
            self.dy = 1.5
            self.dx = 0
            self.jumped = False
            self.apex = False
            self.jumptimer = 0
            #self.canJump = True

        # Move the bounding box
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        # The sides [EXPERIMENTAL]
        self.left.top = self.left.top + self.dy
        self.left.left = self.left.left + self.dx

        self.right.top = self.right.top + self.dy
        self.right.left = self.right.left + self.dx

        self.left = pygame.Rect((self.x, self.y), (self.boundwidth, self.image_h - self.boundwidth))
        self.right = pygame.Rect((self.x + self.image_w - self.boundwidth, self.y), (self.boundwidth, self.image_h - self.boundwidth))
        self.bottom = pygame.Rect((self.x+2,(self.y + self.image_h - 5)), (self.image_w-4, 5))


    def respawn(self, x, y):
        self.x = x
        self.y = y
        self.jumped = False
        self.jumptimer = 0
        self.onplat = False
        self.whichIdle()
        self.dx  = 0
        self.dy  = 0
        self.alive = True
       


    # Determines which walking animation to load.
    def whichWalk(self):
        if self.movetimer < ONEFRAME: # ONEFRAME is defined in constants.  This
            # allows for easy tweaking of animation
            if self.direction == "Right":
                self.image = self.WALK_RIGHT[0]
            elif self.direction == "Left":
                self.image = self.WALK_LEFT[0]
            self.movetimer += 1
        elif self.movetimer < 2*ONEFRAME: 
            if self.direction == "Right":
                self.image = self.WALK_RIGHT[1]
            elif self.direction == "Left":
                self.image = self.WALK_LEFT[1]
            self.movetimer += 1
        elif self.movetimer < 3*ONEFRAME:
            if self.direction == "Right":
                self.image = self.WALK_RIGHT[2]
            elif self.direction == "Left":
                self.image = self.WALK_LEFT[2]
            self.movetimer += 1
        elif self.movetimer < 4*ONEFRAME:
            if self.direction == "Right":
                self.image = self.WALK_RIGHT[3]
            elif self.direction == "Left":
                self.image = self.WALK_LEFT[3]
            self.movetimer += 1
        else:
            self.movetimer = 0

    # Determines which running animation to load.
    def whichRun(self):
        if self.runtimer < ONEFRAME:
            if self.direction == "Right":
                self.image = self.RUNN_RIGHT[0]
            elif self.direction == "Left":
                self.image = self.RUNN_LEFT[0]
            self.runtimer += 1
        elif self.runtimer < 2*ONEFRAME: 
            if self.direction == "Right":
                self.image = self.RUNN_RIGHT[1]
            elif self.direction == "Left":
                self.image = self.RUNN_LEFT[1]
            self.runtimer += 1
        elif self.runtimer < 3*ONEFRAME:
            if self.direction == "Right":
                self.image = self.RUNN_RIGHT[2]
            elif self.direction == "Left":
                self.image = self.RUNN_LEFT[2]
            self.runtimer += 1
        #elif self.runtimer < 4*ONEFRAME:
        #    #self.loadImage(RUNN4)
        #    if self.direction == "Right":
        #        self.image = self.RUNN_RIGHT[3]
        #    elif self.direction == "Left":
        #        self.image = self.RUNN_LEFT[3]
        #    #self.loadImage(self.RUNN[3])
        #    self.runtimer += 1
        else:
            self.runtimer = 0
    def whichIdle(self):
        if self.direction == "Right":
            self.image = self.IDLE_RIGHT
        elif self.direction == "Left":
            self.image = self.IDLE_LEFT

    def whichJump(self):
        if self.direction == "Right":
            self.image = self.JUMP_RIGHT
        elif self.direction == "Left":
            self.image = self.JUMP_LEFT

    def whichFall(self):
        if self.direction == "Right":
            self.image = self.FALL_RIGHT
        elif self.direction == "Left":
            self.image = self.FALL_LEFT

    def whichSlide(self):
        if self.contact_side == "Right":
            self.image = self.SLID_RIGHT
        elif self.contact_side == "Left":
            self.image = self.SLID_LEFT


    ## Takes in state and loads the appropriate image.
    #def loadImage(self, state):
    #    if self.direction == "Right":
    #        #self.image = self.load_image(state)
    #        self.image = state
    #    elif self.direction == "Left":
    #        #self.image = pygame.transform.flip(self.load_image(state), True, False)
    #        self.image = pygame.transform.flip(state,True,False)

        
