from pygame import sprite, transform, image, rect, Surface, mask
from settings import GROUND_HEIGHT, WIDTH, HEIGHT, GROUND_V
from pygame.math import Vector2
from settings import CHROMA_KEY

class Background(sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.image = transform.scale(image.load("./images/background.png"), (WIDTH, HEIGHT - GROUND_HEIGHT)).convert()
		self.rect = self.image.get_rect()

class Ground(sprite.Sprite):
	def __init__(self,groups, game):
		super().__init__(groups)
		self.game = game
		ground_image = transform.scale(image.load("./images/ground.png"), (WIDTH / 20, GROUND_HEIGHT))
		self.image = Surface((WIDTH * 2, GROUND_HEIGHT))
		for i in range(40):
			self.image.blit(ground_image, (i*20-i,0))
		self.image.convert()
		self.rect = self.image.get_rect(topleft = (0,HEIGHT - GROUND_HEIGHT))
		self.pos = Vector2(self.rect.topleft)
		self.animate = True
		self.mask = mask.from_surface(self.image)

	def update(self, dt): # ingame,dead ignored
		if self.animate:
			if self.rect.centerx - 10 <= 0:
				self.pos.x = -10
				self.rect.x = self.pos.x
			else:
				self.pos.x -= GROUND_V * dt # speed times dt
				self.rect.x = self.pos.x

class Title(sprite.Sprite):

	def __init__(self, groups,game):
		super().__init__(groups)
		self.game = game

		img = transform.scale(image.load("./images/title.png"),(WIDTH * 3/4, HEIGHT / 7))
		self.image = img.subsurface(0,1,img.get_width()-1,img.get_height()-1)
		self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 7))

class Text(sprite.Sprite):

	def __init__(self, groups, game, number, location="default"): 
	# location is str, either "current_score", "total_score" or "high_score"
		super().__init__(groups)
		self.game = game
		self.number = number
		self.location = location

		self.width_pr_number = 25
		self.height = 35

		self.update_image()
		self.update_rect()	

	def update_number(self, number):
		self.number = number
		self.update_image()
		self.update_rect()

	def update_image(self):
		temp_surface = Surface((self.width_pr_number * len(str(self.number)), self.height), depth=24)
		temp_surface.fill(CHROMA_KEY)
		temp_surface.set_colorkey(CHROMA_KEY)
		for i,num in enumerate(str(self.number)):
			temp_surface.blit(transform.scale(image.load(f"./images/{num}.png"),(self.width_pr_number,self.height)), (self.width_pr_number*i, 0)), (self.width_pr_number, self.height)
		self.image = temp_surface.convert_alpha()

	def update_rect(self):
		match(self.location):
			case "default":
				self.rect = self.image.get_rect()
			case "current_score":
				self.rect = self.image.get_rect(center = (WIDTH / 2, self.image.get_height()))
			case "total_score":
				self.rect = self.image.get_rect(center = (WIDTH / 2,222)) # TODO location should be relative to height to allow for resizing
			case "high_score":
				self.rect = self.image.get_rect(center = (WIDTH / 2, 310)) # TODO location should be relative to height to allow for resizing

class Menu(sprite.Sprite):

	def __init__(self,groups,game):
		self.game = game
		super().__init__(groups)

		self.image = image.load("./images/score.png")
		self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))