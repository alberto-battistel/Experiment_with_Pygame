from enum import IntEnum,  auto

import pygame as pg

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
    
class Events(IntEnum):
    On_ground = auto()
    On_wall = auto()
    
keys_bindings = {
                            Inputs.Left: [pg.K_a, pg.K_LEFT],
                            Inputs.Right: [pg.K_d,  pg.K_RIGHT], 
                            Inputs.Up: [pg.K_w, pg.K_UP], 
                            Inputs.Down: [pg.K_s, pg.K_DOWN],
                            Inputs.Pause: pg.K_p,
                            Inputs.Shot: pg.K_SPACE,
                            }
