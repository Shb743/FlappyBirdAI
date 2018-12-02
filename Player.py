import pygame

screen = None
gravity = 0
height = 0
jump_speed = 0
decel = 0

class Player():
	player = None
	player_rect = None
	score = 0
	speed = [0, 0]
	def __init__(self):
		self.player = pygame.image.load('Ball.png').convert_alpha() #pygame.image.load("Ball.png")
		self.player_rect = self.player.get_rect()
		self.player_rect = self.player_rect.move([400,300])
		self.speed[1] = gravity
	def move(self,time_delta):
		if ((time_delta > 0) and (time_delta < 10)):
			self.player_rect = self.player_rect.move([ int(round(self.speed[0]*time_delta)), int(round(self.speed[1]*time_delta)) ])
	def jump(self):
		self.speed[1] = -jump_speed

	def update(self, time_delta):
		#print self.score
		#print tmp
		if (abs(self.player_rect.y - (height/2))/(height/2.0) > 0.2):
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
		screen.blit(self.player, self.player_rect)
