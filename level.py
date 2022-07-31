import pygame
from pygame import Vector2 as vec

from main import App

map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,],
            ]

color = (255,  255,  0,  255)
rect_size = vec(32, 32)

class TestWorld:
    def __init__(self, rect_size: vec,  map):
        self.rect_size = rect_size
        self.map = map
        self.map_size = vec(len(self.map),  len(self.map[0]))
        self.rect = pygame.Rect((0, 0), rect_size)
        self. make_surface()
        self.make_block_type()
        self.generate_level()
        
    def make_surface(self):
        width = self.rect_size.x*self.map_size.x
        height = self.rect_size.y*self.map_size.y
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0, 128))
        
    def make_block_type(self):
        self.block = pygame.Surface(self.rect_size)
        self.block.fill(color)
    
    def generate_level(self):
        for row_number, row in enumerate(self.map):
            for col_number, col in enumerate(row):
                position = [col_number * self.rect_size.x,  row_number * self.rect_size.y]
                if col == 1:
                    print(position)
                    self.surface.blit(self.block,  position)
                    

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
