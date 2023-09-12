import pygame
import math

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# Enemy(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupZombieAnimation(self) * Sets up the images, and max frames for the enemies animations
# SetupZombieStats(self, health_ratio, damage_ratio, attack_cooldown_ratio, mov_speed_ratio) * Zombies stats, updated based on ratio's determined by wave number difficulty increases
# SetupZombieTechnical(self,player, spawn_location, shooter_game) * Sets up all zombies technical stuff, NOT stat related.

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * Main update function of this class, gets called every frame by the shooter_game class
# UpdateCurrentFrame(self) * This is called every update to update the current frame for the enemies animation
# UpdateZombieAnimation(self, angle) * Setting the zombies animation, and rotation based on the current animation (attack, walk, idle)
# UpdateBloodSplat(self) * This is the blood splat animation, it gets called by update() after the enemy dies. Once complete enemy is deleted.

# -[CHANGE FUNCTIONS BELOW]-
# 

# -[TIMER FUNCTIONS BELOW]-
# AttackCooldownTimer(self) * The timer that goes down until attack cooldown reaches 0
# DamageTakenTimer(self) * The timer that goers down after a zombie is attacked, (when above 0 the enemy has a health bar above their head).

# -[COMBAT FUNCTIONS BELOW]-
# StartAttackPlayer(self) * The function thats called to start the attack on the player, if attack cooldown is 0 and enemy is in attack range of player
# DealDamageToPlayer(self) * Actually deals damage to the player, theres a delay after attack starts to make it more realistic
# TakeDamage(self, damage) * Lowers zombies health and updates ShooterGame for health bar UI


# -[OUTSIDE CALL FUNCTIONS BELOW]-
# * Any functions called from an outside script *
# CollisionCheck(self, object_hit) * This returns true if the object is colliding with another object

# } END OF Enemy(Class)

# =========== [END OF TABLE OF CONTENTS] ==========
# =================================================

# Loading zombie idle animation
zombie_idle_frames = 17
zombie_idle_animation =   [pygame.image.load(f"Zombie\\zombie_idle\\skeleton-idle_{i}.png") for i in range(zombie_idle_frames)]    

# Loading zombie walk animation
zombie_walk_frames = 17
zombie_walk_animation =   [pygame.image.load(f"Zombie\\zombie_walk\\skeleton-move_{i}.png") for i in range(zombie_walk_frames)]

# Loading zombie attack animation
zombie_attack_frames = 9
zombie_attack_animation =   [pygame.image.load(f"Zombie\\zombie_attack\\skeleton-attack_{i}.png") for i in range(zombie_attack_frames)]

