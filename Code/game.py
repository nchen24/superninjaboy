import pygame, sys, os, Player, Wall, Spike, Shard, Shuriken, Spawner, Block
from pygame.locals import *
from Player import *
from Platform import *
from Wall import *
from Spike import *
from Shard import *
from Shuriken import *
from Spawner import *
from Block import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BCK = "../assets/bluesky.gif"
LEV = 9
RES = (1024, 768)

def quit():
    saveHighscores()
    pygame.quit()
    sys.exit(0)

def saveHighscores():
    f  = open("../highscores.txt", "w")
    for i in range(LEV):
        f.write("Best time for level %d is %s seconds.\n" %(i, str(round(bestTimes[i],2))))
        
def levspeftext():
    if i == 0:
        shurikentext = font.render("Shurikens will kill you.  Note that \
they can pass through green, but not gray blocks.", 1, BLACK)
        screen.blit(shurikentext,(25,200))
        spiketext = font.render ("Spikes will also kill you.", 1, BLACK)
        screen.blit(spiketext,(25,450))
        shardtext = font.render ("This is the goal, a piece of a legendary sword!", 1, BLACK)
        screen.blit(shardtext,(450,500))

        shards[0].image = shards[0].IMGS[2] 

    if i == 1:
        jumptext = font.render ("Jumping while sliding down the wall will cause you to wall jump.", 1, BLACK)
        screen.blit(jumptext,(100,100))
    if i == 3:
        sprinttext = font.render("Hint: If you hold down L-Shift, you will sprint, moving twice as fast horizontally!", 1, BLACK)
        screen.blit(sprinttext, (50,100))

    if i == LEV-1:
        shards[0].image = shards[0].IMGS[1]

def genwall(screen, level):
    mapFile = open("../Levels/Level%s.txt" %level, 'r') 
    vc = 0 
    for line in mapFile:
        hc  = 0 
        for character in line:
            if character == "#":
                walls.append(Wall(screen, hc*16, vc*16))
            if character == "X":
                blocks.append(Block(screen,hc*16, vc*16))
            elif character == "^":
                spikes.append(Spike(screen, hc*16, vc*16, "U"))
            elif character == ">":
                spikes.append(Spike(screen, hc*16, vc*16, "R"))
            elif character == "V":
                spikes.append(Spike(screen, hc*16, vc*16, "D"))
            elif character == "<":
                spikes.append(Spike(screen, hc*16, vc*16, "L"))
            elif character == "P":
                pstart.append(hc*16)
                pstart.append(vc*16)
            elif character == "E":
                shards.append(Shard(screen, hc*16, vc*16))
            elif character == "1":
                spawners.append(Spawner(screen, hc*16, vc*16, "U"))
            elif character == "2":
                spawners.append(Spawner(screen, hc*16, vc*16, "R"))
            elif character == "3":
                spawners.append(Spawner(screen, hc*16, vc*16, "D"))
            elif character == "4":
                spawners.append(Spawner(screen, hc*16, vc*16, "L"))
            hc +=1
        vc +=  1

pygame.init()

# Clock stuff
FPS = 60
clock = pygame.time.Clock()
levClock = pygame.time.Clock()

gameover_font = pygame.font.Font(None, 50)
font = pygame.font.Font(None, 36)

screenDimensions = RES 
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Super Ninja Boy!')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = pygame.image.load(BCK)

pygame.mixer.init()
#back_mus = pygame.mixer.Sound("back_mus.wav")
back_mus = pygame.mixer.Sound("../assets/background_music.wav")
finish = pygame.mixer.Sound("../assets/GemCollected.m4a")
back_mus.set_volume(.15)

# The player
pressed = {'Left' : False, 'Right' : False, 'Shift' : False, 'Space' : False}

onPlat = False
isDead = False
onWall = False
frame = pygame.image.load("../assets/frame.gif")
bestTimes = []
for i in range(LEV):
    bestTimes.append(99999)

