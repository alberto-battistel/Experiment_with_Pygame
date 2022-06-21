import pygame

pygame.init()

settings = {'screen_size': (1280, 800),
            'FPS': 60,
            }
            
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(settings['screen_size'])
        self.clock = pygame.time.Clock()
        self.running = True
            
    def run(self):
        while self.running:
            self.clock.tick(settings['FPS'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((220, 220, 220))
            pygame.display.set_caption("FPS: {:.1f}".format(self.clock.get_fps()))
    pygame.quit()
     
if __name__ == '__main__':
    App().run()
