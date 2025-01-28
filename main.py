import pygame
import random
from pygame.locals import *
from pygame.sprite import Group
from settings import Game_Settings
from bird import Bird
from pipe import Pipe
#initialize the game with frames per iteration
pygame.init()
settings = Game_Settings()
clock = pygame.time.Clock()
# sounds
bg_music = pygame.mixer.Sound('sounds\SoundTrack.mp3')
bg_music.set_volume(0.07)
bg_music.play(loops = -1) # it means that it runs to infinity
###########
pipe_freq = 1500 #ms
last_spawned_pipe = pygame.time.get_ticks() # you can put - pipe_freq to avoid waiting for spawning
score = 0
pass_pipe = False
#text
font = pygame.font.Font('Pixeltype.ttf', 60)
color = (255, 255, 255) # white
def display_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 150
    flappy.rect.y = int(settings.screen_height/2) #same place where we have put it in the first place 
    settings.game_over = False
    settings.flying = False
def display_lives(lives, heart_image, x, y):
    for i in range(lives):
        screen.blit(heart_image, (x + i * (heart_image.get_width()/2), y))
    
#build a screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
#Name of the window
pygame.display.set_caption('WING JUMP')

bg_sky = pygame.image.load('images\Sky.jpg').convert()
bg_ground = pygame.image.load('images\Ground.jpg').convert()
heart_image = pygame.image.load('images\HHeart.png').convert_alpha()
# button #
button_image = pygame.image.load('images\Restart.png').convert()

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

button = Button(settings.screen_width//2 - 60, settings.screen_height//2 - 10, button_image)
#################
bird_group = Group()
pipe_group = Group()

flappy = Bird(150, int(settings.screen_height/2))
bird_group.add(flappy)

run = True
while run:
    screen.blit(bg_sky, (0,0))
    bird_group.draw(screen)
    bird_group.update(settings.flying, settings.game_over)
    pipe_group.draw(screen)
    
    screen.blit(bg_ground, (settings.ground_scroll , 370)) # before the collision to stop drawing the bird's wings
    # scoring system
        #    important    #
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and \
                bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and \
                pass_pipe == False:
            pass_pipe = True
        if pass_pipe:#equelevant to pass_pipe == True
            if bird_group.sprites()[0].rect.right > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    
    display_text(str(score), font, color, settings.screen_width//2 , 10)
    
    #check if there is a collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0 or flappy.rect.bottom >= 375:
        settings.lives -= 1
        if settings.lives <= 0:
            settings.game_over = True
        else:
            reset_game() # resetting the game without the score

    # check wether the bird has hit the ground
    if flappy.rect.bottom >= 370:
        settings.game_over = True
        settings.flying = False
        
    if settings.game_over == False and settings.flying == True:
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_spawned_pipe > pipe_freq:
            pipe_height = random.randint(-40, 55) # to random heights
            bottom_pipe = Pipe(settings.screen_width, int(settings.screen_height/2) + pipe_height, -1, settings.pipe_gap)#to start spawn after a bit
            top_pipe = Pipe(settings.screen_width, int(settings.screen_height/2) + pipe_height, 1, settings.pipe_gap)#y axis takes a height of range + or - 100 pixels
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_spawned_pipe = time_now

        settings.ground_scroll -= settings.scroll_speed # to move the ground
        if abs(settings.ground_scroll) > 45 : settings.ground_scroll = 0
    
        pipe_group.update(settings.scroll_speed)
    
    if settings.game_over == True:
        if button.draw() == True:
            settings.lives = 3
            score = 0
            reset_game()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not settings.flying and not settings.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                settings.flying = True
        if not settings.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN :
                flappy.flap()
    display_lives(settings.lives, heart_image, 0, 0)
    
    clock.tick(60) #fps
    pygame.display.update()
pygame.quit()