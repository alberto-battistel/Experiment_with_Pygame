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

    def return_item(self):
        self.actual_item = next(self.generator)
        return self.actual_item
        
ex = Sequencer("1", "2", "3")
