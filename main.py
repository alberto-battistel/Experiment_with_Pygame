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
    
    def set_caption(self):
        pygame.display.set_caption("FPS: {:.1f}".format(self.clock.get_fps()))
    
    def set_background(self):
        self.screen.fill((220, 220, 220))
                
    def update(self):
        pass
        
    def render(self):
        pass
    
    def quit(self):
        pygame.quit()
                        
    def run(self):
        while self.running:
            self.real_fps = self.clock.get_fps()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.set_background()
            self.set_caption()
            
            self.update()
            self.render()
            
            self.clock.tick(settings['FPS'])
            
    
if __name__ == '__main__':
    game = App()
    game.run()
    game.quit()
