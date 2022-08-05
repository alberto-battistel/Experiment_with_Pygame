#from dataclasses import dataclass

import pygame as pg
#from pygame.locals import *
from pygame import Vector2 as vec
from pygame.sprite import Sprite, Group

from helpers import sign

class EventStack:
    def __init__(self):
        self.events = []
        self.next_events = []
    
    def reset(self):
        self.events = self.next_events
        self.next_events = []
        
    def post(self, *events):
        for event in events:
            self.events.append(event)
        return self.events
      
    def next_post(self, *events):
        for event in events:
            self.next_events.append(event)
#        return self.events    

        
class Physics:
    friction : float = -5
    gravity : float = 800
    movement : vec = vec(1200, 40000)
    max_velocity : vec = vec(200, 2000)
    
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
            self.vel.x = 0
        
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
            self.vel.y = 0
            
        for key, value in collision.items():
            if value:
                setattr(self.sprite.rect, key, value)
        
        return collision
            
