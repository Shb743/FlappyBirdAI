import sys,pygame,time
import Player,Network
from copy import deepcopy

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

Player.screen = screen
Player.height = height
Player.jump_speed = 50
Player.decel = 10
Player.gravity = 10

#Ai Stuffs
batch_size = 100
AIs = [(Player.Player(),Network.DenseNetwork()) for x in range(batch_size) ]
for AI in AIs:
	AI[1].addLayer(1) #input layer
	AI[1].addLayer(5) #Deep layer
	AI[1].addLayer(1,AI[0].jump) #Output layer
#Ai Stuffs*


def Run(timeout = 10.0):
	global AIs
	old_time = (pygame.time.get_ticks()/100.00)
	time_delta = 1.0
	while (timeout > 0):
		screen.fill(black)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		#if event.type == pygame.KEYDOWN:
		#		if event.key == pygame.K_SPACE:
		#			ball.jump()
		#ball.update(time_delta)
		#print time_delta
		for AI in AIs:
			AI[1].fire([ (AI[0].player_rect.y)/(height*1.0) ])
			AI[0].update(time_delta)

		 # The guidelines
		pygame.draw.line(screen,(244,244,66),[0,height/2],[width,height/2],1)

		pygame.display.flip()
		time_delta = ((pygame.time.get_ticks()/100.00) - old_time)
		old_time = (pygame.time.get_ticks()/100.00)
		print int(1/(time_delta/10))
		timeout -= (time_delta/10)
		#print int(round(1/(time_delta/10)))
		#time.sleep(0.02)
	AIs = sorted(AIs, key=lambda x: (x[0].score))
	AIs.reverse()
	print "------"
	for AI in AIs:
		print AI[0].score
Run()

#Keep screen alive
while(1):
	for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	time.sleep(0.1)