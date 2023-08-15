import pygame
from pygame.locals import *
import random
import time
from datetime import datetime


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Basic Pygame program')
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    # Prepare first line of opening text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello there, this is a test of skill and luck", 1, (180, 180, 180))
    textpos = text.get_rect()

    # Prepare second line of opening text
    text2 = font.render("You will be given an increasingly smaller amount of time to press 3 buttons Press the buttons simulateously when the timer expires to attack Should you fail to press all three, you will lose health", 1, (180, 180, 180))
    temp = text2.get_rect()
    textpos2 = Rect(0, 40, temp.w, temp.h)

    # Prepare third line of opening text
    text3 = font.render("Press the delete key on the keyboard to begin", 1, (180, 180, 180))
    temp = text3.get_rect()
    temp2 = screen.get_size()
    textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)

    # Display Opening Text
    centerXPos = background.get_rect().centerx

    textpos.centerx = centerXPos
    textpos2.centerx = centerXPos
    textpos3.centerx = centerXPos

    background.blit(text, textpos)
    background.blit(text2, textpos2)
    background.blit(text3, textpos3)

    # Prepare rectangle for playerhealth
    playerHealthPos = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    playerHealthColor = (0, 0, 255)
    BASEPLAYERPOS = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    BACKGROUNDCOLOR = (0,0,20)

    # Prepare rectangle for enemy health
    enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    enemyHealthColor = (0, 0, 255)
    BASEENEMYPOS = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    BACKGROUNDCOLOR = (0,0,20)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.key.set_repeat()
    timeDelay = 4

    # Event loop
    opening = True
    timerGoing = False
    letter1Pressed = True
    letter2Pressed = True
    letter3Pressed = True
    turnFailed = False
    loopRun = False
    curr_dt = datetime.now()
    looptimestamp = int(round(curr_dt.timestamp()))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and timerGoing == False:
                keyboardState = pygame.key.get_pressed()
                if(keyboardState[127]):
                    return
                
                # Runs on the first button press and sets up the background and whatnot, also changes the flag of opening to false
                if(opening):
                    background.fill(BACKGROUNDCOLOR)
                    pygame.draw.rect(background, ((0, 0, 255)), playerHealthPos)
                    opening = False

                    # Sets the first set of letters
                    pygame.draw.rect(background, BACKGROUNDCOLOR,textpos3)
                    text3 = font.render("Press the " + letter1 + " " + letter2 + " " + letter3 + " keys", 1, (180, 180, 180))
                    temp = text3.get_rect()
                    textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)
                    textpos3.centerx = centerXPos
                    background.blit(text3, textpos3)
                    

                # Updates Health Values based on button pressed
                if(not(loopRun)):
                    if(not(not(timerGoing) and letter1Pressed and letter2Pressed and letter3Pressed)):
                        playerHealthPos = updateHealth(screen, background, playerHealthPos, 15, BACKGROUNDCOLOR, screen.get_size()[1])
                        pygame.draw.rect(background, BACKGROUNDCOLOR, BASEPLAYERPOS)
                        pygame.draw.rect(background, playerHealthColor, playerHealthPos)
                        if playerHealthColor[2]-15 > 0:
                            playerHealthColor = (playerHealthColor[0]+15, playerHealthColor[1], playerHealthColor[2]-15)
                    else:
                        enemyHealthPos = updateHealth(screen, background, enemyHealthPos, 40, BACKGROUNDCOLOR, screen.get_size()[1])
                        pygame.draw.rect(background, BACKGROUNDCOLOR, BASEENEMYPOS)
                        pygame.draw.rect(background, enemyHealthColor, enemyHealthPos)
                        # Updates color to be more red and less green as health goes down
                        if enemyHealthColor[2]-40>0:
                            enemyHealthColor = (enemyHealthColor[0]+40, enemyHealthColor[1], enemyHealthColor[2]-40)
                        else:
                            # Gives the user less time to prepare attacks and resets enemy 
                            enemyHealthColor = (0, 0, 255)
                            timeDelay = timeDelay * 4 / 5
                            enemyHealthPos = resetHealth(screen, background, enemyHealthPos, BACKGROUNDCOLOR, screen.get_size()[1])
                            pygame.draw.rect(background, BACKGROUNDCOLOR, BASEENEMYPOS)
                            pygame.draw.rect(background, enemyHealthColor, enemyHealthPos)
                    loopRun = True

                

                
            elif timerGoing == True and event.type == KEYDOWN:
                keyboardState = pygame.key.get_pressed()
                print("running")
                if(keyboardState[ord(letter1)]):
                    letter1Pressed = True
                elif(keyboardState[ord(letter2)]):
                    letter2Pressed = True
                elif(keyboardState[ord(letter3)]):
                    letter3Pressed = True
            screen.blit(background, (0, 0))
            pygame.display.flip()


                
        # Updates screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Chooses random letters for user to press 
        letter1 = chr(random.randrange(65, 91))
        letter2 = chr(random.randrange(65, 91))
        letter3 = chr(random.randrange(65, 91))
        letter1Pressed = False
        letter2Pressed = False
        letter3Pressed = False
        
        # Waits for the delay between moves to elapse and updates time before the next attack
        timeLeft = timeDelay
        if(not(opening)):
            timerGoing = True
            while(timeLeft > 0):
                timeLeft -= 0.1
                time.sleep(0.1)
            timerGoing = False
            tempTimeConstructor = datetime.now()
            looptimestamp = tempTimeConstructor.timestamp()
            pygame.draw.rect(background, BACKGROUNDCOLOR,textpos3)
            text3 = font.render("Press the " + letter1 + " " + letter2 + " " + letter3 + " keys", 1, (180, 180, 180))
            temp = text3.get_rect()
            textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)
            textpos3.centerx = centerXPos
            background.blit(text3, textpos3)

        background.blit(text3, textpos3)


# Returns the inputted box but shorter 
def updateHealth(background, surface, box, change, color, screenHeight):
    temp = Rect(box.left, box.top, box.w, box.h-change*(screenHeight//255))
    pygame.draw.rect(background, color, box)
    background.blit(surface, temp)
    return temp

def resetHealth(background, surface, box, color, screenHeight):
    temp = Rect(box.left, box.top, box.w, (screenHeight//255*255))
    pygame.draw.rect(background, color, box)
    background.blit(surface, temp)
    return temp


# Runs the Game
if __name__ == '__main__': main()