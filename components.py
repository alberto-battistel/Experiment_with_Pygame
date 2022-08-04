#from dataclasses import dataclass

import pygame as pg
#from pygame.locals import *
from pygame import Vector2 as vec
from pygame.sprite import Sprite, Group

from helpers import sign

 
class EventStack:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.stack = {"inputs": [], 
                        "game_events": [],  }
                        
    def post(self,  event):
        if isinstance(event, pg.key.ScancodeWrapper):
            self.stack["inputs"] = event
        else:
            self.stack["game_events"] = event
            
        return self.stack 

        
class Physics:
    friction : float = -5
    gravity : float = 800
    movement : vec = vec(1200, 3200)
    max_velocity : vec = vec(200, 200)
    
    vel : vec = vec(0, 0)
    acc : vec = vec(0, 0)
    
    def __init__(self, sprite : Sprite, group : Group):
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
        return pg.sprite.spritecollide(self.sprite, self.group, dokill=False)
            
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
            
