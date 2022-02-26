#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 2022

@author: alberto
"""

from colorama import init, Fore, Back, Style
init(autoreset=True)


DEBUGMODE = True
COLOR = Fore.MAGENTA

def debug_print(string):
    if DEBUGMODE:
        print(COLOR + string) 
    
def unpack_list(obj, elements):
    if type(elements) == list:
        for element in elements:
            obj.append(element)
    else:
        obj.append(element)
        
    
class Finite_State_Machine:
    def __init__(self, FSM_name):
        self.name = FSM_name
        self.event_list = [] # so I can an Event as component?
        self.state_list = [] # so I can an State as component?
        self.event_state_table = None
        self.actual_state = None
        
    def __str__(self):
        return self.name
    
    def add_to_states(self, elements):
        unpack_list(self.state_list, elements)
        
    def pass_starting_state(self):
        for state in self.state_list:
            debug_print(state.name)
            if state.is_starting == True:
                self.actual_state = str(state)
                debug_print('Starting state: ' + str(state))
    
    def add_to_events(self, elements):
        unpack_list(self.event_list, elements)
    
    # def event_triggered(self, event):
    #     print('Triggered from ' + self.name + ' found: ' + '{:}'.format(event))
    
    def print_state_list(self):
        for state in self.state_list:
            print(str(state))
        print('')
    
    def print_event_list(self):
        for event in self.event_list:
            print(str(event))
        print('')
        
    # def check_events(self, pygame_event):
    #     for event in self.event_list:
    #         event.check_events(pygame_event)
    #         if event.triggered:
    #             debug_print('From ' + str(self) + ' found: ' + '{:}'.format(event))
    #             event.triggered = False
    
    def check_events(self, pygame_event):
        for event in self.event_list:
            event.check_events(pygame_event)
            if event.triggered:
                debug_print('From ' + str(self) + ' found: ' + '{:}'.format(event))
                event.triggered = False
    
    def check_table(self):
        debug_print(self.actual_state)
        for key,values in self.event_state_table.dictionary.items():
            debug_print(key)
            # I am somewhere here
            if key == self.actual_state:
                for event in self.event_list:
                    if event.triggered:
                        for value in values:
                            if str(event) == value[0]: 
                                debug_print(str(event) + 'moved from ' + self.actual_state)
                                self.actual_state = value[1]            
                    
                    # if event.triggered:
                    #     debug_print(str(event) + 'triggered passage of state')
                
    
class Event_State_Table:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def print_table(self):
        for key,values in self.dictionary.items():
            fmt = "State {}: " + (len(values)-1)*" {},"
            fmt += " {}"
            print(fmt.format(key, *values))
        print('')
 
    
class Event():
    def __init__(self, name, event_list, debug=True):
        self.name = name
        self.triggered = False
        
        self.event_list = []
        if type(event_list) == list:
            for event in event_list:
                self.event_list.append(event)         
        else:
            self.event_list = [event_list]
                                    
    def __str__(self):
        return self.name
            
    def print_list(self):
        for event in self.event_list:
            print('{:} is in the list'.format(event))
        print('')
    
    def check_events(self, pygame_event):
        # print('{:}'.format(pygame_event.key))
        for event in self.event_list:
            # print('Checking {:}'.format(event))
            if pygame_event.key == event:
                self.trigger_event(event)                
            
    def trigger_event(self, event):
        debug_print('From ' + self.name + ' found: ' + '{:}'.format(event))
        self.triggered = True
    
    
class State:    
    def __init__(self, name, is_starting=False):
        self.name = name
        self.is_starting = is_starting
        self.just_entered = True
        self.exit_signal = False
        
    def __str__(self):
        return self.name
        
    def enter_state(self):
        debug_print('Just entered in ' + self.name)
        self.just_entered = False
        
    def in_state(self):
        debug_print('Still in '  + self.name)
        
    def exit_state(self):
        debug_print('Exit ' + self.name)
        
    def run_state(self):
        if self.just_entered:
            self.enter_state()
        else:
            self.in_state()
        
        if self.exit_signal:
            self.exit_state()
