import pygame

screen = None
gravity = 0
height = 0
jump_speed = 0
decel = 0

class Player():
	color = 255,0,0
	oldcolor = 255,0,0
	player_rect = None
	score = 0
	speed = [0, 0]
	def __init__(self):
		self.player_rect = pygame.draw.circle(screen,self.color,[400,300],10)
		self.speed[1] = gravity
	def move(self,time_delta):
		if ((time_delta > 0) and (time_delta < 10)):
			self.player_rect = pygame.draw.circle(screen,self.color,[self.player_rect.centerx+int(round(self.speed[0]*time_delta)),self.player_rect.centery+int(round(self.speed[1]*time_delta))],10)
	def jump(self):
		self.speed[1] = -jump_speed

	def update(self, time_delta):
		#print self.score
		#print tmp
		if (abs(self.player_rect.y - (height/2))/(height/2.0) > 0.1):
			self.score -= 0.1
		else:
			self.score += 0.1
		if self.player_rect.bottom > height:
			if (self.speed[1] < 0.0):
				self.move(time_delta)
		elif self.player_rect.top < 0:
			if (self.speed[1] > 0.0):
				self.move(time_delta)
		else:
			self.move(time_delta)
		if (self.speed[1] < gravity):
			self.speed[1] += decel*time_delta
			if (self.speed[1] > gravity):
				self.speed[1] = gravity
