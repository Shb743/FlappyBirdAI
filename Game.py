import random,pygame

screen = None
screen_height = 0
screen_width = 0
speed = [-10,0]
pipe_color = 44,176,26
black = 0, 0, 0
pipe_width = int(screen_width*0.056)
pipe_spawn_chance = 0.02

class Pipe():
	height = 0
	player_rect = None
	active = True
	def __init__(self):
		global screen_height
		global screen_width
		global pipe_color
		global pipe_width
		#init bounds
		self.height = random.randint(int(screen_height/2.5), int(screen_height/1.5) )
		#init pos
		x = screen_width-pipe_width
		y = screen_height - int(self.height/2)
		if (random.random() > 0.5):
			y = 0
		self.player_rect = pygame.draw.rect(screen,pipe_color,(x,y,pipe_width,self.height))
		

	def move(self,time_delta):
		global pipe_color
		global speed
		if ((time_delta > 0) and (time_delta < 10)):
			if (self.active):
				self.player_rect = pygame.draw.rect(screen,pipe_color,(self.player_rect.x+int(round(speed[0]*time_delta)),self.player_rect.y+int(round(speed[1]*time_delta)),pipe_width,self.height))
				if (self.player_rect.x <= 0):
					self.active = False

	def collidedWith(self,pos,radius=10):
		if ((abs(self.player_rect.centerx-self.pos[0])<((pipe_width/2) +radius)) and (abs(self.player_rect.centery-self.pos[1])<(self.height+radius))):
			return True
		return False



def Run(AIs,timeout = 10.0):
	global screen_height
	global screen_width
	global pipe_width
	global pipe_spawn_chance

	high_score = 10
	highest_scorer = None
	old_time = (pygame.time.get_ticks()/100.00)
	time_delta = 1.0
	pipes = []
	pipe_width = int(screen_width*0.056)
	while (timeout > 0):
		#Time Stuffs
		time_delta = ((pygame.time.get_ticks()/100.00) - old_time)
		old_time = (pygame.time.get_ticks()/100.00)
		#print(f"FPS:{int(1/(time_delta/10))}" )
		timeout -= (time_delta/10.0)
		#Time Stuffs*
		screen.fill(black)#Reset screen
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		#Update AIs
		#print(time_delta)
		for AI in AIs:
			AI[1].fire([ (AI[0].player_rect.y)/(screen_height*1.0) ])
			AI[0].update(time_delta)
			#visuals
			if (highest_scorer):
				highest_scorer.color = highest_scorer.oldcolor
			if (AI[0].score > high_score):
				high_score = AI[0].score
				highest_scorer = AI[0]
			if (highest_scorer):
				highest_scorer.oldcolor = highest_scorer.color
				highest_scorer.color = 255,255,255
			#visuals*
		#Update AIs*
		# The guidelines
		pygame.draw.line(screen,(244,244,66),[0,screen_height/2],[screen_width,screen_height/2],1)

		#Spawn pipes
		if (len(pipes)>0):
			if ( (pipes[-1].player_rect.centerx < (screen_width-(pipe_width*3)) ) and (random.random() < pipe_spawn_chance) ): 
				print(f"pipe pos{pipes[-1].player_rect.centerx}")
				pipes.append(Pipe())
		else:
			pipes.append(Pipe())
		#Spawn pipes*
		#UpdatePipes
		for pipe in pipes:
			#if (not(pipe.player_rect.x < ((screen_width/2)-pipe_width))):
			#	if pipe.collidedWith([AI[0].player_rect.centerx,AI[0].player_rect.centery]):
			#		pass#Kill AI as it hit the pipe
			if (pipe.active):
				pipe.move(time_delta)
			else:
				del pipe
		#UpdatePipes*
		pygame.display.flip()#update display surface
