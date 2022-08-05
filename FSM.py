from enum import Enum,  auto
from collections import deque

import pygame as pg
#from pygame.locals import *

from main import App

from inputs_mapping import Events,  keys_bindings,  bind_keys_to_inputs 
from components import EventStack

class State(Enum):
    Idle = auto()
    Jump = auto()
    Duck = auto()
    Move = auto()
                    
    def enter(self):
        print("Entering " + self.name)
        
    def run(self):
        print("Running " + self.name)
    
    def exit(self):
        print("Exiting " + self.name)
 

class Condition():
    def __init__(self,  *matching_conditions):
        self.matching_conditions = matching_conditions
    
#    def __call__(self,  event_stack):
#        for key,  value in self.matching_conditions.items():
#            if isinstance(value,  list):
#                return any([event_stack[key][v] for v in value])
#            else:
#                return event_stack[key][value]
                
    def __call__(self,  event_stack):
        return any([p in event_stack for p in self.matching_conditions])


class FiniteStateMachine():
    transitions_table = {}
    
    def __init__(self):    
        self.old_state = None
        self.running = False  
        self.stack = deque(maxlen=4)
    
    def start_FSM(self,  starting_state):
       self.actual_state = starting_state
       self.actual_state.enter()
       self.stack.appendleft(self.actual_state)
    
    def trigger_transition(self, new_state: State):
        self.old_state = self.actual_state
        self.old_state.exit()
        self.actual_state = new_state
        self.actual_state.enter()
        self.stack.appendleft(self.actual_state)
        
    def handle_event(self, event_stack):
        target_states = self.transitions_table[self.actual_state]
        for case in target_states:
            for state, condition in case.items():
                if condition(event_stack):
                    if state != self.actual_state:
                        self.trigger_transition(state)
                    else:
                        self.actual_state.run()
        return self.actual_state.name
    
    
if __name__ == "__main__":                

    is_on_ground = Condition(Events.Shot)
    is_jumping = Condition(Events.Up)
    is_moving = Condition(Events.Left, Events.Right)
    is_ducking = Condition(Events.Down)

    fsm = FiniteStateMachine()
    fsm.transitions_table = {State.Idle: [
                                        {State.Jump: is_jumping}, 
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
                                        {State.Jump: is_jumping}, 
                                        {State.Duck: is_ducking}, 
                                        {State.Move: is_moving},
                                        ], 
                        State.Jump: [
                                        {State.Idle: is_on_ground},  
                                        {State.Jump: is_jumping},
                                        ],                 
                                    }

    fsm.start_FSM(State.Idle)
        

    class TestRun(App):
        def __init__(self):
            super().__init__()
            self.font1 = pg.font.SysFont('Verdana', 60)
            self.font2 = pg.font.SysFont('Verdana', 30)
            self.state_to_render = self.font1.render("", True, (255,0,0))
            self.stack_to_render = 5*[self.font2.render("", True, (255,0,0))]
            self.stack = EventStack()
        
        def handle_events(self, inputs,  events):
            self.stack.reset()
            events = bind_keys_to_inputs(inputs,  keys_bindings)
            event_stack = self.stack.post(*events)
            
            state = fsm.handle_event(event_stack)
            stack = [state.name for state in fsm.stack]
            
            self.state_to_render = self.font1.render(state, True, (255,0,0))
            self.stack_to_render = [self.font2.render(state, True, (255,0,255)) for state in stack]
               
        def render(self):
            # actual state
            surface = self.state_to_render
            width,  height = surface.get_size()
            position = [1/4*self.settings['screen_size'][0], 1/2*self.settings['screen_size'][1]]
            position[0] = round(position[0]-width/2)
            position[1] = round(position[1]-height/2)
            self.screen.blit(surface, position)
                
            # stack
            position = [3/4*self.settings['screen_size'][0], 1/4*self.settings['screen_size'][1]]
            for surface in self.stack_to_render:
                height = surface.get_height()
                position[1] += height
                self.screen.blit(surface, position)
                

                        
    game = TestRun()
    game.start()
    game.run()
    game.quit()

