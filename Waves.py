import pygame
import random
import math
import Enemy as enemy # CREATES ENEMIES AND GIVES IT THE CHARACTER CLASS OBJECT SO IT CAN FIND AND ATTACK THE PLAYER
import GroundItem as ground_item # ALSO SPAWNS BOOSTS

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# Waves(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupTechnical(self, shooter_game, screen_width, screen_height) * Setup technical related variables
# SetupWaveAttributes(self) * Set's up the wave attributes
# SetupSpawnCooldown(self) * Sets up variables related to the spawn cooldown
# SetupClock(self) * Sets up the clock at the top of the game screen
# SetupItems(self) * Sets the drop rates for each item (Including boosts)


# -[UPDATE FUNCTIONS BELOW]-
# update(self) * The main update function for this script, gets called every frame by the ShooterGame script

# -[SPAWN FUNCTIONS BELOW]-
# SpawnPickLocation(self) * This function picks a random spawn location, left side, top side, right side, or bottom side.
# SpawnCooldownRate(self) * Sets the spawn cooldown rate, and gets called at the start of each wave by CalculateDifficulty() function
# SpawnCooldownTimerTick(self) * Updates the spawn timer, for spawning enemies
# SpawnCooldownReset(self) * This sets the timer back to 0, when it reaches a certain time it spawns the enemy
# SpawnEnemy(self, spawn_location) * This function actually spawns the enemy and adds it to the enemies list

# -[CHANGE FUNCTIONS BELOW]-
# ZombieKilled(self, location) * This is called when a zombie is killed, and passes the location (Determines drop rate)
# EndOfWave(self) * This gets called when the wave timer reaches 0
# ResetWaveStats(self) * This gets called by EndOfWave(self), resets all variables used in each wave
# CalculateDifficulty(self) * This gets called by NextWavePressed() and it calculates the difficulty of the next wave

# -[ITEM FUNCTIONS BELOW]-
# ItemSpawnWeapon(self, weapon_index, location) * If drop chance rolls a weapon, this function is called, picks a random ammo amount and drops the item.
# ItemSpawnBoost(self, boost_index, location) * If drop chance rolls a boost, this function is called, and spawns the boost based on index paramater
# ItemSpawnArmor(self, location) * If dorp chance rolls an armor, this function is called and drops the armor on the ground.

# -[TIMER FUNCTIONS BELOW]-
# UpdateClock(self) * Updates the actual clock at the top of the screen
# UpdateClockTimer(self) * Increases wave timer by 1, when it reaches 60 (60 fps) it counts as 1 second

# -[OUTSIDE CALL FUNCTIONS BELOW]-
# NextWavePressed(self) * The player pressed the next wave button (This gets called from WaveEndMenu script)

# } END OF Waves(Class)

