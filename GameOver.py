import pygame
import math

# This is the game over screen that pops up when the player dies.

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# ShooterGame(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupUITechnical(self, shooter_game, window, BLACK, WHITE, screen_width) * Sets up all technical stuff for the game over UI
# SetupGameOver(self) * Sets up the UI locations at the start of the game.

# -[UPDATE FUNCTIONS BELOW]-
# update(self, mouse_pos, event) * Called every frame by ShooterGame once the player is dead and the blood animation is done after a delay

# -[ACTION FUNCTIONS BELOW]-
# SetTotalKills(self) *Gets called when the player dies and sets the total kills the player had that game

# -[OUTSIDE CALL FUNCTIONS BELOW]-
# GameEnd(self) * Gets called in the BloodSplat method on MainCharacter after the blood effect animation is done

# =========== [END OF TABLE OF CONTENTS] ==========
# =================================================

class GameOver(pygame.sprite.Sprite):
    def __init__(self, shooter_game, window, BLACK, WHITE, screen_width):
        super().__init__()
        # Gets called when the game first starts.
        self.SetupUITechnical(shooter_game, window, BLACK, WHITE, screen_width)
        self.SetupUILocations()

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupUITechnical(self, shooter_game, window, BLACK, WHITE, screen_width):    
        # Sets up the UI elements, and other technical stuff
        self.game_done = False # If true the game over screen will come up
        self.shooter_game = shooter_game
        self.screen_width = screen_width
        self.game_over_title_padding = 100
        self.game_over_padding = 75
        self.window = window
        self.BLACK = BLACK
        self.WHITE = WHITE
        self.total_kills = 0
        self.click = False # Is the left click button down 

    def SetupUILocations(self):
        #Sets up the UI elements, and locations at the start of the game.

        # exit Button
        self.exit_button_image = pygame.image.load("UI/exit_button.png").convert() # load the image and convert it to a Surface object
        self.exit_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.exit_button_rect = self.exit_button_image.get_rect()
        self.exit_button_padding = 400

        # Game Over Message
        self.game_over_title_font = pygame.font.Font(None, 70)
        self.game_over_title = self.game_over_title_font.render("Game Over!", True, self.WHITE)
        self.game_over_title_location = ((self.screen_width / 2) - (self.game_over_title.get_width() / 2), self.game_over_title_padding)

        # total kills
        self.game_over_font = pygame.font.Font(None, 50)
        self.game_over_message = self.game_over_font.render("You had 0 zombie kills total!", True, self.WHITE)
        self.game_over_location = ((self.screen_width / 2) - (self.game_over_message.get_width() / 2), self.game_over_title_location[1] + self.game_over_padding)

        # exit button location
        self.exit_button_rect.center = (self.game_over_location[0] + self.game_over_message.get_width() / 2, self.game_over_location[1] + self.exit_button_padding)

        # Click shadow UI setup
        self.click_shadow_button_image = pygame.image.load("UI/click_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.click_shadow_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.click_shadow_button_rect = self.click_shadow_button_image.get_rect()
        self.click_shadow_button_image.set_alpha(200)

        # Hover shadow UI setup
        self.hover_shadow_button_image = pygame.image.load("UI/hover_shadow_button.png").convert() # load the image and convert it to a Surface object
        self.hover_shadow_button_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.hover_shadow_button_rect = self.hover_shadow_button_image.get_rect()
        self.hover_shadow_button_image.set_alpha(60)

    # ====================================================================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================

    def update(self, mouse_pos, event): 
        # Called every frame by ShooterGame once the player is dead and the blood animation is done after a delay.
        self.window.fill(self.BLACK)
        self.window.blit(self.game_over_title, self.game_over_title_location)
        self.window.blit(self.game_over_message, self.game_over_location)

        # Player presses the left click down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click = True

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

    # ====================================================================
    # ==================== [ACTION FUNCTIONS BELOW] ======================

    def SetTotalKills(self): 
        # Gets called when the player dies and sets the total kills the player had that game.
        self.game_over_message = self.game_over_font.render("You had " + str(self.total_kills) + " zombie kills total!", True, self.WHITE)
        self.game_over_location = ((self.screen_width / 2) - (self.game_over_message.get_width() / 2), self.game_over_title_location[1] + self.game_over_padding)

    # ====================================================================
    # =================== [OUTSIDE CALL FUNCTIONS BELOW] =================

    def GameEnd(self): 
        # Gets called in the BloodSplat method on MainCharacter after the blood effect animation is done
        self.total_kills = self.shooter_game.waves.total_kills
        self.SetTotalKills()
        self.game_done = True
        self.shooter_game.GameOverMusic()
