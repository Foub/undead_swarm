import pygame
import math

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:
# BulletProjectile(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupBulletProjectile(self, player, spawned_x, spawned_y) * Sets up the techincal stuff for the bullet projectile
# SetupBulletImage(self) * Setting the starting image and location
# SetupBulletProjectileStats(self, damage, max_target_pierce, bullet_type) * Sets up the bullets stats (attributes)

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * Gets called every frame, by the shooter_game script's update call

# } END OF BulletProjectile(Class)


handgun_bullet_projectile = pygame.image.load('Character\Ammo\handgun_bullet_projectile.png')
#handgun_bullet_projectile.set_colorkey((255, 255, 255)) # set the white color to be transparent

shotgun_bullet_projectile = pygame.image.load('Character\Ammo\shotgun_bullet_projectile.png')
#shotgun_bullet_projectile.set_colorkey((255, 255, 255)) # set the white color to be transparent

mp4_bullet_projectile = pygame.image.load('Character\Ammo\mp4_bullet_projectile.png')
#mp4_bullet_projectile.set_colorkey((255, 255, 255)) # set the white color to be transparent


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, spawned_x, spawned_y, destination_x, destination_y, damage, max_target_pierce, player):  
        super().__init__()
        # Called when the bullet is first created.
        self.SetupBulletProjectile(player, spawned_x, spawned_y, destination_x, destination_y)
        self.SetupBulletImage(bullet_type)
        self.SetupBulletProjectileStats(damage, max_target_pierce, bullet_type)

    # ====================================================================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupBulletProjectile(self, player, spawned_x, spawned_y, destination_x, destination_y):
        # Sets up the techincal stuff for the bullet projectile
        self.player = player
        self.enemies_hit = [] # If number exceeds max_target_pierce the bullet will be destroyed (Also one zombie cant be hit by the same bullet more than once)
        self.waves = self.player.waves
        self.start_x = spawned_x
        self.start_y = spawned_y

        # Mouse Detection
        self.destination_x = destination_x # x position of where the bullet is going
        self.destination_y = destination_y # y position of where the bullet is going
        self.angle_degrees = 0 # The angle from the start to end point


    def SetupBulletImage(self, bullet_type):
        # Setting the starting image and location
        if bullet_type == 1:
            self.normal_image = handgun_bullet_projectile.convert()
        elif bullet_type == 2:
            self.normal_image = shotgun_bullet_projectile.convert()
        else:
            self.normal_image = mp4_bullet_projectile.convert()

        self.normal_image.set_colorkey((255, 255, 255)) # set the white color to be transparent
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y

        # bullet Speeds floats to allow decimal increment changes
        self.x_position = float(self.rect.x)
        self.y_position = float(self.rect.y)

    def SetupBulletProjectileStats(self, damage, max_target_pierce, bullet_type):
        # Sets up the bullets stats (attributes)
        self.bullet_damage = damage
        self.max_target_pierce = max_target_pierce # Number of enemies the bullet can travel through before its destroyed

        # Bullets speeds based on gun type.
        self.handgun_bullet_speed = 25
        self.shotgun_bullet_speed = 25
        self.mp4_bullet_speed = 60

        # Setting bullet speed based on bullet type
        if bullet_type == 1:
            self.speed = self.handgun_bullet_speed
        elif bullet_type == 2:
            self.speed = self.shotgun_bullet_speed
        else:
            self.speed = self.mp4_bullet_speed

    # ====================================================================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================

    def update(self): 
            # Gets called every frame, by the shooter_game script's update call

            # Calculate the angle between the character's position and the mouse position
            dx = self.destination_x - self.start_x
            dy = self.destination_y - self.start_y
            angle = math.atan2(dy, dx)
            self.angle_degrees = math.degrees(angle)

            #Move the image in the direction of the angle
            radians = math.radians(self.angle_degrees)
            self.x_position += self.speed * math.cos(radians)
            self.y_position += self.speed * math.sin(radians)
            self.rect.x = self.x_position
            self.rect.y = self.y_position

            #self.image = pygame.transform.rotate(pygame.transform.scale(bullet_projectile, (int(bullet_projectile.get_width() * 0.05), int(bullet_projectile.get_height() * 0.05))), self.angle_degrees)
            rotated_image = pygame.transform.rotate(self.normal_image, -self.angle_degrees)
            scaled_image = pygame.transform.scale(rotated_image, (int(rotated_image.get_width() * 0.05), int(rotated_image.get_height() * 0.05)))
            self.image = scaled_image
            self.rect = self.image.get_rect(center=self.rect.center)

            # Checking if any of the zombies on the map are in the collision rect of the bullet.
            for zombie in self.waves.enemies_list:
                if self.rect.colliderect(zombie) and not zombie in self.enemies_hit:
                     if zombie.CollisionCheck(self) == True:
                        self.enemies_hit.append(zombie)
                        zombie.TakeDamage(self.bullet_damage)

            # if the bullet passes it's max target pierce, it will get destroyed.
            if len(self.enemies_hit) > self.max_target_pierce:
                self.player.weapon.all_bullets.remove(self)
                del self
                     

        




