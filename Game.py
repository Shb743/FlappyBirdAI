import random,pygame

screen = None
screen_height = 0.0
screen_width = 0
speed = [-10,0]
pipe_color = 44,176,26
black = 0, 0, 0
pipe_width = int(screen_width*0.056)
pipe_spawn_chance = 0.02

class Pipe():
	height = 0
	rect = None
	active = True
	def __init__(self):
		global screen_height
		global screen_width
		global pipe_color
		global pipe_width
		#init bounds
		self.height = random.randint(int(screen_height/2.7), int(screen_height/1.5) )
		#init pos
		x = screen_width-pipe_width
		y = screen_height - self.height
		if (random.random() > 0.5):
			y = 0
		self.rect = pygame.draw.rect(screen,pipe_color,(x,y,pipe_width,self.height))
		

	def move(self,time_delta):
		global pipe_color
		global speed
		if ((time_delta > 0) and (time_delta < 10)):
			if (self.active):
				self.rect = pygame.draw.rect(screen,pipe_color,(self.rect.x+int(round(speed[0]*time_delta)),self.rect.y+int(round(speed[1]*time_delta)),pipe_width,self.height))
				if (self.rect.x <= 0):
					self.active = False

	def collidedWith(self,pos,radius=10.0):
		#if (self.rect.centery < (screen_height/2.0) ):
		if ( ((abs(self.rect.centerx-pos[0])) < ((pipe_width/2.0)+radius)) and ( (abs(self.rect.centery-pos[1]))<( (self.height/2.0)+radius) ) ):
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
	active_pipe = None

	#reset AIs
	for AI in AIs:
		AI[0].active = True
	#reset AIs*
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
		active_pipe_loc = 0.5
		active_pipe_height = 0.0
		active_pipe_dist = 1.0
		if (active_pipe != None):
			active_pipe_height = ((active_pipe.height)/(screen_height/1.5))
			active_pipe_dist = (active_pipe.rect.centerx - screen_width)/(screen_width)
			if (active_pipe.rect.centery < (screen_height/2.0)):
				active_pipe_loc = 0.0
			else:
				active_pipe_loc = 1.0
		#print([ ((AIs[0][0].player_rect.centery)/screen_height) ,active_pipe_loc,active_pipe_height,active_pipe_dist,-1.5])
		allDead = True
		for AI in AIs:
			if (AI[0].active == False):
				continue
			allDead = False
			AI[1].fire([ ((AI[0].player_rect.centery)/screen_height) ,active_pipe_loc,active_pipe_height,active_pipe_dist,-1.5]) # (MyY,next_pipe_Up,next_pipe_height,next_pipe_dist,bias)
			AI[0].update(time_delta)
			#Collision Check
			if (active_pipe != None ):
				if (active_pipe.rect.x < ((screen_width/2)-pipe_width)):
					active_pipe = None #No longer the pipe that we need to check
				else:
					if active_pipe.collidedWith([AI[0].player_rect.centerx,AI[0].player_rect.centery]):
						AI[0].active = False

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
		if (allDead):
			return 0
		#Update AIs*
		# The guidelines
		pygame.draw.line(screen,(244,244,66),[0,screen_height/2],[screen_width,screen_height/2],1)

		#Spawn pipes
		if (len(pipes)>0):
			if ( (pipes[-1].rect.centerx < (screen_width-(pipe_width*5)) ) and (random.random() < pipe_spawn_chance) ): 
				#print(f"pipe pos{pipes[-1].rect.centerx}")
				pipes.append(Pipe())
		else:
			pipes.append(Pipe())
		#Spawn pipes*
		#UpdatePipes
		for pipe in pipes:
			if ((active_pipe == None ) and (not(pipe.rect.x < ((screen_width/2)-pipe_width)))):
				active_pipe = pipe
			if (pipe.active):
				pipe.move(time_delta)
			else:
				del pipe
		#UpdatePipes*
		pygame.display.flip()#update display surface
