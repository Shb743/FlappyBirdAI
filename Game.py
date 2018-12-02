import random,pygame
screen = None
screen_height = 0
screen_width = 0
speed = [-10,0]
pipe_color = 44,176,26
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