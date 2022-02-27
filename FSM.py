#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 2022

@author: alberto
"""

from enum import Enum, auto
from colorama import init, Fore, Back, Style

init(autoreset=True)

DEBUGMODE = True
COLOR = Fore.MAGENTA

def debug_print(string):
    if DEBUGMODE:
        print(COLOR + string) 

class FSM_Status(Enum):
    STARTING = 'Starting condition of the FSM'
    ENTER_STATE = 'FSM enters a new state'
    REMAIN_IN_STATE = 'FSM remains in the actual state'
    EXIT_STATE = 'FSM exits the actual state'
    
def unpack_list(obj, elements):
    if type(elements) is list:
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
        self.actual_state = ''
        self.target_state = ''
        self.triggered_events = []
        self.FSM_status = FSM_Status.STARTING
        
    def __str__(self):
        return self.name
    
    def add_to_states(self, elements):
        unpack_list(self.state_list, elements)
        
    def find_starting_state(self):
        for state in self.state_list:
            if state.is_starting == True:
                self.target_state = str(state)
                debug_print('Starting state: ' + self.target_state)
                return self.target_state
        # if no particular state was designed then take the first of the table    
        first_state = self.event_state_table.first_state()
        debug_print('Starting state from the table: ' + first_state)
        self.target_state = first_state
        return self.target_state
    
    def add_to_events(self, elements):
        unpack_list(self.event_list, elements)
    
    def print_state_list(self):
        for state in self.state_list:
            print(str(state))
        print('')
    
    def print_event_list(self):
        for event in self.event_list:
            print(str(event))
        print('')
        
    def check_events(self, pygame_event):
        triggered_events = []
        for event in self.event_list:
            event.check_events(pygame_event)
            if event.triggered:
                triggered_events.append(str(event))
                debug_print('From ' + str(self) + ' found: ' + '{:}'.format(event))
                event.triggered = False
        self.triggered_events = triggered_events    
        return triggered_events
    
    def find_actual_state(self):
        for state,event_combo in self.event_state_table.items():
            if state == self.actual_state:
                return state,event_combo
    
    def check_table(self):
        triggered_events = self.triggered_events
        if len(triggered_events) != 0:
            state,event_combo = self.find_actual_state()
            for (event,target_state) in event_combo:
                for triggered in triggered_events:
                    if event == triggered:
                        self.target_state = target_state
                        self.FSM_status = FSM_Status.ENTER_STATE
                        debug_print('From: ' + state + ' >-' + triggered + '-> ' + target_state)
                        return target_state
        else:
            self.FSM_status = FSM_Status.REMAIN_IN_STATE
            debug_print('No event triggered')
            return ''
        
    def run_FSM(self):
        self.check_table()
        
        if self.FSM_status == FSM_Status.ENTER_STATE:
            self.change_state()
        elif self.FSM_status == FSM_Status.REMAIN_IN_STATE:
            self.remain_in_state()
             
    def change_state(self):
        debug_print('Change state: ' + self.actual_state + ' -> ' + self.target_state)
        self.actual_state = self.target_state
        self.target_state = ''
        
    def remain_in_state(self):
        debug_print('Remain in: ' + self.actual_state)
    
    def exit_state(self):
        pass
        
class Event_State_Table:
    def __init__(self, event_state_dictionary):
        for state,event_combo in event_state_dictionary.items():
            if type(event_combo) is not list:
                event_state_dictionary[state] = [event_combo]
                for comb in event_combo:
                    if type(comb) is not type(()):
                        pass
                    
        self.event_state_dictionary = event_state_dictionary
    
    def items(self):
        return self.event_state_dictionary.items()
    
    def first_state(self):
        list_of_states = list(self.event_state_dictionary.keys())
        return list_of_states[0]
    
    def print_table(self):
        for key,values in self.event_state_dictionary.items():
            fmt = "State {}: " + (len(values)-1)*" {},"
            fmt += " {}"
            print(fmt.format(key, *values))
        print('')
 
    
class Event():
    def __init__(self, name, event_list, debug=True):
        self.name = name
        self.triggered = False
        
        self.event_list = []
        if type(event_list) is list:
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
        for event in self.event_list:
            if pygame_event.key == event:
                self.trigger_event(event)                
            
    def trigger_event(self, event):
        # debug_print('From ' + self.name + ' found: ' + '{:}'.format(event))
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
