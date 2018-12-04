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
Game.screen_width = width*1.0
Game.screen_height = height*1.0

Player.screen = screen
Player.height = height
Player.jump_speed = 50
Player.decel = 15
Player.gravity = 15

#Ai Stuffs
batch_size = 100
AIs = []
model = Network.DenseNetwork()
model.addLayer(5)#Input (MyY,next_pipe_Up,next_pipe_height,next_pipe_dist,bias)
model.addLayer(10)#Deep
model.addLayer(4)#Deep
model.addLayer(1)#output
def create_networks():
	global AIs
	global batch_size
	for i in range(batch_size):
		AIs.append((Player.Player(),model.clone()))
		AIs[-1][1].nodes[-1][0].output_funct = AIs[-1][0].jump
		time.sleep(0.001)
#Check if im loading an AI or training a set from scratch?
fname = input("load from file ?") 
if (len(fname) > 3):
	if (input("Load Array Or Load Player (0/1):")):
		AIs.append( (Player.Player(),load_object(fname)) )
		AIs[0][1].nodes[-1][0].output_funct = AIs[0][0].jump
	else:
		tmpAIs = load_object(fname)
		for tmpAI in tmpAIs:
			AIs.append( (Player.Player(),tmpAI) )
			AIs[-1][1].nodes[-1][0].output_funct = AIs[-1][0].jump
else:
	create_networks()
#Check if im loading an AI or training a set from scratch?*
#Ai Stuffs*



def train(epochs=10, timeout=10.0, retention=10.0, children=5):
	global batch_size
	global model 
	global AIs
	try:
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
				AI[0].active = True
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
	except KeyboardInterrupt:
		print("W: interrupt received, stopping training")

if (len(fname) < 3):
	train(timeout=30 , epochs=5 )
else:
	if (input("train loaded models (y/n)") == "y"):
		train(timeout=30 , epochs=5 )


AIs = AIs[:10]
print("Showing the best ones")
Game.Run(AIs,60)
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
					Game.Run(AIs,60)
					print("Done")
				elif event.key == pygame.K_s:
					fname = input("output file name") 
					if (len(fname) > 3):
						save_object(AIs[0][1].clone(reset=False),fname)
					else:
						save_object(AIs[0][1].clone(reset=False),"AI.pickl")
				elif event.key == pygame.K_a:
					tmpAIs = []
					for AI in AIs:
						tmpAIs.append(AI[1].clone(reset=False))
					fname = input("output file name") 
					if (len(fname) > 3):
						save_object(tmpAIs,fname)
					else:
						save_object(tmpAIs,"AIs.pickl")
				#elif event.key == pygame.K_c:
				#	Game.Pipe()
					
	time.sleep(0.1)