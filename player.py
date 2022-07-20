from dataclasses import dataclass

import pygame
from pygame.locals import *
from pygame import Vector2 as vec

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

@dataclass
class Physics:
    acceleration : float = 0.5
    friction : float = -0.12
    gravity : float = 0.5
    movement : vec = vec(1, 5)
    
    vel : vec = vec(0, 0)
    acc : vec = vec(0, 0)
    
    def move(self,  direction,  delta):
        self.acc = vec(0,  self.gravity)
        self.acc += self.acceleration * (direction  * self.movement.elementwise())
        self.acc += self.vel * self.friction
        self.vel += self.acc * delta
        position = self.vel + 0.5*self.acc * delta
        
        return position


class Player(pygame.sprite.Sprite):
    
    def __init__(self,  settings):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.sprites = Sequencer(*SpriteSheet("first_Experiment.png",  self.rect).get_strip())
        self.surface = self.sprites() 
        self.rect = self.surface.get_rect()
        self.settings = settings
        self.bounding_box = pygame.Rect(0, 0,  *self.settings['screen_size'])
        self.direction = vec(0, 0)
        self.position = vec(0, 0)
        self.physics = Physics()
        
    def handle_events(self, _):
        self.direction = vec(0, 0)
        event = pygame.key.get_pressed()
        
        if event[K_a]:
            self.direction = vec(-1, 0)
        elif event[K_d]:
            self.direction = vec(1, 0)
        elif event[K_w]:
            self.direction = vec(0, -1)
        elif event[K_s]:
            self.direction = vec(0, 1)
        
    def move(self):
        delta = 1
        self.position += self.physics.move(self.direction,  delta)
        self.rect.center = self.position
    
    def update(self):
        self.move()
        self.rect.clamp_ip(self.bounding_box)
        self.position = self.rect.center
        self.surface = self.sprites()
        
                    
class TestRun(App):
    def __init__(self):
        super().__init__()
        self.settings['FPS'] = 30
        self.player = Player(self.settings)
        self.player.settings = self.settings
        self.player.position = vec(*[p/2 for p in self.settings['screen_size']])
        
    def handle_events(self,event):
        self.player.handle_events(event)
        print(event)
                                        
    def update(self):
        self.player.update()
            
    def render(self):
        self.screen.blit(self.player.surface, self.player.rect)


game = TestRun()
game.run()
game.quit()
