import pygame
from pygame import mixer
import MainCharacter as main_character
import MainMenu as main_menu
import WaveEndMenu as wave_end_menu
import GameOver as game_over
import Waves as waves

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# ShooterGame(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupMouseAndKeys(self) * Mouse and keys related
# SetupFonts(self) * Sets up fonts, colors etc...
# SetupMessages(self) * Sets up the variables needed for wave start, and limits messages
# SetupMenus(self) * Sets up any variables needed for game menu, main menu, and wave done menus
# SetupClasses(self) * Sets up any classes (instantiate) that is needed for the game. (Character class, waves, main menu)
# SetupPlayerArmor(self) *UI and drop image*
# SetupHealthBars(self) *UI and UI above player/enemy*
# SetupStaminaBars(self) *UI and UI above player*
# SetupBoost(self) *UI and boost drops*
# SetupWeaponUI(self) * All of the weapon UI related stuff at the bottom of the screen
# SetupGunImages(self) *UI and gun drops* (Also contains muzzle sprites setup)
# SetupSounds(self) 
# SetupTintScreen(self) *used when player dies and screen tints*

# -[UPDATE FUNCTIONS BELOW]-
# UpdateGameScreen(self) *game screen is open, updates most things used in game screen including sprites*
# UpdateWave(self) *called when game screen is open, updates enemy sprites, boost drop sprites and blood splat sprites*
# UpdateGameMenu(self) *Main menu is open, it's detecting player clicks*
# UpdateEndWaveMenu(self, event) *wave ended, and the wave end menu is called here until player goes to next wave*
# UpdateGameOverMenu(self) *player died, updates the game over menu screen*
# UpdateTintTransparency(self) *player died, once blood effects over this is called to tint the screen until game over screen comes up*
# UpdateHealthBar(self, position_x, position_y, health, max_health, player_UI) *updates all health bars (top left, above player, above enemies)*
# UpdateStaminaBar(self, position_x, position_y, stamina, max_stamina, player_UI) *updates top left stamina bar, and stamina bar above player*
# UpdatePlayerArmorUI(self, player_armor) *updates players armor UI top left*
# UpdateBoostUI(self) *updates boost UI top left*
# UpdateMuzzle(self) *updates muzzle sprites if player fired recently*

# -[CHANGE FUNCTIONS BELOW]-
# WaveStartWarning(self, message) *wave start message is being displayed*
# ChangeGameScreen(self, screen_type) *this method will change the game screen depending on parameters*
# OpenEndWaveMenu(self) *this opens the end wave screen intitially*
# StartMuzzleFlash(self, location, weapon_index, muzzle_image, muzzle_rect)
# ExitGame(self) *player chose to exit the game, this closes the game loop and the program*

# -[TIMER / MESSAGE FUNCTIONS BELOW]-
# EscapeCooldownTimer(self) *this is a timer after the player presses escape button, used for menu screen*
# StartLimitsMessage(self, message) *called when player runs out of ammo, this message is displayed also when player tries to shoot without ammo*

# -[SOUND / MUSIC FUNCTIONS BELOW]-
# GameMusic(self) *calls game music*
# GameOverMusic(self) *calls game over music*
# PlayerHitSound(self)
# KnifeAttackSound(self)
# HandgunAttackSound(self)
# ShotgunAttackSound(self)
# Mp4AttackSound(self)
# DeadSound(self) *called when player or enemies die, its blood splat sound*
# OnOffSound(self, on) *turns all sound/music on or off*
# ZombieAttackSound(self)
# ZombieHitSound(self)

# -[OUTSIDE CALL FUNCTIONS BELOW]-
# NextWavePressed(self) * Player pressed the "next wave" button, on the WaveEndMenu script. This function is called

# -[GAME LOOP BELOW]-
# while this.running *game loop*
# } END OF ShooterGame(Class)


# =========== [END OF TABLE OF CONTENTS] ==========
# =================================================

# initialize pygame
pygame.init()

# initialize the sound system in pygame to allow sound files to be used
mixer.init()

# set up the window
window_width = 1920
window_height = 1080
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Undead Swarm")
top_left_corner = (0, 0)
background_image = pygame.image.load("other_sprites/grass_background.png")
center = window.get_rect().center

# Set up the clock
clock = pygame.time.Clock()
current_time = 0.0

class ShooterGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.running = True # The game will run once it hits the game loop

        # Setting up
        self.SetupMouseAndKeys() # Sets up anything needed for mouse and keys
        self.SetupFonts() # Sets up fonts and colors
        self.SetupMessages() # Sets up the variables needed for wave start, and limits messages
        self.SetupMenus() # Sets up any variables needed for game menu, main menu, and wave done menus
        self.SetupClasses() # Sets up any classes (instantiate) that is needed for the game. (Character class, waves, main menu)
        self.SetupPlayerArmor() # Setting up the armor bars for the players UI top left and armor drop images
        self.SetupHealthBars() # Setting up the health bars for the player and enemies and UI top left
        self.SetupStaminaBars() #Setting up the stamina bar above players head and UI top left
        self.SetupBoost() # Setting up boost UI top left buffs and boost item drop images
        self.SetupWeaponUI() # All of the weapon UI related stuff at the bottom of the screen
        self.SetupGunImages() # Draws the gun icon images at the bottom of the screen
        self.SetupSounds() # Setup the sound files to be called later
        self.SetupTintScreen() # Sets up the tint screen UI for if the player dies the screen tints then goes to game over screen
        
    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupMouseAndKeys(self):
        # Mouse and keys related
        self.escape_cooldown_duration = 60 # 1 second because 60 fps 
        self.escape_timer = 0 # current time left on escape cooldown
        self.escape_key_down = False # Used to make the escape key menu button smooth
        self.mouse_pos = pygame.mouse.get_pos() # Current mouse position

    def SetupFonts(self):
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Fonts
        self.ammo_font = pygame.font.Font(None, 32)
        self.limit_font = pygame.font.Font(None, 36)
        self.wave_start_font = pygame.font.Font(None, 70)

    def SetupMessages(self):
        # Wave Start
        self.wave_starting_message = "" # The message that is displayed at the top of the screen at the start of the wave (Starts empty)
        self.wave_starting_message_timer = 0 # How long before the message is displayed
        self.wave_starting_message_padding = 150 # The padding from the top of the screen
        self.wave_starting_message_location = (window_width / 2, self.wave_starting_message_padding)
        self.wave_starting_message_duration = 120 # This should be 2 second because the game runs 60 frames per second.
        self.wave_starting_message_width = 0

        # Limits message
        self.limits_message = "" # The message shown to the player (shows not enough ammo and related messages)
        self.limits_message_timer = 0 # When this hits 0 it removes the message from the screen
        self.limits_message_padding = 70 # How far above the characters location the message will appear
        self.limits_message_duration = 60 # This should be 1 second because the game runs 60 frames per second.
        self.limits_message_location = (0,0) # The location on the screen where the message will appear
        self.message_width = 0 # This width gets updated each time a message gets created.

    def SetupMenus(self):
        # Menus and Game Screen
        self.game_menu = False # 1 index
        self.main_menu_screen = False # 2 index
        self.wave_done_menu = False # 3 index
        self.game_screen = False # 4 index
        self.ChangeGameScreen(1) # Method used to change the screen

        # Game over menu
        self.transparent_current = 0
        self.transparent_increment_original = 1
        self.transparent_increment = self.transparent_increment_original # This increment will change
        self.transparent_increment_change1 = 15 # Transparency increment doubles at this alpha value
        self.transparent_increment_ratio1 = 3 # How much the transparent increment will change (multiplied by this number) to make transparency increase with time.
        self.transparent_increment_change2 = 40 # Transparency increment doubles again at this alpha value
        self.transparent_increment_ratio2 = 6 # How much the transparent increment will change (multiplied by this number) to make transparency increase with time.
        self.transparent_max = 256
        

    def SetupClasses(self):
        # create the character sprite and add it to the group
        self.all_sprites = pygame.sprite.Group()
        self.character = main_character.Character(center, self, window_width, window_height)
        self.all_sprites.add(self.character)

        # Waves script
        self.waves = waves.Waves(self.character, window_width, window_height, self) # Created the waves class
        self.character.SetupWaveClass(self.waves) # Adds the wave class to the MainCharacter script.

        # main menu
        self.main_menu = main_menu.MainMenu(window, window_width, self.BLACK, self) # created the MainMenu class instance

        # wave end menu
        self.wave_end_menu = wave_end_menu.WaveEndMenu(window, window_width, self) # Creating the wave end menu class instance

        # Game Over screen
        self.game_over_menu = game_over.GameOver(self, window, self.BLACK, self.WHITE, window_width)

    def SetupPlayerArmor(self):
        # Sets up the UI for the armor blue squares
        self.player_armor1_location = (40, 35) # square 1
        self.player_armor2_location = (65, 35) # square 2
        self.player_armor3_location = (90, 35) # square 3
        self.player_armor4_location = (115, 35) # square 4
        self.player_armor5_location = (140, 35) # square 5

        # Full Armor Square
        self.armor_image = pygame.image.load("UI/Armor/armor_square.png").convert() 
        self.armor_image.set_colorkey((255, 255, 255)) # set the white color to be transparent

        # Half Armor Square
        self.half_armor_image = pygame.image.load("UI/Armor/armor_square_half.png").convert() 
        self.half_armor_image.set_colorkey((255, 255, 255)) # set the white color to be transparent

        # Assigning the square images to the rect locations
        self.armor_rect1 = self.armor_image.get_rect()
        self.armor_rect1.center = self.player_armor1_location
        self.armor_rect2 = self.armor_image.get_rect()
        self.armor_rect2.center = self.player_armor2_location
        self.armor_rect3 = self.armor_image.get_rect()
        self.armor_rect3.center = self.player_armor3_location
        self.armor_rect4 = self.armor_image.get_rect()
        self.armor_rect4.center = self.player_armor4_location
        self.armor_rect5 = self.armor_image.get_rect()
        self.armor_rect5.center = self.player_armor5_location

        # Setup armor drop sprite
        self.armor_drop_image = pygame.image.load("Character/Armor/armor_drop.png").convert() 
        self.armor_drop_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.armor_drop_rect = self.armor_drop_image.get_rect()

    def SetupHealthBars(self):
        # Below is the health bars that appear above player and enemies when hit
        self.health_bar_width, self.health_bar_height = 100, 10
        self.health_color = (255, 0, 0)  # red
        self.health_UI_color = (30, 30, 30)  # gray
        self.health_padding = 50 # Space above characters location

        # Setting up the health bar in the top left for the player
        self.player_health_bar_width, self.player_health_bar_height = 200, 20
        self.player_health_color = (28, 158, 28)  # green
        self.player_health_UI_color = (71, 10, 10)  # dark red almost black
        self.player_health_location = (30, 50)

    def SetupStaminaBars(self):
        # Stamina bar above players head when being used
        self.stamina_bar_width, self.stamina_bar_height = 100, 10
        self.stamina_color = (247, 228, 201)  # whitish color
        self.stamina_UI_color = (71, 10, 10)  # darker color
        self.stamina_padding = 50 # Space above characters location

        # Stamina bar UI in the top left corner for the player
        self.player_stamina_bar_width, self.player_stamina_bar_height = 200, 20
        self.player_stamina_color = (247, 228, 201)  # whitish color
        self.player_stamina_UI_color = (71, 10, 10)  # darker color
        self.player_stamina_location = (30, 75)

    def SetupBoost(self):
        # Below is the boost images loaded for the buff icon and for the drop images.
        # ORANGE (DOUBLE-DAMAGE)
        self.orange_boost_image = pygame.image.load("Boosts/orange_boost.png").convert() 
        self.orange_boost_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.orange_boost_rect = self.orange_boost_image.get_rect()

        self.orange_boostUI_image = pygame.transform.scale(self.orange_boost_image, (self.orange_boost_image.get_width() // 1.7, self.orange_boost_image.get_height() // 1.7))

        # RED (LIFE REGEN)
        self.red_boost_image = pygame.image.load("Boosts/red_boost.png").convert() 
        self.red_boost_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.red_boost_rect = self.red_boost_image.get_rect()

        self.red_boostUI_image = pygame.transform.scale(self.red_boost_image, (self.red_boost_image.get_width() // 1.7, self.red_boost_image.get_height() // 1.7))

        # BLUE (UNLIMITED AMMO)
        self.blue_boost_image = pygame.image.load("Boosts/blue_boost.png").convert() 
        self.blue_boost_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.blue_boost_rect = self.blue_boost_image.get_rect()

        self.blue_boostUI_image = pygame.transform.scale(self.blue_boost_image, (self.blue_boost_image.get_width() // 1.7, self.blue_boost_image.get_height() // 1.7))

        # PURPLE (INCREASED MOVEMENT SPEED)
        self.purple_boost_image = pygame.image.load("Boosts/purple_boost.png").convert() 
        self.purple_boost_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.purple_boost_rect = self.purple_boost_image.get_rect()

        self.purple_boostUI_image = pygame.transform.scale(self.purple_boost_image, (self.purple_boost_image.get_width() // 1.7, self.purple_boost_image.get_height() // 1.7))

        # The boost image buff top left below stamina bar (set to orange boost as default)
        self.boost_UI_location = (40, 110)
        self.boost_UI_rect = self.orange_boostUI_image.get_rect() # Orange is the same size as all the other boosts so we only have to make 1 rect
        self.boost_UI_rect.center = self.boost_UI_location

    def SetupWeaponUI(self):
        # UI Elements
        self.weapon_slot_padding = 5
        self.weapon_slot_image = pygame.image.load("UI/PNG/Cell01.png")

        self.ammo_height_ratio = .80 # This is used to determine how far above the gun UI the ammo UI will be

        # Setting up the 4 weapon UI slots at the bottom of the screen to hold the weapon UIs
        self.weapon_slot1_rect = self.weapon_slot_image.get_rect()
        self.weapon_slot1_rect.bottomleft = ((window_width / 2) - (self.weapon_slot_image.get_width() * 2) - (self.weapon_slot_padding * 1.5), window_height - self.weapon_slot_padding)

        self.weapon_slot2_rect = self.weapon_slot_image.get_rect()
        self.weapon_slot2_rect.bottomleft = (self.weapon_slot1_rect.bottomright[0] + self.weapon_slot_padding, self.weapon_slot1_rect.bottomright[1])

        self.weapon_slot3_rect = self.weapon_slot_image.get_rect()
        self.weapon_slot3_rect.bottomleft = (self.weapon_slot2_rect.bottomright[0] + self.weapon_slot_padding, self.weapon_slot2_rect.bottomright[1])

        self.weapon_slot4_rect = self.weapon_slot_image.get_rect()
        self.weapon_slot4_rect.bottomleft = (self.weapon_slot3_rect.bottomright[0] + self.weapon_slot_padding, self.weapon_slot3_rect.bottomright[1])

        # Setting up the image for the highlight UI that shows the player which weapon they have selected.
        self.weapon_highlight_square = pygame.image.load("UI/weapon_highlight_square.png").convert() 
        self.weapon_highlight_square.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.weapon_highlight_rect = self.weapon_highlight_square.get_rect()

    def SetupGunImages(self):
         # The method for drawing the gun images at the bottom of the screen
        # Also includes the ground item versions of the guns.

        # Knife image bottom of screen
        self.knife_image = pygame.image.load("UI/knife_icon.png").convert() 
        self.knife_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.knife_rect = self.knife_image.get_rect()
        self.knife_rect.center = self.weapon_slot1_rect.center

        # Handgun image bottom of screen
        self.handgun_image = pygame.image.load("UI/handgun_icon.png").convert()
        self.handgun_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.handgun_rect = self.handgun_image.get_rect()
        self.handgun_rect.center = self.weapon_slot2_rect.center

        # Handgun drop image
        self.handgun_drop = pygame.image.load("UI/handgun_icon.png").convert() 
        self.handgun_drop.set_colorkey((255, 255, 255)) # set the white color to be transparent

        # Shotgun image bottom of screen
        self.shotgun_image = pygame.image.load("UI/shotgun_icon.png").convert() 
        self.shotgun_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.shotgun_rect = self.shotgun_image.get_rect()
        self.shotgun_rect.center = self.weapon_slot3_rect.center

        # Shotgun drop image
        self.shotgun_drop = pygame.image.load("UI/shotgun_icon.png").convert() 
        self.shotgun_drop.set_colorkey((255, 255, 255)) # set the white color to be transparent

        # MP4 image bottom of screen
        self.mp4_image = pygame.image.load("UI/mp4_icon.png").convert() 
        self.mp4_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.mp4_rect = self.mp4_image.get_rect()
        self.mp4_rect.center = self.weapon_slot4_rect.center

        # MP4 drop image
        self.mp4_drop = pygame.image.load("UI/mp4_icon.png").convert() 
        self.mp4_drop.set_colorkey((255, 255, 255)) # set the white color to be transparent

        # Muzzle Sprites (used for gunfire effect when shooting a bullet (Also holds location for bullet to spawn))
        self.muzzle_image = None
        self.muzzle_rect = None
        self.muzzle_time_duration = 20
        self.muzzle_timer = 0

    def SetupSounds(self):
        # Below sets up the sound files used in the game and sets the default volume.

        # Music
        self.game_music = mixer.Sound("sounds/game_music.mp3")
        self.game_music.set_volume(0.04) # Volume is too loud for this clip so its being set to 4% volume
        self.game_over_music = mixer.Sound("sounds/game_over_music.mp3")
        self.game_over_music.set_volume(0.05)

        # Player weapon, and other sounds.
        self.knife_sound = mixer.Sound("sounds/attack_knife.mp3")
        self.knife_sound.set_volume(0.10)
        self.handgun_sound = mixer.Sound("sounds/attack_handgun.mp3")
        self.handgun_sound.set_volume(0.05)
        self.shotgun_sound = mixer.Sound("sounds/attack_shotgun.mp3")
        self.shotgun_sound.set_volume(0.10)
        self.mp4_sound = mixer.Sound("sounds/attack_mp4.mp3")
        self.mp4_sound.set_volume(0.10)
        self.player_hit = mixer.Sound("sounds/player_hit.mp3")
        self.player_hit.set_volume(0.10)

        # Zombie related sounds
        self.zombie_attack = mixer.Sound("sounds/Zombie/zombie_attack.mp3")
        self.zombie_attack.set_volume(0.10)
        self.zombie_dead = mixer.Sound("sounds/Zombie/zombie_dies.mp3")
        self.zombie_dead.set_volume(0.10)
        self.zombie_hit = mixer.Sound("sounds/Zombie/zombie_hit.mp3")
        self.zombie_hit.set_volume(0.10)

    def SetupTintScreen(self):
        # Sets up the tint screen for when the game's over
        self.tint_screen_image = pygame.image.load("Effects/tint_screen.png").convert() 
        self.tint_screen_rect = self.tint_screen_image.get_rect()
        self.tint_screen_image.set_alpha(0) # Setting transparency to 100% (invisible) and it will slowly turn black

    # ====================================================================
    # ===================== [UPDATE FUNCTIONS BELOW] =====================

    def UpdateGameScreen(self):
        # Game Screen is opened. [At the same time as UpdateWave]

        # updates sprites update methods.  
        this.all_sprites.update(keys, event)        
    
        # draw the players character if hes not dead
        if this.character.dead == False: # Character not dead
            this.all_sprites.draw(window)
        elif this.character.blood_splat_current_frame < this.character.blood_splat_frames: # Character dead and blood frame animation is not finished
            window.blit(this.character.current_blood_frame_image, this.character.blood_effect_rect)

        # Drawing bullets if any and updating their update methods
        if len(self.character.weapon.all_bullets.sprites()) != 0: # This means theres bullets to draw
            self.character.weapon.all_bullets.update()
            self.character.weapon.all_bullets.draw(window)

        # This will make any guns the player doesn't have ammo for transparent. This is to show the player they dont have ammo and they cant pick the gun until they do.
        if this.character.GetAmmoCount(1) <= 0:
            self.handgun_image.set_alpha(77) # 77 out of 256. This means it's 30% transparent.
        else:
            self.handgun_image.set_alpha(256) # This means it's 100% transparent (256/256).
        if this.character.GetAmmoCount(2) <= 0:
            self.shotgun_image.set_alpha(77) # 77 out of 256. This means it's 30% transparent.
        else:
            self.shotgun_image.set_alpha(256) # This means it's 100% transparent (256/256).
        if this.character.GetAmmoCount(3) <= 0:
            self.mp4_image.set_alpha(77) # 77 out of 256. This means it's 30% transparent.
        else:
            self.mp4_image.set_alpha(256) # This means it's 100% transparent (256/256).

        # Blit the images onto the screen (weapon slots and the weapon icons on top of the slots)
        window.blit(self.weapon_slot_image, self.weapon_slot1_rect)
        window.blit(self.weapon_slot_image, self.weapon_slot2_rect)
        window.blit(self.weapon_slot_image, self.weapon_slot3_rect)
        window.blit(self.weapon_slot_image, self.weapon_slot4_rect)
        window.blit(self.knife_image, self.knife_rect)
        window.blit(self.handgun_image, self.handgun_rect)
        window.blit(self.shotgun_image, self.shotgun_rect)
        window.blit(self.mp4_image, self.mp4_rect)

        # Getting Ammo and setting UI [UI above the gun images that shows the current ammo for that gun]
        handgun_ammo_UI = self.ammo_font.render(str(this.character.GetAmmoCount(1)), True, self.BLACK)
        handgun_ammo_location = (self.weapon_slot2_rect.center[0], self.weapon_slot2_rect.center[1] - (self.weapon_slot2_rect.height * self.ammo_height_ratio))

        shotgun_ammo_UI = self.ammo_font.render(str(this.character.GetAmmoCount(2)), True, self.BLACK)
        shotgun_ammo_location = (self.weapon_slot3_rect.center[0], self.weapon_slot3_rect.center[1] - (self.weapon_slot3_rect.height * self.ammo_height_ratio))

        mp4_ammo_UI = self.ammo_font.render(str(this.character.GetAmmoCount(3)), True, self.BLACK)
        mp4_ammo_location = (self.weapon_slot4_rect.center[0], self.weapon_slot4_rect.center[1] - (self.weapon_slot4_rect.height * self.ammo_height_ratio))

        # Display Ammo UI that was retrieved above
        window.blit(handgun_ammo_UI, handgun_ammo_location)
        window.blit(shotgun_ammo_UI, shotgun_ammo_location)
        window.blit(mp4_ammo_UI, mp4_ammo_location)

        # set weapon Highlight UI [The red square over the selected weapon]
        if this.character.character_weapon == 0: # Player has knife out
            self.weapon_highlight_rect.center = self.knife_rect.center
        if this.character.character_weapon == 1: # Player has handgun out
            self.weapon_highlight_rect.center = self.handgun_rect.center
        if this.character.character_weapon == 2: # Player has shotgun out
            self.weapon_highlight_rect.center = self.shotgun_rect.center
        if this.character.character_weapon == 3: # Player has mp4 out
            self.weapon_highlight_rect.center = self.mp4_rect.center

        # Display highlight UI from above
        window.blit(self.weapon_highlight_square, self.weapon_highlight_rect)
    
        # Lowering the limits message timer if theres a message, and also displaying that message on the screen for the remainding timer.
        if this.limits_message_timer > 0:
            this.limits_message_timer -= 1
            this.limits_message_location = (this.character.rect.center[0] - (this.message_width / 2), this.character.rect.center[1] - this.limits_message_padding)
            window.blit(this.limits_message, this.limits_message_location)

        # Lowering the wave starting message timer if there is a wave starting, and displays the message on that screen for the duration.
        if this.wave_starting_message_timer > 0:
            this.wave_starting_message_timer -= 1
            temp_message_location = (this.wave_starting_message_location[0] - (this.wave_starting_message_width / 2), this.wave_starting_message_location[1])
            window.blit(this.wave_starting_message, temp_message_location)

        # Displaying a health bar above the player for a certain duration after taking damage.
        if this.character.damage_taken == True:
            position_x = self.character.rect.center[0] - (self.health_bar_width / 2) # Center the health bar
            position_y = self.character.rect.center[1] 
            self.UpdateHealthBar(position_x, position_y, self.character.current_health, self.character.max_health, False)

        # Updates the armor, health, stamina and buff icons in the top left of the screen
        self.UpdatePlayerArmorUI(self.character.character_armor)
        self.UpdateHealthBar(self.player_health_location[0], self.player_health_location[1], self.character.current_health, self.character.max_health, True)
        self.UpdateStaminaBar(self.player_stamina_location[0], self.player_stamina_location[1], self.character.current_stamina, self.character.max_stamina, True)
        self.UpdateBoostUI()

        # Displaying the clock at the top of the screen
        if this.waves.clock > 0:
            window.blit(this.waves.wave_clock_message, this.waves.wave_clock_location)

    def UpdateWave(self):
        # Gets called when the game screen is open [At the same time as UpdateGameScreen]
        self.waves.update() # updating the waves script

        # create a Pygame group to hold the enemies and blood explosions [if dying]
        enemies_group = pygame.sprite.Group()
        blood_group = []

        # add the enemies to the group
        if len(self.waves.enemies_list) > 0:
            for enemy in self.waves.enemies_list:
                if enemy.dead == False: # This enemy is alive
                    enemies_group.add(enemy)
                    pygame.draw.rect(window, (255, 0, 0), enemy.collision_rect)
                else: # This enemy is dead but the blood effects aren't done yet
                    blood_group.append(enemy)

            # draw the enemies from above [if any are alive]
            enemies_group.draw(window)
            for enemy in enemies_group:
                if enemy.damage_taken == True: # Draws the health bars above the zombies if they took damage recently
                    position_x = enemy.rect.center[0] - (self.health_bar_width / 2) # Center the health bar
                    position_y = enemy.rect.center[1] 
                    self.UpdateHealthBar(position_x, position_y, enemy.current_health, enemy.max_health, False)

            # Draw the blood splats above [if zombie(s) died recently]
            for blood_splat in blood_group: # Going through any enemies that might be in the blood splat phase of dying
                window.blit(blood_splat.current_blood_frame_image, blood_splat.blood_effect_rect)

        # Three item drops below, drawing sprites and updating items if on the ground
        # Displays any weapon items on the ground if there are any
        if len(self.waves.weapon_item):
            for weapon_item in self.waves.weapon_item:
                if weapon_item.gun_index == 1: # Handgun
                    weapon_item.update()
                    window.blit(self.handgun_drop, weapon_item.rect)
                elif weapon_item.gun_index == 2: # Shotgun
                    weapon_item.update()
                    window.blit(self.shotgun_drop, weapon_item.rect)
                else: # MP4 gun
                    weapon_item.update()
                    window.blit(self.mp4_drop, weapon_item.rect)

        # Displays any boost items on the ground if there are any
        if len(self.waves.boost_item):
            for boost_item in self.waves.boost_item:
                if boost_item.boost_index == 1: # ORANGE
                    boost_item.update()
                    window.blit(self.orange_boost_image, boost_item.rect)
                elif boost_item.boost_index == 2: # RED
                    boost_item.update()
                    window.blit(self.red_boost_image, boost_item.rect)
                elif boost_item.boost_index == 3: # BLUE
                    boost_item.update()
                    window.blit(self.blue_boost_image, boost_item.rect)
                else: # PURPLE
                    boost_item.update()
                    window.blit(self.purple_boost_image, boost_item.rect)

        # Display the armor items on the ground if there are any
        if len(self.waves.armor_item):
            for armor_item in self.waves.armor_item:
                armor_item.update()
                window.blit(self.armor_drop_image, armor_item.rect)

    def UpdateGameMenu(self):
        # Game menu is open
        self.main_menu.update(self.mouse_pos, event) # main menu is open, this updates it's update method
    
    def UpdateEndWaveMenu(self, event):
        # Wave finished and wave end menu is displaying the UI elements
        window.fill(self.BLACK)
        window.blit(this.wave_end_menu.wave_end_message, this.wave_end_menu.wave_end_location)
        window.blit(this.wave_end_menu.wave_kills_message, this.wave_end_menu.wave_kills_location)
        window.blit(this.wave_end_menu.next_wave_button_image, this.wave_end_menu.next_wave_button_rect)

        self.wave_end_menu.update(self.mouse_pos, event) # Updating wave_end_menu class

    def UpdateGameOverMenu(self):
        # Player died, game over menu is displayed, this updates the clicks and mouse location
        this.game_over_menu.update(this.mouse_pos, event)

    def UpdateTintTransparency(self):
        # Player died, after blood explosion this tints the screen slowly until full black, then game over menu comes up.
        
        # If transparent ratio hits first ratio, the increment is increased to dim faster.
        if self.transparent_current >= self.transparent_increment_change1:
            self.transparent_increment = self.transparent_increment_original * self.transparent_increment_ratio1
        # If transparent ratio hits second ratio, the increment is increased to dim faster again.
        elif self.transparent_current >= self.transparent_increment_change2:
            self.transparent_increment = self.transparent_increment_original * self.transparent_increment_ratio2

        # Setting the transparent ratio of the tint from the increment change above
        self.transparent_current += self.transparent_increment
        if self.transparent_current == self.transparent_max:
            self.transparent_current = self.transparent_max

        self.tint_screen_image.set_alpha(int(self.transparent_current)) # Changes the transparency of the tint screen
        window.blit(self.tint_screen_image, top_left_corner) # Displaying the tint screen

    def UpdateHealthBar(self, position_x, position_y, health, max_health, player_UI):
        # Drawing the health bars based on the player or zombies current health

        # Draw the background of the health bar
        if player_UI: # updating players health bar UI top left
            pygame.draw.rect(window, self.player_health_UI_color, (position_x, position_y, self.player_health_bar_width, self.player_health_bar_height))
        else: # drawing the background health bar above player or zombie
            pygame.draw.rect(window, self.health_UI_color, (position_x, position_y, self.health_bar_width, self.health_bar_height))
    
        # Calculate the width of the health bar based on the current health of player or zombie
        if player_UI: # updating players health bar UI top left
            health_width = int(health / max_health * self.player_health_bar_width)
        else: # updating player/zombies health bar above them when hit
            health_width = int(health / max_health * self.health_bar_width)
    
        if player_UI: # draw players health bar UI top left
            pygame.draw.rect(window, self.player_health_color, (position_x, position_y, health_width, self.player_health_bar_height))
        else: # Draw the health bar above the player or zombie
            pygame.draw.rect(window, self.health_color, (position_x, position_y, health_width, self.health_bar_height))

    def UpdateStaminaBar(self, position_x, position_y, stamina, max_stamina, player_UI):
        # Drawing the stamina bars based on the players current stamina

        # Draw the background of the stamina bar
        if player_UI: # draw players stamina background bar UI top left
            pygame.draw.rect(window, self.player_stamina_UI_color, (position_x, position_y, self.player_stamina_bar_width, self.player_stamina_bar_height))
        else: # draw players stamina background bar above players head if holding run key (shift default)
            pygame.draw.rect(window, self.stamina_UI_color, (position_x, position_y, self.stamina_bar_width, self.stamina_bar_height))
    
        # Calculate the width of the stamina bar based on players current stamina
        if player_UI: # updating players stamina bar UI top left
            stamina_width = int(stamina / max_stamina * self.player_stamina_bar_width)
        else: # updating players stamina bar above their head of holding run key (shift default)
            stamina_width = int(stamina / max_stamina * self.stamina_bar_width)
    
        if player_UI: # draw players stamina bar UI top left
            pygame.draw.rect(window, self.player_stamina_color, (position_x, position_y, stamina_width, self.player_stamina_bar_height))
        else: # Draw players stamina bar above the player head if holding run key (shift default)
            pygame.draw.rect(window, self.stamina_color, (position_x, position_y, stamina_width, self.stamina_bar_height))

    def UpdatePlayerArmorUI(self, player_armor):
        # This method updates the armor UI top left (blue squares) based on players current armor
        # Max 10 armor, each square counts as 2 armor (5 squares max) 50% damage blocked per attack but reduces armor by 1 

        if player_armor >= 1:
            if player_armor >= 2: # Player has first armor square (2 armor minimum)
                window.blit(this.armor_image, this.armor_rect1)
            else: # Player has 1 armor, first armor square is half size
                window.blit(this.half_armor_image, this.armor_rect1)
        if player_armor > 2: 
            if player_armor >= 4: # Player has second armor square (4 armor minimum)
                window.blit(this.armor_image, this.armor_rect2)
            else: # Player has 3 armor, second armor square is half size
                window.blit(this.half_armor_image, this.armor_rect2)
        if player_armor > 4:
            if player_armor >= 6: # Player has third armor square (6 armor minimum)
                window.blit(this.armor_image, this.armor_rect3)
            else: # Player has 5 armor, third armor square is half size
                window.blit(this.half_armor_image, this.armor_rect3)
        if player_armor > 6:
            if player_armor >= 8: # Player has fourth armor square (8 armor minimum)
                window.blit(this.armor_image, this.armor_rect4)
            else: # Player has 7 armor, fourth armor square is half size
                window.blit(this.half_armor_image, this.armor_rect4)
        if player_armor > 8:
            if player_armor == 10: # Player has five armor square (10 armor [max])
                window.blit(this.armor_image, this.armor_rect5)
            else: # Player has 9 armor, five armor square is half size
                window.blit(this.half_armor_image, this.armor_rect5)

    def UpdateBoostUI(self):
        # Updating the players boost icons top left, with the duration remaining on the boost.
    
        # This means the player has a boost active
        if not self.character.character_boost == 0: 
            # Drawing boost icon
            if self.character.character_boost == 1: # ORANGE BOOST
                window.blit(this.orange_boostUI_image, this.boost_UI_rect)
            elif self.character.character_boost == 2: # RED BOOST
                window.blit(this.red_boostUI_image, this.boost_UI_rect)
            elif self.character.character_boost == 3: # BLUE BOOST
                window.blit(this.blue_boostUI_image, this.boost_UI_rect)
            elif self.character.character_boost == 4: # PURPLE BOOST
                window.blit(this.purple_boostUI_image, this.boost_UI_rect)

            # Updating the text duration over the boost icon
            self.boost_timer_text = pygame.font.Font(None, 25) # Font for the clock
            self.boost_timer_UI = self.boost_timer_text.render(str(int(self.character.boost_timer / 60)), True, self.BLACK) # Message for the clock

            # Drawing the text duration
            window.blit(this.boost_timer_UI, this.boost_UI_rect.center)

    def UpdateMuzzle(self):
        # Updates and displays the muzzle flash if the player shot a gun recently
        if self.muzzle_timer > 0:
            self.muzzle_timer -= 1
            window.blit(self.muzzle_image, self.muzzle_rect) #If muzzle animation still going on, draw the sprite for the animation frame
    
    # ====================================================================
    # ===================== [CHANGE FUNCTIONS BELOW] =====================

    def WaveStartWarning(self, message):
        # Method to start wave warning message on top of the screen
        self.wave_starting_message = self.wave_start_font.render(message, True, self.RED)
        self.wave_starting_message_width = self.wave_starting_message.get_width()
        self.wave_starting_message_timer = self.wave_starting_message_duration

    def ChangeGameScreen(self, screen_type): # Game pauses when menus are open
        # Changes the game screen from, game menu, main menu screen, wave done menu and game screen. The screen type parameter passed is the menu or screen opened.
        if screen_type == 1: # Game Menu (pauses sounds/music)
            self.game_menu = True
            self.main_menu_screen = False
            self.wave_done_menu = False
            self.game_screen = False
            self.OnOffSound(False)
        elif screen_type == 2: # Main Menu (pauses sounds/music)
            self.game_menu = False
            self.main_menu_screen = True
            self.wave_done_menu = False
            self.game_screen = False
            self.OnOffSound(False)
        elif screen_type == 3: # Wave Done Menu (pauses sounds/music)
            self.game_menu = False
            self.main_menu_screen = False
            self.wave_done_menu = True
            self.game_screen = False
            self.OnOffSound(False)
        elif screen_type == 4: # Game Screen (Actual game)
            self.game_menu = False
            self.main_menu_screen = False
            self.wave_done_menu = False
            self.game_screen = True
            self.OnOffSound(True)

    def OpenEndWaveMenu(self):
        # Wave finished and wave end menu screen is being displayed
        self.ChangeGameScreen(3)
    
    def StartMuzzleFlash(self, location, weapon_index, muzzle_image, muzzle_rect):
        # Method to display muzzle flash

        # Setting the image and rect for this muzzle flash
        self.muzzle_image = muzzle_image
        self.muzzle_rect = muzzle_rect

        # Setting the location, and resetting the timer (when timer runs out muzzle image dissapears)
        self.muzzle_rect.x = float(location[0] - (muzzle_rect.width / 2))
        self.muzzle_rect.y = float(location[1] - (muzzle_rect.height / 2))
        self.muzzle_timer = self.muzzle_time_duration

    def ExitGame(self):
        # Exits out of the game and closes the program
        self.running = False

    # ====================================================================
    # ================== [TIMER/MESSAGE FUNCTIONS BELOW] =================

    def EscapeCooldownTimer(self):
        # This reduces the timer for the escape button cooldown (If player hit escape recently and opened a menu or closed it)
        if this.escape_timer > 0:
            this.escape_timer -= 1
    
    def StartLimitsMessage(self, message):
        # Limit message was started and it will display the message parameter for a duration
        self.limits_message = self.limit_font.render(message, True, self.RED)
        self.message_width = self.limits_message.get_width()
        self.limits_message_timer = self.limits_message_duration

    # ====================================================================
    # =================== [SOUND/MUSIC FUNCTIONS BELOW] ==================
    
    def GameMusic(self):
        self.game_music.play()

    def GameOverMusic(self):
        self.game_music.stop()
        self.game_over_music.play()

    def PlayerHitSound(self):
        self.player_hit.play()

    def KnifeAttackSound(self):
        self.knife_sound.play()

    def HandgunAttackSound(self):
        self.handgun_sound.play()

    def ShotgunAttackSound(self):
        self.shotgun_sound.play()

    def Mp4AttackSound(self):
        self.mp4_sound.play()

    def DeadSound(self):
        self.zombie_dead.play()

    def OnOffSound(self, on):
        if on == True:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()

    # == Zombie sounds below ==
    def ZombieAttackSound(self):
        self.zombie_attack.play()

    def ZombieHitSound(self):
        self.zombie_hit.play()

    # ====================================================================
    # ================= [OUTSIDE CALL FUNCTIONS BELOW] ===================

    def NextWavePressed(self):
        # These functions are called by outside scripts
        self.ChangeGameScreen(4)
    
this = ShooterGame() # Create a instance of this class

# game loop
while this.running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            this.ExitGame()

    # handle input
    keys = pygame.key.get_pressed()

    # Current time in miliseconds
    temp_time = pygame.time.get_ticks()
    time_since_last_frame = temp_time - current_time
    current_time = temp_time

    # Player pressed the escape button
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        this.escape_key_down = True

    # Changing between the menu and game screen based on escape button presses.
    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        if this.escape_key_down == True and this.escape_timer <= 0:
            this.escape_timer = this.escape_cooldown_duration
            this.escape_key_down = False
            if this.game_screen == True:
                this.ChangeGameScreen(1) # 1 == game menu
            else:
                this.ChangeGameScreen(4) # 4 == game screen

    # Getting mouse position
    this.mouse_pos = pygame.mouse.get_pos()

    # Changing between the game screens based on which boolean is true.
    if this.game_over_menu.game_done == True:
        this.UpdateGameOverMenu()
        pygame.display.update() # Gets called here because the remaining code won't run
        continue # Skips the rest of the code because the game is "over"

    if this.game_screen == True:
        # Putting the grass background into the window
        window.blit(background_image, top_left_corner)
        this.UpdateWave()
        this.UpdateGameScreen()
        this.character.weapon.update()

        # Player is dead, adding tint screen
        if this.character.blood_splat_done == True:
            this.UpdateTintTransparency() 
  
    elif this.game_menu == True:
        this.UpdateGameMenu()
    elif this.wave_done_menu == True:
        this.UpdateEndWaveMenu(event)

    if this.character.weapon.knife_attack_timer > 0:
        # Draw the square hitbox on the screen
        pygame.draw.rect(window, (255, 0, 0), this.character.weapon.knife_hitbox)

    this.EscapeCooldownTimer()
    this.UpdateMuzzle()
    pygame.display.update()
    # Limit the frame rate to 60 FPS (HAS TO BE AT BOTTOM OF GAME LOOP)
    clock.tick(60)
# clean up pygame
pygame.quit()