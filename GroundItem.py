import pygame

# THERE IS 3 SEPERATE ITEMS CURRENTLY IN THIS SCRIPT (GAME) THE TABLE OF CONTENTS WILL CONTAIN ALL 3 ITEM CLASSES:

# =================================================
# ============== [TABLE OF CONTENTS] ==============
# (EVERY FUNCTION IN THIS SCRIPT) 
# * Is used to add a description:

# GroundWeapon(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupGroundWeapon(self, gun_index, ammo_count, location, shooter_game) * Set up the ground weapon item
# SetupGroundWeaponImages(self, shooter_game) * Sets up the three gun images for the dropped weapon items

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * Updates every update call by the Wave class when there is any weapons on the ground.

# End of GroundWeapon(class)}

# GroundBoost(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupGroundBoost(self, boost_index, location, shooter_game) * # Set up the ground boost item
# SetupGroundBoostImages(self) * Sets up the four boost images for the dropped boost items

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * Updates every update call by the Wave class when there is any boosts on the ground.

# End of GroundBoost(class)}

# GroundArmor(Class){
# __init__() *called when the class is created*

# -[SETUP FUNCTIONS BELOW]-
# SetupGroundArmor(self) * Sets up all aspects of the ground armor item

# -[UPDATE FUNCTIONS BELOW]-
# update(self) * Updates every update call by the Wave class when there is any armor on the ground.

# End of GroundArmor(class)}

# =========== [END OF TABLE OF CONTENTS] ==========
# =================================================

class GroundWeapon(pygame.sprite.Sprite):
    def __init__(self, gun_index, ammo_count, location, shooter_game):
        super().__init__()
        # called when the item is first created
        self.SetupGroundWeapon(gun_index, ammo_count, location, shooter_game)
        self.SetupGroundWeaponImages()

    # ========================== GROUND WEAPON ===========================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupGroundWeapon(self, gun_index, ammo_count, location, shooter_game):
        # Set up the ground weapon item
        self.gun_index = gun_index
        self.ammo_count = ammo_count
        self.location = location
        self.shooter_game = shooter_game
        self.player = shooter_game.character
        self.ground_duration = 60 * 15 # 15 seconds

    def SetupGroundWeaponImages(self):
        # Sets up the three gun images for the dropped weapon items

        # Handgun dropped
        if self.gun_index == 1:
            self.rect = self.shooter_game.handgun_image.get_rect()
            self.rect.center = self.location
        # Shotgun dropped
        elif self.gun_index == 2:
            self.rect = self.shooter_game.shotgun_image.get_rect()
            self.rect.center = self.location
        # MP4 dropped
        else:
            self.rect = self.shooter_game.mp4_image.get_rect()
            self.rect.center = self.location
    
    # ========================== GROUND WEAPON ===========================
    # ===================== [UPDATE FUNCTIONS BELOW] =====================

    def update(self):
        # Updates every frame, called by the Waves class update

        if self.rect.colliderect(self.player.rect):
            # Detects if the player collides with this item. If the player does the item is destroyed and added to the player.
            self.player.SetAmmoCount(self.gun_index, self.ammo_count)
            self.player.waves.weapon_item.remove(self)
            del self
        elif self.ground_duration > 0:
            # lowers the ground duration timer, when it reaches 0 the item is destroyed.
            self.ground_duration -= 1
        else: 
            # Player took too long to pick up the boost and it disapeared 
            self.player.waves.weapon_item.remove(self)
            del self

class GroundBoost(pygame.sprite.Sprite):
    def __init__(self, boost_index, location, shooter_game):
        super().__init__()
        # called when the item is first created
        self.SetupGroundBoost(boost_index, location, shooter_game)
        self.SetupGroundBoostImages()
    
    # ========================== GROUND BOOST ============================
    # ===================== [SETUP FUNCTIONS BELOW] ======================

    def SetupGroundBoost(self, boost_index, location, shooter_game):
        # Set up the ground boost item
        self.boost_index = boost_index
        self.ground_duration = 60 * 15 # 15 seconds
        self.location = location
        self.shooter_game = shooter_game
        self.player = shooter_game.character

    def SetupGroundBoostImages(self):
        # Sets up the four boost images for the dropped boost items

        # ORANGE BOOST (DOUBLE-DAMAGE)
        if self.boost_index == 1:
            self.rect = self.shooter_game.orange_boost_image.get_rect()
            self.rect.center = self.location
        # RED BOOST (LIFE REGEN)
        elif self.boost_index == 2:
            self.rect = self.shooter_game.red_boost_image.get_rect()
            self.rect.center = self.location
        # BLUE BOOST (UNLIMITED AMMO)
        elif self.boost_index == 3:
            self.rect = self.shooter_game.blue_boost_image.get_rect()
            self.rect.center = self.location
        # PURPLE BOOST (INCREASED MOVEMENTSPEED)
        else:
            self.rect = self.shooter_game.purple_boost_image.get_rect()
            self.rect.center = self.location

    # ========================== GROUND BOOST ============================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================
    
    def update(self):
        # Updates every frame, called by the Waves class update

        if self.rect.colliderect(self.player.rect):
            # Detects if the player collides with this item. If the player does the item is destroyed and added to the player.
            self.player.PickedUpBoost(self.boost_index)
            self.player.waves.boost_item.remove(self)
            del self

        elif self.ground_duration > 0:
            # lowers the ground duration timer, when it reaches 0 the item is destroyed.
            self.ground_duration -= 1
        else: 
            # Player took too long to pick up the boost and it disapeared 
            self.player.waves.boost_item.remove(self)
            del self

class GroundArmor(pygame.sprite.Sprite):
    def __init__(self, location, shooter_game):
        super().__init__()
        # called when the item is first created
        self.SetupGroundArmor(location, shooter_game)

    # ========================== GROUND ARMOR ============================
    # ===================== [SETUP FUNCTIONS BELOW] ======================
        
    def SetupGroundArmor(self, location, shooter_game):
        # Sets up all aspects of the ground armor item
        self.armor_amount = 10
        self.ground_duration = 60 * 15 # 15 seconds
        self.location = location
        self.player = shooter_game.character
        self.rect = shooter_game.armor_image.get_rect()
        self.rect.center = self.location

    # ========================== GROUND ARMOR ============================
    # ==================== [UPDATE FUNCTIONS BELOW] ======================
    
    def update(self):
        # Updates every frame, called by the Waves class update

        if self.rect.colliderect(self.player.rect):
            # Detects if the player collides with this item. If the player does the item is destroyed and added to the player.
            self.player.ArmorPickup(self.armor_amount)
            self.player.waves.armor_item.remove(self)
            del self
        elif self.ground_duration > 0:
            # lowers the ground duration timer, when it reaches 0 the item is destroyed.
            self.ground_duration -= 1
        else: 
            # Player took too long to pick up the boost and it disapeared 
            self.player.waves.armor_item.remove(self)
            del self


