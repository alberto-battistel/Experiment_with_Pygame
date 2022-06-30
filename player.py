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
            index = (index+1)%self.max_length

    def __call__(self):
        self.actual_item = next(self.generator)
        return self.actual_item
        

def sprite_loader(resource):
    return pygame.image.load(resource).convert_alpha()
        
        
ex = Sequencer("1", "2", "3")

def import_image(asset_name):
    sheet = pygame.image.load(asset_name).convert_alpha()
    return sheet
    
def get_strip(sheet, rect):
    sheet_width = sheet.get_width()
    step = rect.width
    images = []
    for x_position in range(0,  sheet_width, step):
        rect.x = x_position
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        images.append(pygame.transform.scale2x(pygame.transform.scale2x(image)))
#        images.append(image)
    return images

#def image_at(self, rectangle, colorkey = None):
#        "Loads image from x,y,x+offset,y+offset"
#        rect = pygame.Rect(rectangle)
#        image = pygame.Surface(rect.size).convert()
#        image.blit(self.sheet, (0, 0), rect)
#        if colorkey is not None:
#            if colorkey is -1:
#                colorkey = image.get_at((0,0))
#            image.set_colorkey(colorkey, pygame.RLEACCEL)
#        return image
#    # Load a whole bunch of images and return them as a list
#def images_at(self, rects, colorkey = None):
#    "Loads multiple images, supply a list of coordinates" 
#    return [self.image_at(rect, colorkey) for rect in rects]
#
#rects = [pygame.Rect(x, 0,  16, 16) for x in range(0, 128)]

#sheet = import_image("first_Experiment.png")
#images = get_strip(sheet, pygame.Rect(0, 0, 16, 16))
#sprites = Sequencer(*images)

class TestRun(App):
    def __init__(self):
        super().__init__()
        self.sheet = import_image("first_Experiment.png")
        self.images = get_strip(self.sheet, pygame.Rect(0, 0, 16, 16))
        self.sprites = Sequencer(*self.images)
#        self.surface = self.sprites()
        self.surface = self.sheet
        self.rect = self.surface.get_rect()
        
    def handle_events(self,event):
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
                    
                    
#    def update(self):
#        self.surface = self.sprites()
            
    def render(self):
        self.screen.blit(self.surface, self.rect)


game = TestRun()
game.run()
game.quit()