blood_splat_frames = 9
blood_splat_animation = [pygame.image.load(f"Effects\\blood_splatter\\blood_splatter_{i}.png") for i in range(blood_splat_frames)]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, health_ratio, damage_ratio, attack_cooldown_ratio, mov_speed_ratio, spawn_location, shooter_game):
        super().__init__()

        # The are called when the enemy (zombie) is first created
        self.SetupZombieAnimation()
        self.SetupZombieStats(health_ratio, damage_ratio, attack_cooldown_ratio, mov_speed_ratio)
        self.SetupZombieTechnical(player, spawn_location, shooter_game) 

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupZombieAnimation(self):
        
        self.zombie_idle_animation = zombie_idle_animation
        self.zombie_walk_animation = zombie_walk_animation
        self.zombie_attack_animation = zombie_attack_animation
        self.blood_splat_animation = blood_splat_animation

        # Blood effects
        self.blood_splat_current_frame = 0
        self.blood_splat_frame_increment = 0.4
        self.current_blood_frame_image = self.blood_splat_animation[0]
        self.blood_effect_rect = self.current_blood_frame_image.get_rect()

        # Setting the transparency of all of the blood splat animation sprites
        for blood_image in self.blood_splat_animation:
            blood_image.set_colorkey((255, 255, 255))

    def SetupZombieStats(self, health_ratio, damage_ratio, attack_cooldown_ratio, mov_speed_ratio):
        # Zombies stats, updated based on ratio's determined by wave number difficulty increases
        self.attack_cooldown_rate = 5 * attack_cooldown_ratio
        self.attack_cooldown = 180 - self.attack_cooldown_rate # 2 seconds (60 fps) ratio will go down with each wave making their attacks faster
        self.movement_speed_rate = 0.2 *  mov_speed_ratio
        self.movement_speed = 1.3 + self.movement_speed_rate 
        self.max_health = 40 * health_ratio
        self.current_health = self.max_health
        self.damage = 8 * damage_ratio
        self.attack_cooldown_timer = 0
        self.attack_range = 80

    def SetupZombieTechnical(self,player, spawn_location, shooter_game):
        # Sets up all zombies technical stuff, NOT stat related.

        # Zombie booleans
        self.damage_taken = False # This will have a timer after taking damage and will be set back to false. Its for the health bar duration above zombies head
        self.player_attacked = False
        self.attacking = False
        self.walking = False
        self.dead = False
        
        # Zombie image, rect and location info
        self.image = self.zombie_idle_animation[0]
        self.rect = self.image.get_rect()
        self.rect.x = spawn_location[0]
        self.rect.y = spawn_location[1]
        self.position_x = spawn_location[0]
        self.position_y = spawn_location[1]

        # Setup collision
        self.collide_height = 100
        self.collide_width = 100
        self.collision_rect = pygame.Rect(self.rect.center[0] - (self.collide_width / 2), self.rect.center[1] - (self.collide_height / 2), self.collide_width, self.collide_height)

        # Zombie cooldown/timer related
        self.attack_damage_delay = 35 # How many frames after the attack animation starts before the damage hits the player (more realistic)
        self.attack_delay_timer = 0
        self.damage_taken_timer = 0
        self.damage_taken_time = 150

        # Zombie animation related
        self.current_frame = float(0) # So it allows decimals
        self.current_frame_increment = float(0.15) # So it allows decimals

        # Other stuff
        self.shooter_game = shooter_game # Shooter_game main class reference
        self.player = player # Player class reference

    # ====================================================================
    # ===================== [UPDATE FUNCTIONS BELOW] =====================

    def update(self):
        # Updated every frame (60 fps) called by the main scripts main update call

        # The enemy is dead, this calls the UpdateBloodSplat() until the enemy is deleted
        if self.dead == True:
            self.UpdateBloodSplat()
            return

        # Calculate distance to player
        dx = self.player.rect.center[0] - self.rect.center[0]
        dy = self.player.rect.center[1] - self.rect.center[1]
        dist = math.sqrt(dx ** 2 + dy ** 2)

        # Get the angle
        angle = math.atan2(dy, dx)

        # Reducing attack cooldown if the zombie recently attacked
        self.AttackCooldownTimer()

        # Stop moving if within attack range
        if dist <= self.attack_range:
            self.walking = False # Setting walking boolean to false, because the zombie can't attack and move at the same time (also because zombie is in attack range)
            if self.attacking == False and self.attack_cooldown_timer <= 0 and self.player.current_health > 0 and self.current_health > 0:
                # If player and zombie isn't dead, the attack cooldown is 0, and its within attack range the zombie will attack
                self.StartAttackPlayer()
        else:
            # If the zombie isn't in attack range its automatically walking because they non stop walk to the players current location
            self.walking = True

        # Zombie attacked the player but the damage isn't dealt yet because there's a delay to make it more realistic
        if self.player_attacked == True: 
            # The attack delay timer is still under the set damage delay
            if self.attack_delay_timer < self.attack_damage_delay:
                self.attack_delay_timer += 1
            else:
            # Once the attack delay timer reaches the damage delay, it deals damage to the player.
                self.DealDamageToPlayer()

        # Setting the current animation frame and the animation sprites
        self.UpdateCurrentFrame()
        self.UpdateZombieAnimation(angle)

        # If zombie is walking, this will make the zombie actually walk.
        if self.walking == True:
            # Move towards player 
            self.position_x += math.cos(angle) * self.movement_speed
            self.position_y += math.sin(angle) * self.movement_speed

        # Updating image rotation, and image rect.
        self.image = pygame.transform.rotate(self.image, math.degrees(-angle))
        self.rect = self.image.get_rect(center=(self.position_x, self.position_y))
        self.blood_effect_rect.center = self.rect.center

        # Collision related
        self.collision_rect.x = self.rect.center[0] - (self.collide_width / 2)
        self.collision_rect.y = self.rect.center[1] - (self.collide_height / 2)
        self.collision_rect.width = self.collide_width
        self.collision_rect.height = self.collide_height

    def UpdateCurrentFrame(self):
        # Sets the current animation frame and resets it if the frame hits the max frame for that animation type

        # Increasing current frame
        self.current_frame += self.current_frame_increment

        # Checking if frame is over the animation clip limit. If so it resets it back to 0 to make an animation loop.
        if self.attacking:
            # Zombie attacking
            if self.current_frame > zombie_attack_frames:
                self.current_frame = 0
                self.attacking = False
        elif self.walking:
            # Zombie walking
            if self.current_frame > zombie_walk_frames:
                self.current_frame = 0
        else:
            # Zombie idle
            if self.current_frame > zombie_idle_frames:
                self.current_frame = 0

    def UpdateZombieAnimation(self, angle):
        # Setting the zombies animation, and rotation based on the current animation (attack, walk, idle)
        if self.attacking:
            # Zombie attacking
            temp_image = self.zombie_attack_animation[int(self.current_frame)]
        elif self.walking:
            # Zombie walking
            temp_image = self.zombie_walk_animation[int(self.current_frame)]
        else:
            # Zombie idle
            temp_image = self.zombie_idle_animation[int(self.current_frame)]

        # Setting the zombies current sprite, and setting it to the rect location
        self.image = pygame.transform.rotate(pygame.transform.scale(temp_image, (int(temp_image.get_width() * 0.5), int(temp_image.get_height() * 0.5))), int(angle))       
        self.rect = self.image.get_rect(center=self.rect.center)

    def UpdateBloodSplat(self):
        # Blood splat animation, called in update() after enemy dies

        # Increasing the blood splat current frame by the increment
        self.blood_splat_current_frame += self.blood_splat_frame_increment

        if self.blood_splat_current_frame >= blood_splat_frames: 
            # Zombie is officially dead, blood splat animation is done playing and now the enemy is being deleted
            self.player.waves.ZombieKilled(self.rect.center)
            self.player.waves.enemies_list.remove(self)
            del self
        else:
            # Blood splat animation isn't done yet, setting the image to the current frame of the blood splat animation
            self.current_blood_frame_image = self.blood_splat_animation[int(self.blood_splat_current_frame)]

    # ====================================================================
    # ===================== [TIMER FUNCTIONS BELOW] ======================

    def AttackCooldownTimer(self):
        # Zombie attacked recently and the cooldown timer is going down
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1

    def DamageTakenTimer(self):
        # Zombie took damage recently, when timer is above 0 it displays the health bar above their head
        if self.damage_taken_timer > 0:
            self.damage_taken_timer -= 1
        else:
            self.damage_taken = False

    # ====================================================================
    # ==================== [COMBAT FUNCTIONS BELOW] ======================

    def StartAttackPlayer(self):
        # Zombie started attacking the player
        self.attacking = True
        self.player_attacked = True
        self.current_frame = 0
        self.attack_cooldown_timer = self.attack_cooldown

    def DealDamageToPlayer(self):
        # Deals damage to the player
        self.player_attacked = False
        self.attack_delay_timer = 0
        self.shooter_game.ZombieAttackSound()
        self.player.TakeDamage(self.damage)

    def TakeDamage(self, damage):
        # Lowers zombies health and updates ShooterGame for health bar UI 

        # If player has boost(orange), it will double the damage the zombie takes
        if self.player.HasBoost(1):
            damage = damage * 2

        # Damage taken is set to true and timer is set (while true theres a health bar above the zombie)
        self.damage_taken = True
        self.damage_taken_timer = self.damage_taken_time

        # Lowering the zombies health based on the damage dealt
        self.current_health -= damage

        if self.current_health <= 0:
            # Health reached 0, zombie is dead and the dead sound is played
            self.dead = True
            self.shooter_game.DeadSound()
        else:
            # Health still above 0, zombie hit sound is played
            self.shooter_game.ZombieHitSound()


    # ====================================================================
    # ==================== [OUTSIDE FUNCTIONS BELOW] =====================

    # Any functions called from an outside script

    def CollisionCheck(self, object_hit):
        # This returns true if the object is colliding with another object
        if self.collision_rect.colliderect(object_hit):
            return True
        else:
            return False
    


    