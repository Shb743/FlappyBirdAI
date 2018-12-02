import sys,pygame,time
import Player,Network
from copy import deepcopy
#For saving/loading the best AI
try:
	import cPickle as pickle
except ModuleNotFoundError:
	import pickle

def save_object(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output)


def load_object(filename):
	""" Unpickle a file of pickled data. """
	with open(filename, "rb") as f:
		try:
			return pickle.load(f)
		except EOFError:
			pass
#For saving/loading the best AI*

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
high_score = 0
highest_scorer = None
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

#Check if im loading an AI or training a set from scratch?
fname = input("load from file ?") 
if (len(fname) > 3):
	AIs.append( (Player.Player(),load_object(fname)) )
	AIs[0][1].nodes[-1][0].output_funct = AIs[0][0].jump
else:
	create_networks()
#Check if im loading an AI or training a set from scratch?*
#Ai Stuffs*




def Run(timeout = 10.0):
	global AIs
	global high_score
	global highest_scorer
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
			#visuals
			if (highest_scorer):
				highest_scorer.color = highest_scorer.oldcolor
			if (AI[0].score > high_score):
				high_score = AI[0].score
				highest_scorer = AI[0]
			highest_scorer.oldcolor = highest_scorer.color
			highest_scorer.color = 255,255,255
			#visuals*
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
	high_score = 0



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
			AI[0].color = 0,0,255
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
				AIs[-1][0].color = 0,255,0
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

if (len(fname) < 3):
	train(timeout=20 , epochs=3 )

print("Showing the best one")
AIs = AIs[:1]
Run()
print("Done")
#Keep screen alive
while(1):
	for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print("Showing the best one")
					Run()
					print("Done")
				elif event.key == pygame.K_s:
					tmp = AIs[0][1].nodes[-1][0].output_funct
					AIs[0][1].nodes[-1][0].output_funct = None
					fname = input("output file name") 
					if (len(fname) > 3):
						save_object(AIs[0][1],fname)
					else:
						save_object(AIs[0][1],"AI.pickl")
					AIs[0][1].nodes[-1][0].output_funct = tmp
	time.sleep(0.1)