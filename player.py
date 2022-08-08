#from dataclasses import dataclass
from enum import Enum,  auto
import types


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
from test_enum import States as State

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
is_in_air = Condition(Events.On_air)

player_states = ["Idle", 
                        "In_air", 
#                        "Jump", 
                        "Duck", 
                        "Move", ]

State.add_attr("bindings_directions", bindings_directions)
[State(s) for s in player_states]



@State.In_air.redefine
def enter(self):
    print("!!Entering " + self.name)

@State.In_air.redefine
def run(self):
    if self.count > 10:
        self.bindings_directions[Events.Up] = vec(0,  0)
        print("!!Running " + self.name)

@State.In_air.redefine
def exit(self):
    self.bindings_directions[Events.Up] = vec(0,  -1)
    print("!!Exiting " + self.name)

def bind_directions(bindings_directions,  event_stack):
    direction = vec(0, 0)
    for key,  value in bindings_directions.items():
                if event_stack[key] > 0:
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
        self.FSM = FiniteStateMachine(State.Idle, State.In_air, State.Duck, State.Move)
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
                                        {State.In_air: is_jumping},
                                        ],
#                        State.Jump: [
#                                        {State.In_air: is_in_air}, 
#                                        {State.Idle: is_on_ground}, 
#                                        ]                 
                                    }
        self.FSM.start_FSM(State.In_air)
    
    def add_component(self, name, instance):
        if hasattr(instance, "parent"):
            setattr(instance, "parent", self)
        setattr(self, name,  instance)
        
        
    def handle_inputs(self, event_stack):
        direction = bind_directions(self.FSM.actual_state.bindings_directions,  event_stack)
#        print(direction)
        state = self.FSM.handle_event(event_stack)
#        print(state)
#        if (self.FSM.actual_state is State.Jump) and not (self.FSM.old_state is State.Jump):
#            print("here")
#            self.game.stack.post(Events.On_air)
            
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
            self.game.stack.post(Events.On_ground)
        self.image = self.sprites()

        
if __name__ == "__main__":                      
    class TestRun(App):
        def __init__(self):
            super().__init__()
            self.settings = {'screen_size': (16*32, 16*32),
                                        'FPS': 60,
                                        }
            self.stack = EventStack(events_dict={Events.Left: 0, 
                                                                        Events.Right: 0, 
                                                                        Events.Up: 0, 
                                                                        Events.Down: 0, 
                                                                        Events.On_ground: 0,
                                                                        Events.Shot: 0, 
                                                                        Events.On_air: 0, }, 
                                                    rules = {Events.Left: 1, 
                                                                    Events.Right: 1, 
                                                                    Events.Up: 10, 
                                                                    Events.Down: 1, 
                                                                    Events.On_ground: 10,
                                                                    Events.Shot: 0,
                                                                    Events.On_air: 20, })
            
        def add_something(self):
            self.level = level.TestWorld(rect_size=level.rect_size, map=level.map)
            self.player = Player(self,  self.level.tiles)
            self.player.position = vec(*[p/2 for p in self.settings['screen_size']]) + vec(0, -32)
            
        def handle_events(self, inputs,  events):
            
            events = bind_keys_to_inputs(inputs, keys_bindings)
#            print(events)
            
            self.stack.update()
            event_stack = self.stack.post(*events)
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
