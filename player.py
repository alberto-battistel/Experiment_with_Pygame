#from dataclasses import dataclass


import pygame as pg
#from pygame.locals import *
from pygame import Vector2 as vec
from pygame import Rect
from pygame.sprite import Sprite 

from main import App
import level
from helpers import Sequencer, SpriteSheet 
from components import Physics
from FSM import FiniteStateMachine,  Condition


keys_mapping = {pg.K_a: vec(-1,  0),
                            pg.K_d: vec(1,  0), 
                            pg.K_w: vec(0,  -1), 
                            pg.K_s: vec(0,  1),
#                            pg.K_SPACE: lambda: print("space"),
                            pg.K_LEFT: vec(-1,  0), 
                            pg.K_RIGHT: vec(1,  0), 
                            pg.K_UP: vec(0,  -1), 
                            pg.K_DOWN: vec(0,  -1), }

is_on_ground = Condition(inputs=pg.K_SPACE)
is_jumping = Condition(inputs=pg.K_w)
is_moving = Condition(inputs=[pg.K_a, pg.K_d])
is_ducking = Condition(inputs=pg.K_s)

class Player(Sprite):
    
    def __init__(self,  settings,  group):
        super().__init__()
        self.rect = Rect(0, 0, 16, 16)
        self.sprites = Sequencer(*SpriteSheet("first_Experiment.png",  self.rect).get_strip())
        self.image = self.sprites() 
        self.rect = self.image.get_rect()
        self.settings = settings
        self.bounding_box = Rect(0, 0,  *self.settings['screen_size'])
        self.direction = vec(0, 0)
        self._position = vec(0, 0)
        self.physics = Physics(self,  group)
        self.FSM = FiniteStateMachine()
        
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

        
if __name__ == "__main__":                      
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
