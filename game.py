import pygame
from sys import exit
from time import time
from sprites import Background, Ground, Title, Text, Menu
from settings import WIDTH, HEIGHT, GROUND_HEIGHT, PIPE_OFFSET, GROUND_V
from bird import Bird
from pipepair import PipePair
from datafile import DataFile

class Game:
	def __init__(self):
		
		# window
		pygame.init()
		pygame.display.set_caption("Flappy bird")
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))

		# file handling
		self.datafile = DataFile()

		# sprite groups
		self.render_sprites = pygame.sprite.Group()
		self.bird_sprite = pygame.sprite.GroupSingle()
		self.collission_sprites = pygame.sprite.Group()

		# sprite setup
		Background(self.render_sprites)
		
		self.bird = Bird([self.bird_sprite, self.render_sprites],self)

		self.ground = Ground([self.render_sprites,self.collission_sprites],self)

		self.pipes = []
		for i in range(3):
			self.pipes.append(PipePair([self.render_sprites,self.collission_sprites],self,i))

		self.title = Title(self.render_sprites,self)

		self.score_sprite = Text(self.render_sprites, self, 0, "current_score")
		self.score_sprite.kill()

		self.menu_sprite = Menu(self.render_sprites, self)
		self.menu_sprite.kill()

		self.high_score_sprite = Text(self.render_sprites, self, self.datafile.get_high_score(), "high_score")
		self.high_score_sprite.kill()

		self.total_score_sprite = Text(self.render_sprites, self,0, "total_score")
		self.total_score_sprite.kill()

		# other variables
		self.ingame = False
		self.score = 0

		self.pipe_speed = GROUND_V

	def run(self):

		previous_time = time()

		while True:

			dt = time() - previous_time
			previous_time = time()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					if pygame.key.name(event.key) == "space":
						# space bar pressed

						if not self.ingame and not self.bird.dead:
							# space pressed while bobbing, start game
							self.bird.jump()
							self.ingame = True
							self.score = 0
							self.title.rect.x += WIDTH # move the title off screen
							self.render_sprites.add(self.score_sprite)

						if self.ingame and self.bird.dead:
							# space pressed while in menu, reset to bobbing
							self.ingame = False
							self.bird.reset()
							self.ground.animate = True
							self.title.rect.x -= WIDTH # move the title into the screen
							for pipe in self.pipes:
								pipe.reset()
							self.menu_sprite.kill()
							self.high_score_sprite.kill()
							self.total_score_sprite.kill()

						if self.ingame and not self.bird.dead:
							# space pressed while ingame, jump
							self.bird.jump()

			self.window.fill("black")

			# update and draw sprites
			self.render_sprites.update(dt)
			self.render_sprites.draw(self.window)

			# collissions
			if not self.bird.dead:
				if pygame.sprite.spritecollide(self.bird_sprite.sprite, self.collission_sprites, False):
					if pygame.sprite.spritecollide(self.bird_sprite.sprite, self.collission_sprites, False, pygame.sprite.collide_mask):
						self.die()
				if self.bird.rect.top < -20:
					self.die()

			pygame.display.update()

	def die(self):
		self.bird.die()
		self.ground.animate = False
		self.total_score_sprite.update_number(self.score)
		if self.score > self.datafile.get_high_score():
			self.datafile.set_high_score(self.score)
			self.high_score_sprite.update_number(self.score)