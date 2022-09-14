from pygame.sprite import Sprite
from random import randrange
from settings import PIPE_SPACE, PIPE_MIN_LENGTH, HEIGHT, GROUND_HEIGHT, CHROMA_KEY, WIDTH, GROUND_V, PIPE_OFFSET
from pygame.image import load
from pygame.transform import scale, flip
from pygame import Surface, mask
from pygame.rect import Rect
from pygame.math import Vector2

class PipePair(Sprite):
	def __init__(self, groups,game, index):
		super().__init__(groups)
		self.game = game
		self.index_in_pipes_list = index

		self.pos = Vector2((self.index_in_pipes_list+1)*PIPE_OFFSET+WIDTH,0)

		self.upper_length = randrange(PIPE_MIN_LENGTH, HEIGHT - GROUND_HEIGHT - PIPE_MIN_LENGTH - PIPE_SPACE, 1)
		self.lower_length = HEIGHT - GROUND_HEIGHT - self.upper_length - PIPE_SPACE

		self.width = 75
		self.rect = Rect(self.pos.x,0,self.pos.x+self.width,HEIGHT-GROUND_HEIGHT)

		img = scale(load("./images/pipe.png"),(self.width,HEIGHT-GROUND_HEIGHT))

		upper_rect = Rect(0,0,self.width,self.upper_length)
		upper_img = flip(img.subsurface(upper_rect),False,True).convert_alpha()

		lower_rect = Rect(0,0,self.width,self.lower_length)
		lower_img = img.subsurface(lower_rect).convert_alpha()

		# create surface with size=self.rect and bit depth of 24
		self.image = Surface((self.rect.width, self.rect.height), depth=24).convert_alpha() 
		self.image.fill(CHROMA_KEY) # fill surface with chromakey
		self.image.set_colorkey(CHROMA_KEY) # set surface colorkey as the chromekey
		self.image.blit(upper_img,(0,0)) # blit images onto surface
		self.image.blit(lower_img,(0,upper_rect.height+PIPE_SPACE))
		self.image.convert()

		self.mask = mask.from_surface(self.image)
		self.point_given = False

	def update(self,dt):
		if self.game.ingame and not self.game.bird.dead:
			self.pos.x -= self.game.pipe_speed * dt
			self.rect.x = self.pos.x

			if self.rect.x < -self.width:
				self.new()
			
			if self.rect.x < self.game.bird.rect.x and not self.point_given:
				self.game.score += 1
				self.game.score_sprite.update_number(self.game.score)
				self.point_given = True


	def new(self): # essentially makes this object represent a new pair of pipes by moving to the right of window 
		# and changing pipe lengths seudorandomly 

		# update position

		match(self.index_in_pipes_list): #could be optimized, this is unelegant
			case 0:
				self.pos.x = self.game.pipes[2].rect.x + PIPE_OFFSET
				self.rect.x = self.pos.x
			case 1:
				self.pos.x = self.game.pipes[0].rect.x + PIPE_OFFSET
				self.rect.x = self.pos.x
			case 2:
				self.pos.x = self.game.pipes[1].rect.x + PIPE_OFFSET
				self.rect.x = self.pos.x

		# update pipe lengths and set new image for drawing

		self.upper_length = randrange(PIPE_MIN_LENGTH, HEIGHT - GROUND_HEIGHT - PIPE_MIN_LENGTH - PIPE_SPACE, 1)
		self.lower_length = HEIGHT - GROUND_HEIGHT - self.upper_length - PIPE_SPACE

		img = scale(load("./images/pipe.png"),(self.width,HEIGHT-GROUND_HEIGHT))

		upper_rect = Rect(0,0,self.width,self.upper_length)
		upper_img = flip(img.subsurface(upper_rect),False,True).convert_alpha()

		lower_rect = Rect(0,0,self.width,self.lower_length)
		lower_img = img.subsurface(lower_rect).convert_alpha()

		# create surface with size=self.rect and bit depth of 24
		self.image = Surface((self.rect.width, self.rect.height), depth=24).convert_alpha() 
		self.image.fill(CHROMA_KEY) # fill surface with chromakey
		self.image.set_colorkey(CHROMA_KEY) # set surface colorkey as the chromekey
		self.image.blit(upper_img,(0,0)) # blit images onto surface
		self.image.blit(lower_img,(0,upper_rect.height+PIPE_SPACE))
		self.image.convert()

		self.mask = mask.from_surface(self.image)

		self.point_given = False

	def reset(self): #pretty much the same as new() but resets positions to default values instead of basing on previous pipes
		# update position

		match(self.index_in_pipes_list): #could be optimized, this is unelegant
			case 0:
				self.pos.x = WIDTH + PIPE_OFFSET
				self.rect.x = self.pos.x 
			case 1:
				self.pos.x = WIDTH + PIPE_OFFSET*2
				self.rect.x = self.pos.x
			case 2:
				self.pos.x = WIDTH + PIPE_OFFSET*3
				self.rect.x = self.pos.x

		# update pipe lengths and set new image for drawing

		self.upper_length = randrange(PIPE_MIN_LENGTH, HEIGHT - GROUND_HEIGHT - PIPE_MIN_LENGTH - PIPE_SPACE, 1)
		self.lower_length = HEIGHT - GROUND_HEIGHT - self.upper_length - PIPE_SPACE

		img = scale(load("./images/pipe.png"),(self.width,HEIGHT-GROUND_HEIGHT))

		upper_rect = Rect(0,0,self.width,self.upper_length)
		upper_img = flip(img.subsurface(upper_rect),False,True).convert_alpha()

		lower_rect = Rect(0,0,self.width,self.lower_length)
		lower_img = img.subsurface(lower_rect).convert_alpha()

		# create surface with size=self.rect and bit depth of 24
		self.image = Surface((self.rect.width, self.rect.height), depth=24).convert_alpha() 
		self.image.fill(CHROMA_KEY) # fill surface with chromakey
		self.image.set_colorkey(CHROMA_KEY) # set surface colorkey as the chromekey
		self.image.blit(upper_img,(0,0)) # blit images onto surface
		self.image.blit(lower_img,(0,upper_rect.height+PIPE_SPACE))
		self.image.convert()

		self.mask = mask.from_surface(self.image)

		self.point_given = False
