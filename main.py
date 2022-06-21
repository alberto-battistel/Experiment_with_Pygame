import pygame

pygame.font.init()

settings = {'screen_size': (1280, 800),
            'FPS': 60,
            }

screen = pygame.display.set_mode(settings['screen_size'])

clock = pygame.time.Clock()

run = True
while run:
		clock.tick(settings['FPS'])
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				
		pygame.display.set_caption("FPS: {:.1f}".format(clock.get_fps()))
