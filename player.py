#from dataclasses import dataclass


import pygame as pg
from pygame import Vector2 as vec
from pygame import Rect
from pygame.sprite import Sprite 

from main import App
import level
from helpers import Sequencer, SpriteSheet
from inputs_mapping import Events, keys_bindings,  bind_keys_to_inputs 
from components import Physics
from components import EventStack
from FSM import FiniteStateMachine,  Condition

bindings_directions = {
                            Events.Left: vec(-1,  0), 
                            Events.Right: vec(1,  0), 
                            Events.Up: vec(0,  -1), 
                            Events.Down: vec(0,  1), 
                            }

is_on_ground = Condition(Events.On_ground)
is_jumping = Condition(Events.Up)
is_moving = Condition(Events.Left, Events.Right)
is_ducking = Condition(Events.Down)


class Player(Sprite):
    
    def __init__(self,  game,  group):
        super().__init__()
        self.rect = Rect(0, 0, 16, 16)
        self.sprites = Sequencer(*SpriteSheet("first_Experiment.png",  self.rect).get_strip())
        self.image = self.sprites() 
        self.rect = self.image.get_rect()
        self.game = game
        self.settings = game.settings
        self.bounding_box = Rect(0, 0,  *self.settings['screen_size'])
        self.direction = vec(0, 0)
        self._position = vec(0, 0)
        self.physics = Physics(self,  group)
        self.FSM = FiniteStateMachine()
        
    def handle_inputs(self, event_stack):
        direction = vec(0, 0)
        
        for key,  value in bindings_directions.items():
            if key in event_stack:
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

    def update(self):
        self.move()
        if self.collision['bottom']:
            self.game.stack.next_post(Events.On_ground)
        self.image = self.sprites()

        
if __name__ == "__main__":                      
    class TestRun(App):
        def __init__(self):
            super().__init__()
            self.settings = {'screen_size': (16*32, 16*32),
                                        'FPS': 60,
                                        }
            self.stack = EventStack()
            
        def add_something(self):
            self.level = level.TestWorld(rect_size=level.rect_size, map=level.map)
            self.player = Player(self,  self.level.tiles)
            self.player.position = vec(*[p/2 for p in self.settings['screen_size']])
            
        def handle_events(self, inputs,  events):
            
            events = bind_keys_to_inputs(inputs,keys_bindings )
#            for e in events:
#                print(e)
                
            self.stack.reset()
            event_stack = self.stack.post(*events)
            for e in self.stack.events:
                print(e)
            self.player.handle_inputs(event_stack)
                                            
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
