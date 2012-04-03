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
PLAT1 = "../assets/platform1-2.gif"
PLAT2 = "../assets/platform1-3.gif"
SKY = "../assets/sky_background.png"
BCK = "../assets/bluesky.png"

def quit():
    pygame.quit()
    sys.exit(0)

walls = []
spikes = []
pstart = []
shards = []

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

screenDimensions = (1024, 768)
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Super Ninja Boy!')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
#background = pygame.image.load(SKY)

# The player
pressed = {'Left' : False, 'Right' : False, 'Shift' : False, 'Space' : False}
plat1 = Platform(screen, PLAT1, 400, 650)
plat2 = Platform(screen, PLAT2, 600, 600)
plat3 = Platform(screen, PLAT2, 100, 600)

onPlat = False
isDead = False

genwall(screen, 2)
snb = Player(screen, pstart[0], pstart[1])

LevelComplete = False

while True:
    if LevelComplete == False:
        # time things
        time_passed = clock.tick(FPS)

        screen.fill(WHITE)
        #screen.blit(background, (0,0))

        for w in walls:
            w.draw()
            if w.rect.colliderect(snb.bottom) and (w.active == False or w.active == True):
                snb.dy = 0
                snb.jumped = False
                snb.jumptimer = 0
                snb.apex = False
                snb.onplat = True
                w.active = True
                #print("activated")
            elif not(w.rect.colliderect(snb.bottom)) and w.active == True:
                w.active = False

            if w.rect.colliderect(snb.left):
                snb.contact_side = "Left"
                snb.x = (w.x + w.image_w)

            if w.rect.colliderect(snb.right):
                snb.contact_side = "Right"
                snb.x = (w.x - snb.image_w)

        onPlat = False
        for w in walls:
            if w.active == True:
                onPlat = True
        if onPlat == False:
            snb.onplat = False

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

    if LevelComplete == True:

        # Handles end-level actions

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()

        screen.fill((15,183,232))

        # Game over text
        text = gameover_font.render("LEVEL COMPLETE!", 1, (251, 217, 21))
        screen.blit(text,(300,250))

        # Final score text
        #final_score_text = final_score_font.render("FINAL SCORE: " + str(score), 1, (61, 255, 255))
        #screen.blit(final_score_text,(300,300))

        pygame.display.flip()
