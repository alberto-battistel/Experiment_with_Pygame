import pygame
from pygame.locals import *

pygame.init()

settings = {'screen_size': (600, 400),
            'FPS': 10,
            }
            
pygame.init()
        
settings = settings
screen = pygame.display.set_mode(settings['screen_size'])
clock = pygame.time.Clock()
running = True

def set_caption():
    pygame.display.set_caption("FPS: {:.1f}".format(clock.get_fps()))

while running:
    real_fps = clock.get_fps()
    
    events = pygame.event.get()
    print("number of events: " + str(len(events)))
    for event in events:
        print(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
#    set_caption()
#    
#    self.update()
#    self.render()

    set_caption()
        
    pygame.display.flip()
    
    clock.tick(settings['FPS'])
