import pygame
from pygame.locals import *

from main import App

class Sequencer():
    def __init__(self, *sprites):
        self.sprites = sprites[:]
        self.max_length = len(self.sprites)
        self.generator = self._return_item()
        self.actual_item = self.sprites[0]
        
    def _return_item(self):
        index = 0
        while True:
            yield self.sprites[index]
            yield self.sprites[index]
            yield self.sprites[index]
            index = (index+1)%self.max_length

    def __call__(self):
        self.actual_item = next(self.generator)
        return self.actual_item
  
  
class SpriteSheet():
    def __init__(self,  asset_name,  rect):
        self.asset_name = asset_name
        self.rect = rect.copy()
        self.sheet = self.import_image()
        self.images = self.get_strip()
            
    def import_image(self):
        sheet = pygame.image.load(self.asset_name).convert_alpha()
        return sheet
    
    def get_strip(self):
        sheet_width = self.sheet.get_width()
        step = self.rect.width
        images = []
        for x_position in range(0,  sheet_width, step):
            self.rect.x = x_position
            image = pygame.Surface(self.rect.size,  pygame.SRCALPHA)
            image.blit(self.sheet, (0, 0), self.rect)
            images.append(pygame.transform.scale2x(pygame.transform.scale2x(image)))
    #        images.append(image)
        return images

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.sprites = Sequencer(*SpriteSheet("first_Experiment.png",  self.rect).get_strip())
        self.surface = self.sprites() 
        self.rect = self.rect = self.surface.get_rect()
        self.settings = None
        
    def handle_events(self,  event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.rect.move_ip(-20, 0)
                if self.rect.left < 0:
                    self.rect.left = 0
            elif event.key == K_d:
                self.rect.move_ip(20, 0)
                if self.rect.right > self.settings['screen_size'][0]:
                    self.rect.right = self.settings['screen_size'][0]
            elif event.key == K_w:
                self.rect.move_ip(0, -20)
                if self.rect.top < 0:
                    self.rect.top = 0
            elif event.key == K_s:
                self.rect.move_ip(0, 20)
                if self.rect.bottom > self.settings['screen_size'][1]:
                    self.rect.bottom = self.settings['screen_size'][1]
    
    def update(self):
        self.surface = self.sprites()
        
                    
class TestRun(App):
    def __init__(self):
        super().__init__()
        self.settings['FPS'] = 30
        self.player = Player()
        self.player.settings = self.settings
#        Sequencer(*SpriteSheet("first_Experiment.png",  pygame.Rect(0, 0, 16, 16)).get_strip())
#        self.surface = self.sprites()
#        self.rect = self.surface.get_rect()
        
    def handle_events(self,event):
        self.player.handle_events(event)
                                        
    def update(self):
        self.player.update()
            
    def render(self):
        self.screen.blit(self.player.surface, self.player.rect)


game = TestRun()
game.run()
game.quit()
