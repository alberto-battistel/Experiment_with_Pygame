import pygame
#from pygame.locals import *

pygame.init()

settings = {'screen_size': (600, 400),
            'FPS': 60,
            }
            
pygame.init()
        
settings = settings
screen = pygame.display.set_mode(settings['screen_size'])
clock = pygame.time.Clock()
running = True

def set_caption():
    pygame.display.set_caption("FPS: {:.1f}".format(clock.get_fps()))

keys = {pygame.K_a: lambda: print("left"),
pygame.K_d: lambda: print("right"), 
pygame.K_w: lambda: print("up"), 
pygame.K_s: lambda: print("down"),
pygame.K_SPACE: lambda: print("space"),
            pygame.K_LEFT: lambda: print("left"), 
            pygame.K_RIGHT: lambda: print("right"), 
            pygame.K_UP: lambda: print("up"), 
            pygame.K_DOWN: lambda: print("down"), }

def get_inputs():
    inputs = pygame.key.get_pressed()
    return inputs
    
inputs = []

while running:
    real_fps = clock.get_fps()
    
    events = pygame.event.get()
#    print("number of events: " + str(len(events)))
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    inputs = get_inputs()
    for key,  value in keys.items():
        if inputs[key]:
            value()        
    
    set_caption()
        
    pygame.display.flip()
    
    clock.tick(settings['FPS'])
