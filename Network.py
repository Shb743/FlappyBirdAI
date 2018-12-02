import random
class Neuron():
	connections = None #list of lists [ [neuron,weight], ...]
	output_funct = None#for output nodes
	current_inp = 0.0#Sum Inputs from previous layer
	def __init__(self,connections,output_funct=None):
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
					con[1] = random.random()
				else:										#Slightly adjust weight
					if (random.random() > 0.5):
						con[1] += random.random()/50
					else:
						con[1] -= random.random()/50

class DenseNetwork():
	nodes = None 
	IV_size = None
	def __init__(self):
		pass

	def addLayer(self, size, output = False):
		if (self.nodes == None):
			self.IV_size = size
			if (output):
				return -1
			self.nodes = [[]]
			for i in range(size):
				self.nodes[0].append(Neuron([]))
		else:
			self.nodes.append([])
			for i in range(size):
				me = None
				if (output != False):
					me = Neuron([],output)
				else:
					me = Neuron([])
				self.nodes[-1].append(me)
				for node in self.nodes[-2]:
					node.connections.append([me,random.random()])

	def fire(self,IV):
		if (len(IV) != self.IV_size):
			return -1
		else:
			for i in range(self.IV_size):
				self.nodes[0][i].current_inp += IV[i]
				self.nodes[0][i].fire()
			for i in range(1,len(self.nodes)):
				for j in range(len(self.nodes[i])):
					self.nodes[i][j].fire()

	def mutate(self, chance=0.8, completeChangeChance=.1):
		for i in range(1,len(self.nodes)):
			if (random.random() < chance): #pick layer to mutate 80 % of the time
				for j in range(len(self.nodes[i])):
					if (random.random() < chance): #pick node to mutate 80 % of the time
						self.nodes[i][j].mutate(chance,completeChangeChance)
'''a = DenseNetwork()
def pwint():
	print("Fired")
print a.nodes
a.addLayer(4)
print a.nodes
print "-------"
a.addLayer(5)
print a.nodes
print "-------"
a.addLayer(1,pwint)
print a.nodes'''

