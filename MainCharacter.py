import pygame
import math
import Weapons as weapons

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# MainCharacter(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupCharacterTechnical(self, center, shooter_game, window_width, window_height) * Setup character variables NOT STATS, technical related stuff
# SetupCharacterStats(self) * All stats related to the characters abilities
# SetupWaveClass(self, waves) * Adds the wave class to the player on creation
# SetupEquipment(self) * Sets up ammo size, and other equipment related variables
# SetupBoosts(self) * Sets up all variables related to boosts
# ** SetupAnimation AND SetupAnimationSprites are moved to the animation section even though they are a setup method **

# -[UPDATE FUNCTIONS BELOW]-
# Update(self, keys, event) * The actual update loop of the character (called by the main script every frame)
# UpdateStaminaRegen(self) * Gets called by the update function in this class (regens stamina when not draining)
# UpdateRedBoost(self)
# ** Update player animation is placed in the animation related functions **

# -[CHANGE FUNCTIONS BELOW]-
# TakeDamage(self, damage) * Gets called when the character is hit by something that causes damage
# StaminaDrain(self) * This method is called when the player holds the run hotkey (shift) calls StaminaChange() method
# StaminaChange(self, stamina_amount) * Called to increase or decrease current stamina amount
# PlayerKilled(self) * Called when the players current health reaches <= 0
# PickedUpBoost(self, boost_index) * Called when the player picks up a boost
# RemoveBoost (self) * Timer ran out, boost buff is removed
# ArmorPickup (self, armor_amount) * Called when player picks up armor item on the ground
# NewWave(self) * Called when a new wave is started to reset the players health, and stamina to max amount

# -[ANIMATION RELATED FUNCTIONS BELOW]-
# SetupAnimationSprites(self) * Sets up all animation sprites, and frame sizes per animation
# SetupAnimation(self) * Sets up all animation related variables for future use. (called when character is instantiated)
# UpdatePlayerAnimation(self) * Updates players animation based on weapon, action and current animation frame.
# BloodSplat(self) * Called after the PlayerKilled method, it creates the bloodsplat effect
# SetMaxFrames(self, frames_count) * Is called to set the max frames to the current animations frame limit
# MuzzleAnimation (self, weapon_index) * Called after gun fire to get location of muzzle, create animation and set bullet spawn point

# -[ATTACK RELATED FUNCTIONS BELOW]-
# WeaponSwitch(self, keys) * Called when player presses, 1, 2, 3 or 4. Changes the players weapon
# PlayerAction(self, keys) * Detects any player actions and updates the script accordingly (attack, mov, ect.)
# KnifeAttack(self) * Called when player tries to attack with a knife
# GunAttack(self) * Called when player tries to attack with one of the three guns
# SetAttackCooldown(self, weapon_index) * Attack cooldown is set after the player attacks with 1 of the 4 weapons.
# CheckAttackCooldown(self) * Checks and lowers attack cooldown

# -[CHECK FUNCTIONS BELOW]-
# HasBoost(self, boost_index) * Checks if the player has a boost of the type passed in parameter
# CheckPurpleBoost(self) * Checks if player has purple boost, if it does the players mov speed is increased

# -[TIMER / MESSAGE FUNCTIONS BELOW]-
# DamageTakenTimer(self) * After player takes damage, this method is called in the update method until timer reaches 0
# SendLimitMessage(self, message) * Sends the limit message to the main script to display above player


# -[GETTER / SETTER FUNCTIONS BELOW]-
# SetAmmoCount (self, weapon_index, amount) * Sets the ammo count for that weapon type
# GetAmmoCount (self, weapon_index) * Returns the ammo left of that weapon type

# } END OF MainCharacter(Class)

