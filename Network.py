import random,os
from copy import deepcopy

random_data = os.urandom(7)
seed = int.from_bytes(random_data, byteorder="big")
random.seed(seed)

class Neuron():
	connections = None #list of lists [ [neuron,weight], ...]
	output_funct = None#for output nodes
	current_inp = 0.0#Sum Inputs from previous layer
	activation_function = None#currently the only one is on the output layer and is a step function
	def __init__(self,connections,output_funct=None,activation_function=None):
		self.connections = connections
		self.output_funct = output_funct

	def fire(self):
		if (self.output_funct == None):
			for connection in self.connections:
				connection[0].current_inp += (self.current_inp*connection[1])
		else:
			if (self.current_inp >= 0.5): #Activation function
				self.output_funct()
		self.current_inp = 0.0

	def mutate(self,chance=0.8,completeChangeChance=.1):
		for con in self.connections:
			if (random.random() < chance): #pick connection to mutate 80 % of the time
				if (random.random() < completeChangeChance): #completely new weight 10 % of the time
					con[1] = random.uniform(-1,1) 
				else:										#Slightly adjust weight
					con[1] += random.uniform(-0.02,0.02) 

class DenseNetwork():
	layers = None 
	IV_size = None
	def __init__(self):
		pass

	def clone(self,reset=True,outputs=False):
		clonedNetwork = DenseNetwork()
		if (reset):
			for i in range(len(self.layers)):
				clonedNetwork.addLayer(len(self.layers[i]))
		else:
			clonedNetwork.layers = deepcopy(self.layers)
			clonedNetwork.IV_size = self.IV_size
			#Remove any outputs
			for layer in clonedNetwork.layers:
				for node in layer:
					node.output_funct = None
			#Remove any outputs*
		#Reset the output vector
		if (outputs):
			for i in range(len(clonedNetwork.layers[-1])):
				clonedNetwork.layers[-1][i].output_funct = outputs[i]
		#Reset the output vector*

		return clonedNetwork

	def addLayer(self, size, output = None,activation_function=None):
		if (self.layers == None):
			self.IV_size = size
			if (output):
				return -1
			self.layers = [[]]
			for i in range(size):
				self.layers[0].append(Neuron([]))
		else:
			self.layers.append([])
			for i in range(size):
				#create neuron
				me = None
				if (isinstance(output, list)):
					me = Neuron([],output[i],activation_function)
				else:
					me = Neuron([],output,activation_function)
				#create neuron*
				self.layers[-1].append(me)
				for node in self.layers[-2]:
					node.connections.append([me,random.uniform(-1,1)])

	def fire(self,IV):
		if (len(IV) != self.IV_size):
			raise ValueError("Input vector size is wrong")
		else:
			for i in range(self.IV_size):
				self.layers[0][i].current_inp += IV[i]
				self.layers[0][i].fire()
			for i in range(1,len(self.layers)):
				for j in range(len(self.layers[i])):
					self.layers[i][j].fire()

	def mutate(self, chance=0.8, completeChangeChance=.1):
		for i in range(1,len(self.layers)):
			if (random.random() < chance): #pick layer to mutate 80 % of the time
				for j in range(len(self.layers[i])):
					if (random.random() < chance): #pick node to mutate 80 % of the time
						self.layers[i][j].mutate(chance,completeChangeChance)
'''a = DenseNetwork()
def pwint():
	print("Fired")
print a.layers
a.addLayer(4)
print a.layers
print "-------"
a.addLayer(5)
print a.layers
print "-------"
a.addLayer(1,pwint)
print a.layers'''

