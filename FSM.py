#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 2022

@author: alberto
"""


class Finite_State_Machine:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def event_triggered(self, event):
        print('From ' + self.name + ' ' + event.key)
    
    
class Event_State_Table:
    def __init__(self, name):
        pass
    
    
class Event(Finite_State_Machine):
    def __init__(self, name, event_list):
        self.name = name
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
                # trigger_event(self, event)
                print('From ' + self.name + ' found: ' + '{:}'.format(event))
    
    def trigger_event(self, event):
        print('From ' + self.name + ' ' + event.key)
        # super.event_triggered(event)
    
class State:
    just_entered = True
    exit_signal = False
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
    def enter_state():
        print('just entered')
        just_entered = False
        return just_entered
        
    def in_state():
        print('still in state')
        
    def exit_state():
        print('exit state')
        
    if just_entered:
        enter_state()
    else:
        in_state()
    
    if exit_signal:
        exit_state()
