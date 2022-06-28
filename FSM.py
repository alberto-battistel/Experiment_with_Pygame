from enum import Enum

import pygame
from pygame.locals import *

from main import App

class State(Enum):
    consonants = 'consonants'
    vocals = 'vocals'
    foreign = 'foreign letters'
                    
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
        
is_vocal = Condition( 'a', 'e', 'i', 'o',  'u')
is_foreign = Condition('j','k', 'w', 'y', 'x')
is_consonant = Condition('q', 'r', 't', 'z', 'p')

class FiniteStateMachine():
    table = {State.consonants: [{State.vocals: is_vocal}, 
                                        {State.foreign: is_foreign} ], 
                    State.vocals: [{State.foreign: is_foreign},
                                        {State.consonants: is_consonant}, ],  
                    State.foreign: [{State.vocals: is_vocal}, 
                                        {State.consonants: is_consonant}, ]
                                        }
                    
    def __init__(self):    
        self.actual_state = State.consonants
        self.old_state = None
        self.running = False  
    
    def start_FSM(self):
       self.actual_state.enter()
    
    def trigger_transition(self, new_state: State):
        self.old_state = self.actual_state
        self.old_state.exit()
        self.actual_state = new_state
        self.actual_state.enter()
        
    def handle_events(self, event):
        target_states = self.table[self.actual_state]
        for case in target_states:
            for state, condition in case.items():
                if condition(event):
                    print(event)
                    self.trigger_transition(state)
                    return
        print(event)
        self.actual_state.run()
                    


#if __name__ == "main":                
events = "aeppwo"
fsm = FiniteStateMachine()
fsm.start_FSM()
for event in events:
    fsm.handle_events(event)
    

class TestRun(App):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Verdana', 60)
        self.string_2_render = None
        
    def handle_events(self,event):
        if event.type == KEYDOWN:
            key = chr(event.key)
            self.string_2_render = self.font.render(key, True, (255,0,0))
            
    def render(self):
        if self.string_2_render is not None:
            self.screen.blit(self.string_2_render, [int(s/2) for s in self.settings['screen_size']])
            

                    
game = TestRun()
game.run()
game.quit()

