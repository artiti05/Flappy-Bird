import pygame
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image1 = pygame.image.load('images\Bird1.png').convert_alpha()
        self.image2 = pygame.image.load('images\Bird2.png').convert_alpha()
        self.image3 = pygame.image.load('images\Bird3.png').convert_alpha()
        self.images = [self.image1, self.image2, self.image3]
        self.index = 0
        self.image = self.images[self.index]
        # self.image = pygame.transform.scale(self.Before_image, (width, height))  # Scale the image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] # for the pos which is changing
        # bird's physics
        self.velocity = 0
        self.animation_speed = 0.2
        self.counter = 0
        self.clicked = False
        #sounds
        self.jump_sounds = pygame.mixer.Sound('sounds\Jumping.mp3')
        self.jump_sounds.set_volume(0.08)
        # cooldown period in milliseconds
        self.flap_cooldown = 150
        self.last_flap_time = pygame.time.get_ticks()
    def flap(self):
        current_time = pygame.time.get_ticks()
        
        if self.clicked == False and (current_time - self.last_flap_time > self.flap_cooldown):
            self.clicked = True
            self.velocity = -8
            self.jump_sounds.play()
            self.last_flap_time = current_time
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and (current_time - self.last_flap_time > self.flap_cooldown):# the get pressed return a sequence containing the truth values of every mouse botton
            self.clicked == True
            self.velocity = -8 # when updating it makes the bottom of the rect decreases for a bit
            self.jump_sounds.play()
            self.last_flap_time = current_time
        if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        if pygame.key.get_pressed()[pygame.K_SPACE] == 0:
                self.clicked = False
    def update(self, flying, game_over):
        # gravity
        if flying == True:
            self.velocity += 0.5
            if self.velocity > 15:
                self.velocity = 15 # maximum speed 
            if self.rect.bottom < 370:
                self.rect.y += int(self.velocity) # for y cordinates to be integers
        if game_over == False:    # jump
            # if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:# the get pressed return a sequence containing the truth values of every mouse botton
            #     self.clicked == True
            #     self.velocity = -5 # when updating it makes the bottom of the rect decreases for a bit
            #     self.jump_sounds.play()
            # if pygame.mouse.get_pressed()[0] == 0:
            #     self.clicked = False
            # if pygame.key.get_pressed()[pygame.K_SPACE] == 0:
            #     self.clicked = False

            self.counter += self.animation_speed
            if self.counter >= 1:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index] 
            # rotation 
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
            self.rect = self.image.get_rect(center = self.rect.center)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            self.rect = self.image.get_rect(center = self.rect.center)
