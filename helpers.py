from math import copysign
from enum import IntEnum,  auto

import pygame as pg
from pygame import Surface


sign = lambda x: copysign(1, x)


def bind_keys_to_inputs(inputs:pg.key.ScancodeWrapper, keys_bindings:dict):
    active_inputs = []
    for key, value in keys_bindings.items():
        if isinstance(value, list):
            for v in value:
                if inputs[v]:
                   active_inputs.append(key)
                   break
        else:
            if inputs[value]:
                   active_inputs.append(key)
    return active_inputs

class Inputs(IntEnum):
    Left = auto()
    Right = auto()
    Up = auto()
    Down = auto()
    Pause = auto()
    Shot = auto()
    
keys_bindings = {
                            Inputs.Left: [pg.K_a, pg.K_LEFT],
                            Inputs.Right: [pg.K_d,  pg.K_RIGHT], 
                            Inputs.Up: [pg.K_w, pg.K_UP], 
                            Inputs.Down: [pg.K_s, pg.K_DOWN],
                            Inputs.Pause: pg.K_p,
                            Inputs.Shot: pg.K_SPACE,
                            }
                            

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
        sheet = pg.image.load(self.asset_name).convert_alpha()
        return sheet
    
    def get_strip(self):
        sheet_width = self.sheet.get_width()
        step = self.rect.width
        images = []
        for x_position in range(0,  sheet_width, step):
            self.rect.x = x_position
            image = Surface(self.rect.size,  pg.SRCALPHA)
            image.blit(self.sheet, (0, 0), self.rect)
            images.append(pg.transform.scale2x(pg.transform.scale2x(image)))
    #        images.append(image)
        return images
