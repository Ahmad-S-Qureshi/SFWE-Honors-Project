import pygame
from pygame.locals import *
import random
import time
from datetime import datetime



def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption('Triple Letter Speed')
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    # Prepare first line of opening text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello there, this is a test of skill and luck", 1, (180, 180, 180))
    textpos = text.get_rect()

    # Prepare second line of opening text
    text2 = font.render("You will be given an increasingly smaller amount of time to press 3 buttons in order to attack ", 1, (180, 180, 180))
    temp = text2.get_rect()
    textpos2 = Rect(0, 40, temp.w, temp.h)

    # Prepare third line of opening text
    text3 = font.render("Press the A key on the keyboard to begin", 1, (180, 180, 180))
    temp = text3.get_rect()
    temp2 = screen.get_size()
    textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)

    # Prepare fourth line of opening text
    text4 = font.render("Should you fail to press all three, you will lose health", 1, (180, 180, 180))
    temp = text4.get_rect()
    textpos4 = Rect(0, 80, temp.w, temp.h)

    # Display Opening Text
    centerXPos = background.get_rect().centerx

    textpos.centerx = centerXPos
    textpos2.centerx = centerXPos
    textpos3.centerx = centerXPos
    textpos4.centerx = centerXPos

    background.blit(text, textpos)
    background.blit(text2, textpos2)
    background.blit(text3, textpos3)
    background.blit(text4, textpos4)

    # Prepare rectangle for playerhealth
    playerHealthPos = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    playerHealthColor = [0, 0, 255]
    BASEPLAYERPOS = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    BACKGROUNDCOLOR = (0,0,20)

    # Prepare rectangle for enemy health
    enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    enemyHealthColor = [0, 0, 255]
    BASEENEMYPOS = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    BACKGROUNDCOLOR = (0,0,20)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.key.set_repeat()
    timeBetweenTurns = 4

    # Event loop
    opening = True
    lettersPressed = [False, False, False]
    turnPassed = True
    letters = [" ", " ", " "]
    turnStartTime = datetime.now().timestamp()
    gameGoing = True
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and gameGoing:
                keyboardState = pygame.key.get_pressed()
                #print(datetime.now().timestamp())
                if(keyboardState[127]):
                    return

                # Runs on the first button press and sets up the background and whatnot, also changes the flag of opening to false
                elif(opening and keyboardState[65+32]):
                    opening = False
                    print("opening")
                    background.fill(BACKGROUNDCOLOR)
                    pygame.draw.rect(background, ((0, 0, 255)), playerHealthPos)
                    pygame.draw.rect(background, (0, 0, 255), enemyHealthPos)
                    opening = False
                    letters = [" ", " ", " "]


                    # Sets the first set of letters
                    letters = updateLetters(letters)
                    print(letters[0] + " " + letters[1] + " " + letters[2])
                    pygame.draw.rect(background, BACKGROUNDCOLOR,textpos3)
                    text3 = font.render("Press the " + letters[0] + " " + letters[1] + " " + letters[2] + " keys", 1, (180, 180, 180))
                    temp = text3.get_rect()
                    textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)
                    textpos3.centerx = centerXPos
                    background.blit(text3, textpos3)
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    

                # Updates Health Values based on button pressed
                elif(not(letters[0] == " ")):
                    print(letters[0] + " " + letters[1] + " " + letters[2])

                    if(keyboardState[ord(letters[0])+32] and (not(lettersPressed[0]))):
                        lettersPressed[0] = True
                        print("letter 1 pressed")

                    elif(keyboardState[ord(letters[1])+32] and (not(lettersPressed[1]))):
                        lettersPressed[1] = True
                        print("letter 2 pressed")

                    elif(keyboardState[ord(letters[2])+32] and (not(lettersPressed[2]))):
                        lettersPressed[2] = True
                        print("letter 3 pressed")

                    else:
                        turnPassed = False
                        print("Turn Failed")
                        
                    
        # Waits for the delay between moves to elapse and updates time before the next attack
        if(not(opening) and (gameGoing)):
            # Runs turn timer
            if(turnStartTime + timeBetweenTurns < datetime.now().timestamp()):
                if(lettersPressed[0] and lettersPressed[1] and lettersPressed[2] and turnPassed):
                    if(enemyHealthColor[2]-40 >0):
                        enemyHealthPos = updateHealth(screen, background, enemyHealthPos, 40, BACKGROUNDCOLOR, screen.get_size()[1])
                        pygame.draw.rect(background, BACKGROUNDCOLOR, BASEENEMYPOS)
                        enemyHealthColor = [enemyHealthColor[0]+40, 0, enemyHealthColor[2]-40]
                    else:
                        enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
                        enemyHealthColor = [0, 0, 255]
                        timeBetweenTurns = timeBetweenTurns * 0.7
                    pygame.draw.rect(background, enemyHealthColor, enemyHealthPos)
                    score = score + 1
                    print("enemy hurt")
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    
                else:
                    if(playerHealthColor[2] - 15 > 0):
                        playerHealthPos = updateHealth(screen, background, playerHealthPos, 15, BACKGROUNDCOLOR, screen.get_size()[1])
                        pygame.draw.rect(background, BACKGROUNDCOLOR, BASEPLAYERPOS)
                        playerHealthColor = [playerHealthColor[0]+15, 0, playerHealthColor[2]-15]
                        pygame.draw.rect(background, playerHealthColor, playerHealthPos)
                        print("player hurt")
                        pygame.display.flip()
                    else:
                        gameGoing = end(gameGoing)
                        print(str(playerHealthColor[2]))
                        background.fill((30, 30, 30))
                        background.blit(text, textpos)
                        background.blit(text2, textpos2)
                        text3 = font.render("Your score was " +str(score) +" press A to play again", 1, (180, 180, 180))
                        background.blit(text3, textpos3)
                        background.blit(text4, textpos4)
                        screen.blit(background, (0, 0))
                        pygame.display.flip()

                if(gameGoing):
                    print("turn run")
                    letters = updateLetters(letters)
                    lettersPressed = resetPressed()
                    turnPassed = True
                    pygame.draw.rect(background, BACKGROUNDCOLOR,textpos3)
                    text3 = font.render("Press the " + letters[0] + " " + letters[1] + " " + letters[2] + " keys", 1, (180, 180, 180))
                    temp = text3.get_rect()
                    textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)
                    textpos3.centerx = centerXPos
                    background.blit(text3, textpos3)
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    turnStartTime = datetime.now().timestamp()
                    turnPassed = True
                
                print(letters[0] + " " + letters[1] + " " + letters[2])
        elif((not gameGoing)):
            keyboardState = pygame.key.get_pressed()
            if(keyboardState[65+32]):
                background.fill(BACKGROUNDCOLOR)
                playerHealthPos = Rect(30, 30, 30, screen.get_size()[1]//255*255)
                enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
                playerHealthColor = [0, 0, 255]
                enemyHealthColor = [0, 0 , 255]
                pygame.draw.rect(background, ((0, 0, 255)), playerHealthPos)
                pygame.draw.rect(background, (0, 0, 255), enemyHealthPos)
                gameGoing = True
                # Sets the first set of letters
                letters = updateLetters(letters)
                print(letters[0] + " " + letters[1] + " " + letters[2])
                pygame.draw.rect(background, BACKGROUNDCOLOR,textpos3)
                text3 = font.render("Press the " + letters[0] + " " + letters[1] + " " + letters[2] + " keys", 1, (180, 180, 180))
                temp = text3.get_rect()
                textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)
                textpos3.centerx = centerXPos
                background.blit(text3, textpos3)
                screen.blit(background, (0, 0))
                timeBetweenTurns = 4
                turnStartTime = datetime.now().timestamp()
                pygame.display.flip()
                score=0;   
            

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

def updateLetters(letters):
    temp = [" ", " ", " "]
    temp[0] = chr(random.randrange(65, 91))
    temp[1] = chr(random.randrange(65, 91))
    temp[2] = chr(random.randrange(65, 91))
    print(temp[0])
    return temp  

def resetPressed():
    return [False, False, False]

def end(gameState):
    print("game ended")
    return False


# Runs the Game
if __name__ == '__main__': main()