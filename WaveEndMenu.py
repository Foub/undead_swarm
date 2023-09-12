import pygame

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# WaveEndMenu(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupScreen(self, screen, screen_width, shooter_game) * Sets up the buttons, and other UI elements for the screen
# SetupImages(self) * Called from WaveEnded when the wave ends. Sets up the images and location

# -[UPDATE FUNCTIONS BELOW]-
# update(self, mouse_pos, event) * Main update call, it's called every frame by shooter_game class update

# -[CHANGE FUNCTIONS BELOW]-
# WaveEnded(self) * Gets called at the end of the wave by the waves script (EndOfWave(self) function)
# NextWavePressed(self) * The player pressed the next wave button and this function is called.

# } END OF WaveEndMenu(Class)

# set up the WaveEndMenu class
class WaveEndMenu(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, shooter_game):
        super().__init__()

        # Functions that are called when the class is first created (game start)
        self.SetupScreen(screen, screen_width, shooter_game)

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupScreen(self, screen, screen_width, shooter_game):
        # Sets up the screen UI for later use (CALLED AT THE START OF THE GAME)
        self.WHITE = (255, 255, 255)
        self.click = False
        self.screen = screen
        self.screen_width = screen_width
        self.shooter_game = shooter_game
        self.waves = shooter_game.waves
        self.wave_end_padding = 40
        self.wave_kills_padding = 110

    def SetupImages(self):
        # Called from WaveEnded when the wave ends. Sets up the images and location

        # Wave End Message
        self.wave_end = pygame.font.Font(None, 70)
        self.wave_end_message = self.wave_end.render("Wave " + str(self.shooter_game.waves.wave_number - 1) + " completed!", True, self.WHITE)
        self.wave_end_location = ((self.screen_width / 2) - (self.wave_end_message.get_width() / 2), self.wave_end_padding) 

        # Wave Kills
        self.wave_kills_font = pygame.font.Font(None, 50)
        self.wave_kills_message = self.wave_kills_font.render("You had " + str(self.shooter_game.waves.wave_kills) + " zombie kills this wave!", True, self.WHITE)
        self.wave_kills_location = ((self.screen_width / 2) - (self.wave_kills_message.get_width() / 2), self.wave_kills_padding)

        # Next Wave Button
        self.next_wave_button_image = pygame.image.load("UI/next_wave_button.png").convert() # load the image and convert it to a Surface object
        self.next_wave_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.next_wave_button_rect = self.next_wave_button_image.get_rect()
        self.next_wave_button_rect.center = (self.screen_width / 2, self.wave_end_location[1] + 800)

        # Shadow click UI
        self.click_shadow_button_image = pygame.image.load("UI/click_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.click_shadow_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.click_shadow_button_rect = self.click_shadow_button_image.get_rect()
        self.click_shadow_button_image.set_alpha(200)

        # hover UI
        self.hover_shadow_button_image = pygame.image.load("UI/hover_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.hover_shadow_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.hover_shadow_button_rect = self.hover_shadow_button_image.get_rect()
        self.hover_shadow_button_image.set_alpha(60)

    # ====================================================================
    # ===================== [UPDATE FUNCTIONS BELOW] =====================

    def update(self, mouse_pos, event):
        # Player presses the left click down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click = True
        # Player released the left click
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click = False

        # NEXT WAVE BUTTON
        if self.next_wave_button_rect.collidepoint(mouse_pos):
            if self.click == True:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Player releases left click
                    self.shooter_game.change_game_screen(4) # Changing it to the game screen.
                else: # Player has left click down
                    self.screen.blit(self.click_shadow_button_image, self.next_wave_button_rect)
                    self.NextWavePressed()
            else:
                self.screen.blit(self.hover_shadow_button_image, self.next_wave_button_rect)
        else:
            self.screen.blit(self.next_wave_button_image, self.next_wave_button_rect)

    # ====================================================================
    # ===================== [CHANGE FUNCTIONS BELOW] =====================

    def WaveEnded(self):
        # Called when the wave is done, the waves script EndofWave(self) function calls this
        self.SetupImages()

    def NextWavePressed(self):
        # The player pressed the next wave button
        self.waves.NextWavePressed()
        self.shooter_game.NextWavePressed()
 
