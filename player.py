#from dataclasses import dataclass
from enum import Enum,  auto

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
                            Events.Down: vec(0,  0), 
                            }

is_on_ground = Condition(Events.On_ground)
is_jumping = Condition(Events.Up)
is_moving = Condition(Events.Left, Events.Right)
is_ducking = Condition(Events.Down)

class State(Enum):
    Idle = auto()
    In_air = auto()
    Duck = auto()
    Move = auto()
                    
    def enter(self):
        print("Entering " + self.name)
        
    def run(self):
        print("Running " + self.name)
    
    def exit(self):
        print("Exiting " + self.name)

State.bindings_directions = bindings_directions
State.In_air.bindings_directions[Events.Up] = vec(0,  -1)

def bind_directions(bindings_directions,  event_stack):
    direction = vec(0, 0)
    for key,  value in bindings_directions.items():
                if key in event_stack:
                    direction += value
    return direction


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
        self.FSM.transitions_table = {State.Idle: [
                                        {State.In_air: is_jumping}, 
                                        {State.Move: is_moving}, 
                                        {State.Duck: is_ducking}, 
                                        {State.Idle: is_on_ground},
                                        ], 
                        State.Duck: [
                                        {State.Idle: is_on_ground},
                                        {State.Duck: is_ducking}, 
                                         ],  
                        State.Move: [
                                        {State.Idle: is_on_ground}, 
                                        {State.In_air: is_jumping}, 
                                        {State.Duck: is_ducking}, 
                                        {State.Move: is_moving},
                                        ], 
                        State.In_air: [
                                        {State.Idle: is_on_ground},  
#                                        {State.In_air: is_jumping},
                                        ],                 
                                    }
        self.FSM.start_FSM(State.In_air)
        
    def handle_inputs(self, event_stack):
#        direction = vec(0, 0)
#        
#        for key,  value in bindings_directions.items():
#            if key in event_stack:
#                direction += value
        direction = bind_directions(self.FSM.actual_state.bindings_directions,  event_stack)
        state = self.FSM.handle_event(event_stack)
        
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
                                        'FPS': 30,
                                        }
            self.stack = EventStack()
            
        def add_something(self):
            self.level = level.TestWorld(rect_size=level.rect_size, map=level.map)
            self.player = Player(self,  self.level.tiles)
            self.player.position = vec(*[p/2 for p in self.settings['screen_size']])
            
        def handle_events(self, inputs,  events):
            
            events = bind_keys_to_inputs(inputs,keys_bindings )
                
            self.stack.reset()
            event_stack = self.stack.post(*events)
#            for e in self.stack.events:
#                print(e)
            self.player.handle_inputs(event_stack)
                                            
        def update(self):
            self.player.update()
                
        def render(self):
            self.screen.blit(self.level.surface,  (0, 0))
            self.screen.blit(self.player.image, self.player.rect)


    game = TestRun()
    game.start()
    game.run()
    game.quit()
