import pygame
import thorpy as tp
import pygame_gui
import math
from sprites import Hoop, CollideRect, Ball, Spike

pygame.init()
pygame.display.set_caption('Ballz in Hoopz')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
balltime = 0
shoot = False
balldiameter = 80
thetai = 35
pullDistance = 0
collide = False
collide2 = False
bruh = 0
scored = False
shotsMade = 0
specialTime = 0
shotTaken = False
gameStarted = False
gameOver = False
missed = False
shotMade = False

specials = ['Normal', 'Bouncy']
special = 'Normal'
gameMode = 'Streak'
timeLeft = 10

def setPosHoop(x, y):
    hoop.rect.x = x
    hoop.rect.y = y

    hoopCollisionLeft.rect.x = x + 2
    hoopCollisionLeft.rect.y = y + 2

    hoopCollisionRight.rect.x = x + 140 - 12
    hoopCollisionRight.rect.y = y + 2

    netCollisionLeft.rect.x = x + 2
    netCollisionLeft.rect.y = y + 12

    netCollisionRight.rect.x = x + 140 - 26
    netCollisionRight.rect.y = y + 12

allSpritesList = pygame.sprite.Group()
collideSprites = pygame.sprite.Group()

hoop = Hoop(140, 140)
hoopCollisionLeft = CollideRect(10, 10, 0)
hoopCollisionRight = CollideRect(10, 10, 0)
netCollisionLeft = CollideRect(10, 140, 5)
netCollisionRight = CollideRect(10, 140, -5)
setPosHoop(screen.get_width() - 140, screen.get_height() / 2)

ball = Ball(balldiameter, balldiameter)
ball.rect.x = screen.get_width() / 4
ball.rect.y = screen.get_height() / 2
startx = screen.get_width() / 4
dragX = screen.get_width() / 4
starty = screen.get_height() / 2
dragY = screen.get_height() / 2
dragging = False

bottomBarrier = CollideRect(screen.get_width(), 10, 0)
bottomBarrier.rect.x = 0
bottomBarrier.rect.y = screen.get_height()
rightBarrier = CollideRect(10, screen.get_height(), 0)
rightBarrier.rect.x = screen.get_width()
rightBarrier.rect.y = 0
leftBarrier = CollideRect(10, screen.get_height(), 0)
leftBarrier.rect.x = -10
leftBarrier.rect.y = 0
topBarrier = CollideRect(screen.get_width(), 10, 0)
topBarrier.rect.x = 0
topBarrier.rect.y = -10

spike1 = Spike()
spike1.rect.x = 700
spike1.rect.y = 360
spike2 = Spike()
spike2.rect.x = 1080
spike2.rect.y = 100

allSpritesList.add(ball)
allSpritesList.add(hoop)
allSpritesList.add(hoopCollisionLeft)
allSpritesList.add(hoopCollisionRight)
allSpritesList.add(netCollisionLeft)
allSpritesList.add(netCollisionRight)
allSpritesList.add(bottomBarrier)
allSpritesList.add(rightBarrier)
allSpritesList.add(leftBarrier)
allSpritesList.add(topBarrier)
allSpritesList.add(spike1)
allSpritesList.add(spike2)

collideSprites.add(hoopCollisionLeft)
collideSprites.add(hoopCollisionRight)
collideSprites.add(netCollisionLeft)
collideSprites.add(netCollisionRight)
collideSprites.add(bottomBarrier)
collideSprites.add(rightBarrier)
collideSprites.add(leftBarrier)
collideSprites.add(topBarrier)

hoopBarriers = [hoopCollisionLeft, hoopCollisionRight]
netBarriers = [netCollisionLeft, netCollisionRight]

def getPos(inputT):
    t = inputT
    i = pullDistance / 10
    iy = i*math.sin((thetai))
    ix = i*math.cos((thetai))
    g = 9.8
    formula = [ix*t, -0.5*g*math.pow(t, 2) + iy*t]

    return formula

manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()), 'theme.json')

scoreText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((90, 35), (300, 50)),
                                            text='Shots Made: 0',
                                            manager=manager)
timeLeftText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((90, 35), (300, 50)),
                                            text='Time Left: 10',
                                            manager=manager)
