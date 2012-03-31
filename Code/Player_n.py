import pygame, spritesheet, os, sys
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


###################
# Other constants #
###################
ONEFRAME  = 20
JUMPLIMIT = 100
SPRINTMOD = 2

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
        self.image = self.load_image(IDLE1)
        self.screen = screen
        self.x   = x
        self.y   = y
        self.dx  = 0
        self.dy  = 0
        self.ddx = .1
        self.ddy = 0
        self.dx_max = .8
        self.dy_max = .8
        self.image_w, self.image_h = self.image.get_size()
        self.ss = spritesheet.spritesheet("../assets/sprite_sheet_colors_fixed.png")

        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.bottom = pygame.Rect((self.x,(self.y + self.image_h - 5)), (self.image_w, 5))

        # pygame.Rect takes ((start_x, start_y), (width, height))[EXPERIMENTAL]
        self.boundwidth = 5
        self.left = pygame.Rect((self.x, self.y), (self.boundwidth, self.image_h))
        self.right = pygame.Rect((self.x + self.image_w - self.boundwidth, self.y), (self.boundwidth, self.image_h))

        self.alive = True
        self.jumped = False
        self.apex = False # True if the player has reached the max jump height
        self.jumptimer = 0
        self.direction = "Right"
        self.movetimer = 0
        self.runtimer  = 0
        self.onplat = False

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self, pressed, screenDimensions):
        if pressed['Space'] == True and not(self.jumped) and not(self.apex):
            if self.jumptimer > JUMPLIMIT:
                self.apex = True
            else:
                self.jumptimer += 1

            self.loadImage(JUMP1)
            self.dy = -.8

        elif self.rect.bottomright[1] < screenDimensions[1] and self.onplat == False:
            self.loadImage(FALL1)
            self.dy = .8
        else:
            self.loadImage(IDLE1)
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

        self.bottom = pygame.Rect((self.x,(self.y + self.image_h - 5)), (self.image_w, 5))

    # Determines which walking animation to load.
    def whichWalk(self):
        if self.movetimer < ONEFRAME: # ONEFRAME is defined in constants.  This
            xmage = self.ss.image_at((0,0,9,23), colorkey = (255,255,255))
            self.image = xmage
            #self.loadImage(WALK1)     # allows for easy tweaking of animation
            if self.direction == "Right":
                self.image = xmage
            elif self.direction == "Left":
                self.image = pygame.transform.flip(xmage, True, False)
            self.movetimer += 1
        elif self.movetimer < 2*ONEFRAME: 
            self.loadImage(WALK2)
            self.movetimer += 1
        elif self.movetimer < 3*ONEFRAME:
            self.loadImage(WALK3)
            self.movetimer += 1
        elif self.movetimer < 4*ONEFRAME:
            self.loadImage(WALK4)
            self.movetimer += 1
        else:
            self.movetimer = 0

    # Determines which running animation to load.
    def whichRun(self):
        if self.runtimer < ONEFRAME:
            self.loadImage(RUNN1)
            self.runtimer += 1
        elif self.runtimer < 2*ONEFRAME: 
            self.loadImage(RUNN2)
            self.runtimer += 1
        elif self.runtimer < 3*ONEFRAME:
            self.loadImage(RUNN3)
            self.runtimer += 1
        elif self.runtimer < 4*ONEFRAME:
            self.loadImage(RUNN4)
            self.runtimer += 1
        else:
            self.runtimer = 0

    # Takes in state and loads the appropriate image.
    def loadImage(self, state):
        if self.direction == "Right":
            self.image = self.load_image(state)
        elif self.direction == "Left":
            self.image = pygame.transform.flip(self.load_image(state), True, False)

        
