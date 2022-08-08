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

class Events(IntEnum):
    Left = auto()
    Right = auto()
    Up = auto()
    Down = auto()
    Pause = auto()
    Shot = auto()
    On_ground = auto()
    On_wall = auto()
    On_air = auto()
    
keys_bindings = {
                            Events.Left: [pg.K_a, pg.K_LEFT],
                            Events.Right: [pg.K_d,  pg.K_RIGHT], 
                            Events.Up: [pg.K_w, pg.K_UP], 
                            Events.Down: [pg.K_s, pg.K_DOWN],
                            Events.Pause: pg.K_p,
                            Events.Shot: pg.K_SPACE,
                            }
