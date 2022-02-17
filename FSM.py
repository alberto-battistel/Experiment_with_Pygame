

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
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
    def enter_state():
        print('just entered')
        just_entered = False
        
    def in_state():
        print('still in state')
        
    def exit_state():
        print('exit state')
