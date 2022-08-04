#from dataclasses import dataclass
from math import copysign

import pygame
#from pygame.locals import *
from pygame import Vector2 as vec

from main import App
import level
from helpers import Sequencer, SpriteSheet 

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
   

class Physics:
    friction : float = -5
    gravity : float = 800
    movement : vec = vec(1200, 3200)
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
                    collision["right"] = coll.rect.left
                elif delta_position.x < 0:
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
                    collision["bottom"] = coll.rect.top
                elif delta_position.y < 0:
                    collision["top"] = coll.rect.bottom
        
        for key, value in collision.items():
            if value:
                setattr(self.sprite.rect, key, value)
        
        return collision
            
            
class Stack:
    stack = {"inputs": [], 
                   "game_events": [],  }
                    
    def post(self,  event):
        if isinstance(event, pygame.key.ScancodeWrapper):
            self.stack["inputs"] = event
        else:
            self.stack["game_events"] = event
            
    def check(self, ):
        pass
            
    
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
#        print(self.collision)
                
    def update(self):
        self.move()
        self.image = self.sprites()
        
                    
class TestRun(App):
    def __init__(self):
        super().__init__()
        self.settings = {'screen_size': (16*32, 16*32),
                                    'FPS': 60,
                                    }
        
    def add_something(self):
        self.level = level.TestWorld(rect_size=level.rect_size, map=level.map)
        self.player = Player(self.settings,  self.level.tiles)
        self.player.settings = self.settings
        self.player.position = vec(*[p/2 for p in self.settings['screen_size']])
        
    def handle_events(self, inputs,  events):
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
