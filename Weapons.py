import pygame
import math
import BulletProjectile as bullet_projectile

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# Weapons(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupKnifeHitBox(self) * Sets up the parameters for the knife hitbox at the start of the game
# SetupTechnicalStuff(self, player) * Sets up the technical stuff related to the weapon class
# SetupWeaponStats(self) * Sets, damage, cooldown, pierced targets and clipsize for all 3 guns, and knife damage.

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * Actual update function that's called every frame by the ShooterGame update class
# UpdateKnifeAttackHitbox(self) * Gets updated in the update method after a player initiates the knife attack

# -[COMBAT FUNCTIONS BELOW]-
# Knife and Gun mechanics functions are in the OUTSIDE CALL list because they are only called by scripts outside of this script.
# GetFacingDirection(self) * Sets up the facing direction location to be called when the knife mechanics is damaging enemies in the radius
# SpawnBullet(self, spawn_location) * Called from GunMechanics() function when shooting a gun (The actual method for spawning the bullet after a gun attack)
# DamageZombies(self, zombie_hit) * Gets called in the update call for every zombie in the hitbox.

# -[SOUND FUNCTIONS BELOW]-
# KnifeSound(self) * It will only get called once right when the knife attack animation is halfway done (called in update call)

# -[OUTSIDE CALL FUNCTIONS BELOW]-
# GetClipsize (self, index) * Called by other scripts to get the clip size of that weapon type
# KnifeMechanics(self) * Called by the character class when attempting to attack with a knife
# GunMechanics(self, spawn_location) * Called by the character class when attempting to fire a gun


# } END OF Weapons(Class)