specialModeButton = pygame_gui.elements.UIDropDownMenu(options_list=["Normal", "Bouncy", "Moving"],
                                                    starting_option="Normal",
                                                    relative_rect=pygame.Rect((490, 35), (300, 50)),
                                                    manager=manager)
gameModeButton = pygame_gui.elements.UIDropDownMenu(options_list=["Streak", "Time Attack"],
                                                    starting_option="Streak",
                                                    relative_rect=pygame.Rect((890, 35), (300, 50)),
                                                    manager=manager)
helpText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 100), (1280, 50)),
                                            text="Press SPACE to shoot, 'R' to reset ball, and BACKSPACE to end game",
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(object_id='#helptext'))
gameEndWindow = pygame_gui.windows.UIMessageWindow(
    rect=pygame.Rect((390, 160), (500, 400)),
    html_message="Game Over! Press BACKSPACE to play again.",
    manager=manager,
    window_title="Game Over!")

gameEndWindow.hide()

while running:
    dt = clock.tick(60)/1000.0
    if gameStarted == True and round(timeLeft) > 0:
        timeLeft -= dt
    timeLeftText.set_text(f'Time Left: {(round(timeLeft))}')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == specialModeButton:
                special = event.text
            elif event.ui_element == gameModeButton:
                gameMode = event.text
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            gameEndWindow = pygame_gui.windows.UIMessageWindow(
                rect=pygame.Rect((390, 160), (500, 400)),
                html_message="Game Over! Press BACKSPACE to play again.",
                manager=manager,
                window_title="Game Over!")
            gameEndWindow.hide()
        
        manager.process_events(event)

    manager.update(dt)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")
    manager.draw_ui(screen)

    if ball.drag() and dragging == False:
        dragging = True

    if pygame.MOUSEMOTION and dragging == True and shotTaken == False:
        dragX = pygame.mouse.get_pos()[0]
        dragY = pygame.mouse.get_pos()[1]
        thetai = math.atan2((dragY - (starty + balldiameter/2)), -(dragX - (startx + balldiameter/2)))
        thetai %= 2*math.pi
        pullDistance = math.sqrt(math.pow((dragX) - (startx + balldiameter/2), 2) + math.pow((dragY) - (starty + balldiameter/2), 2))
        if pullDistance > 250:
            pullDistance = 250

    if pygame.mouse.get_pressed()[0] == 0:
        dragging = False

    if shotTaken == False:
        for x in range(15):
            pygame.draw.circle(screen, (255, 255, 255), (startx + getPos(x/10)[0] * 30 + balldiameter/2, starty + getPos(x/10)[1] * -30 + balldiameter/2), 5)

    allSpritesList.update()
    allSpritesList.draw(screen)
    collideSprites.update()

    if gameMode == "Streak":
        scoreText.show()
        timeLeftText.hide()
    else:
        scoreText.hide()
        timeLeftText.show()

    if specialTime >= 2:
        specialTimeFactor = -1
    elif specialTime <= 0:
        specialTimeFactor = 1

    hoopVelocity = 0
    if special == "Moving":
        setPosHoop(screen.get_width() - 140 - (specialTime / 2 * 300), hoop.rect.y)
        hoopVelocity = -((dt*specialTimeFactor) / 2 * 300)
    else:
        setPosHoop(screen.get_width() - 140, screen.get_height() / 2)

    spike1.rect.y = 540 - (specialTime / 2 * 500)
    spike2.rect.x = 1080 - (specialTime / 2 * 500)

    if gameOver == False and (pygame.sprite.collide_mask(ball, spike1) != None or pygame.sprite.collide_mask(ball, spike2) != None):
        startx = ball.rect.x
        starty = ball.rect.y
        thetai = 0
        pullDistance = 20
        balltime = 0
        spike1.rect.x = -100
        spike2.rect.x = -100
        gameOver = True
        gameEndWindow.show()

    if shoot == False and round(timeLeft) == 0 and gameOver == False and gameMode == 'Time Attack':
        gameOver = True
        gameEndWindow.show()
    elif missed == True and gameMode == "Streak" and gameOver == False:
        gameOver = True
        gameEndWindow.show()

    if (ball.rect.y >= hoop.rect.y and ball.rect.y < hoop.rect.y + 140) and (ball.rect.x + balldiameter/2 > hoopCollisionLeft.rect.x + 10 and ball.rect.x + balldiameter/2 < hoopCollisionRight.rect.x - 10) and scored == False:
        scored = True
        shotMade = True
        shotsMade += 1
        scoreText.set_text(f"Shots Made: {shotsMade}")
        timeLeft += 5
        timeLeftText.set_text(f"Time Left: {(round(timeLeft))}")

    collisions = 0
    totalTheta = 0
    for collider in collideSprites:
        if pygame.sprite.collide_mask(ball, collider) != None:
            collisions += 1
            if collider.collided == False:
                collider.collided = True
                shoot = False
                bruh += 1
                collide = True
                clip = pygame.sprite.collide_mask(ball, collider)
                pd = pullDistance/10
                tangent = math.atan2(-9.8*balltime + pd*math.sin(thetai), pd*math.cos(thetai))
                collideTangent = math.atan2(clip[1] - 40, 40 - clip[0]) + math.pi
                collideTangent %= 2*math.pi
                if collideTangent < math.pi/4:
                    collideAngle = math.pi
                    direction = 'right'
                elif collideTangent < 3*math.pi/4:
                    collideAngle = 0
                    direction = 'top'
                elif collideTangent < 5*math.pi/4:
                    collideAngle = math.pi
                    direction = 'left'
                elif collideTangent < 7*math.pi/4:
                    collideAngle = 0
                    direction = 'bottom'
                else:
                    collideAngle = math.pi
                    direction = 'right'

                velocityX = pd*math.cos(thetai) + hoopVelocity
                velocityY = -9.8*balltime + pd*math.sin(thetai)
                thetai = collideAngle - tangent
                totalTheta += thetai
                thetai = totalTheta
                if collider in netBarriers or collider in hoopBarriers:
                    if direction == 'right':
                        ball.rect.x -= 2 + hoopVelocity * 2 if hoopVelocity < 0 else 2
                    elif direction == 'top':
                        ball.rect.y += 2
                    elif direction == 'left':
                        ball.rect.x += 2 + hoopVelocity * 2 if hoopVelocity > 0 else 2
                    elif direction == 'bottom':
                        ball.rect.y -= 2

                balltime = 0
                startx = ball.rect.x
                starty = ball.rect.y
                bounceFactor = 4 if collider in hoopBarriers else 6
                if special == "Bouncy":
                    bounceFactor *= 1.5
                pullDistance = (math.sqrt(math.pow(velocityX, 2) + math.pow(velocityY, 2)) - 0.25) * bounceFactor
                if pullDistance / bounceFactor <= 0 and shotMade == False:
                    missed = True
                else:
                    shoot = True
        else:
            collider.collided = False
    if collisions == 0:
        collide = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shotTaken == False and gameOver == False:
        shotTaken = True
        shoot = True
        gameStarted = True
        specialModeButton.disable()
        gameModeButton.disable()
        shotMade = False
    if keys[pygame.K_r] and shotTaken == True:
        if shotMade == False:
            missed = True
        shoot = False
        balltime = 0
        thetai = 35
        pullDistance = 0
        collide = False
        scored = False
        ball.rect.y = screen.get_height() / 2
        ball.rect.x = screen.get_width() / 4
        startx = screen.get_width() / 4
        starty = screen.get_height() / 2
        shotTaken = False

    if keys[pygame.K_BACKSPACE]:
        specialModeButton.enable()
        gameModeButton.enable()
        shoot = False
        balltime = 0
        thetai = 35
        pullDistance = 0
        collide = False
        scored = False
        ball.rect.y = screen.get_height() / 2
        ball.rect.x = screen.get_width() / 4
        startx = screen.get_width() / 4
        starty = screen.get_height() / 2
        shotTaken = False
        timeLeft = 10
        shotsMade = 0
        timeLeftText.set_text(f'Time Left: {(round(timeLeft))}')
        scoreText.set_text(f"Shots Made: {shotsMade}")
        gameStarted = False
        gameOver = False
        gameEndWindow.hide()
        shotMade = False
        missed = False
        spike1.rect.x = 700
        spike2.rect.x = 1080
        specialTime = 0
    
    if gameOver == False:
        specialTime += (specialTimeFactor * dt)

    if shoot == True:
        balltime += dt
        ball.rect.y = starty + getPos(balltime)[1] * -30
        ball.rect.x = startx + getPos(balltime)[0] * 30

    mouse_rel = pygame.mouse.get_rel()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
