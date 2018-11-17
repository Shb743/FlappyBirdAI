# pygame
import sys, pygame, time
from click import Neuron

pygame.init()

size = width, height = 800, 600
speed = [0, 3.0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
# The main object
ball = pygame.image.load("superman.png")
ball = pygame.transform.scale(ball,(86,59))
ballrect = ball.get_rect()
ballrect = ballrect.move([350,300])

batch = [Neuron(0,0) for i in xrange(100)]
for neuron in batch:
    print neuron.weight

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

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

    # The guidelines
    pygame.draw.line(screen,(244,244,66),[0,200],[800,200],5)
    pygame.draw.line(screen,(244,244,66),[0,350],[800,350],5)

    
    pygame.display.flip()
    time.sleep(0.01)
    if (speed[1] < 3.0):
        speed[1] += 0.2
