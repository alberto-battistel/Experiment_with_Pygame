#from dataclasses import dataclass
from math import copysign

import pygame
#from pygame.locals import *
from pygame import Vector2 as vec

from main import App
import level

sign = lambda x: copysign(1, x)

keys_mapping = {pygame.K_a: vec(-1,  0),
                            pygame.K_d: vec(1,  0), 
                            pygame.K_w: vec(0,  -1), 
                            pygame.K_s: vec(0,  1),
#                            pygame.K_SPACE: lambda: print("space"),
                            pygame.K_LEFT: vec(-1,  0), 
                            pygame.K_RIGHT: vec(1,  0), 
                            pygame.K_UP: vec(0,  -1), 
                            pygame.K_DOWN: vec(0,  -1), }
   

class Sequencer():
    def __init__(self, *sprites):
        self.sprites = sprites[:]
        self.max_length = len(self.sprites)
        self.generator = self._return_item()
        self.actual_item = self.sprites[0]
        
    def _return_item(self):
        index = 0
        while True:
            yield self.sprites[index]
            yield self.sprites[index]
            yield self.sprites[index]
            index = (index+1)%self.max_length

    def __call__(self):
        self.actual_item = next(self.generator)
        return self.actual_item
  
  
class SpriteSheet():
    def __init__(self,  asset_name,  rect):
        self.asset_name = asset_name
        self.rect = rect.copy()
        self.sheet = self.import_image()
        self.images = self.get_strip()
            
    def import_image(self):
        sheet = pygame.image.load(self.asset_name).convert_alpha()
        return sheet
    
    def get_strip(self):
        sheet_width = self.sheet.get_width()
        step = self.rect.width
        images = []
        for x_position in range(0,  sheet_width, step):
            self.rect.x = x_position
            image = pygame.Surface(self.rect.size,  pygame.SRCALPHA)
            image.blit(self.sheet, (0, 0), self.rect)
            images.append(pygame.transform.scale2x(pygame.transform.scale2x(image)))
    #        images.append(image)
        return images


class Physics:
    friction : float = -5
    gravity : float = 200
    movement : vec = vec(800, 800)
    max_velocity : vec = vec(200, 200)
    
    vel : vec = vec(0, 0)
    acc : vec = vec(0, 0)
    
    def __init__(self, sprite : pygame.sprite.Sprite, group : pygame.sprite.Group):
        self.sprite = sprite
        self.group = group
        
    
    def clamp(self,  vector):
        if abs(vector.x) > self.max_velocity.x:
            vector.x = sign(vector.x)*self.max_velocity.x
        if abs(vector.y) > self.max_velocity.y:
            vector.y = sign(vector.y)*self.max_velocity.y
        return vector
            
    def calculate_velocity(self,  direction,  delta=1):
        self.acc = vec(0,  self.gravity)
        self.acc += (direction * self.movement.elementwise())
        self.acc += self.vel * self.friction
        self.vel += 0.5 * self.acc * delta #averaged new velocity
        self.vel = self.clamp(self.vel)

#        print(self.vel)
        
        return self.vel
        
    def calculate_movement(self,  direction,  delta=1):
        velocity = self.calculate_velocity(direction,  delta)
        delta_position = velocity * delta 
        return delta_position    
        
    def check_collisions(self):     
        return pygame.sprite.spritecollide(self.sprite, self.group, dokill=False)
            
    def move_collide(self,  direction,  delta):
        collision = {"right": None, 
                            "left": None, 
                            "top": None, 
                            "bottom": None, }
        delta_position = self.calculate_movement(direction,  delta)
        # x direction
        new_position = vec(self.sprite.position.x + delta_position.x,  self.sprite.position.y)
        self.sprite.position = new_position
        collided = self.check_collisions()
        if collided:
            for coll in collided:
                if delta_position.x > 0:
    #                print("right collision")
                    collision["right"] = coll.rect.left
                elif delta_position.x < 0:
    #                print("left collision")
                    collision["left"] = coll.rect.right
        
        for key, value in collision.items():
            if value:
                setattr(self.sprite.rect, key, value)
        
        # y direction
        new_position = vec(self.sprite.position.x, self.sprite.position.y + delta_position.y)
        self.sprite.position = new_position
        collided = self.check_collisions()
        if collided:
            for coll in collided:
                if delta_position.y > 0:
    #                print("down collision")
                    collision["bottom"] = coll.rect.top
                elif delta_position.y < 0:
    #                print("up collision")
                    collision["top"] = coll.rect.bottom
        
        for key, value in collision.items():
            if value:
                setattr(self.sprite.rect, key, value)
        
        return collision
            
class Player(pygame.sprite.Sprite):
    
    def __init__(self,  settings,  group):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.sprites = Sequencer(*SpriteSheet("first_Experiment.png",  self.rect).get_strip())
        self.image = self.sprites() 
        self.rect = self.image.get_rect()
        self.settings = settings
        self.bounding_box = pygame.Rect(0, 0,  *self.settings['screen_size'])
        self.direction = vec(0, 0)
        self._position = vec(0, 0)
        self.physics = Physics(self,  group)
        
    def handle_inputs(self, inputs):
        direction = vec(0, 0)
        
        for key,  value in keys_mapping.items():
            if inputs[key]:
                direction += value
        
        self.direction = direction
            
        return self.direction
    
    @property
    def position(self):
        return vec(self.rect.center)
    
    @position.setter
    def position(self,  value : vec):
        value = vec(round(value.x), round(value.y))
        self._position = value
        self.rect.center = value
        
    def move(self):
        self.collision = self.physics.move_collide(self.direction,  delta=1/self.settings['FPS'])
        print(self.collision)
#        for key, value in game.player.collision.items():
#            if value:
#                setattr(self.rect, key, value)
                
    def update(self):
        self.move()
        self.rect.clamp_ip(self.bounding_box)
        self.position = vec(self.rect.center)
        self.image = self.sprites()
        
                    
class TestRun(App):
    def __init__(self):
        super().__init__()
        self.settings = {'screen_size': (16*32, 16*32),
                                    'FPS': 30,
                                    }
        
    def add_something(self):
        self.level = level.TestWorld(rect_size=level.rect_size, map=level.map)
        self.player = Player(self.settings,  self.level.tiles)
        self.player.settings = self.settings
        self.player.position = vec(*[p/2 for p in self.settings['screen_size']])
        
    def handle_inputs(self, inputs):
        self.player.handle_inputs(inputs)
                                        
    def update(self):
        self.player.update()
#        print(self.player.position)
            
    def render(self):
        self.screen.blit(self.level.surface,  (0, 0))
        self.screen.blit(self.player.image, self.player.rect)


game = TestRun()
game.start()
game.run()
game.quit()