# set up the Waves class
class Waves:
    def __init__(self, player, screen_width, screen_height, shooter_game):
        # These methods are called at the start of the game when the wave script is instantiated is first created
        self.SetupTechnical(shooter_game, screen_width, screen_height, player)
        self.SetupWaveAttributes()
        self.SetupSpawnCooldown()
        self.SetupClock()
        self.SetupItems()

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupTechnical(self, shooter_game, screen_width, screen_height, player):
        # Sets up technical variables
        self.shooter_game = shooter_game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player

        # Annoucement
        self.annoucemnt_made = False # Stops the annoucement from being displayed more then once per wave

        # Music related
        self.game_music_played = False # Stops the background music from being played more then once per wave

    def SetupWaveAttributes(self):
        # Set's up the wave attributes

        # Wave information
        self.difficulty = 1 # 1 is 100% difficulty, it scales with level
        self.wave_number = 1 # The current wave, starts at 1
        self.wave_kills = 0 # Total wave kills for this wave
        self.total_kills = 0 # Total kills for this play through
        self.enemies_list = []


    def SetupSpawnCooldown(self):
        # Sets up variables related to the spawn cooldown
        self.spawn_cooldown_actual = 0 # Spawn time before its translated to seconds
        self.spawn_cooldown_timer = float(0) # current timer for the zombie spawn
        self.spawn_cooldown_base = float(4) # spawns a zombie every 4 seconds after the initial wait period before the spawn
        self.spawn_cooldown_rate = 0.5
        self.spawn_cooldown = self.spawn_cooldown_base   

        # The wave time when monsters start spawning
        self.spawn_at_time = 10 # in seconds  

    def SetupClock(self):
        # Sets up all clock related stuff
        self.RED = (255, 0, 0)

        self.clock_actual = 0 # divided by 60 frames per second
        self.clock = 0 # The time in seconds
        self.wave_length = 120 # in seconds (The clock its this number then the wave is over)
        self.clock_padding = 25 # The padding from the top of the screen
        self.wave_clock = pygame.font.Font(None, 70) # Font for the clock
        self.wave_clock_message = self.wave_clock.render(str(self.clock), True, self.RED) # Message for the clock
        self.wave_clock_location = ((self.screen_width / 2) - self.wave_clock_message.get_width(), self.clock_padding) # clock location
        self.wave_timer = float(0)
        self.wave_timer_actual = 0 

    def SetupItems(self):
        # Setting up the weapon drop chances and ammo drop chances.

        # DROP CHANCE EXPLAINED:
        # The drop chances shown below are actually divided by 3. 
        # You can't have 2 items drop at the same time so, weapon, armor and boost all have a 33% chance to roll
        # When an item rolls it then rolls the drop chances below to see if it will get an item

        # GUNS
        self.weapon_item = []
        self.handgun_ammo_amount = [5, 10, 15]
        self.shotgun_ammo_amount = [5, 10, 15]
        self.mp4_ammo_amount = [5, 10, 15]
        self.handgun_drop_chance = 0.25 # 25% drop rate
        self.shotgun_drop_chance = 0.30 # 5% drop rate
        self.mp4_drop_chance = 0.40 # 10% drop rate

        # Boosts
        self.boost_item = []
        self.orange_boost_drop_chance = 0.08 # double-damage ORANGE 5% drop chance
        self.oranage_boost_duration = 20 * 60 #(20 seconds because 60 frames per second)
        self.red_boost_drop_chance = 0.16# regen 1hp/sec (maybe more) RED 5% drop chance
        self.red_boost_duration = 30 * 60 #(30 seconds because 60 frames per second)
        self.blue_boost_drop_chance = 0.24# unlimited ammo for boost BLUE 5% drop chance
        self.blue_boost_duration = 20 * 60 #(20 seconds because 60 frames per second)
        self.purple_boost_drop_chance = 0.32# increased movement speed PURPLE 5% drop chance
        self.purple_boost_duration = 30 * 60 #(20 seconds because 60 frames per second)

        # Armor
        self.armor_item = []
        self.armor_drop_chance = 0.15 # 15% drop chance

    # ====================================================================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================

    def update(self):
        # Gets called every update frame by the ShooterGame script

        # Updating wave timer (this gets called 60 times a second)
        self.UpdateClock()

        # Plays on the first frame of every wave
        if self.game_music_played == False:
            self.game_music_played = True
            self.shooter_game.GameMusic() # Starting the game music
        
        # If its been the wait period (currently 10 seconds) before the game will start spawning zombies.
        if self.wave_timer >= self.spawn_at_time:

            # Wave timer starts
            self.UpdateClockTimer()

            # Annoucing wave start the first frame after the 10 second wait period
            if self.annoucemnt_made == False:
                self.shooter_game.WaveStartWarning("Wave " + str(self.wave_number) + " is starting soon!")
                self.annoucemnt_made = True
                
            # Spawning zombie or setting the spawn zombie cooldown timer
            if self.spawn_cooldown_timer > self.spawn_cooldown:
                self.SpawnCooldownReset() # Sets the timer of how much time before the next spawn happens after this one.

                # Currently spawning twice per cooldown
                spawn_location = self.SpawnPickLocation()
                self.SpawnEnemy(spawn_location)
                spawn_location = self.SpawnPickLocation()
                self.SpawnEnemy(spawn_location)
            else:
                self.SpawnCooldownTimerTick() # Timer tick (60 per second) is increased by 1
            
            # Updating the enmies update methods
            if len(self.enemies_list) > 0:
                for enemy in self.enemies_list:
                    enemy.update()

            # If the clock reaches this time (currently 120 seconds) the wave ends and the player survived that wave.
            if self.clock >= self.wave_length:
                self.EndOfWave()

    # ====================================================================
    # ===================== [SPAWN FUNCTIONS BELOW] ======================

    def SpawnPickLocation(self):
        # Picks a random spawn location for the zombies (called when a zombie is spawning)
        random_number = random.random()
        if random_number < 0.25:
            # LEFT SIDE
            random_number = random.random() # roll the random number again (0.0 - 1.0)
            return (0, random_number * self.screen_height)
        elif random_number >= 0.25 and random_number < 0.50:
            # TOP SIDE
            random_number = random.random() # roll the random number again (0.0 - 1.0)
            return (random_number * self.screen_width, 0)
        elif random_number >= 0.50 and random_number < 0.75:
            # RIGHT SIDE
            random_number = random.random() # roll the random number again (0.0 - 1.0)
            return (self.screen_width, random_number * self.screen_height)
        else:
            # BOTTOM SIDE
            random_number = random.random() # roll the random number again (0.0 - 1.0)
            return (random_number * self.screen_width, self.screen_height)
        
    def SpawnCooldownRate(self):
        # Sets the spawn cooldown rate based on the current wave (called onceper wave, at the start of the wave)
        self.spawn_cooldown = self.spawn_cooldown_rate * self.difficulty
        self.spawn_cooldown = self.spawn_cooldown_base - self.spawn_cooldown

    def SpawnCooldownTimerTick(self):
        # Updates the spawn timer tick
        self.spawn_cooldown_actual += 1
        self.spawn_cooldown_timer = float(self.spawn_cooldown_actual / 60)

    def SpawnCooldownReset(self):
        # Resets the spawn timer
        self.spawn_cooldown_actual = 0
        self.spawn_cooldown_timer = 0

    def SpawnEnemy(self, spawn_location):
        # Called to spawn the enemy (zombie)
        zombie = enemy.Enemy(self.player, self.difficulty, self.difficulty, self.difficulty, self.difficulty, spawn_location, self.shooter_game)
        self.enemies_list.append(zombie)

    # ====================================================================
    # ==================== [CHANGE FUNCTIONS BELOW] ======================

    def ZombieKilled(self, location):
        # Zombie was killed by player

        # Update stats
        self.wave_kills += 1 # Gets reset after every wave
        self.total_kills += 1 # Stays for the whole game.

        # 0 - 100% this is used to determine if a weapon, boost, or amror will drop. Its not gaurunteed to drop an item but it stops multiple item drops from 1 death
        one_item_drop = random.random() 

        # It's chceking the number drop chances based on the drop chances set in SetupItems()
        if one_item_drop < 0.33:
            # Based on gun drop chances, its rolling a chance at a gun drop.
            self.weapon_drop_chance = random.random() # 0 - 100%
            if self.weapon_drop_chance <= self.handgun_drop_chance:
                self.ItemSpawnWeapon(1, location)
            elif self.weapon_drop_chance <= self.shotgun_drop_chance:
                self.ItemSpawnWeapon(2, location)
            elif self.weapon_drop_chance <= self.mp4_drop_chance:
                self.ItemSpawnWeapon(3, location)
        elif one_item_drop < 0.66:
            # Based on boost drop chances, its rolling a chance at a gun drop.
            self.boost_drop_chance = random.random() # 0 - 100%
            if self.boost_drop_chance <= self.orange_boost_drop_chance:
                self.ItemSpawnBoost(1, location)
            elif self.boost_drop_chance <= self.red_boost_drop_chance:
                self.ItemSpawnBoost(2, location)
            elif self.boost_drop_chance <= self.blue_boost_drop_chance:
                self.ItemSpawnBoost(3, location)
            elif self.boost_drop_chance <= self.purple_boost_drop_chance:
                self.ItemSpawnBoost(4, location)
        else:
            # Based on armor drop chances, its rolling a chance at a armor drop.
            self.armor_drop = random.random() # 0 - 100%
            if self.armor_drop <= self.armor_drop_chance:
                self.ItemSpawnArmor(location)
    
    def EndOfWave(self):
        # Wave ends (timer runs out) and this method gets called.
        self.wave_number += 1
        self.shooter_game.wave_end_menu.WaveEnded()
        self.ResetWaveStats()
        self.shooter_game.OpenEndWaveMenu()
        self.player.NewWave()

    def ResetWaveStats(self):
        # This function resets the wave stats at the end of each wave
        self.clock_actual = 0 # divided by 60 frames per second
        self.clock = 0 # The time in seconds
        self.wave_kills = 0 # Total wave kills for this wave
        self.enemies_list = []
        self.wave_timer = float(0)
        self.wave_timer_actual = 0 
        self.annoucemnt_made = False
        self.game_music_played = False

    def CalculateDifficulty(self):
        # Define the parameters for the difficulty curve
        self.difficulty = 1 + (self.wave_number / 10) * 1.05
        self.SpawnCooldownRate() # sets the spawn cooldown based on wave number

    # ====================================================================
    # ====================== [ITEM FUNCTIONS BELOW] ======================

    def ItemSpawnWeapon(self, weapon_index, location):
        # The gun_index is the gun (1=handgun, 2=shotgun, 3=mp3) that is dropping

        # Rolling between 0 - 100%, this number is compared to the drop chance ratios of the ammo
        self.random_ammo_number = random.random()
 
        if self.random_ammo_number < 0.2:
            # handgun dropped, using the random_ammo_number to determine how much ammo is dropping
            if(weapon_index == 1):
                ammo_ammount = self.handgun_ammo_amount [0]
            elif(weapon_index == 2):
                ammo_ammount = self.shotgun_ammo_amount [0]
            else:
                ammo_ammount = self.mp4_ammo_amount [0]
        elif self.random_ammo_number < 0.85:
            # shotgun dropped, using the random_ammo_number to determine how much ammo is dropping
            if(weapon_index == 1):
                ammo_ammount = self.handgun_ammo_amount [1]
            elif(weapon_index == 2):
                ammo_ammount = self.shotgun_ammo_amount [1]
            else:
                ammo_ammount = self.mp4_ammo_amount [1]
        else:
            # mp4 dropped, using the random_ammo_number to determine how much ammo is dropping
            if(weapon_index == 1):
                ammo_ammount = self.handgun_ammo_amount [2]
            elif(weapon_index == 2):
                ammo_ammount = self.shotgun_ammo_amount [2]
            else:
                ammo_ammount = self.mp4_ammo_amount [2]
        self.weapon_item.append(ground_item.GroundWeapon(weapon_index, ammo_ammount, location, self.shooter_game))

    def ItemSpawnBoost(self, boost_index, location):
        # A boost is dropping, the boost_index determines the boost dropping (1=orange, 2=red, 3=blue, 4=purple)
        if boost_index == 1: # ORANGE
            self.boost_item.append(ground_item.GroundBoost(boost_index, location, self.shooter_game))
        elif boost_index == 2: # RED
            self.boost_item.append(ground_item.GroundBoost(boost_index, location, self.shooter_game))
        elif boost_index == 3: # BLUE
            self.boost_item.append(ground_item.GroundBoost(boost_index, location, self.shooter_game))
        elif boost_index == 4: # PURPLE
            self.boost_item.append(ground_item.GroundBoost(boost_index, location, self.shooter_game))

    def ItemSpawnArmor(self, location):
        # Armor is dropping, creating the armor item
        self.armor_item.append(ground_item.GroundArmor(location, self.shooter_game))

    # ====================================================================
    # ===================== [TIMER FUNCTIONS BELOW] ======================

    def UpdateClock(self):
        # Updates the wave clock
        self.wave_timer_actual += 1
        self.wave_timer = float(self.wave_timer_actual / 60)
    
    def UpdateClockTimer(self):
        # Updates the clock for the wave time.

        # Updates actual clock then divides it by 60 frames to get the clock in seconds.
        self.clock_actual += 1
        if self.clock_actual >= 60:
            self.clock = int(self.clock_actual / 60)

        # Setting the seconds and minutes variables
        seconds = self.clock
        minutes = 0

        # updates the timer to have minutes on left side of : and seconds on the right side
        if seconds >= 60:
            # The timer is above 60 seconds and is 1 minute or higher

            # Setting the seconds and minutes variables
            minutes = int(seconds / 60)
            seconds = seconds - (60 * minutes)

            # seconds is less then 10 so its putting a zero before the single number digit
            if seconds < 10:
                seconds = "0" + str(seconds)

            # Adding the minutes and seconds together with ":" between, the setting it to a message
            time = str(minutes) + ":" + str(seconds)
            self.wave_clock_message = self.wave_clock.render(str(time), True, self.RED)
        else: 
            # Setting the timer message in seconds because its under 1 minute (: isn't used so it just shows the time in seconds)
            self.wave_clock_message = self.wave_clock.render(str(seconds), True, self.RED)

    # ====================================================================
    # ================= [OUTSIDE CALL FUNCTIONS BELOW] ===================

    def NextWavePressed(self):
        # These functions are called by outside scripts
        self.CalculateDifficulty()
    

    

    

    

   

    

    

   

   

    

    

   

    

    

    
        
    