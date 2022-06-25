from enum import Enum, auto

from main import App

class State(Enum):
    state1 = auto()
    state2 = auto()
    state3 = auto()
                    
    def enter(self):
        print("Entering" + self.__name__)
        
    def run(self):
        pass
    
    def exit(self):
        print("Exiting" + self.__name__)

class FiniteStateMachine():
    def __init__(self):    
        self.actual_state = State.state1
        self.old_state = None
        self.running = False  
        
        print(1)
    
    #@classmethod
    #def initiate(cls):
        #cls.actual_state = cls.state1
        #cls.old_state = None
        #cls.running = False
    
    #@classmethod
    #def change_state(cls, new_state):
        #cls.old_state = cls.actual_state
        #cls.actual_state = new_state
    
    
        
    #def __call__(self):
        #if self.running == False:
            #self.enter()
        #else:
            #self.run()    

fsm = FiniteStateMachine()

#fsm = State.initiate()
#fsm.enter()




#class TestRun(App):
    #def __init__(self):
        #super.__init__()
        
    #def handle_events(self,event):
        #if event.type == pg.KEYDOWN and event.key == pg.K_a:
                    
#game = App()
#game.run()