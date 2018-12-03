import random,pygame

screen = None
screen_height = 0
screen_width = 0
speed = [-10,0]
pipe_color = 44,176,26
black = 0, 0, 0

class Pipe():
	height = 0
	width = 15
	player_rect = None
	active = True
	def __init__(self):
		global screen_height
		global screen_width
		global pipe_color
		#init bounds
		self.height = random.randint(int(screen_height/2.5), int(screen_height/1.5) )
		self.width = int(screen_width*0.056)
		#init pos
		x = screen_width-self.width
		y = screen_height - int(self.height/2)
		if (random.random() > 0.5):
			y = 0
		self.player_rect = pygame.draw.rect(screen,pipe_color,(x,y,self.width,self.height))
		

	def move(self,time_delta):
		global pipe_color
		global speed
		if ((time_delta > 0) and (time_delta < 10)):
			if (self.active):
				self.player_rect = pygame.draw.rect(screen,pipe_color,(self.player_rect.x+int(round(speed[0]*time_delta)),self.player_rect.y+int(round(speed[1]*time_delta)),self.width,self.height))
				if (self.player_rect.x <= 0):
					self.active = False

	def collidedWith(self,pos):
		if (((self.player_rect.centerx-self.pos[0])<self.width) and ((self.player_rect.centery-self.pos[1])<self.height)):
			return True
		return False



def Run(AIs,timeout = 10.0):
	global screen_height
	global screen_width

	high_score = 10
	highest_scorer = None
	old_time = (pygame.time.get_ticks()/100.00)
	time_delta = 1.0
	pipe = Pipe()
	while (timeout > 0):
		screen.fill(black)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		#Update AIs
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

		pipe.move(time_delta)
		pygame.display.flip()#update display surface
		#Time Stuffs
		time_delta = ((pygame.time.get_ticks()/100.00) - old_time)
		old_time = (pygame.time.get_ticks()/100.00)
		#print(f"FPS:{int(1/(time_delta/10))}" )
		timeout -= (time_delta/10)
		#Time Stuffs*