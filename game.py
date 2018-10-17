     # pygame

import sys, pygame, time
pygame.init()

size = width, height = 800, 600
speed = [0, 3.0]
black = 0, 0, 0

children = []

screen = pygame.display.set_mode(size)

ball = pygame.image.load("basketball_ball.png")
ballrect = ball.get_rect()
ballrect = ballrect.move([350,300])
cp = height//2


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            print children

        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed[1] = -3.5

    if ballrect.bottom > height:
        if (speed[1] < 0.0):
            ballrect = ballrect.move(speed)

    elif ballrect.top < 0:
        if (speed[1] > 0.0):
         ballrect = ballrect.move(speed)
    else:
        ballrect = ballrect.move(speed)

    screen.fill(black)
    screen.blit(ball, ballrect)
    # children.append()
    # print
    children.append(ballrect[1])
    pygame.display.flip()
    time.sleep(0.01)
    print children
    if (speed[1] < 3.0):
        speed[1] += 0.2
