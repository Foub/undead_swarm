import pygame

# THIS SCRIPT IS FOR THE MAIN MENU AND CONTAINS THE FOLLOWING BUTTONS 
#              1) CHARACTER (Grayed out because the character feature hasn't been added yet)
#              2) PLAY GAME (Stars the game)
#              3) ACHIEVEMENTS (Grayed out because the character and achievements feature hasn't been added yet)
#              4) OPTIONS (Will open the options menu to change the settings)
#              5) EXIT BUTTON (Will close the game loop and exit the game application)

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# MainMenu(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupImages(self) * Setting up all the images, and rect required for this menu UI
# SetupScreen(self, shooter_game, window, window_width, BLACK) * Setting up the important variables used in this script.

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * The main update function for this script, gets called every frame by the ShooterGame script

# } END OF MainMenu(Class)

# set up the MainMenu class
class MainMenu(pygame.sprite.Sprite):
    def __init__(self, window, window_width, BLACK, shooter_game):
        super().__init__()

        # These are called at the start of the game when the MainMenu class is first created
        self.SetupImages()
        self.SetupScreen(shooter_game, window, window_width, BLACK)   

    # ====================================================================
    # ====================== [SETUP FUNCTIONS BELOW] =====================

    def SetupImages(self):
        # Setting up all the images, and rect required for this menu UI

        # Character Button
        self.character_button_image = pygame.image.load("UI/character_button.png").convert() # load the image and convert it to a Surface object
        self.character_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.character_button_rect = self.character_button_image.get_rect()

        # play game Button
        self.play_game_button_image = pygame.image.load("UI/play_game_button.png").convert() # load the image and convert it to a Surface object
        self.play_game_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.play_game_button_rect = self.play_game_button_image.get_rect()

        # achievements Button
        self.achievements_button_image = pygame.image.load("UI/achievements_button.png").convert() # load the image and convert it to a Surface object
        self.achievements_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.achievements_button_rect = self.achievements_button_image.get_rect()

        # options Button
        self.options_button_image = pygame.image.load("UI/options_button.png").convert() # load the image and convert it to a Surface object
        self.options_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.options_button_rect = self.options_button_image.get_rect()

        # exit Button
        self.exit_button_image = pygame.image.load("UI/exit_button.png").convert() # load the image and convert it to a Surface object
        self.exit_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.exit_button_rect = self.exit_button_image.get_rect()

        self.click_shadow_button_image = pygame.image.load("UI/click_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.click_shadow_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.click_shadow_button_rect = self.click_shadow_button_image.get_rect()
        self.click_shadow_button_image.set_alpha(200)

        self.hover_shadow_button_image = pygame.image.load("UI/hover_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.hover_shadow_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.hover_shadow_button_rect = self.hover_shadow_button_image.get_rect()
        self.hover_shadow_button_image.set_alpha(60)

        self.disabled_button_image = pygame.image.load("UI/hover_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.disabled_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.disabled_button_rect = self.disabled_button_image.get_rect()
        self.disabled_button_image.set_alpha(150)

    def SetupScreen(self, shooter_game, window, window_width, BLACK):
        # Setting up the important variables used in this script.
        self.shooter_game = shooter_game
        self.window = window
        self.window_width = window_width
        self.BLACK = BLACK   
        self.click = False # Is the left click button down 
        self.first_padding = 300 # between the top screen and where the character button is lcoation
        self.buttons_padding = 100 # the padding the remainding buttons will be from each other, top down

        # Sets up the locaiton of the UI elements
        self.character_button_rect.center = (int(self.window_width / 2), int(self.first_padding))
        self.play_game_button_rect.center = (self.character_button_rect.center[0], self.character_button_rect.center[1] + self.buttons_padding)
        self.achievements_button_rect.center = (self.play_game_button_rect.center[0], self.play_game_button_rect.center[1] + self.buttons_padding)
        self.options_button_rect.center = (self.achievements_button_rect.center[0], self.achievements_button_rect.center[1] + self.buttons_padding)
        self.exit_button_rect.center = (self.options_button_rect.center[0], self.options_button_rect.center[1] + self.buttons_padding)

    # ====================================================================
    # ====================== [UPDATE FUNCTIONS BELOW] ====================
    
    def update(self, mouse_pos, event):
        # Updates with every frame (Called by shooter_game every frame)
        self.window.fill(self.BLACK)
        self.window.blit(self.character_button_image, self.character_button_rect)
        self.window.blit(self.play_game_button_image, self.play_game_button_rect)
        self.window.blit(self.achievements_button_image, self.achievements_button_rect)
        self.window.blit(self.options_button_image, self.options_button_rect)
        self.window.blit(self.exit_button_image, self.exit_button_rect)

        # Player presses the left click down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click = True
        
        # CHARACTER BUTTON
        self.window.blit(self.character_button_image, self.character_button_rect)
        self.window.blit(self.disabled_button_image, self.character_button_rect)
        # PLAY GAME BUTTON
        if self.play_game_button_rect.collidepoint(mouse_pos):
            if self.click:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Player releases left click
                    self.shooter_game.ChangeGameScreen(4) # Changing it to the game screen.
                else: # Player has left click down
                    self.window.blit(self.click_shadow_button_image, self.play_game_button_rect)
            else:
                self.window.blit(self.hover_shadow_button_image, self.play_game_button_rect)
        else:
            self.window.blit(self.play_game_button_image, self.play_game_button_rect)
        # ACHIEVEMENTS BUTTON
        self.window.blit(self.achievements_button_image, self.achievements_button_rect)
        self.window.blit(self.disabled_button_image, self.achievements_button_rect)
        # OPTIONS BUTTON
        self.window.blit(self.options_button_image, self.options_button_rect)
        self.window.blit(self.disabled_button_image, self.options_button_rect)
        # EXIT BUTTON
        if self.exit_button_rect.collidepoint(mouse_pos):
            if self.click:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Player releases left click
                    self.shooter_game.ExitGame()
                else: # Player has left click down
                    self.window.blit(self.click_shadow_button_image, self.exit_button_rect)
            else:
                self.window.blit(self.hover_shadow_button_image, self.exit_button_rect)
        else:
            self.window.blit(self.exit_button_image, self.exit_button_rect)

        # Player released the left click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click = False

    