# set up the MainCharacter class
class Character(pygame.sprite.Sprite):
    def __init__(self, center, shooter_game, window_width, window_height):
        super().__init__()
        # These methods are called at the start of the game when the character is first created
        # SetupAnimationSprites is called first because its needed for other setup functions
        self.SetupAnimationSprites() # Character animation sprites that are used for idle, walk, and attack animations
        self.SetupCharacterTechnical(center, shooter_game, window_width, window_height) # Technical related variables for character
        self.SetupCharacterStats() # Character stats
        self.SetupEquipment() # Character equpment
        self.SetupBoosts() # Character boosts
        self.SetupAnimation() # Sets up the animation frames and other variables needed
        self.SetAmmoCount(1, 10) # Starting with 10 handgun bullets
        self.SetAmmoCount(2, 10) # Starting with 10 shotgun bullets
        self.SetAmmoCount(3, 10) # Starting with 10 mp4 bullets

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupCharacterTechnical(self, center, shooter_game, window_width, window_height):
        # Setup character variables NOT STATS, technical related stuff
        self.shooter_game = shooter_game # holding ShooterGame (Main script) reference

        # Mouse Detection
        self.mouse_down = False
        self.mouse_x = 0 # Current spot the player clicked x position
        self.mouse_y = 0 # Current spot the player clicked y position

        # Damage taken related variables
        self.damage_taken = False # This will have a timer after taking damage and will be set back to false. Its for the health bar duration above players head
        self.damage_taken_timer = 0
        self.damage_taken_time = 170
        
        # Characters Other Attributes
        self.shift_active = False
        self.run_multiplier = 1.8 # The multiplier to change the movement speed of the character if running
        self.walking = False
        self.attacking = False
        self.dead = False
        self.current_attack_cooldown = 0.0 # If this is above 0 the player recently did an attack and cant attack again until its back at 0
        self.knife_cooldown_ratio = 2 # (2 * the attack_frame to get the cooldown for that weapon)
        self.guns_cooldown_ratio = 6 # This is much higher because the animation for gun attacks is only 3 vs knife attack which is 20 I think
        self.window_width = window_width
        self.window_height = window_height

        # Setting the starting image and location
        self.image = self.character_knife_idle[0]
        self.rect = self.image.get_rect()
        self.x_position = float(center[0] - (self.rect.width / 2))
        self.y_position = float(center[1] - (self.rect.height / 2))
        self.rect.x = self.x_position
        self.rect.y = self.y_position
        self.angle_degrees = 0

    def SetupCharacterStats(self):
        # All character stats that are not set in the SetupCharacterTechnical function\
        self.movement_speed = 2.2 # the normal movement speed
        self.current_movement_speed = 0 # the actual movement speed (influenced by purple boost)
        self.max_health = 100 # Max health
        self.current_health = self.max_health # current health
        self.max_stamina = 100 # Max stamina
        self.current_stamina = self.max_stamina
        self.stamina_regen = 15 # The amount of frames required to regen 1 stamina
        self.current_stam_regen = 0 # The current frame for stamina regen
        self.stamina_drain = 4 # The amount of frames required to drain 1 stamina when player is holding shift to run
        self.current_stam_drain = 0 # The current frame for stamina drain

    def SetupWaveClass(self, waves):
        # Adding wave class to character
        self.waves = waves

    def SetupEquipment(self):  
        # Holds the weapon classes for calling player attacking          
        self.weapon = weapons.Weapon(self)

        # Equipment
        self.character_weapon = 0 # 0 = KNIFE, 1 = HANDGUN, 2 = SHOTGUN, 3 = MP4
        self.character_armor = 10 # Starting armor (2 armor = 1 full square)
        self.character_max_armor = 10 

        # Ammo left
        self.handgun_ammo = 0
        self.handgun_maxammo = self.weapon.GetClipsize(1)
        self.shotgun_ammo = 0
        self.shotgun_maxammo = self.weapon.GetClipsize(2)
        self.mp4_ammo = 0
        self.mp4_maxammo = self.weapon.GetClipsize(3)

        # muzzle flash
        self.handgun_muzzle_flash = 60
        self.shotgun_muzzle_flash = 70
        self.mp4_muzzle_flash = 70

    def SetupBoosts(self):
        # Sets up all boost related vairables
        self.character_boost = 0 # 1 = double-damage ORANGE, 2 = regen 1hp/sec (maybe more) RED, 3 = unlimited ammo for boost BLUE, 4 = increased movement speed PURPLE [ 0 MEANS NO BOOST!! ]
        self.boost_duration = 30 * 60 # (30 seconds (60 frames per second))
        self.boost_timer = 0 # if it reaches 30 the boost is removed from the player

        # Red Boost
        self.red_boost_regen_ammount = 3
        self.red_boost_interval = 0

        # Purple Boost
        self.purple_boost_movement_speed = 4 # movement speed with purple boost active

    # ====================================================================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================

    def update(self, keys, event):
        # Updates with every frame (Main update method of character, calls all other update methods)

        # If player is dead it will break out of update loop after doing the blood splat animation for the players death
        if self.dead == True:
            self.BloodSplat()
            return

        # self.mouse_down is true if player is holding left click down (or pressed it). When left click is released its set to false
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_down = True
        else:
            self.mouse_down = False
        
        # These keys switch the players weapons (1 = knife, 2 = handgun, 3 = shotgun, 4 = mp4)
        if (keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4]):
            self.WeaponSwitch(keys)

        # These functions check for attack cooldown, players current key press, updates the animation and frames, lowers damage taken timer if needed
        self.CheckAttackCooldown() # Increments current_frame, also handles weapon cooldowns and sets values to 0 if max is reached.
        self.PlayerAction(keys) # Detects if player is moving or attacking and initiates those actions.
        self.UpdatePlayerAnimation() # Handles the characters animations based on the which state the character is in
        self.DamageTakenTimer() # If damage was recently taken this method will reduce the timer to remove the health bar

        # Checking if player is holding down the shift button (STAMINA)
        if keys[pygame.K_LSHIFT]:
            self.StaminaDrain() # Player is holding down left shift button so the stamina bar is draining
        else:
            self.UpdateStaminaRegen() # Regens players stamina if it's below max stamina
            self.current_stam_drain = 0

        # Setting the character location based on the X and Y positions
        self.rect.x = float(self.x_position - (self.rect.width / 2))
        self.rect.y = float(self.y_position - (self.rect.height / 2))
        self.blood_effect_rect.center = self.rect.center

        # If player is 0 health or below the player is killed.
        if self.current_health <= 0:
            self.PlayerKilled()
        elif self.character_boost == 2: # Player has red buff (hp regen)
            self.UpdateRedBoost()

        self.CheckPurpleBoost() # Checks if the player has the PURPLE BOOST

        # Lowering boost timer, if timer reaches 0 it removes the boost from the player
        if self.boost_timer > 0:
            self.boost_timer -= 1
        elif self.character_boost != 0:
            self.RemoveBoost()

    def UpdateStaminaRegen(self):
        # regens stamina, called in update frames
        self.shift_active = False # Player can't be holding the shift button because stamina would drain instead of regen
        self.current_stam_regen += 1

        # The stamina regen tick is going
        if self.current_stam_regen >= self.stamina_regen:
            self.StaminaChange(1)
            self.current_stam_regen = 0

    def UpdateRedBoost(self):
        # Updating the red boost
        self.red_boost_interval += 1

        # Checking if red boost tick is happening, if so it will reset the tick timer and increase players health
        if self.red_boost_interval >= 60:
            self.red_boost_interval = 0
            self.current_health += self.red_boost_regen_ammount

            # If max health or over the current health is set back to max health.
            if self.current_health > self.max_health:
                self.current_health = self.max_health

    # ====================================================================
    # ==================== [CHANGE FUNCTIONS BELOW] ======================

    def TakeDamage(self, damage):
        # Lowers players health and updates ShooterGame for health bar UI 

        # Player is already dead
        if self.current_health <= 0:
            return

        # Checking if player has armor, if so it reduces armor by 1 and the player takes 50% of the damage.
        if self.character_armor > 0:
            self.character_armor -= 1
            damage_dealt = float(damage * 0.50) # if player has armor its reduced by 1 and the player takes half the damage from this zombie attack
        else:
            damage_dealt = damage  

        # Damage taken stuff, this boolean sets the health bar above the player for the timer
        self.damage_taken = True
        self.damage_taken_timer = self.damage_taken_time

        # Lowering players health by damage dealth, if it reaches 0 the player is killed in the next update frame, if not the player makes the hit sound effect
        self.current_health -= damage_dealt
        if self.current_health <= 0:
            self.current_health = 0
        else:
            self.shooter_game.PlayerHitSound()

    def StaminaDrain(self):
        # drains stamina called in update frames
        self.shift_active = True # Player is holding down shift button
        self.current_stam_drain += 1

        # If the stamina tick reaches the timer, it drains the stamina by 1 then resets the stamina tick
        if self.current_stam_drain >= self.stamina_drain:
            self.StaminaChange(-1)
            self.current_stam_drain = 0

    def StaminaChange(self, stamina_amount):
        # Changes the players current stamina (> 0, < max) negative stamina_amount means its draining
        self.current_stamina += stamina_amount

        # Below is used to keep the current stamina within 0 and max stamina
        if self.current_stamina > self.max_stamina:
            self.current_stamina = self.max_stamina
        elif self.current_stamina < 0:
            self.current_stamina = 0

    def PlayerKilled(self):
        # Player is killed this is the method called (called in update method)
        if self.current_health <= 0:
            self.dead = True
            self.damage_taken_timer = 0
            self.damage_taken = False
            self.shooter_game.DeadSound() 

    def PickedUpBoost(self, boost_index):
        # Player picked up a boost
        self.boost_timer = self.boost_duration
        self.character_boost = boost_index

    def RemoveBoost (self):
        # Boost timer ran out and the boost is removed from the player
        self.boost_timer = 0
        self.character_boost = 0

        # Red boost related, it resets the tick timer
        if self.character_boost == 2: # RED BOOST
            self.red_boost_interval = 0 # Reseting this back to 0 for when it gets called again

    def ArmorPickup (self, armor_amount):
        # Player walked over an armor item and picked it up
        self.character_armor += armor_amount
        if self.character_armor > self.character_max_armor:
            self.character_armor = self.character_max_armor

    def NewWave(self):
        # Called when a new wave starts (resets hp and stamina to max)
        self.current_health = self.max_health
        self.current_stamina = self.max_stamina

    # ====================================================================
    # =============== [ANIMATION RELATED FUNCTIONS BELOW] ================

    def SetupAnimationSprites(self):
        # Setting up the animation sprites, loading them from the file locations and setting the frames int

        # KNIFE ANIMATION IMAGES BELOW
        # Loading character idle_knife animation
        self.knife_idle_frames = 20
        self.character_knife_idle =   [pygame.image.load(f"Character\\idle_knife\\survivor-idle_knife_{i}.png") for i in range(20)]    

        # Loading character walk_knife animation
        self.knife_walk_frames = 20
        self.character_knife_walk =   [pygame.image.load(f"Character\\walk_knife\\survivor-move_knife_{i}.png") for i in range(20)]

        # Loading character attack_knife animation
        self.knife_attack_frames = 15
        self.character_knife_attack =   [pygame.image.load(f"Character\\melee_knife\\survivor-meleeattack_knife_{i}.png") for i in range(15)]

        # HANDGUN ANIMATION IMAGES BELOW
        self.handgun_idle_frames = 18
        self.character_handgun_idle =   [pygame.image.load(f"Character\\idle_handgun\\survivor-idle_handgun_{i}.png") for i in range(19)]

        self.handgun_walk_frames = 20
        self.character_handgun_walk =   [pygame.image.load(f"Character\\walk_handgun\\survivor-move_handgun_{i}.png") for i in range(20)]

        self.handgun_attack_frames = 3
        self.character_handgun_attack =   [pygame.image.load(f"Character\\shoot_handgun\\survivor-shoot_handgun_{i}.png") for i in range(3)]

        # SHOTGUN ANIMATION IMAGES BELOW
        self.shotgun_idle_frames = 20
        self.character_shotgun_idle =   [pygame.image.load(f"Character\\idle_shotgun\\survivor-idle_shotgun_{i}.png") for i in range(20)]

        self.shotgun_walk_frames = 20
        self.character_shotgun_walk =   [pygame.image.load(f"Character\\walk_shotgun\\survivor-move_shotgun_{i}.png") for i in range(20)]

        self.shotgun_attack_frames = 3
        self.character_shotgun_attack =   [pygame.image.load(f"Character\\shoot_shotgun\\survivor-shoot_shotgun_{i}.png") for i in range(3)]

        # MP4 ANIMATION IMAGES BELOW
        self.mp4_idle_frames = 20
        self.character_mp4_idle =   [pygame.image.load(f"Character\\idle_mp4\\survivor-idle_rifle_{i}.png") for i in range(20)]

        self.mp4_walk_frames = 20
        self.character_mp4_walk =   [pygame.image.load(f"Character\\walk_mp4\\survivor-move_rifle_{i}.png") for i in range(20)]

        self.mp4_attack_frames = 3
        self.character_mp4_attack =   [pygame.image.load(f"Character\\shoot_mp4\\survivor-shoot_rifle_{i}.png") for i in range(3)]

        # Muzzle Flash Image
        self.muzzle_flash_image = pygame.image.load('Character\Ammo\muzzle_flash.png')
        self.muzzle_flash_rect = self.muzzle_flash_image.get_rect()

    def SetupAnimation(self):
        # This is called when the character is created.
        # Adding the sprite animation sheets to the character

        # KNIFE ANIMATION SHEETS
        self.knife_idle = self.character_knife_idle
        self.knife_walk = self.character_knife_walk
        self.knife_attack = self.character_knife_attack

        # HANDGUN ANIMATION SHEETS\friends\
        self.handgun_idle = self.character_handgun_idle
        self.handgun_walk = self.character_handgun_walk
        self.handgun_attack = self.character_handgun_attack

        # SHOTGUN ANIMATION SHEETS
        self.shotgun_idle = self.character_shotgun_idle
        self.shotgun_walk = self.character_shotgun_walk
        self.shotgun_attack = self.character_shotgun_attack

        # MP4 ANIMATION SHEETS
        self.mp4_idle = self.character_mp4_idle
        self.mp4_walk = self.character_mp4_walk
        self.mp4_attack = self.character_mp4_attack

        # Animation Frame related
        self.current_frame = float(0)
        self.frame_increment = 0.3
        self.SetMaxFrames(self.knife_idle_frames)

        # Blood effects
        self.blood_splat_frames = 9
        self.blood_splat_current_frame = 0
        self.blood_splat_frame_increment = 0.4
        self.blood_splat_animation = [pygame.image.load(f"Effects\\blood_splatter\\blood_splatter_{i}.png") for i in range(self.blood_splat_frames)]
        self.current_blood_frame_image = self.blood_splat_animation[0]
        self.after_blood_duration = 2 * 60 # This is the amount of seconds (divided by 60 frames) after the blood splat is done before the game ends
        self.after_blood_timer = 0
        self.blood_splat_done = False

        self.blood_effect_rect = self.current_blood_frame_image.get_rect()

        # Setting the transparency of all of the images
        for blood_image in self.blood_splat_animation:
            blood_image.set_colorkey((255, 255, 255))

    def UpdatePlayerAnimation(self):    
        # Updates the players animations and the rotation based on the mouse location.

        # Calculate the angle between the character's position and the mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_x = mouse_pos[0]
        self.mouse_y = mouse_pos[1]

        # Setting rotation 
        dx = self.mouse_x - self.x_position
        dy = self.mouse_y - self.y_position
        angle = math.atan2(-dy, dx)
        self.angle_degrees = math.degrees(angle)

        # Sets current frame to 0 if it hits max frames for that animation
        if self.current_frame >= self.max_frame:
            self.current_frame = self.max_frame

        # set the character's image to the current animation frame
        if self.attacking and (self.character_weapon == 0 or not self.walking): #IT WILL USE THE WALK ANIMATION INSTEAD IF THE PLAYER IS WALKING WHILE SHOOTING (KNIFE ATTACKS STOP MOVEMENT)
            if self.character_weapon == 0: #0 = KNIFE
                self.image = pygame.transform.rotate(pygame.transform.scale(self.knife_attack[int(self.current_frame)], (int(self.knife_attack[int(self.current_frame)].get_width() * 0.5), int(self.knife_attack[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 1: #1 = HANDGUN
                self.image = pygame.transform.rotate(pygame.transform.scale(self.handgun_attack[int(self.current_frame)], (int(self.handgun_attack[int(self.current_frame)].get_width() * 0.5), int(self.handgun_attack[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 2: #2 = SHOTGUN
                self.image = pygame.transform.rotate(pygame.transform.scale(self.shotgun_attack[int(self.current_frame)], (int(self.shotgun_attack[int(self.current_frame)].get_width() * 0.5), int(self.shotgun_attack[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 3: #3 = MP4
                self.image = pygame.transform.rotate(pygame.transform.scale(self.mp4_attack[int(self.current_frame)], (int(self.mp4_attack[int(self.current_frame)].get_width() * 0.5), int(self.mp4_attack[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
        elif self.walking: # Character walking
            if self.character_weapon == 0: #0 = KNIFE
                self.image = pygame.transform.rotate(pygame.transform.scale(self.knife_walk[int(self.current_frame)], (int(self.knife_walk[int(self.current_frame)].get_width() * 0.5), int(self.knife_walk[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 1: #1 = HANDGUN
                self.image = pygame.transform.rotate(pygame.transform.scale(self.handgun_walk[int(self.current_frame)], (int(self.handgun_walk[int(self.current_frame)].get_width() * 0.5), int(self.handgun_walk[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 2: #2 = SHOTGUN
                self.image = pygame.transform.rotate(pygame.transform.scale(self.shotgun_walk[int(self.current_frame)], (int(self.shotgun_walk[int(self.current_frame)].get_width() * 0.5), int(self.shotgun_walk[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 3: #3 = MP4
                self.image = pygame.transform.rotate(pygame.transform.scale(self.mp4_walk[int(self.current_frame)], (int(self.mp4_walk[int(self.current_frame)].get_width() * 0.5), int(self.mp4_walk[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
        elif not self.walking: # Character idle
            if self.character_weapon == 0: #0 = KNIFE
                self.image = pygame.transform.rotate(pygame.transform.scale(self.knife_idle[int(self.current_frame)], (int(self.knife_idle[int(self.current_frame)].get_width() * 0.5), int(self.knife_idle[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 1: #1 = HANDGUN
                self.image = pygame.transform.rotate(pygame.transform.scale(self.handgun_idle[int(self.current_frame)], (int(self.handgun_idle[int(self.current_frame)].get_width() * 0.5), int(self.handgun_idle[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 2: #2 = SHOTGUN
                self.image = pygame.transform.rotate(pygame.transform.scale(self.shotgun_idle[int(self.current_frame)], (int(self.shotgun_idle[int(self.current_frame)].get_width() * 0.5), int(self.shotgun_idle[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
            if self.character_weapon == 3: #3 = MP4
                self.image = pygame.transform.rotate(pygame.transform.scale(self.mp4_idle[int(self.current_frame)], (int(self.mp4_idle[int(self.current_frame)].get_width() * 0.5), int(self.mp4_idle[int(self.current_frame)].get_height() * 0.5))), self.angle_degrees)
        self.rect = self.image.get_rect()

    def BloodSplat(self):
        # This gets called when the player is killed, in the update call every frame to display the blood splat animation
        self.blood_splat_current_frame += self.blood_splat_frame_increment
        if self.blood_splat_current_frame >= self.blood_splat_frames: # Player is officially dead, blood splat animation was played and now the wave ends is deleted
            self.blood_splat_done = True
            if self.after_blood_timer < self.after_blood_duration:
                self.after_blood_timer += 1
            else: # Closes the game because the player died and the blood animation is done
                self.shooter_game.game_over_menu.GameEnd()
        else:
            self.current_blood_frame_image = self.blood_splat_animation[int(self.blood_splat_current_frame)]

    def SetMaxFrames(self, frames_count):
        # Basic function to set max frame based on frame count (anything that changes max_frame goes through here.)
        self.max_frame = frames_count

    def MuzzleAnimation (self, weapon_index):
        # Player shot a gun and this is the method called after to display the muzzle flash animation
        player_pos = (self.x_position, self.y_position)
        muzzle_pos = (0, 0)

        # Calculate the direction that the character sprite is facing
        rotation_angle = math.radians(self.angle_degrees)
        facing_direction = pygame.math.Vector2(math.cos(rotation_angle), -math.sin(rotation_angle))

        if self.character_weapon == 1:
            # Calculate the new position of the flash in front of the character
            perpendicular_direction = pygame.math.Vector2(facing_direction.y, -facing_direction.x)
            muzzle_pos = player_pos + facing_direction * self.handgun_muzzle_flash
            shift_amount = 25
            shift_vector = perpendicular_direction * shift_amount
            muzzle_pos -= shift_vector
        elif self.character_weapon == 2:
            # Calculate the new position of the flash in front of the character
            perpendicular_direction = pygame.math.Vector2(facing_direction.y, -facing_direction.x)
            muzzle_pos = player_pos + facing_direction * self.shotgun_muzzle_flash
            shift_amount = 25
            shift_vector = perpendicular_direction * shift_amount
            muzzle_pos -= shift_vector
        elif self.character_weapon == 3:
            # Calculate the new position of the flash in front of the character
            perpendicular_direction = pygame.math.Vector2(facing_direction.y, -facing_direction.x)
            muzzle_pos = player_pos + facing_direction * self.mp4_muzzle_flash
            shift_amount = 25
            shift_vector = perpendicular_direction * shift_amount
            muzzle_pos -= shift_vector

        self.shooter_game.StartMuzzleFlash(muzzle_pos, weapon_index, self.muzzle_flash_image, self.muzzle_flash_rect)
        return muzzle_pos

    # ====================================================================
    # ================ [ATTACK RELATED FUNCTIONS BELOW] ==================

    def WeaponSwitch(self, keys):
        # Player pressed, 1, 2, 3, or 4 to change the weapon they are holding.

        # Attack cooldown reached 0 so the player is able to change their weapon
        if self.current_attack_cooldown <= 0: # Wont allow the player to change weapons if they are still under an attack cooldown period
            if keys[pygame.K_1]: # KNIFE
                self.character_weapon = 0
            elif keys[pygame.K_2]: # HANDGUN
                if self.GetAmmoCount(1) > 0 or self.character_boost == 3: # Player has enough ammo
                    self.character_weapon = 1
                else:
                    self.SendLimitMessage("Not enough handgun ammo!!")
            elif keys[pygame.K_3]: # SHOTGUN
                if self.GetAmmoCount(2) > 0 or self.character_boost == 3: # Player has enough ammo
                    self.character_weapon = 2
                else:
                    self.SendLimitMessage("Not enough shotgun ammo!!")
            elif keys[pygame.K_4]: # MP4
                if self.GetAmmoCount(3) > 0 or self.character_boost == 3: # Player has enough ammo
                    self.character_weapon = 3
                else:
                    self.SendLimitMessage("Not enough mp4 ammo!!")
            else:
                print("ERROR: WEAPON SWITCH ERROR") 

            # Resetting the curret_frame so the animations start at frame 0
            self.current_frame = 0

    
    def PlayerAction(self, keys):
        # Player pressed key and is attacking or moving.

        # Player is trying to attack with a knife
        if self.current_attack_cooldown <= 0 and not self.attacking:
            if self.mouse_down == True and self.character_weapon == 0:
                self.KnifeAttack()
            elif self.mouse_down == True:
                self.GunAttack()

        # (Character weapon is a gun OR character isn't attacking) AND (player is trying to move with A,W,S,D keys)
        if (not self.character_weapon == 0 or not self.attacking) and (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            self.walking = True
        
            if self.shift_active == True and self.current_stamina > 0:
                current_movement_speed = self.current_movement_speed * self.run_multiplier
            else:
                current_movement_speed = self.current_movement_speed 

            # Player pushed a,s,d, or w to move
            if keys[pygame.K_a]:
                self.x_position -= current_movement_speed
            if keys[pygame.K_d]:
                self.x_position += current_movement_speed
            if keys[pygame.K_w]:
                self.y_position -= current_movement_speed
            if keys[pygame.K_s]:
                self.y_position += current_movement_speed

            # This keeps the player inside the playable window screen
            if self.x_position < 0:
                self.x_position = 0
            elif self.x_position > self.window_width:
                self.x_position = self.window_width
            if self.y_position < 0:
                self.y_position = 0
            elif self.y_position > self.window_height:
                self.y_position = self.window_height

            # Setting the characters max animation frames, so the proper animation can be displayed and loop perfectly.
            if self.character_weapon == 0:
                self.SetMaxFrames(self.knife_walk_frames)
            elif self.character_weapon == 1:
                self.SetMaxFrames(self.handgun_walk_frames)
            elif self.character_weapon == 2:
                self.SetMaxFrames(self.shotgun_walk_frames)
            elif self.character_weapon == 3:
                self.SetMaxFrames(self.mp4_walk_frames)

        elif not self.attacking and not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            # Character is standing there not attacking, just idle
            self.walking = False

            # Setting the characters max animation frames, so the proper animation can be displayed and loop perfectly.
            if self.character_weapon == 0:
                self.SetMaxFrames(self.knife_idle_frames)
            elif self.character_weapon == 1:
                self.SetMaxFrames(self.handgun_idle_frames)
            elif self.character_weapon == 2:
                self.SetMaxFrames(self.shotgun_idle_frames)
            elif self.character_weapon == 3:
                self.SetMaxFrames(self.mp4_idle_frames)

   
    def KnifeAttack(self):
        # Player is attacking with a knife
        self.attacking = True
        self.current_frame = 0
        self.SetMaxFrames(self.knife_attack_frames)
        self.SetAttackCooldown(0)
        self.weapon.KnifeMechanics()
 
    def GunAttack(self):
        # Player is attacking with a gun
        self.attacking = True
        self.current_frame = 0

        # Setting the characters max animation frames, so the proper animation can be displayed and loop perfectly.
        if self.character_weapon == 1:
            if self.GetAmmoCount(1) > 0: # Handgun
                # Ammo count above 0, or blue boost active. Initiatiating shooting mechanics and spawning bullet at muzzle location
                self.SetMaxFrames(self.handgun_attack_frames)
                self.SetAttackCooldown(1)
                bullet_spawn = self.MuzzleAnimation(1)
                self.weapon.GunMechanics(bullet_spawn)
            else:
                self.SendLimitMessage("Not enough handgun ammo!!")
        elif self.character_weapon == 2: # Shotgun
            if self.GetAmmoCount(2) > 0:
                # Ammo count above 0, or blue boost active. Initiatiating shooting mechanics and spawning bullet at muzzle location
                self.SetMaxFrames(self.shotgun_attack_frames)
                self.SetAttackCooldown(2)
                bullet_spawn = self.MuzzleAnimation(2)
                self.weapon.GunMechanics(bullet_spawn)
            else:
                self.SendLimitMessage("Not enough shotgun ammo!!") 
        elif self.character_weapon == 3: # MP4 Gun
            if self.GetAmmoCount(3) > 0:
                # Ammo count above 0, or blue boost active. Initiatiating shooting mechanics and spawning bullet at muzzle location
                self.SetMaxFrames(self.mp4_attack_frames)
                self.SetAttackCooldown(3)
                bullet_spawn = self.MuzzleAnimation(3)
                self.weapon.GunMechanics(bullet_spawn)
            else:
                self.SendLimitMessage("Not enough mp4 ammo!!") 
        else:
            # This is a bug and should never happen
            print("ERROR: No gun was selected for the GunAttack function")

    def SetAttackCooldown(self, weapon_index):
        # The player recently attacked and a cooldown is being set based on the weapon used.
        if weapon_index == 0: # Knife attack
            self.current_attack_cooldown = self.knife_attack_frames * self.knife_cooldown_ratio
        elif weapon_index == 1: # Handgun attack
            self.current_attack_cooldown = self.handgun_attack_frames * self.guns_cooldown_ratio
        elif weapon_index == 2: # Shotgun attack
            self.current_attack_cooldown = self.shotgun_attack_frames * self.guns_cooldown_ratio
        elif weapon_index == 3: # MP4 gun attack
            self.current_attack_cooldown = self.mp4_attack_frames * self.guns_cooldown_ratio

    def CheckAttackCooldown(self):
        # Checks attack cooldown and lowers them based on the increment. 

        # Changing current_frame by frame_increment, once it reaches that animations max frame it is returned back to 0 to restart the animation loop.
        self.current_frame += self.frame_increment
        if int(self.current_frame) >= self.max_frame:
            # This means the attack animation is done (Setting current frame back to 0)
            self.current_frame = 0
            self.attacking = False # Setting this false when any animation is done regardless of the player clicking because there is a cooldown period for each weapon
                
        # This stops the attack cooldown from going below 0, and it's a fail safe to make sure attacking is set to false
        if self.current_attack_cooldown <= 0:
             self.current_attack_cooldown = 0
             self.attacking = False # This should already be false when the attack animation fnishes a couple of lines above.
        else: 
            # Lowering attack cooldown timer
            self.current_attack_cooldown -= self.frame_increment
    
    # ====================================================================
    # ===================== [CHECK FUNCTIONS BELOW] ======================

    def HasBoost(self, boost_index):
        # Returns if player has boost passed in parameter or not
        if self.character_boost == boost_index:
            # Player has boost of this index 
            return True 
        else: 
            # Player DOESN'T have boost of this index
            return False

    def CheckPurpleBoost(self):
        # check if player currently has the pruple boost, if so it increases their movement speed
        if self.character_boost == 4: 
            # PURPLE BOOST increasing movement speed for player
            self.current_movement_speed = self.purple_boost_movement_speed
        else:
            # Purple boost isn't active so player's movement speed is set to the default amount
            self.current_movement_speed = self.movement_speed

    # ====================================================================
    # ================ [TIMER / MESSAGE FUNCTIONS BELOW] =================

    def DamageTakenTimer(self):
        # Timer is reduced every frame after taking damage until the timer reaches 0 and the damage taken boolean is set to false.
        if self.damage_taken_timer > 0:
            self.damage_taken_timer -= 1
        else:
            self.damage_taken = False

    def SendLimitMessage(self, message):
        # Sends the limit message to the ShooterGame to display it on the screen
        self.shooter_game.StartLimitsMessage(message)

    # ====================================================================
    # ================ [GETTER / SETTER FUNCTIONS BELOW] =================
   
    def GetAmmoCount (self, weapon_index):
        # Returns ammo count of weapon index paramter

        if self.character_boost == 3: # Blue boost (returns 99 bullets because it's unlimited bullets boost)
            return 99
        elif weapon_index == 1:
            return self.handgun_ammo
        elif weapon_index == 2:
            return self.shotgun_ammo
        elif weapon_index == 3:
            return self.mp4_ammo
    
    def SetAmmoCount (self, weapon_index, amount):
        # Sets the ammo of the weapon based on the weapon index and amount parameters

        if self.character_boost == 3 and amount < 0: 
            # BLUE BOOST and player shot a bullet. The bullet is cancelled out because blue buff gives unlimited ammo
            return # won't run the code below

        # If player doesn't have blue boost the below code will check the ammo for the weapon index
        if weapon_index == 1:
            self.handgun_ammo += amount # If amounts negative it will take away bullets.
            if self.handgun_ammo > self.handgun_maxammo:
                self.handgun_ammo = self.handgun_maxammo
            elif self.handgun_ammo < 0:
                self.handgun_ammo = 0
        elif weapon_index == 2:
            self.shotgun_ammo += amount # If amounts negative it will take away bullets.
            if self.shotgun_ammo > self.shotgun_maxammo:
                self.shotgun_ammo = self.shotgun_maxammo
            elif self.shotgun_ammo < 0:
                self.shotgun_ammo = 0
        elif weapon_index == 3:
            self.mp4_ammo += amount # If amounts negative it will take away bullets.
            if self.mp4_ammo > self.mp4_maxammo:
                self.mp4_ammo = self.mp4_maxammo
            elif self.mp4_ammo < 0:
                self.mp4_ammo = 0
        else:
            print("Weapon index bug")  