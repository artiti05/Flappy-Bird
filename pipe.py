import pygame
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, gap):
        super().__init__()
        self.image = pygame.image.load('images\Pipe.png').convert_alpha()
        self.rect = self.image.get_rect()
        # position 1 from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y-int(gap/2)]
        if position == -1:
            self.rect.topleft = [x, y+int(gap/2)]
    
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        
        if self.rect.right < 0:
            self.kill()