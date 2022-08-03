from enum import Enum,  auto
from collections import deque

import pygame
from pygame.locals import *

from main import App

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
    def __init__(self,  *matching_events):
        self.matching_events = matching_events
    
    def __call__(self,  inputs):
        return any([inputs[me] for me in self.matching_events])


is_on_ground = Condition(K_SPACE)
is_jumping = Condition(K_w)
is_moving = Condition(K_a,  K_d)
is_ducking = Condition(K_s)

class FiniteStateMachine():
    table = {State.Idle: [
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
        
    def handle_event(self, inputs):
        target_states = self.table[self.actual_state]
        for case in target_states:
            for state, condition in case.items():
                if condition(inputs):
                    if state != self.actual_state:
                        self.trigger_transition(state)
                    else:
                        self.actual_state.run()
        return self.actual_state.name
    
    
#if __name__ == "main":                

fsm = FiniteStateMachine()
fsm.start_FSM(State.Idle)
    

class TestRun(App):
    def __init__(self):
        super().__init__()
        self.font1 = pygame.font.SysFont('Verdana', 60)
        self.font2 = pygame.font.SysFont('Verdana', 30)
        self.state_to_render = self.font1.render("", True, (255,0,0))
        self.stack_to_render = 5*[self.font2.render("", True, (255,0,0))]
    
    def handle_inputs(self, inputs):
        state = fsm.handle_event(inputs)
        stack = [state.name for state in fsm.stack]
        
        self.state_to_render = self.font1.render(state, True, (255,0,0))
        self.stack_to_render = [self.font2.render(state, True, (255,0,255)) for state in stack]
        
#        if event.type == KEYDOWN:
#            state = fsm.handle_event(event)
#            stack = [state.name for state in fsm.stack]
#            
#            self.state_to_render = self.font1.render(state, True, (255,0,0))
#            self.stack_to_render = [self.font2.render(state, True, (255,0,255)) for state in stack]

    
    def handle_events(self,event):
        if event.type == KEYDOWN:
            state = fsm.handle_event(event)
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

