#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 2022

@author: alberto
"""

class Finite_State_Machine:
    def __init__(self):
        pass
    
    
class Event_State_Table:
    def __init__(self):
        pass
    
    
class Event:
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
    
    
class State:
    just_entered = True
    exit_signal = False
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
    def enter_state(self):
        print('just entered')
        just_entered = False
        return just_entered
        
    def in_state(self):
        print('still in state')
        
    def exit_state(self):
        print('exit state')
        
    if just_entered:
        enter_state()
    else:
        in_state()
    
    if exit_signal:
        exit_state()
