class Game_Settings:
    
    def __init__(self):
        self.screen_width = 805 #x axis
        self.screen_height = 455 #y axis
        # state game
        self.flying = False
        self.game_over = False
        self.lives = 3
        
        self.ground_scroll = 0
        self.scroll_speed = 4 # the difference of the width between the 2 images and the time supposed to reset the screen ground
        
        self.pipe_gap = 130
