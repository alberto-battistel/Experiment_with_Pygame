import pygame

pygame.init()

settings = {'screen_size': (600, 400),
            'FPS': 60,
            }
            
class App:
    def __init__(self):
        pygame.init()
        
        self.settings = settings
        self.screen = pygame.display.set_mode(settings['screen_size'])
        self.clock = pygame.time.Clock()
        self.running = True
    
    def set_caption(self):
        pygame.display.set_caption("FPS: {:.1f}".format(self.clock.get_fps()))
    
    def set_background(self):
        self.screen.fill((220, 220, 220))
                
    def handle_inputs(self, inputs):
        pass
    
    def get_inputs(self):
        self.inputs = pygame.key.get_pressed()
        return self.inputs
    
    def update(self):
        pass
        
    def render(self):
        pass
    
    def quit(self):
        pygame.quit()
                        
    def run(self):
        while self.running:
            self.real_fps = self.clock.get_fps()
            
            events = pygame.event.get()
#            print("number of events: " + str(len(events)))
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                
            inputs = self.get_inputs()
            self.handle_inputs(inputs)
            
            self.set_background()
            self.set_caption()
            
            self.update()
            self.render()
            
            pygame.display.flip()
            
            self.clock.tick(settings['FPS'])
            
    
if __name__ == '__main__':
    game = App()
    game.run()
    game.quit()
