from pygame.sprite import Sprite
from pygame import image, Surface, rect
from pygame.math import Vector2
from pygame.transform import scale, rotate
from settings import WIDTH, HEIGHT

class Bird(Sprite):
	def __init__(self,groups,game):
		super().__init__(groups)
		self.game = game

		self.width = 55 #55
		self.height = 40 #40

		width = image.load("./images/bird.png").get_width()
		height = image.load("./images/bird.png").get_height()

		self.images = [
		scale(image.load("./images/bird.png").subsurface(rect.Rect(0,0,width / 3,height)), (self.width, self.height)).convert_alpha(),
		scale(image.load("./images/bird.png").subsurface(rect.Rect(width / 3,0,width / 3,height)),(self.width,self.height)).convert_alpha(),
		scale(image.load("./images/bird.png").subsurface(rect.Rect(width*2/3,0,width / 3,height)),(self.width,self.height)).convert_alpha(),
		scale(image.load("./images/bird.png").subsurface(rect.Rect(width / 3,0,width / 3,height)),(self.width,self.height)).convert_alpha()
		]

		self.image = self.images[1]
		self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
		self.dead = False
		self.index = 0
		self.v = Vector2(0,0)
		self.gravity = Vector2(0,1000)
		self.pos = Vector2(WIDTH / 2, HEIGHT / 2)
		self.angle = 0

		self.animation_speed = 10
		self.animation_rect = rect.Rect(0,0,1,1) # rect that is moved with dt, the pos_x determines animation stage
		self.animation_pos = Vector2(0,0)
		self.animation_v = Vector2(self.animation_speed,0)

	def update(self, dt):
		if self.game.ingame and not self.dead:
			self.update_image(dt)
			self.update_pos(dt)
			self.calculate_angle()
		if not self.game.ingame:
			self.bob(dt)

	def update_pos(self, dt):
		v_max = 400
		g_max = 400
		self.pos += self.v * dt
		self.rect.y = self.pos.y
		self.v += self.gravity * dt
		if self.v.y < -v_max: # max speed
			self.v.y = -v_max
		if self.v.y > g_max:
			self.v.y = g_max

	def update_image(self,dt):
		# update image, TODO this should be optimized

		self.animation_pos += self.animation_v * dt
		self.animation_rect.x = self.animation_pos.x

		if self.animation_rect.x > 3:
			self.animation_pos.x = 0
			self.animation_rect.x = 0
		
		self.image = rotate(self.images[self.animation_rect.x],self.angle)
	
	def jump(self):
		self.v += Vector2(0,-600) # jump speed

	def die(self):
		self.dead = True
		self.game.score_sprite.update_number(0)
		self.game.score_sprite.kill()
		self.game.render_sprites.add(self.game.menu_sprite)
		self.game.render_sprites.add(self.game.high_score_sprite)
		self.game.render_sprites.add(self.game.total_score_sprite)

	def reset(self):
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.pos = Vector2(WIDTH / 2, HEIGHT / 2)
		self.v = Vector2(0,0)
		self.dead = False
		self.angle = 0
		self.image = self.images[1]
		self.animation_speed = 100

	def bob(self,dt):
		# uses velocity vector and vertical coord to bob bird

		if self.v.y >= 0 and self.rect.y > HEIGHT / 2 - self.height / 4:
			self.v.y = 50
		if self.rect.y < HEIGHT / 2 - self.height / 4:
			self.v.y = -50
		if self.rect.y > HEIGHT / 2 + self.height / 4:
			self.v.y = 50

		self.pos -= self.v * dt
		self.rect.y = self.pos.y

	def calculate_angle(self):
		if self.v.y < 0:
			self.angle = round(-self.v.y * 0.06)
		if self.v.y > 0:
			self.angle = round(-self.v.y * 0.18)