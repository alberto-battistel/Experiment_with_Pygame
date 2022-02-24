import pygame

import FSM

pygame.font.init()

screen_size = {'width':1280, 
               'height':800,
               }

FPS = 10

WIN = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("First Game!")

clock = pygame.time.Clock()

FSM_test = FSM.Finite_State_Machine('FSM_test')
FSM_event = FSM.Event('input', event_list=[pygame.K_LEFT, pygame.K_RIGHT])

event_list = []

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                print(event.key)
                # FSM_event.check_events(event)
            elif event.key == pygame.K_RIGHT:
                print(event.key)
    event_list.append(event) 
                
pygame.quit()

for ii,event in enumerate(event_list):
    if event.type == pygame.KEYDOWN:
        print(ii)
