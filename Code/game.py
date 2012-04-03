import pygame, sys, os, Player, Wall, Spike, Shard
from pygame.locals import *
from Player import *
from Platform import *
from Wall import *
from Spike import *
from Shard import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY = "../assets/sky_background.png"
BCK = "../assets/bluesky.gif"
LEV = 4
RES = (1024, 768)

def quit():
    pygame.quit()
    sys.exit(0)

def genwall(screen, level):
    mapFile = open("../Levels/Level%s.txt" %level, 'r') 
    vc = 0
    hc = 0
    for line in mapFile:
        vc += 1
        hc =  0
        for character in line:
            hc +=1
            if character == "#":
                walls.append(Wall(screen, hc*16, vc*16))
            if character == "^":
                spikes.append(Spike(screen, hc*16, vc*16))
            if character == "P":
                pstart.append(hc*16)
                pstart.append(vc*16)
            if character == "E":
                shards.append(Shard(screen, hc*16, vc*16))

pygame.init()

# Clock stuff
FPS = 60
clock = pygame.time.Clock()

gameover_font = pygame.font.Font(None, 50)

screenDimensions = RES 
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Super Ninja Boy!')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = pygame.image.load(BCK)

# The player
pressed = {'Left' : False, 'Right' : False, 'Shift' : False, 'Space' : False}

onPlat = False
isDead = False
onWall = False

for i in range(LEV):
    LevelComplete = False
    walls  = []
    spikes = []
    pstart = []
    shards = []
    genwall(screen, i+1)
    snb = Player(screen, pstart[0], pstart[1])
    while LevelComplete == False:
        # time things
        time_passed = clock.tick(FPS)

        #screen.fill(WHITE)
        screen.blit(background, (0,0))
    
        for w in walls:
            w.draw()

            if w.rect.colliderect(snb.bottom) and (w.floor_active == False or w.floor_active == True):
                snb.dy = 0
                snb.jumped = False
                snb.jumptimer = 0
                snb.apex = False
                snb.onplat = True
                w.floor_active = True
            elif not(w.rect.colliderect(snb.bottom)) and w.floor_active == True:
                w.floor_active = False
    
            if w.rect.colliderect(snb.left) and (w.wall_active == False or w.wall_active == True):
                snb.contact_side = "Left"
                snb.x = (w.x + w.image_w - 1)
                snb.onwall = True
                w.wall_active = True
            elif w.rect.colliderect(snb.right) and (w.wall_active == False or w.wall_active == True):
                snb.contact_side = "Right"
                snb.x = (w.x - snb.image_w + 1)
                snb.onwall = True
                w.wall_active = True
            elif (not(w.rect.colliderect(snb.right)) and not(w.rect.colliderect(snb.left))):
                w.wall_active = False
    

        onPlat = False
        onWall = False

        if snb.onwall == True:
            print("sliding")
        else:
            print("standing/falling")
        if snb.onplat == True:
            print("on dat plat")
        else:
            print("tha plat ain't thea")


        for w in walls:
            if w.floor_active == True:
                onPlat = True
            if w.wall_active == True:
                onWall = True

        if onPlat == False:
            snb.onplat = False
        if onWall == False:
            snb.onwall = False

        for s in spikes:
            s.draw()
            if s.rect.colliderect(snb.rect):
                snb.alive = False
    
        for h in shards:
            h.draw()
            if h.rect.colliderect(snb.rect):
                LevelComplete = True
    
        if snb.alive == False:
            snb.respawn(pstart[0], pstart[1])
    
        snb.update(pressed, screenDimensions)
        snb.draw()
    
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_LEFT:
                    pressed['Left'] = True
                elif event.key == K_RIGHT:
                    pressed['Right'] = True
                elif event.key == K_LSHIFT:
                    pressed['Shift'] = True
                elif event.key == K_SPACE:
                    pressed['Space'] = True
                    snb.jumped = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    pressed['Left'] = False
                elif event.key == K_RIGHT:
                    pressed['Right'] = False
                elif event.key == K_LSHIFT:
                    pressed['Shift'] = False
                elif event.key == K_SPACE:
                    pressed['Space'] = False
                    snb.canJump = True
    
        # Handles end-level actions
    
    #for event in pygame.event.get():
    #
    #    if event.type == KEYDOWN:
    #        if event.key == K_ESCAPE:
    #            quit()
    #
    #screen.fill((15,183,232))
    #
    ## Game over text
    #text = gameover_font.render("LEVEL COMPLETE!", 1, (251, 217, 21))
    #screen.blit(text,(300,250))
    
    #pygame.display.flip()
