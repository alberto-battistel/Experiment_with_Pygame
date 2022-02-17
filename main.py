import pygame

pygame.font.init()

screen_size = {'width':900, 
               'height':500,
               }

FPS = 60

WIN = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("First Game!")

run = True
while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