for i in range(LEV):
    
    LevelComplete = False
    time = 0
    walls  = []
    blocks = []
    spikes = []
    pstart = []
    shards = []
    spawners = []
    genwall(screen, i+1)
    snb = Player(screen, pstart[0], pstart[1])
    while LevelComplete == False:
    #text = gameover_font.render("LEVEL COMPLETE!", 1, (251, 217, 21))
        # time things
        levClock.tick()
        time = time + levClock.get_time()
        time_passed = clock.tick(FPS)

        back_mus.play()

        screen.blit(background, (0,0))
        screen.blit(frame, (16,16))
        levelTime = font.render(str((time - time%10) / 1000.0), 1, (255, 0, 0))
        screen.blit(levelTime, (80, 58))

        levspeftext()

        for w in walls:
            w.draw()

            if w.rect.colliderect(snb.bottom) and (w.floor_active == False or w.floor_active == True)\
                or ((w.rect.colliderect(snb.left) and w.rect.colliderect(snb.bottom)) and (w.wall_active == False or w.wall_active == True))\
                or ((w.rect.colliderect(snb.right) and w.rect.colliderect(snb.bottom)) and (w.wall_active == False or w.wall_active == True)):

                if pressed['Space'] == False:
                    snb.canJump = True

                snb.dy = 0
                snb.jumped = False
                snb.jumptimer = 0
                snb.apex = False
                snb.onplat = True
                w.floor_active = True
                snb.wallJump_Left = False
                snb.wallJump_Right = False
            elif not(w.rect.colliderect(snb.bottom)) and w.floor_active == True:
                w.floor_active = False

            if w.rect.colliderect(snb.top):
                snb.dy = 0
                snb.apex = True

            if w.rect.colliderect(snb.left) and (w.wall_active == False or w.wall_active == True):

                if pressed['Space'] == False:
                    snb.canJump = True

                snb.contact_side = "Left"
                snb.x = (w.x + w.image_w - 1)
                snb.onwall = True
                w.wall_active = True
                snb.wallJump_Left = False
                snb.wallJump_Right = False

            elif w.rect.colliderect(snb.right) and (w.wall_active == False or w.wall_active == True):
                
                if pressed['Space'] == False:
                    snb.canJump = True
                
                snb.contact_side = "Right"
                snb.x = (w.x - snb.image_w + 1)
                snb.onwall = True
                w.wall_active = True
                snb.wallJump_Left = False
                snb.wallJump_Right = False
            elif (not(w.rect.colliderect(snb.right)) and not(w.rect.colliderect(snb.left))):
                w.wall_active = False
    
        onPlat = False
        onWall = False

        for w in walls:
            if w.floor_active == True:
                onPlat = True
            if w.wall_active == True:
                onWall = True
        for b in blocks:
            b.draw()

        if onPlat == False:
            snb.onplat = False
        if onWall == False:
            snb.onwall = False

        if onPlat == False and onWall == False:
            snb.canJump = False

        for s in spikes:
            s.draw()
            if s.rect.colliderect(snb.rect):
                snb.alive = False

        for sp in spawners:
            sp.update()
            for s in sp.shurikens:
                if s.rect.colliderect(snb.rect) and s.active == True:
                    snb.alive = False
                for b in blocks:
                    if s.rect.colliderect(b.rect):
                        s.active = False
    
        for h in shards:
            h.draw()
            if h.rect.colliderect(snb.rect):
                finish.play()
                LevelComplete = True

    
        if snb.alive == False:
            time = 0 
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
                    snb.old_press_time = snb.current_press_time
                    snb.current_press_time = time
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    pressed['Left'] = False
                elif event.key == K_RIGHT:
                    pressed['Right'] = False
                elif event.key == K_LSHIFT:
                    pressed['Shift'] = False
                elif event.key == K_SPACE:
                    pressed['Space'] = False
                    #snb.canJump = True
                    snb.release_time = time
    
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
    #screen.blit(text,(300,250))
    
    #pygame.display.flip()
    
    # Player beat the level
    if(time < bestTimes[i]):
        bestTimes[i] = ((time - time%10) / 1000.0)
quit()