# =========== [END OF TABLE OF CONTENTS] ==========
# =================================================

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        # Set up when the class is first created.
        self.SetupTechnicalStuff(player) # Sets up the technical stuff related to the weapon class
        self.SetupKnifeHitBox() # Sets up the knife hitbox stats
        self.SetupWeaponStats() # Sets, damage, cooldown, pierced targets and clipsize for all 3 guns, and knife damage.
        self.SetupShotgun() # Sets up the shotgun bullet location and targets for the spread effect.

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupKnifeHitBox(self):
        # Sets up the hitbox stats at the start when the weapons class is created
        self.knife_hitbox = None
        self.knife_swing_width = 100
        self.knife_swing_height = 40
        self.knife_swing_offset = 30
        self.knife_attack_duration = 40
        self.knife_attack_timer = 0   

    def SetupTechnicalStuff(self, player):
        # Sets up all of the technical stuff that's needed later on
        self.player = player
        self.knife_pos = (0, 0)
        self.all_bullets = pygame.sprite.Group() # This list holds the sprites of the bullets
        self.knife_sound_played = False
        self.hit_targets = [] #enemies hit with the knife attack are placed here
        self.targets_damaged = [] #the ones damaged so they dont get hit again

    def SetupWeaponStats(self):
        # Sets, damage, cooldown, pierced targets and clipsize for all 3 guns, and knife damage.

        # KNIFE
        self.knife_damage = 40

        # HANDGUN
        self.handgun_cooldown = 1 # second(s)
        self.handgun_damage = 20
        self.handgun_max_targets_pierced = 1 # Number of enemies the bullet can travel through before its destroyed
        self.handgun_clipsize = 30

        # SHOTGUN
        self.shotgun_cooldown = 3.0 # second(s)
        self.shotgun_damage = 15
        self.shotgun_max_targets_pierced = 1 # Number of enemies the bullet can travel through before its destroyed
        self.shotgun_clipsize = 20

        # MP4
        self.mp4_cooldown = 0.2 # second(s)
        self.mp4_damage = 25
        self.mp4_max_targets_pierced = 2 # Number of enemies the bullet can travel through before its destroyed
        self.mp4_clipsize = 50

    def SetupShotgun(self):
        # Shotgun spread will work in rows of 3's example:
        #                *   *   *
        self.shotgun_bullet_count = 3
        self.shotgun_middle_bullet_offset = 10
        self.shotgun_side_bullet_offset = 3


    # ====================================================================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================

    def update(self):
        # Called every frame (60 fps) by the ShooterGame class
        
        if self.knife_attack_timer > 0:
            # If the player recently attacked this update will continue to detect enemies in the radius and initiate the Damage zombies method
            self.knife_attack_timer -= 1
            self.GetFacingDirection()
            self.UpdateKnifeAttackHitbox()
            self.KnifeSound() # It will only get called once right when the knife attack animation is halfway done
            for zombie in self.player.waves.enemies_list:
                if self.knife_hitbox.colliderect(zombie.rect):
                    if zombie.CollisionCheck(self.knife_hitbox) == True:
                        self.DamageZombies(zombie)
        else:
            # If the player didn't recently attack, it clears all of the variables that are used for attacks
            self.hit_targets.clear()
            self.targets_damaged.clear()
            self.knife_hitbox = None
            self.knife_sound_played = False

    def UpdateKnifeAttackHitbox(self):
        # Gets updated in the update method after a player initiates the knife attack
        # Calculate the position and orientation of the knife based on the player's position and facing direction
        self.knife_pos = self.player_pos + (self.facing_direction * self.knife_swing_offset)
        self.knife_hitbox = pygame.Rect(self.knife_pos[0], self.knife_pos[1], self.knife_swing_height, self.knife_swing_width)

        surface = pygame.Surface((self.knife_hitbox.width, self.knife_hitbox.height))
        rect = surface.get_rect()
        
        surface = pygame.transform.rotate(surface, -self.angle_degrees)
        rect.center = self.knife_hitbox.center
        self.knife_hitbox = rect
        self.knife_hitbox.center = rect.center

    # ====================================================================
    # ==================== [COMBAT FUNCTIONS BELOW] ======================

    def DamageZombies(self, zombie_hit):
        # Gets called for every zombie in the hitbox.
        # damage enemy (checks if enemy was hit by this attack in a different frame. If so it wont damage the enemy again)

        if not zombie_hit in self.hit_targets:
            self.hit_targets.append(zombie_hit)

        if self.knife_attack_timer > (self.knife_attack_duration / 2): # The knife attack is less then halfway done the animation
            return
        elif len(self.hit_targets) > 0: # This makes a delay in the time it takes for a zombie to take the damage. So the zombie doesn't take damage the milisecond the animation starts
            if not zombie_hit in self.targets_damaged:
                zombie_hit.TakeDamage(self.knife_damage)
                self.targets_damaged.append(zombie_hit)
 
    def GetFacingDirection(self):
        # Sets up the facing direction location to be called when the knife mechanics is damaging enemies in the radius
        self.player_pos = (self.player.rect.center[0], self.player.rect.center[1])
        dx = self.player.mouse_x - self.player_pos[0]
        dy = self.player.mouse_y - self.player_pos[1]
        angle = math.atan2(-dy, dx)
        self.angle_degrees = math.degrees(angle)

        # Calculate the direction that the character sprite is facing
        rotation_angle = math.radians(self.angle_degrees)
        self.facing_direction = pygame.math.Vector2(math.cos(rotation_angle), -math.sin(rotation_angle))

    def GetTarget(self, shotgun, spawn_location):
        # Gets the target location of the bullet based on players facing direction
        # shotgun_bullets is null unless it's the shotgun being fired

        # Calculate the direction that the bullet sprite is facing
        rotation_angle = math.radians(self.player.angle_degrees)
        bullet_target_direction = pygame.math.Vector2(math.cos(rotation_angle), -math.sin(rotation_angle))
        main_bullet_target = spawn_location + bullet_target_direction * self.shotgun_middle_bullet_offset 

        if not shotgun:
            self.FireGun(spawn_location, main_bullet_target)
        else:
            # Shotgun was fired
            # Calculate the perpendicular vector to the bullet_target_direction
            perpendicular_direction = pygame.math.Vector2(-bullet_target_direction.y, bullet_target_direction.x)

            # Calculate the positions of the side bullets
            left_bullet_target = main_bullet_target - perpendicular_direction * self.shotgun_side_bullet_offset
            right_bullet_target = main_bullet_target + perpendicular_direction * self.shotgun_side_bullet_offset
            self.FireShotgun(spawn_location, left_bullet_target, main_bullet_target, right_bullet_target)

    def FireGun(self, spawn_location, target_location):
        if(self.player.character_weapon == 1 and self.player.GetAmmoCount(1) > 0):
            self.player.SetAmmoCount(1, -1)
            self.player.shooter_game.HandgunAttackSound()
            self.SpawnBullet(1, spawn_location, target_location)
        elif(self.player.character_weapon == 3 and self.player.GetAmmoCount(3) > 0):
            self.player.SetAmmoCount(3, -1)
            self.player.shooter_game.Mp4AttackSound()
            self.SpawnBullet(3, spawn_location, target_location)
        
    def FireShotgun(self, spawn_location, left_bullet_target, main_bullet_target, right_bullet_target):
        if(self.player.character_weapon == 2 and self.player.GetAmmoCount(2) > 0):
            self.player.SetAmmoCount(2, -1)
            self.player.shooter_game.ShotgunAttackSound()
            self.SpawnBullet(2, spawn_location, left_bullet_target)
            self.SpawnBullet(2, spawn_location, main_bullet_target)
            self.SpawnBullet(2, spawn_location, right_bullet_target)

    def SpawnBullet(self, weapon_index, spawn_location, target_location):
        # The actual method for spawning the bullet after a gun attack

        # HANDGUN ATTACK SPAWNS BULLET
        if(weapon_index == 1):
            bullet = bullet_projectile.Bullet(weapon_index, spawn_location[0], spawn_location[1], target_location[0], target_location[1], self.handgun_damage, self.handgun_max_targets_pierced, self.player) # Creating a bullet
            self.player.weapon.all_bullets.add(bullet)
        # SHOTGUN ATTACK SPAWNS BULLET
        elif(weapon_index == 2):
            bullet = bullet_projectile.Bullet(weapon_index, spawn_location[0], spawn_location[1], target_location[0], target_location[1], self.shotgun_damage, self.shotgun_max_targets_pierced, self.player) # Creating a bullet
            self.player.weapon.all_bullets.add(bullet)
        # MP4 ATTACK SPAWNS BULLET
        elif(weapon_index == 3):
            bullet = bullet_projectile.Bullet(weapon_index, spawn_location[0], spawn_location[1], target_location[0], target_location[1], self.mp4_damage, self.mp4_max_targets_pierced, self.player) # Creating a bullet
            self.player.weapon.all_bullets.add(bullet)

    # ====================================================================
    # ===================== [SOUND FUNCTIONS BELOW] ======================

    def KnifeSound(self):
        if not self.knife_sound_played:
            if self.knife_attack_timer < (self.knife_attack_duration / 2): # The attack animation passed the halfway mark to completetion
                self.player.shooter_game.KnifeAttackSound()
                self.knife_sound_played = True

    # ====================================================================
    # ================= [OUTSIDE CALL FUNCTIONS BELOW] ===================
        
    def GetClipsize (self, index): 
        # Returns the base clipsize for each gun (Max ammo amount per gun)
        if index == 0:
            return None
        if index == 1:
            return self.handgun_clipsize
        if index == 2:
            return self.shotgun_clipsize
        if index == 3:
            return self.mp4_clipsize  
    
    def KnifeMechanics(self):
        # Knife mechanics is called when the player attacks with a knife and it sets up the variables to damage zombies in the update method
        # Get the facing direction
        #self.GetFacingDirection()
        self.knife_attack_timer = self.knife_attack_duration

    def GunMechanics(self, spawn_location):
        # Gun mechanics is called when the player attacks with a gun and spawns the bullet
        # This method checks if the player has ammo for that type of gun. If so the gun will fire a bullet
        if(self.player.character_weapon == 1): # 1 == HANDGUN
            if(self.player.GetAmmoCount(1) > 0):
                self.GetTarget(False, spawn_location)
        # Checking if player has bullets for that gun type
        if(self.player.character_weapon == 2): # 2 == SHOTGUN
            if(self.player.GetAmmoCount(2) > 0):
                self.GetTarget(True, spawn_location)
        # Checking if player has bullets for that gun type
        if(self.player.character_weapon == 3): # 3 == MP4
            if(self.player.GetAmmoCount(3) > 0):
                self.GetTarget(False, spawn_location)
    
    

    

    
    
    

    

    
            
        
    
    
        

