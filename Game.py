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
AIs = []
def create_networks():
	global AIs
	global batch_size
	AIs = [(Player.Player(),Network.DenseNetwork()) for x in range(batch_size) ]
	for AI in AIs:
		AI[1].addLayer(1) #input layer
		AI[1].addLayer(5) #Deep layer
		AI[1].addLayer(1,AI[0].jump) #Output layer
create_networks()
#Ai Stuffs*


def Run(timeout = 10.0):
	global AIs
	old_time = (pygame.time.get_ticks()/100.00)
	time_delta = 1.0
	while (timeout > 0):
		screen.fill(black)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		#Update AIs
		for AI in AIs:
			AI[1].fire([ (AI[0].player_rect.y)/(height*1.0) ])
			AI[0].update(time_delta)
		#Update AIs*
		# The guidelines
		pygame.draw.line(screen,(244,244,66),[0,height/2],[width,height/2],1)

		pygame.display.flip()#update display surface
		#Time Stuffs
		time_delta = ((pygame.time.get_ticks()/100.00) - old_time)
		old_time = (pygame.time.get_ticks()/100.00)
		#print(f"FPS:{int(1/(time_delta/10))}" )
		timeout -= (time_delta/10)
		#Time Stuffs*



def train(epochs=10, timeout=10.0, retention=10.0, children=5):
	global AIs
	global batch_size

	for x in range(epochs):
		Run(timeout)
		#Get Best Performing AIs
		AIs = sorted(AIs, key=lambda x: (x[0].score))
		AIs.reverse()
		#Get Best Performing AIs*
		#Retain top x% 
		AIs = AIs[:int(len(AIs)*(retention/100.0))]
		retainedAISize = len(AIs)
		print(f"keeping top {retention}% of AIs : {retainedAISize}")
		for AI in AIs:
			print(AI[0].score)
			AI[0].score = 0
		print("\n\n\n")
		#Retain top x% *
		#All retained AIs should have y mutated copies
		for i in range(retainedAISize):
			tmp = AIs[i][1].nodes[-1][0].output_funct
			AIs[i][1].nodes[-1][0].output_funct = None
			for j in range(children):
				AIs.append( (Player.Player(),deepcopy(AIs[i][1]))  )
				AIs[-1][1].nodes[-1][0].output_funct = AIs[-1][0].jump
				AIs[-1][1].mutate()
			AIs[i][1].nodes[-1][0].output_funct = tmp
		#All retained AIs should have y mutated copies*
		#Fill up remaining batch size with new copies
		print(f"AIs with children : {len(AIs)}")
		while(len(AIs) < batch_size):
			AIs.append((Player.Player(),Network.DenseNetwork()))
			AIs[-1][1].addLayer(1) #input layer
			AIs[-1][1].addLayer(5) #Deep layer
			AIs[-1][1].addLayer(1,AIs[-1][0].jump) #Output layer
		print(f"AIs with children and new inits: {len(AIs)}")
		#Fill up remaining batch size with new copies*

train(timeout=10 , epochs=10)

print("Showing the best one")
AIs = AIs[:1]
Run()
print("Done")
#Keep screen alive
while(1):
	for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	time.sleep(0.1)