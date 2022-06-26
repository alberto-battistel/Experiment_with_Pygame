from enum import Enum

#from main import App

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

class FiniteStateMachine():
    table = {State.consonants: [{State.vocals: ['a', 'e', 'i', 'o',  'u', ]}, 
                                        {State.foreign: ['j','k', 'w', 'y', 'x',  ]}, ], 
                    State.vocals: [{State.foreign: ['j','k', 'w', 'y', 'x',  ]},
                                        {State.consonants: ['q', 'r', 't', 'z', 'p', ]}, ],  
                    State.foreign: [{State.vocals: ['a', 'e', 'i', 'o',  'u', ]}, 
                                        {State.consonants: ['q', 'r', 't', 'z', 'p', ]}, ]
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
            for key, value in case.items():
                if event in value:
                    print(event)
                    self.trigger_transition(key)
                    return
        print(event)
        self.actual_state.run()
                    
                
events = "aeppwo"
fsm = FiniteStateMachine()
fsm.start_FSM()
for event in events:
    fsm.handle_events(event)
    


 
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



#fsm = State.initiate()
#fsm.enter()




#class TestRun(App):
    #def __init__(self):
        #super.__init__()
        
    #def handle_events(self,event):
        #if event.type == pg.KEYDOWN and event.key == pg.K_a:
                    
#game = App()
#game.run()
