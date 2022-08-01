import pygame
from pygame import Vector2 as vec

from main import App

map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,],
            ]

color = (100,  200,  150,  255)
rect_size = vec(32, 32)

def make_tile_image(rect_size):
    tile_image = pygame.Surface(rect_size)
    tile_image.fill(color)
    innerer_block = pygame.Surface(rect_size - vec(4, 4))
    innerer_color = tuple(min(c+50,  255) for c in color)
    innerer_block.fill(innerer_color)
    tile_image.blit(innerer_block,  (2, 2))
    return tile_image

class Tile(pygame.sprite.Sprite):
            def __init__(self,  image,  position):
                pygame.sprite.Sprite.__init__(self, self.containers)
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.move_ip(position)
                                
#group = pygame.sprite.Group()
#
#Tile.containers = group
#image = make_tile_image(rect_size)
#Tile(image,  (0, 0))



class TestWorld:
    def __init__(self, rect_size: vec,  map):
        self.rect_size = rect_size
        self.map = map
        self.map_size = vec(len(self.map),  len(self.map[0]))
        self.rect = pygame.Rect((0, 0), rect_size)
        self.make_surface()
        self.make_tile_type(Tile)
        self.generate_level()
        
    def make_surface(self):
        width = self.rect_size.x*self.map_size.x
        height = self.rect_size.y*self.map_size.y
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
    def make_tile_type(self,  tile_class):
#        self.tile = pygame.Surface(self.rect_size)
#        self.tile.fill(color)
#        innerer_block = pygame.Surface(self.rect_size - vec(4, 4))
#        innerer_color = tuple(min(c+50,  255) for c in color)
#        innerer_block.fill(innerer_color)
#        self.tile.blit(innerer_block,  (2, 2))
        
        self.image = make_tile_image(self.rect_size)
        self.tiles = pygame.sprite.Group()
        self.tile_class = tile_class
        self.tile_class.containers = self.tiles
        
          
    def generate_level(self):
        for row_number, row in enumerate(self.map):
            for col_number, col in enumerate(row):
                position = [col_number * self.rect_size.x,  row_number * self.rect_size.y]
                if col == 1:
                    print(position)
                    tile = self.tile_class(self.image,  position)
                    self.surface.blit(tile.image,  position)
                    

if __name__ == "__main__":
    
    class TestRun(App):
        def __init__(self):
            super().__init__()
            self.settings = {'screen_size': (16*32, 16*32),
                                    'FPS': 60,
                                    }
                                    
        def add_something(self):
            self.level = TestWorld(rect_size=rect_size, map=map)
                     
        def render(self):
            self.screen.blit(self.level.surface,  (0, 0))
    
    game = TestRun()
    game.start()
    game.run()
    game.quit()
