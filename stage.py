import arcade
import constants as cn
from constants import State
import player as p
import os
import datetime as dt  # TIMER FOR MAX MATCH TIME

# TODO / Important Stuff:
#       UI SPRITES AREN'T CONNECTED TO THE VALUES THEY REPRESENT YET
#       Slow-down from collision detection makes tics vary in speed, which can vary the speed of attacks based on
#           how much is happening in the code

# --- Constants ---
SCREEN_TITLE = "Fight Stage"


class Stage(arcade.Window):
    """
        Main app class for the fighting arena.
            Calls methods from the player class from dummy and player_1.
            Mouse IO is currently unused, however it will likely be used in the case of pause menu/ ui.
    """

    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT, SCREEN_TITLE)
        # Player and Computer(?)
        self.player_1 = None
        self.dummy = None

        self.floors = arcade.SpriteList()
        self.floor = None

        self.ui = arcade.SpriteList()
        self.d_portrait = None
        self.p_1_portrait = None
        self.d_health = None
        self.p_1_health = None
        self.d_block = None
        self.p_1_block = None
        self.d_super = None
        self.p_1_super = None
        self.timer = None

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set up the player info
        self.player_main_hurtbox = None
        self.player_extended_hurtbox = None
        self.player_hitbox = None

        # Set up the dummy info
        self.dummy_main_hurtbox = None
        self.dummy_extended_hurtbox = None
        self.dummy_hitbox = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BATTLESHIP_GREY)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Startup Locations
        p1_center = [int(4 * cn.SCREEN_WIDTH / 5), int(2 * cn.SCREEN_HEIGHT / 5)]
        d_center = [int(cn.SCREEN_WIDTH / 5), int(2 * cn.SCREEN_HEIGHT / 5)]
        f_center = [int(cn.SCREEN_WIDTH / 2), int(cn.SCREEN_HEIGHT / 10)]  # STAGE FLOOR CENTER

        # -- PLAYER HURTBOXES --
        self.player_main_hurtbox = arcade.SpriteSolidColor(cn.SPRITE_PLAYER_WIDTH,  # Main Player Health/Body Hit Box
                                                           cn.SPRITE_PLAYER_HEIGHT,
                                                           [0, 255, 0])
        self.player_main_hurtbox.center_x = p1_center[0]
        self.player_main_hurtbox.center_y = p1_center[1]
        self.player_extended_hurtbox = arcade.SpriteSolidColor(int(cn.SPRITE_PLAYER_WIDTH / 3),
                                                               # Extended Player Health/Body Hit Box
                                                               10,
                                                               [255, 255, 255])
        self.player_extended_hurtbox.center_x = p1_center[0]
        self.player_extended_hurtbox.center_y = p1_center[1]

        # -- PLAYER HITBOXES --
        self.player_hitbox = arcade.SpriteSolidColor(1,  # Player Hit/Damage Hit Box
                                                     1,
                                                     [255, 0, 0])
        self.player_hitbox.center_x = 0
        self.player_hitbox.center_y = 0

        # ===

        # -- DUMMY HURTBOXES --
        self.dummy_main_hurtbox = arcade.SpriteSolidColor(cn.SPRITE_PLAYER_WIDTH,  # Test Dummy Health/Body Hit Box
                                                          cn.SPRITE_PLAYER_HEIGHT,
                                                          [0, 0, 250])
        self.dummy_main_hurtbox.center_x = d_center[0]
        self.dummy_main_hurtbox.center_y = d_center[1]
        self.dummy_extended_hurtbox = arcade.SpriteSolidColor(1,  # Extended Player Health/Body Hit Box
                                                              1,
                                                              [0, 0, 250])
        self.dummy_extended_hurtbox.center_x = d_center[0]
        self.dummy_extended_hurtbox.center_y = d_center[1]

        # -- DUMMY HITBOXES --
        self.dummy_hitbox = arcade.SpriteSolidColor(1,  # Player Hit/Damage Hit Box
                                                    1,
                                                    [255, 0, 0])
        self.dummy_hitbox.center_x = 0
        self.dummy_hitbox.center_y = 0

        # -- PLAYER INITIALIZATION --
        self.player_1 = p.Player(p1_center[0], p1_center[1],
                                 cn.SPRITE_PLAYER_WIDTH, cn.SPRITE_PLAYER_HEIGHT,
                                 self.player_main_hurtbox, self.player_extended_hurtbox,
                                 self.player_hitbox, 2)  # input_map = 2 for right split keymap
        self.dummy = p.Player(d_center[0], d_center[1],
                              cn.SPRITE_PLAYER_WIDTH, cn.SPRITE_PLAYER_HEIGHT,
                              self.dummy_main_hurtbox, self.dummy_extended_hurtbox,
                              self.dummy_hitbox, 1)  # input_map = 1 for left split keymap

        # -- STAGE GEOMETRY SETUP --
        self.floor = arcade.SpriteSolidColor(int(3 * cn.SCREEN_WIDTH),  # Main Player Health/Body Hit Box
                                             int(cn.SCREEN_HEIGHT / 3),
                                             [0, 0, 0])
        self.floor.center_x = f_center[0]
        self.floor.center_y = f_center[1]
        self.floors.append(self.floor)

        # -- STAGE UI SETUP --
        # TODO: SETUP ALL THE UI ASPECTS AS SPRITES
        # DUMMY TRACKER UI
        self.d_portrait = arcade.SpriteSolidColor(cn.PORTRAIT_DIMENSIONS[0],
                                                  cn.PORTRAIT_DIMENSIONS[1],
                                                  [0, 0, 250])
        self.d_portrait.center_x = int(cn.PORTRAIT_DIMENSIONS[0] * 1.1)
        self.d_portrait.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9)
        self.d_health = arcade.SpriteSolidColor(int(self.dummy.health * cn.HEALTH_BAR_PIXEL_CONSTANT),
                                                30,  # HEIGHT OF HEALTH BAR
                                                [255, 0, 0])
        self.d_health.center_x = int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                     ((self.dummy.health * cn.HEALTH_BAR_PIXEL_CONSTANT)/2))
        # * 1.6 is to correct the offset from the portrait
        self.d_health.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) + 20
        # 20px is for offset for block bar
        self.d_block = arcade.SpriteSolidColor(int(self.dummy.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT),
                                                 30,  # HEIGHT OF HEALTH BAR
                                                 [125, 249, 255])
        self.d_block.center_x = int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                    ((self.dummy.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT) / 2))
        # * 1.6 is to correct the offset from the portrait
        self.d_block.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) - 20
        # 20px is for offset for block bar

        # PLAYER TRACKER UI
        self.p_1_portrait = arcade.SpriteSolidColor(cn.PORTRAIT_DIMENSIONS[0],
                                                    cn.PORTRAIT_DIMENSIONS[1],
                                                    [0, 255, 0])
        self.p_1_portrait.center_x = cn.SCREEN_WIDTH - int(cn.PORTRAIT_DIMENSIONS[0] * 1.1)
        self.p_1_portrait.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9)
        self.p_1_health = arcade.SpriteSolidColor(int(self.player_1.health * cn.HEALTH_BAR_PIXEL_CONSTANT),
                                                  30,  # HEIGHT OF HEALTH BAR
                                                  [255, 0, 0])
        self.p_1_health.center_x = cn.SCREEN_WIDTH - int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                                         ((self.player_1.health * cn.HEALTH_BAR_PIXEL_CONSTANT) / 2))
        # * 1.6 is to correct the offset from the portrait
        self.p_1_health.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) + 20
        # 20px is for offset for block bar
        self.p_1_block = arcade.SpriteSolidColor(int(self.player_1.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT),
                                                 30,  # HEIGHT OF HEALTH BAR
                                                 [125, 249, 255])
        self.p_1_block.center_x = cn.SCREEN_WIDTH - int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                                        ((self.player_1.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT) / 2))
        # * 1.6 is to correct the offset from the portrait
        self.p_1_block.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) - 20
        # 20px is for offset for block bar

        # TIMER
        self.timer = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1]*1.5),
                                             int(cn.PORTRAIT_DIMENSIONS[1]*1.5),
                                             [255, 255, 100])
        self.timer.center_x = cn.SCREEN_WIDTH / 2
        self.timer.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9)
        # 20px is for offset for block bar

        # UI APPEND TO LIST
        self.ui.append(self.d_portrait)
        self.ui.append(self.p_1_portrait)
        self.ui.append(self.d_health)
        self.ui.append(self.p_1_health)
        self.ui.append(self.d_block)
        self.ui.append(self.p_1_block)
        self.ui.append(self.timer)

        """
        self.ui.append(self.d_super)
        self.ui.append(self.p_1_super)
        """

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.player_1.player_hurtboxes.draw()
        self.player_1.player_hitboxes.draw()
        self.dummy.player_hurtboxes.draw()
        self.dummy.player_hitboxes.draw()
        self.floors.draw()
        self.ui.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_1.update(floors=self.floors)
        self.dummy.update(floors=self.floors)
        self.floors.update()
        self.ui.update()

        self.player_1.grav_cycle(floors=self.floors)
        self.dummy.grav_cycle(floors=self.floors)
        self.whos_on_first()
        self.ui_update()

        # Now the hard part: retooling hit detection for the new inputs
        #   - We don't need to check for moves from the dummy (it doesn't even have inputs)
        #     or the stun on player_1 (it literally can't be hit)

        # Check to see if the player has attacked the dummy,

        # TODO: Block works, but hit detection's kinda borked. Dbl hits are back.
        #       Hit stun being improperly implemented is almost certainly the issue.
        """
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠜⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿
        ⣿⣿⡏⠁⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⡄⠀⠀⠀⠀⢀⣴⣿⣿⣿
        ⣿⣿⣷⣄⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡧⠇⢀⣤⣶⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣾⣮⣭⣿⡻⣽⣒⠀⣤⣜⣭⠐⢐⣒⠢⢰⢸⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⡟⣾⣿⠂⢈⢿⣷⣞⣸⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣷⣶⣾⡿⠿⣿⠗⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⠋⠉⠑⠀⠀⢘⢻⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⡿⠟⢹⣿⣿⡇⢀⣶⣶⠴⠶⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⡿⠀⠀⢸⣿⣿⠀⠀⠣⠀⠀⠀⠀⠀⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿da
        ⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠹⣿⣧⣀⠀⠀⠀⠀⡀⣴⠁⢘⡙⢿⣿⣿⣿⣿⣿⣿
        ⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⠗⠂⠄⠀⣴⡟⠀⠀⡃⠀⠉⠉⠟⡿⣿⣿⣿
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠾⠛⠂⢹⠀⠀⠀⢡⠀⠀⠀⠀⠀⠙⠛⠿⢿⣿
        """
        hit_on_dummy = 0
        if self.dummy.stun == 0:  # 1st see if Dummy isn't already stunned
            hit_on_dummy = 0
            for hitbox in self.player_1.player_hitboxes:
                if arcade.check_for_collision_with_list(hitbox, self.dummy.player_hurtboxes):
                    hit_on_dummy += 1
            # I will admit the below if statement is a bit wack, as it functions off the fact that
            #   for ints to booleans, 0 will show as False and any other number will show as True,
            #   but, y'know, it works, and I just explained it, so we're good I guess
            if hit_on_dummy:  # IF HIT AND ~NOT STUNNED~
                print("HIT ON D1 " + str(dt.datetime.now()))
                for hitbox in self.player_1.player_hitboxes:
                    hitbox.hit_box_algorithm = 'None'
                    hitbox.center_x = 0  # Move Hit/Damage box away to avoid...
                    hitbox.center_y = 0  # accidentally registering attacks 2x.
                    hitbox.width = 0.1  # Set the width and height to 0 to avoid...
                    hitbox.height = 0.1  # accidentally registering attacks 2x.
                arcade.set_background_color(arcade.color.YELLOW)
                # --- HEAVY ---
                if self.player_1.state == State.h_kick:
                    hit_stun = self.dummy.block_check(cn.H_K_HIT_DAMAGE)
                    if hit_stun:
                        self.dummy.stun = cn.H_STUN_TIME  # Max stun time for heavy moves
                elif self.player_1.state == State.h_punch:
                    hit_stun = self.dummy.block_check(cn.H_P_HIT_DAMAGE)
                    if hit_stun:
                        self.dummy.stun = cn.H_STUN_TIME  # Max stun time for heavy moves
                # --- SPECIALS ---
                elif (self.player_1.state == State.aa_punch) | (self.player_1.state == State.lp_punch):
                    hit_stun = self.dummy.block_check(cn.S_P_HIT_DAMAGE)
                    if hit_stun:
                        self.dummy.stun = cn.S_STUN_TIME  # Max stun time for special moves
                elif (self.player_1.state == State.aa_kick) | (self.player_1.state == State.lp_kick):
                    hit_stun = self.dummy.block_check(cn.S_K_HIT_DAMAGE)
                    if hit_stun:
                        self.dummy.stun = cn.S_STUN_TIME  # Max stun time for special moves
                # --- LIGHT ---
                elif self.player_1.state == State.l_kick:
                    hit_stun = self.dummy.block_check(cn.L_K_HIT_DAMAGE)
                    if hit_stun:
                        self.dummy.stun = cn.L_STUN_TIME  # Max stun time for light moves
                elif self.player_1.state == State.l_punch:
                    hit_stun = self.dummy.block_check(cn.L_P_HIT_DAMAGE)
                    if hit_stun:
                        self.dummy.stun = cn.L_STUN_TIME  # Max stun time for light moves
                print("DUMMY HEALTH = " + str(self.dummy.health))
                if self.dummy.health <= 0:
                    self.dummy.health = cn.PLAYER_HEALTH
            else:  # IF NOT HIT AND ~NOT STUNNED~
                for hitbox in self.player_1.player_hitboxes:
                    hitbox.hit_box_algorithm = 'Simple'
                arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
        else:  # IF STUNNED
            for hitbox in self.player_1.player_hitboxes:
                hitbox.hit_box_algorithm = 'None'
            if self.dummy.stun > 0:
                self.dummy.stun -= 1
                arcade.set_background_color(arcade.color.YELLOW)
            else:
                self.dummy.stun = 0
                arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
                for hurtbox in self.dummy.player_hurtboxes:
                    hurtbox.COLOR = [0, 0, 250]
        # Check to see if the dummy has attacked the player,
        if self.player_1.stun == 0:  # 1st see if player isn't already stunned
            hit_on_player = 0
            for hitbox in self.dummy.player_hitboxes:
                if arcade.check_for_collision_with_list(hitbox, self.player_1.player_hurtboxes):
                    hit_on_player += 1
            # I will admit the below if statement is a bit wack, as it functions off the fact that
            #   for ints to booleans, 0 will show as False and any other number will show as True,
            #   but, y'know, it works, and I just explained it, so we're good I guess
            if hit_on_player:  # IF HIT AND ~NOT STUNNED~
                print("HIT ON P1 " + str(dt.datetime.now()))
                for hitbox in self.dummy.player_hitboxes:
                    hitbox.hit_box_algorithm = 'None'
                    hitbox.center_x = 0  # Move Hit/Damage box away to avoid...
                    hitbox.center_y = 0  # accidentally registering attacks 2x.
                    hitbox.width = 0.1  # Set the width and height to 0 to avoid...
                    hitbox.height = 0.1  # accidentally registering attacks 2x.
                arcade.set_background_color(arcade.color.ORANGE)
                # --- HEAVY ---
                if self.dummy.state == State.h_kick:
                    hit_stun = self.player_1.block_check(cn.H_K_HIT_DAMAGE)
                    if hit_stun:
                        self.player_1.stun = cn.H_STUN_TIME  # Max stun time for heavy moves
                elif self.dummy.state == State.h_punch:
                    hit_stun = self.player_1.block_check(cn.H_P_HIT_DAMAGE)
                    if hit_stun:
                        self.player_1.stun = cn.H_STUN_TIME  # Max stun time for heavy moves
                # --- SPECIALS ---
                elif (self.dummy.state == State.aa_punch) | (self.dummy.state == State.lp_punch):
                    hit_stun = self.player_1.block_check(cn.S_P_HIT_DAMAGE)
                    if hit_stun:
                        self.player_1.stun = cn.S_STUN_TIME  # Max stun time for special moves
                elif (self.dummy.state == State.aa_kick) | (self.dummy.state == State.lp_kick):
                    hit_stun = self.player_1.block_check(cn.S_K_HIT_DAMAGE)
                    if hit_stun:
                        self.player_1.stun = cn.S_STUN_TIME  # Max stun time for special moves
                # --- LIGHT ---
                elif self.dummy.state == State.l_kick:
                    hit_stun = self.player_1.block_check(cn.L_K_HIT_DAMAGE)
                    if hit_stun:
                        self.player_1.stun = cn.L_STUN_TIME  # Max stun time for light moves
                elif self.dummy.state == State.l_punch:
                    hit_stun = self.player_1.block_check(cn.L_P_HIT_DAMAGE)
                    if hit_stun:
                        self.player_1.stun = cn.L_STUN_TIME  # Max stun time for light moves
                print("PLAYER HEALTH = " + str(self.player_1.health))
                if self.player_1.health <= 0:
                    self.player_1.health = cn.PLAYER_HEALTH
            else:  # IF NOT HIT AND ~NOT STUNNED~
                for hitbox in self.dummy.player_hitboxes:
                    hitbox.hit_box_algorithm = 'Simple'
                if (not hit_on_dummy) and (self.dummy.stun <= 0):
                    arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
        else:  # IF STUNNED
            for hitbox in self.dummy.player_hitboxes:
                hitbox.hit_box_algorithm = 'None'
            if self.player_1.stun > 0:
                self.player_1.stun -= 1
                arcade.set_background_color(arcade.color.ORANGE)
            else:
                self.player_1.stun = 0
                if (not hit_on_dummy) and (self.dummy.stun <= 0):
                    arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
                for hurtbox in self.player_1.player_hurtboxes:
                    hurtbox.COLOR = [0, 255, 0]

        self.player_1.hit_cycle()
        self.player_1.hurt_cycle()

        self.dummy.hit_cycle()
        self.dummy.hurt_cycle()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        ### Right now I've tuned it for the directional inputs I came up with in
            potential_control_schema.txt.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.player_1.player_key_press(key, key_modifiers)
        self.dummy.player_key_press(key, key_modifiers)
        """
        if self.player_1.state_counter == 0:
            # USE EITHER STATE.HIT OR STUN-LOCK TO KEEP TRACK OF WHEN THEY CAN'T START NEW MOVES
            if not self.player_1.state == State.hit:
                if not (self.player_1.keymap is None):
                    if self.player_1.SPRINT == key:
                        if self.player_1.right & self.player_1.lefting:
                            print("LEFTING SPRINTING")
                            self.player_1.sprinting = True
                            # SPRINT LEFT BEHAVIOR GOES HERE
                        elif (not self.player_1.right) & self.player_1.righting:
                            print("RIGHTING SPRINTING")
                            self.player_1.sprinting = True
                            # SPRINT RIGHT BEHAVIOR GOES HERE
                        else:
                            print("DIR INPUT NEEDED BEFORE SPRINT PRESSED")
                            self.player_1.sprinting = False
                    else:
                        match key:
                            case self.player_1.JUMP:
                                print("JUMPING")
                                self.player_1.state = State.idle
                                if self.player_1.lefting:
                                    self.player_1.left_jump = True
                                elif self.player_1.righting:
                                    self.player_1.right_jump = True
                                else:
                                    self.player_1.neutral_jump = True
                                self.player_1.jumping = True
                            case self.player_1.DAFOE:
                                print("DAFOEING")
                                self.player_1.dafoeing = True
                                # LOOK UP BEHAVIOR GOES HERE
                            case self.player_1.CROUCH:
                                print("CROUCHING")
                                self.player_1.crouching = True
                                # CROUCH BEHAVIOR GOES HERE
                            case self.player_1.LEFT:
                                print("LEFTING")
                                self.player_1.lefting = True
                                self.player_1.righting = False
                                # MOVE LEFT BEHAVIOR GOES HERE
                                if not self.player_1.right:
                                    self.player_1.state = State.blocking
                                    print("BLOCKING")
                                    self.player_1.change_x_L -= int(3 * cn.PLAYER_SPEED / 5)
                                else:
                                    self.player_1.change_x_L -= cn.PLAYER_SPEED
                            case self.player_1.RIGHT:
                                print("RIGHTING")
                                self.player_1.righting = True
                                self.player_1.lefting = False
                                # MOVE RIGHT BEHAVIOR GOES HERE
                                if self.player_1.right:
                                    self.player_1.state = State.blocking
                                    print("BLOCKING")
                                    self.player_1.change_x_R += int(3 * cn.PLAYER_SPEED / 5)
                                else:
                                    self.player_1.change_x_R += cn.PLAYER_SPEED
                            case self.player_1.PUNCH:
                                print("PUNCH")
                                self.player_1.punching = True
                                if ((self.player_1.righting & (not self.player_1.right)) |
                                        (self.player_1.lefting & self.player_1.right)):
                                    print("light punch")
                                    self.player_1.state = State.l_punch  # LIGHT PUNCH
                                    self.player_1.state_counter = cn.L_HIT_LENGTH
                                elif self.player_1.dafoeing:
                                    print("anti-air punch")
                                    self.player_1.state = State.aa_punch  # ANTI-AIR PUNCH
                                    self.player_1.state_counter = cn.S_HIT_LENGTH
                                elif self.player_1.crouching:
                                    print("low-profile punch")
                                    self.player_1.state = State.lp_punch  # LOW-PROFILE PUNCH
                                    self.player_1.state_counter = cn.L_HIT_LENGTH
                                else:
                                    print("heavy punch")
                                    self.player_1.state = State.h_punch  # HEAVY PUNCH
                                    self.player_1.state_counter = cn.H_HIT_LENGTH
                            case self.player_1.KICK:
                                print("KICKING")
                                self.player_1.kicking = True
                                if ((self.player_1.righting & (not self.player_1.right)) |
                                        (self.player_1.lefting & self.player_1.right)):
                                    print("light kick")
                                    self.player_1.state = State.l_kick  # LIGHT KICK
                                    self.player_1.state_counter = cn.L_HIT_LENGTH
                                elif self.player_1.dafoeing:
                                    print("anti-air kick")
                                    self.player_1.state = State.aa_kick  # ANTI-AIR KICK
                                    self.player_1.state_counter = cn.S_HIT_LENGTH
                                elif self.player_1.crouching:
                                    print("low-profile kick")
                                    self.player_1.state = State.lp_kick  # LOW-PROFILE KICK
                                    self.player_1.state_counter = cn.S_HIT_LENGTH
                                else:
                                    print("heavy kick")
                                    self.player_1.state = State.h_kick  # HEAVY KICK
                                    self.player_1.state_counter = cn.H_HIT_LENGTH
            """

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.player_1.player_key_release(key, key_modifiers)
        self.dummy.player_key_release(key, key_modifiers)
        """
        match key:
            case self.player_1.SPRINT:
                print("NO SPRINTING")
                self.player_1.sprinting = False
            case self.player_1.JUMP:
                print("NO JUMPING")
            case self.player_1.DAFOE:
                print("NO DAFOEING")
                self.player_1.dafoeing = False
            case self.player_1.CROUCH:
                print("NO CROUCHING")
                self.player_1.crouching = False
            case self.player_1.LEFT:
                print("NO LEFTING")
                self.player_1.lefting = False
                self.player_1.change_x_L = 0
                if self.player_1.state == State.blocking:
                    self.player_1.state = State.idle
                    print("NO BLOCKING")
            case self.player_1.RIGHT:
                print("NO RIGHTING")
                self.player_1.righting = False
                self.player_1.change_x_R = 0
                if self.player_1.state == State.blocking:
                    self.player_1.state = State.idle
                    print("NO BLOCKING")
            case self.player_1.PUNCH:
                print("NO PUNCHING")
                self.player_1.punching = False
            case self.player_1.KICK:
                print("NO KICKING")
                self.player_1.kicking = False
        """

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        """
        self.player_1.center_x = x
        self.player_1.center_y = y
        if int(self.player_1.state) > 2:
            for hitbox in self.player_1.player_hitboxes:
                hitbox.center_x = x
                hitbox.center_y = y
        """

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def whos_on_first(self):
        if (not (self.player_1.jump_or_nah(floors=self.floors))) & self.player_1.jumping:
            if self.player_1.center_x >= self.dummy.center_x:
                self.player_1.change_x_J -= 10

            else:
                self.player_1.change_x_J += 10
        else:
            if self.player_1.center_x >= self.dummy.center_x:
                self.player_1.right = True
                self.dummy.right = False
            elif self.player_1.center_x < self.dummy.center_x:
                self.player_1.right = False
                self.dummy.right = True
            self.player_1.change_x_J = 0
        if self.dummy.jump_or_nah(floors=self.floors):
            pass

    def ui_update(self):
        # --- DUMMY UI REFRESH ---
        self.d_health.width = int(self.dummy.health * cn.HEALTH_BAR_PIXEL_CONSTANT)
        self.d_health.center_x = int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                     ((self.dummy.health * cn.HEALTH_BAR_PIXEL_CONSTANT)/2))
        self.d_block.width = int(self.dummy.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT)
        self.d_block.center_x = int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                    ((self.dummy.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT) / 2))
        # --- PLAYER UI REFRESH ---
        self.p_1_health.width = int(self.player_1.health * cn.HEALTH_BAR_PIXEL_CONSTANT)
        self.p_1_health.center_x = cn.SCREEN_WIDTH - int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                                         ((self.player_1.health * cn.HEALTH_BAR_PIXEL_CONSTANT) / 2))
        self.p_1_block.width = int(self.player_1.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT)
        self.p_1_block.center_x = cn.SCREEN_WIDTH - int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                                        ((self.player_1.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT) / 2))


def main():
    """ Main function """
    game = Stage(cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
