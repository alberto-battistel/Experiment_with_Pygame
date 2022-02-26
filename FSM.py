#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 2022

@author: alberto
"""

from colorama import init, Fore, Back, Style
init(autoreset=True)


DEBUGMODE = False
COLOR = Fore.MAGENTA

def debug_print(string):
    if DEBUGMODE:
        print(COLOR + string) 
    
    
class Finite_State_Machine:
    def __init__(self, FSM_name):
        self.name = FSM_name
        self.event_list = [] # so I can an Event as component?
        
    def __str__(self):
        return self.name
    
    # def event_triggered(self, event):
    #     print('Triggered from ' + self.name + ' found: ' + '{:}'.format(event))
    
    def print_event_list(self):
        for event in self.event_list:
            print(event.name)
    
    def check_events(self, pygame_event):
        for event in self.event_list:
            event.check_events(pygame_event)
            if event.triggered:
                debug_print('From ' + self.name + ' found: ' + '{:}'.format(event))
                event.triggered = False
    
    def check_table(self, table):
        pass
                
    
class Event_State_Table:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def print_table(self):
        for key,values in self.dictionary.items():
            fmt = "State {}: " + (len(values)-1)*" {},"
            fmt += " {}"
            print(fmt.format(key, *values))
 
    
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
            
        self.debug = debug
                        
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
    def __init__(self, name):
        self.name = name
        self.just_entered = True
        self.exit_signal = False
        
    def __str__(self):
        return self.name
        
    def enter_state(self):
        print('just entered')
        self.just_entered = False
        
    def in_state():
        print('still in state')
        
    def exit_state():
        print('exit state')
        
    def run_state(self):
        if self.just_entered:
            self.enter_state()
        else:
            self.in_state()
        
        if self.exit_signal:
            self.exit_state()
