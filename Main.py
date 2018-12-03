import sys,pygame,time
import Player,Network,Game
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

screen = pygame.display.set_mode(size)

Game.screen = screen
Game.screen_width = width
Game.screen_height = height

Player.screen = screen
Player.height = height
Player.jump_speed = 50
Player.decel = 10
Player.gravity = 10

#Ai Stuffs
batch_size = 100
AIs = []
model = Network.DenseNetwork()
model.addLayer(1)#Input
model.addLayer(5)#Deep
model.addLayer(1)#output
def create_networks():
	global AIs
	global batch_size
	AIs = [(Player.Player(),model.clone()) for x in range(batch_size) ]
	for AI in AIs:
		AI[1].nodes[-1][0].output_funct = AI[0].jump

#Check if im loading an AI or training a set from scratch?
fname = input("load from file ?") 
if (len(fname) > 3):
	AIs.append( (Player.Player(),load_object(fname)) )
	AIs[0][1].nodes[-1][0].output_funct = AIs[0][0].jump
else:
	create_networks()
#Check if im loading an AI or training a set from scratch?*
#Ai Stuffs*



def train(epochs=10, timeout=10.0, retention=10.0, children=5):
	global batch_size
	global model 
	global AIs
	for x in range(epochs):
		Game.Run(AIs,timeout)
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
		#Quit here if last training loop
		if (epochs == (x+1)):
			break
		#Quit here if last training loop*
		#All retained AIs should have y mutated copies
		for i in range(retainedAISize):
			for j in range(children):
				tmp = Player.Player()
				AIs.append( (tmp,AIs[i][1].clone(reset=False,outputs=[tmp.jump])) )
				tmp.color = 0,255,0
				AIs[-1][1].mutate()
		#All retained AIs should have y mutated copies*
		#Fill up remaining batch size with new copies
		print(f"AIs with children : {len(AIs)}")
		while(len(AIs) < batch_size):
			tmp = Player.Player()
			AIs.append( (tmp,model.clone(reset=True,outputs=[tmp.jump])) )
		print(f"AIs with children and new inits: {len(AIs)}")
		#Fill up remaining batch size with new copies*

if (len(fname) < 3):
	train(timeout=10 , epochs=3 )

#Take best AI
#AIs = AIs[:1]
#Take best AI*
print("Showing the best ones")
AIs[0][0].score = 0
Game.Run(AIs,10.0)
print(f"It got a score of {AIs[0][0].score}")
print("Done")
#Keep screen alive
while(1):
	for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print("Showing the best one")
					Game.Run(AIs,5)
					print("Done")
				elif event.key == pygame.K_s:
					fname = input("output file name") 
					if (len(fname) > 3):
						save_object(AIs[0][1].clone(reset=False),fname)
					else:
						save_object(AIs[0][1].clone(reset=False),"AI.pickl")
				#elif event.key == pygame.K_c:
				#	Game.Pipe()
					
	time.sleep(0.1)