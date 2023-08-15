import pygame
from pygame.locals import *
import random
import time
from datetime import datetime



def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Triple Letter Speed')
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    # Prepare opening text
    font = pygame.font.Font(None, 36)
    font.set_bold(False)
    drawInstructions(background, font, screen)
    drawCenteredText("Press the A key on the keyboard to begin", background, font, screen.get_size()[1]-80, screen)

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
    timeBetweenTurns = 3

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
                    letters = updateLetters()
                    print(letters[0] + " " + letters[1] + " " + letters[2])
                    letters = grandReset(background, BACKGROUNDCOLOR, screen, letters, font)
                    gameGoing = True
                    timeBetweenTurns = 3
                    playerHealthColor = [0,0,255]
                    enemyHealthColor = [0,0,255]
                    turnStartTime = datetime.now().timestamp()
                    score = 0
                    pygame.display.flip()


                    # Sets the first set of letters
                    letters = turnReset(background, screen, font)
                    screen.blit(background, (0,0))
                    pygame.display.flip()
                    

                # Updates Health Values based on button pressed
                elif(not(letters[0] == " ")):
                    print(letters[0] + " " + letters[1] + " " + letters[2])

                    if(keyboardState[ord(letters[0])+32] and (not(lettersPressed[0]))):
                        lettersPressed[0] = True
                        letterCover1 = font.render("—", 9, (180, 180, 180))
                        letterCover1Pos = Rect(screen.get_width()/2-10, screen.get_height()-82, 30, 40)
                        background.blit(letterCover1, letterCover1Pos)
                        screen.blit(background, (0,0))
                        print("letter 1 pressed")
                        pygame.display.flip()

                    elif(keyboardState[ord(letters[1])+32] and (not(lettersPressed[1]))):
                        lettersPressed[1] = True
                        letterCover2 = font.render("—", 9, (180, 180, 180))
                        letterCover2Pos = Rect(screen.get_width()/2+15, screen.get_height()-82, 30, 40)
                        background.blit(letterCover2, letterCover2Pos)
                        screen.blit(background, (0,0))
                        print("letter 2 pressed")
                        pygame.display.flip()

                    elif(keyboardState[ord(letters[2])+32] and (not(lettersPressed[2]))):
                        lettersPressed[2] = True
                        letterCover3 = font.render("—", 9, (180, 180, 180))
                        letterCover3Pos = Rect(screen.get_width()/2+40, screen.get_height()-82, 30, 40)
                        background.blit(letterCover3, letterCover3Pos)
                        screen.blit(background, (0,0))
                        print("letter 3 pressed")
                        pygame.display.flip()

                    else:
                        turnPassed = False
                        FailedSymbol = font.render("Turn Failed", 9, (255, 30, 30))
                        FailedSymbolPos = Rect(screen.get_width()/2-60, screen.get_height()-122, 30, 40)
                        background.blit(FailedSymbol, FailedSymbolPos)
                        screen.blit(background, (0,0))
                        pygame.display.flip()
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
                        timeBetweenTurns = timeBetweenTurns * 0.85
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
                        temp = text3.get_rect()
                        textpos3 = Rect(0, temp2[1]-80, temp.w, temp.h)
                        textpos3.centerx = centerXPos
                        background.blit(text3, textpos3)
                        background.blit(text4, textpos4)
                        background.blit(text5, textpos5)
                        screen.blit(background, (0, 0))
                        pygame.display.flip()

                if(gameGoing):
                    print("turn run")
                    letters = updateLetters()
                    lettersPressed = resetPressed()
                    turnPassed = True
                    letters = turnReset(background, screen, font)
                    try:
                        FailedSymbol.fill(BACKGROUNDCOLOR)
                        background.blit(FailedSymbol, FailedSymbolPos)
                    except: 
                        print("No mess up yet")
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    turnStartTime = datetime.now().timestamp()
                    turnPassed = True
                
                print(letters[0] + " " + letters[1] + " " + letters[2])
        elif((not gameGoing)):
            keyboardState = pygame.key.get_pressed()
            if(keyboardState[65+32]):
                letters = updateLetters()
                print("got here")
                print(letters[0] + " " + letters[1] + " " + letters[2])
                letters = grandReset(background, BACKGROUNDCOLOR, screen, letters, font)
                gameGoing = True
                opening = False
                timeBetweenTurns = 3
                turnStartTime = datetime.now().timestamp()
                score = 0
                playerHealthPos.height = screen.get_size()[1]//255*255
                enemyHealthPos.height = screen.get_size()[1]//255*255

                playerHealthColor = [0,0,255]
                enemyHealthColor = [0,0,255]
                pygame.display.flip()


            
        
        #background.blit(text3, textpos3)


# Returns the inputted box but shorter 
def updateHealth(background, surface, box, change, color, screenHeight):
    temp = Rect(box.left, box.top, box.w, box.h-change*(screenHeight//255))
    pygame.draw.rect(background, color, box)
    background.blit(surface, temp)
    return temp

def resetHealth(background, surface, box, screenHeight):
    temp = Rect(box.left, box.top, box.w, (screenHeight//255*255))
    pygame.draw.rect(background, [0, 0, 255], box)
    background.blit(surface, temp)
    return temp

def updateLetters():
    temp = [" ", " ", " "]
    temp[0] = chr(random.randrange(65, 91))
    temp[1] = chr(random.randrange(65, 91))
    temp[2] = chr(random.randrange(65, 91))
    print("reset letters")
    return temp  

def resetPressed():
    return [False, False, False]

def end(gameState):
    print("game ended")
    return False

def grandReset(background, BACKGROUNDCOLOR, screen, letters, font):
    drawInstructions(background, font, screen)
    background.fill(BACKGROUNDCOLOR)
    playerHealthPos = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    pygame.draw.rect(background, ((0, 0, 255)), playerHealthPos)
    pygame.draw.rect(background, (0, 0, 255), enemyHealthPos)
    drawCenteredText("Press the " + letters[0] + " " + letters[1] + " " + letters[2] + " keys", background, font, screen.get_size()[1]-80, screen)
    letters = updateLetters()
    screen.blit(background, (0,0))
    return letters

def turnReset(background, screen, font):
    letters = updateLetters()
    print(letters[0] + " " + letters[1] + " " + letters[2])
    drawCenteredText("Press the " + letters[0] + " " + letters[1] + " " + letters[2] + " keys", background, font, screen.get_size()[1], screen)
    screen.blit(background, (0, 0))
    return letters

def drawInstructions(background, font, screen):
    drawCenteredText("This is a test of skill and luck", background, font, 0, screen)
    drawCenteredText("You will be given an increasingly smaller amount of time to press 3 buttons in order to attack ", background, font, 40, screen)
    drawCenteredText("Should you fail to press all three, you will lose health", background, font, 80, screen)
    drawCenteredText("You do not need to press them at the same time, just press them", background, font, 120, screen)

def drawCenteredText(text, background, font, height, screen):
    tempText = font.render(text, 1, (180, 180, 180))
    tempTextRect = tempText.get_rect()
    tempTextPos = Rect(0, height, tempTextRect.w, tempTextRect.h)
    centerXPos = background.get_rect().centerx
    tempTextPos.centerx = centerXPos
    background.blit(tempText, tempTextPos)
    screen.blit(background, (0,0))
    
    

# Runs the Game
if __name__ == '__main__': main()