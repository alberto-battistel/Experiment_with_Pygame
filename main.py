import pygame

pygame.font.init()

screen_size = {'width':1280, 
			   'height':800,
			   }

FPS = 60

WIN = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("First Game!")

clock = pygame.time.Clock()

run = True
while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				
		pygame.display.set_caption("FPS: {:.1f}".format(clock.get_fps()))
