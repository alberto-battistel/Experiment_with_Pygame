from enum import Enum, auto
import types


class State(Enum):
    Idle = auto()
    In_air = auto()
    Jump = auto()
    Duck = auto()
    Move = auto()

#    def __init__(self,  _):
#        self.count = 0
#        self.bindings_directions = None
        
    def enter(self):
        pass
#        print("Entering " + self.name)
        
    def run(self):
        pass
#        print("Running " + self.name)
    
    def exit(self):
        pass
#        print("Exiting " + self.name)


class States:
    members = []
    _value = 0
    
    @classmethod
    @property
    def value(cls):
        cls._value += 1
        return cls._value
    
    @classmethod
    def add_name(cls,  instance):
            setattr(cls, instance.name,  instance)
    
    def __eq__(self,  value):
        if type(value) == str:
            return str(self.value)== value
        elif type(value) == int:
            return self.value == value
    
    def __init__(self,  name):
        self.name = name
        self.value = self.value
        self.count = 0
        self.members.append(self)
        self.add_name(self)
                
    def __call__(self):
        return self.value
        
    def __repr__(self):
        return str(self.value)
        
    def enter(self):
        pass
        print("Entering " + self.name)
        
    def run(self):
        pass
        print("Running " + self.name)
    
    def exit(self):
        pass
        print("Exiting " + self.name)
        
    def redefine(self, fun_name, fun):
        if hasattr(self, fun_name):
            setattr(self, fun_name, types.MethodType(run, States.a))
        else:
            print(fun_name,  "is not implemented")
        
States("a")
States("b")
[States(p) for p in["c", "d"]]

def run(obj_instance):
    if obj_instance.count == 0:
        print("something")
    
States.a.run = types.MethodType(run, States.a)

def run(obj_instance):
    if obj_instance.count == 0:
        print("something")

States.b.redefine("run",  run)
