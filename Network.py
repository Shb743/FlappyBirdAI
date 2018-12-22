import random,os
from copy import deepcopy

random_data = os.urandom(7)
seed = int.from_bytes(random_data, byteorder="big")
random.seed(seed)

class Neuron():
	connections = None #list of lists [ [neuron,weight], ...]
	output_funct = None#for output nodes
	current_inp = 0.0#Sum Inputs from previous layer
	activation_function = lambda self,x: x #Default does nothing
	inverse_function = lambda self,x: x #Default does nothing
	def __init__(self,connections,output_funct=None,activation_functions=None ):
		self.connections = connections
		self.output_funct = output_funct
		if (activation_functions != None):
			self.activation_function = activation_functions[0]
			self.inverse_function = activation_functions[1]

	def fire(self):
		self.current_inp = self.activation_function(self.current_inp)#Activate
		if (self.output_funct == None):
			for connection in self.connections:
				connection[0].current_inp += (self.current_inp*connection[1])
		else:
			if (self.current_inp >= 0.5): #Activation function
				if (self.output_funct != None):
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

	def backPropogate(self,IV,EOV):
		self.fire(IV,test=True)#Run IV through the network
		#Get output vector and work backwards
		OV = []
		for j in range(len(self.layers[-1])):
			OV.append(self.layers[-1][j].current_inp)
		#Get output vector and work backwards*

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

	def addLayer(self, size, output = None,activation_functions=None):
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
					me = Neuron([],output[i],activation_functions)
				else:
					me = Neuron([],output,activation_functions)
				#create neuron*
				self.layers[-1].append(me)
				for node in self.layers[-2]:
					node.connections.append([me,random.uniform(-1,1)])#Random weight from -1 to 1

	def fire(self,IV,test=False):
		if (len(IV) != self.IV_size):
			raise ValueError("Input vector size is wrong")
		else:
			#Set inputs and fire first layer
			for i in range(self.IV_size):
				self.layers[0][i].current_inp += IV[i]
				self.layers[0][i].fire()
			#Set inputs and fire first layer*
			#Fire all layers
			layers = len(self.layers)
			if (test):
				layers -= 1
			for i in range(1,layers):
				for j in range(len(self.layers[i])):
					self.layers[i][j].fire()
			#Fire all layers*

	def mutate(self, chance=0.8, completeChangeChance=.1):
		for i in range(1,len(self.layers)):
			if (random.random() < chance): #pick layer to mutate 80 % of the time
				for j in range(len(self.layers[i])):
					if (random.random() < chance): #pick node to mutate 80 % of the time
						self.layers[i][j].mutate(chance,completeChangeChance)
