import pygame, os, sys, Spritesheet
from pygame.locals import *
from Spritesheet import *

###############################
# Constants for image loading #
###############################
SS = "../assets/player_standard.png"

IDLE_L = (0,25,18,23)
FALL_L = (180,25,18,23) 
JUMP_L = (160,25,18,23)
WALK_L = ((20,25,18,23),(40,25,18,23),(60,25,18,23),(80,25,18,23))
RUNN_L = ((100,25,18,23),(120,25,18,23),(140,25,18,23))
SLID_L = (200,25,18,23)

IDLE_R = (0,0,18,23)
FALL_R = (180,0,18,23)
JUMP_R = (160,0,18,23)
WALK_R = ((20,0,18,23),(40,0,18,23),(60,0,18,23),(80,0,18,23)) 
RUNN_R = ((100,0,18,23),(120,0,18,23),(140,0,18,23))
SLID_R = (200,0,18,23)

###################
# Other constants #
###################
ONEFRAME = 11
JUMPLIMIT = 50
SPRINTMOD = 2
RES = (1024, 768)

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
        self.WALK_RIGHT = self.ss.images_at(WALK_R, colorkey = -1)
        self.WALK_LEFT  = self.ss.images_at(WALK_L, colorkey = -1)

        self.RUNN_RIGHT = self.ss.images_at(RUNN_R, colorkey = -1)
        self.RUNN_LEFT  = self.ss.images_at(RUNN_L, colorkey = -1)

        self.JUMP_RIGHT = self.ss.image_at(JUMP_R,  colorkey = -1)
        self.JUMP_LEFT  = self.ss.image_at(JUMP_L,  colorkey = -1)

        self.IDLE_RIGHT = self.ss.image_at(IDLE_R,  colorkey = -1)
        self.IDLE_LEFT  = self.ss.image_at(IDLE_L,  colorkey = -1)
        
        self.FALL_RIGHT = self.ss.image_at(FALL_R,  colorkey = -1)
        self.FALL_LEFT  = self.ss.image_at(FALL_L,  colorkey = -1)

        self.SLID_RIGHT = self.ss.image_at(SLID_R,  colorkey = -1)
        self.SLID_LEFT  = self.ss.image_at(SLID_L,  colorkey = -1)

        self.direction = "Right"
        self.whichIdle()

        self.screen = screen
        self.x   = x
        self.y   = y
        self.dx  = 0
        self.dy  = 0

        self.ddx = .5
        self.ddy = 0

        self.dx_max = 2
        self.dy_max = 2

        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.bottom = pygame.Rect((self.x + 7,(self.y + self.image_h - 14)), (self.image_w - 4, 5))

        # pygame.Rect takes ((start_x, start_y), (width, height))[EXPERIMENTAL]
        self.boundwidth = 2
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
        self.wallJump_Left = False
        self.wallJump_Right = False

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self, pressed, screenDimensions):

        if self.x < 0 or self.x > RES[0] or self.y < 0 or self.y > RES[1]:
            self.alive = False

        if pressed['Space'] == True and not(self.jumped) and not(self.apex) and self.canJump == True:
            if self.jumptimer > JUMPLIMIT:
                self.apex = True
                self.canJump = False
                self.wallJump_Left = False
                self.wallJump_Right = False
            else:
                self.jumptimer += 1

            self.whichJump()
            self.dy = -2

            if self.onplat == True:
                print("on dat plat")

            if self.wallJump_Left == True and self.onplat == False:
                self.x += -2
            elif self.wallJump_Right == True and self.onplat == False:
                self.x += 2
                print("Go Right!")

            self.onplat = False

        elif self.onplat == False and self.onwall == False:
            self.whichFall()
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

        #HANDLES JUMPING OFF OF A WALL
        if self.onwall == True and self.onplat == False:

            if self.contact_side == "Left" and pressed['Right']:
                self.dx = 2

            elif self.contact_side == "Right" and pressed['Left']:
                self.dx = -2

            elif self.contact_side == "Left" and pressed['Space'] and not(self.jumped) and not(self.apex) and self.canJump == True:
                self.direction = "Right"
                self.onplat = False
                if self.jumptimer > JUMPLIMIT:
                    self.apex = True
                    self.canJump = False
                else:
                    self.jumptimer += 1

                self.image = self.JUMP_RIGHT
                self.dy = -2
                self.dx = 2
                self.wallJump_Right = True

            elif self.contact_side == "Right" and pressed['Space'] and not(self.jumped) and not(self.apex) and self.canJump == True:
                self.direction = "Left"
                self.onplat = False
                if self.jumptimer > JUMPLIMIT:
                    self.apex = True
                    self.canJump = False
                else:
                    self.jumptimer += 1

                self.image = self.JUMP_LEFT
                self.dy = -2
                self.dx = -2
                self.wallJump_LEFT = True

            else:
                self.whichSlide()
                self.dy = 1.5
                self.dx = 0
                self.jumped = False
                self.apex = False
                self.jumptimer = 0
                self.canJump = True


        # Move the bounding box
        self.image_w, self.image_h = self.image.get_size()
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
        self.bottom = pygame.Rect((self.x+5,(self.y + self.image_h - 5)), (self.image_w-10, 5))

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

        
