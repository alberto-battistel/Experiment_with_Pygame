import pygame
from pygame.math import Vector2 as vec

from main import App

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
        self.rect = pygame.Rect(0,0,100,100)
        self.position = vec(self.Rect.center)
        
    def move(self, vector):
        self.rect.move_ip(vector)
        
    def update(self):
        self.position = vec(self.Rect.center)
        displacement = vec(20,20)
        if (self.position + displacement) <= 500:
            self.move(displacement)
        else:
            self.self.Rect.center = vec(100,100)
        
class TestRun(App):
    def __init__(self):
        super.__init__()
        
    def update(self):
        Entity.update()
        
if __name__ == '__main__':
    
    rect = Entity()
    
    class TestRun(App):
        def __init__(self):
            super.__init__()
            
        def update(self):
            rect.update()    
                
    game = TestRun()
    game.run()
    game.quit()
    
        