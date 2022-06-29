from enum import Enum,  auto

import pygame
from pygame.locals import *

from main import App

class State(Enum):
    idle = auto()
    jump = auto()
    duck = auto()
    move = auto()
                    
    def enter(self):
        print("Entering " + self.name)
        
    def run(self):
        print("Running " + self.name)
    
    def exit(self):
        print("Exiting " + self.name)


class Condition():
    def __init__(self,  *matching_events):
        self.matching_events = matching_events
        
    def __call__(self,  event):
        if event in self.matching_events:
            return True
        else:
            return False 

is_on_ground = Condition(K_SPACE)
is_jumping = Condition(K_w)
is_moving = Condition(K_a,  K_d)
is_ducking = Condition(K_s)

class FiniteStateMachine():
    table = {State.idle: [
                                    {State.jump: is_jumping}, 
                                    {State.move: is_moving}, 
                                    {State.duck: is_ducking}, 
                                    {State.idle: is_on_ground},
                                    ], 
                    State.duck: [
                                    {State.idle: is_on_ground},
                                    {State.duck: is_ducking}, 
                                     ],  
                    State.move: [
                                    {State.idle: is_on_ground}, 
                                    {State.jump: is_jumping}, 
                                    {State.duck: is_ducking}, 
                                    {State.move: is_moving},
                                    ], 
                    State.jump: [
                                    {State.idle: is_on_ground},  
                                    {State.jump: is_jumping},
                                    ],                 
                                }
                    
    def __init__(self):    
        self.actual_state = State.idle
        self.old_state = None
        self.running = False  
    
    def start_FSM(self):
       self.actual_state.enter()
    
    def trigger_transition(self, new_state: State):
        self.old_state = self.actual_state
        self.old_state.exit()
        self.actual_state = new_state
        self.actual_state.enter()
        
    def handle_event(self, event):
        target_states = self.table[self.actual_state]
        for case in target_states:
            for state, condition in case.items():
                if condition(event.key):
                    print(event.key)
                    if state != self.actual_state:
                        self.trigger_transition(state)
                    else:
                        self.actual_state.run()
        return self.actual_state.name


#if __name__ == "main":                

fsm = FiniteStateMachine()
fsm.start_FSM()
    

class TestRun(App):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Verdana', 60)
        self.string_2_render = None
        
    def handle_events(self,event):
        if event.type == KEYDOWN:
            state = fsm.handle_event(event)
#            key = chr(event.key)
            self.string_2_render = self.font.render(state, True, (255,0,0))
            
    def render(self):
        if self.string_2_render is not None:
            self.screen.blit(self.string_2_render, [int(s/2) for s in self.settings['screen_size']])
            

                    
game = TestRun()
game.run()
game.quit()

