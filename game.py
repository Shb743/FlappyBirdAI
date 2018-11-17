# pygame

import sys, pygame, time
import click

pygame.init()

size = width, height = 800, 600
speed = [0, 3.0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("superman.png")
ball = pygame.transform.scale(ball,(192,108))
ballrect = ball.get_rect()
ballrect = ballrect.move([350,300])
cp = height//2

batch_of_neurons = [click.Neuron(0,0) for i in range(100)]
print batch_of_neurons

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
    pygame.display.flip()
    time.sleep(0.01)
    if (speed[1] < 3.0):
        speed[1] += 0.2
