from enum import Enum, auto
import types





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
            
    @classmethod
    def add_attr(cls, attr_name, value):
        setattr(cls, attr_name,  value.copy())
    
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
        return self.name + ": " + str(self.value)
    
    def __hash__(self):
        return self.value
    
    def enter(self):
        pass
        print("Entering " + self.name)
        
    def run(self):
        pass
        print("Running " + self.name)
    
    def exit(self):
        pass
        print("Exiting " + self.name)
        
    def redefine(self, fun):
        fun_name = fun.__name__
        print(self)
        if hasattr(self, fun_name):
            setattr(self, fun_name, types.MethodType(fun, self))
        else:
            print(fun_name,  "is not implemented")


if __name__ == '__main__':
    from pygame import Vector2 as vec
    from inputs_mapping import Events
    player_states = ["Idle", 
                        "In_air", 
                        "Jump", 
                        "Duck", 
                        "Move", ]

    bindings_directions = {
                                Events.Left: vec(-1,  0), 
                                Events.Right: vec(1,  0), 
                                Events.Up: vec(0,  -1), 
                                Events.Down: vec(0,  1), 
                                }

    States.add_attr("bindings_directions", bindings_directions)
    [States(s) for s in player_states]
    
#    # different ways to initialize a State    
#    States("a")
#    States("b")
#    [States(p) for p in["c", "d"]]
#
#    # different ways to override a function
#    def run(obj_instance):
#        if obj_instance.count == 0:
#            print("something")
#        
#    States.a.run = types.MethodType(run, States.a)
#
#    def run(obj_instance):
#        if obj_instance.count == 0:
#            print("something")
#
#    States.b.redefine(run)
#
#    @States.c.redefine
#    def run(self):
#        print("new")
#
#    States.add_attr("u", {3: 34})
