import arcade
import constants as cn
from constants import State
import game_views as gv
import player as p
import computer_controller as c
import os
import datetime as dt  # TIMER FOR MAX MATCH TIME

# --- Constants ---
SCREEN_TITLE = "Fight Stage"


class StageView(arcade.View):
    """
        Main app class for the fighting arena.
            Calls methods from the player class from dummy and player_1.
            Mouse IO is currently unused, however it will likely be used in the case of pause menu/ ui.
    """

    def __init__(self):
        # Call the parent class initializer
        super().__init__()
        self.window.set_mouse_visible(False)
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

        self.player_sprite=None

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        # Set up background image info
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = None

        # Set up game clock info
        self.total_time = 0.0
        self.timer_text = None

        # Set up start countdown info
        self.start_time = 0
        self.countdown_sprite = None
        
        # Game View Sprites
        self.player_health_bar_sprite = None
        self.dummy_health_bar_sprite = None
        self.timer_sprite = None

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.player_controller_num = None
        self.dummy_controller_num = None
        self.controller = None

        # Countdown after a player has won
        self.victory_countdown = None

    def setup(self, setup_inputs):
        """ Set up the game variables. Call to re-start the game. """
        # Startup Locations

        p1_center = [int(4 * cn.SCREEN_WIDTH / 5), int(2 * cn.SCREEN_HEIGHT / 5)]
        d_center = [int(cn.SCREEN_WIDTH / 5), int(2 * cn.SCREEN_HEIGHT / 5)]
        f_center = [int(cn.SCREEN_WIDTH / 2), int(cn.SCREEN_HEIGHT / 15)]  # STAGE FLOOR CENTER

        # -- PLAYER HURTBOXES --
        self.player_main_hurtbox = arcade.SpriteSolidColor(cn.SPRITE_PLAYER_WIDTH,  # Main Player Health/Body Hit Box
                                                           cn.SPRITE_PLAYER_HEIGHT,
                                                           [0, 255, 0])
        self.player_main_hurtbox.center_x = p1_center[0]
        self.player_main_hurtbox.center_y = p1_center[1]
        self.player_extended_hurtbox = arcade.SpriteSolidColor(int(cn.SPRITE_PLAYER_WIDTH / 3), # Extended Player Health/Body Hit Box
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

        # TODO: Sync this with the UI, so different setups can be selected
        # For controller_nums, 0 is full keymap, 1 is left split, 2 is right split, < 0 is mister roboto
        self.player_controller_num = setup_inputs[0]  # input_map = 2 for right split keymap
        self.dummy_controller_num = setup_inputs[1]  # input_map = 1 for left split keymap

        # -- PLAYER INITIALIZATION --
        self.player_1 = p.Player(p1_center[0], p1_center[1],
                                 cn.SPRITE_PLAYER_WIDTH, cn.SPRITE_PLAYER_HEIGHT,
                                 self.player_main_hurtbox, self.player_extended_hurtbox,
                                 self.player_hitbox, self.player_controller_num,1)  # input_map = 2 for right split keymap

        self.dummy = p.Player(d_center[0], d_center[1],
                              cn.SPRITE_PLAYER_WIDTH, cn.SPRITE_PLAYER_HEIGHT,
                              self.dummy_main_hurtbox, self.dummy_extended_hurtbox,
                              self.dummy_hitbox, self.dummy_controller_num,3)  # input_map = 1 for left split keymap

        if (self.player_controller_num == 0) & (self.dummy_controller_num < 0):
            self.controller = c.Controller(self.dummy, self.player_1)
            self.controller.setup()

        # -- STAGE GEOMETRY SETUP --
        self.floor = arcade.SpriteSolidColor(int(3 * cn.SCREEN_WIDTH),  # Main Player Health/Body Hit Box
                                             int(cn.SCREEN_HEIGHT / 3),
                                             arcade.color_from_hex_string(cn.FLOOR_COLOR))
        self.floor.center_x = f_center[0]
        self.floor.center_y = f_center[1]
        self.floors.append(self.floor)

        # -- STAGE UI SETUP --
        # DUMMY TRACKER UI

        # TODO Replace portrait with image of fighter
        if (self.dummy.character_input == 1):
            self.d_portrait = arcade.Sprite("images/Lisa/pfp.png",
                                            scale=0.35)
        elif (self.dummy.character_input == 2):
            self.d_portrait = arcade.Sprite("images/Jackie/pfp.png",
                                            scale=0.35)
        elif (self.dummy.character_input == 3):
            self.d_portrait = arcade.Sprite("images/Jason/pfp.png",
                                            scale=0.35)
        elif (self.dummy.character_input == 4):
            self.d_portrait = arcade.Sprite("images/Chris/pfp.png",
                                            scale=0.35)
        else:
            self.d_portrait = arcade.Sprite("image/Elon/pfp.png",
                                            scale=0.35)

        self.d_portrait.center_x = int(cn.PORTRAIT_DIMENSIONS[0] * 1.1)
        self.d_portrait.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) - 3
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
        self.d_block.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) - 23.5
        # 20px is for offset for block bar

        # PLAYER TRACKER UI

        # TODO Replace portrait with image of fighter
        if (self.player_1.character_input == 1):
            self.p_1_portrait = arcade.Sprite("images/Lisa/pfp.png",
                                            scale=0.35)
        elif (self.player_1.character_input == 2):
            self.p_1_portrait = arcade.Sprite("images/Jackie/pfp.png",
                                            scale=0.4)
        elif (self.player_1.character_input == 3):
            self.p_1_portrait = arcade.Sprite("images/Jason/pfp.png",
                                            scale=0.45)
        elif (self.player_1.character_input == 4):
            self.p_1_portrait = arcade.Sprite("images/Chris/pfp.png",
                                            scale=0.4)
        else:
            self.p_1_portrait = arcade.Sprite("images/Elon/pfp.png",
                                              scale=0.5)
            
        self.p_1_portrait.center_x = cn.SCREEN_WIDTH - int(cn.PORTRAIT_DIMENSIONS[0] * 1.1)
        self.p_1_portrait.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) - 3
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
        self.p_1_block.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9) - 23.5
        # 20px is for offset for block bar

        # TIMER
        self.timer = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1]*1.5),
                                             int(cn.PORTRAIT_DIMENSIONS[1]*1.5),
                                             [255, 255, 100])
        self.timer.center_x = cn.SCREEN_WIDTH / 2
        self.timer.center_y = cn.SCREEN_HEIGHT - int(cn.PORTRAIT_DIMENSIONS[1] * 0.9)

        # Health bar UI sprites
        self.player_health_bar_sprite = arcade.Sprite("sprites/health_6.png",
                                               center_x=self.p_1_health.center_x + 61,
                                               center_y=self.p_1_health.center_y - 24,
                                               flipped_horizontally=True)
        
        self.dummy_health_bar_sprite = arcade.Sprite("sprites/health_6.png",
                                               center_x=self.d_health.center_x - 61,
                                               center_y=self.d_health.center_y - 24)
        
                
        # Set the background to the desired image (default as Waterman green)
        self.background = arcade.load_texture("images/backgrounds/votey.jpg")
        
        # Timer UI sprite
        self.timer_sprite = arcade.Sprite("sprites/timer.png",
                                          center_x= self.timer.center_x,
                                          center_y= self.timer.center_y)
        
        # Set up game clock info
        self.timer_text = arcade.Text(
            text = "60",
            start_x = cn.SCREEN_WIDTH/2,
            start_y = cn.SCREEN_HEIGHT - 85,
            color=arcade.color.BLACK,
            font_size= 25,
            anchor_x="center",
            font_name=cn.TIMER_FONT
        )

        # Set up the start countdown
        self.start_time = cn.COUNTDOWN_TIME

        self.countdown_sprite = arcade.Sprite("sprites/get_ready_sprite.png",
                                              center_x=cn.SCREEN_WIDTH/2,
                                              center_y=cn.SCREEN_HEIGHT/2 - 100)

        # UI APPEND TO LIST
        self.ui.append(self.player_health_bar_sprite)
        self.ui.append(self.dummy_health_bar_sprite)
        self.ui.append(self.timer_sprite)
        self.ui.append(self.d_portrait)
        self.ui.append(self.p_1_portrait)
        self.ui.append(self.d_health)
        self.ui.append(self.p_1_health)
        self.ui.append(self.d_block)
        self.ui.append(self.p_1_block)


       
        """
        self.ui.append(self.d_super)
        self.ui.append(self.p_1_super)
        """

        # Set up the game clock
        self.total_time = cn.MAX_MATCH_TIME

        # Set up victory countdown 
        self.victory_countdown = cn.VICTORY_COUNTDOWN

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Draw the background
        arcade.draw_lrwh_rectangle_textured(0, 140,
                                            cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT,
                                            self.background)

        # Call draw() on all your sprite lists below
       # self.player_1.player_hurtboxes.draw()
        self.player_1.player_sprites.draw()
        #self.player_1.player_hitboxes.draw()

      #  self.dummy.player_hurtboxes.draw()
       # self.dummy.player_hitboxes.draw()
        self.dummy.player_sprites.draw()

        self.floors.draw()
        self.ui.draw()
        self.timer_text.draw()
        self.countdown_sprite.draw()

    def on_update(self, delta_time):
        """
        Calls update (and grav_cycle) functions for both players,
            updates UI, and calls whos_on_first.
        Also calls hit and hurt cycle (attack animations for both players,
            and deals with the hit collision logic.
        """
        self.player_1.update(floors=self.floors)
        self.dummy.update(floors=self.floors)
        self.floors.update()
        self.ui.update()

        if not (self.controller is None):
            self.controller.update()

        self.player_1.grav_cycle(floors=self.floors)
        self.dummy.grav_cycle(floors=self.floors)
        self.whos_on_first()
        self.ui_update(delta_time)

        # Now the hard part: retooling hit detection for the new inputs
        #   - We don't need to check for moves from the dummy (it doesn't even have inputs)
        #     or the stun on player_1 (it literally can't be hit)

        # Check to see if the player has attacked the dummy,
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
        ⣿⣿⣿⣿⣿⣿⡿⠀⠀⢸⣿⣿⠀⠀⠣⠀⠀⠀⠀⠀⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿
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
                if not self.dummy.being_hit:
                    self.dummy.being_hit = True
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
                    if self.dummy.health < 0:
                        # self.dummy.health = cn.PLAYER_HEALTH
                        # self.dummy.block_health = cn.FULL_BLOCK
                        # TODO: END GAME
                        pass
            else:  # IF NOT HIT AND ~NOT STUNNED~
                self.dummy.being_hit = False
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
                if not self.player_1.being_hit:
                    self.player_1.being_hit = True
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
                    if self.player_1.health < 0:
                        # self.player_1.health = cn.PLAYER_HEALTH
                        # self.player_1.block_health = cn.FULL_BLOCK
                        # TODO: END GAME
                        pass
            else:  # IF NOT HIT AND ~NOT STUNNED~
                self.player_1.being_hit = False
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

        if self.dummy.center_x < 0:
            self.dummy.center_x = 0
        elif self.dummy.center_x > cn.SCREEN_WIDTH:
            self.dummy.center_x = cn.SCREEN_WIDTH

        if self.player_1.center_x < 0:
            self.player_1.center_x = 0
        elif self.player_1.center_x > cn.SCREEN_WIDTH:
            self.player_1.center_x = cn.SCREEN_WIDTH

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.P:   # pause game
            # pass self, the current view, to preserve this view's state
            pause = gv.PauseView(self, self.player_controller_num, self.dummy_controller_num)
            self.window.show_view(pause)

        self.player_1.player_key_press(key, key_modifiers)
        self.dummy.player_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.player_1.player_key_release(key, key_modifiers)
        self.dummy.player_key_release(key, key_modifiers)

    def whos_on_first(self):
        """
        Checks who's on which side of the arena, and keeps track of that
        """
        if (not (self.player_1.jump_or_nah(floors=self.floors))) & self.player_1.jumping:
            if self.player_1.center_x >= self.dummy.center_x:
                self.player_1.change_x_J -= 10
            else:
                self.player_1.change_x_J += 10
        elif (not (self.dummy.jump_or_nah(floors=self.floors))) & self.dummy.jumping:
            if self.dummy.center_x >= self.dummy.center_x:
                self.dummy.change_x_J -= 10
            else:
                self.dummy.change_x_J += 10
        else:
            if self.player_1.center_x >= self.dummy.center_x:
                self.player_1.right = True
                self.dummy.right = False
            elif self.player_1.center_x < self.dummy.center_x:
                self.player_1.right = False
                self.dummy.right = True
            self.player_1.change_x_J = 0

    def ui_update(self, delta_time):
        """
        Updates the UI
        """

        """
        Update the countdown sequence
        """
        self.player_1.player_sprites.visible=False
        self.dummy.player_sprites.visible=False

        if self.start_time <= cn.COUNTDOWN_TIME and self.start_time > (cn.COUNTDOWN_TIME*0.75):
            self.countdown_sprite = arcade.Sprite("sprites/get_ready_sprite.png",
                                            center_x=cn.SCREEN_WIDTH/2,
                                            center_y=cn.SCREEN_HEIGHT/2)

        elif self.start_time <= (cn.COUNTDOWN_TIME*0.75) and self.start_time > (cn.COUNTDOWN_TIME*0.5):
            self.countdown_sprite = arcade.Sprite("sprites/three.png",
                                                  center_x=cn.SCREEN_WIDTH/2,
                                                  center_y=cn.SCREEN_HEIGHT/2)
        elif self.start_time <= (cn.COUNTDOWN_TIME*0.5) and self.start_time > (cn.COUNTDOWN_TIME*0.25):
            self.countdown_sprite = arcade.Sprite("sprites/two.png",
                                                  center_x=cn.SCREEN_WIDTH/2 - 1,
                                                  center_y=cn.SCREEN_HEIGHT/2 - 12)
                    # Decrement the countdown time
        elif self.start_time <= (cn.COUNTDOWN_TIME*0.25) and self.start_time > 0:
            self.countdown_sprite = arcade.Sprite("sprites/one.png",
                                                  center_x=cn.SCREEN_WIDTH/2 + 4,
                                                  center_y=cn.SCREEN_HEIGHT/2 + 2) 
                    # Decrement the countdown time
        else:
            self.countdown_sprite.visible = False
            self.player_1.player_sprites.visible=True
            self.dummy.player_sprites.visible=True
            self.start_time = 0.0

            """
            Update the game clock
            """

            minutes = int(self.total_time) / 60
            seconds = int(self.total_time) % 60

            if minutes == 0.0 and seconds == 0.0:
                # Change the view to "Game Over" view
                self.window.show_view(gv.GameOverView("timeout",self.player_controller_num, self.dummy_controller_num))

                # Make sure time does not decrease
                self.total_time = 0.0
            else:
                # Accumulate the total time
                self.total_time -= delta_time

            # Create the text for the timer
            self.timer_text.text = f"{seconds:02d}"

        self.start_time -= delta_time

        # --- DUMMY UI REFRESH ---
        if self.dummy.health < 1:
            self.d_health.alpha = 0

            print("Victory countdown " + str(self.victory_countdown))

            countdown_check = round(self.victory_countdown, 2)

            if (countdown_check <= 0.0):
                game_end = gv.GameOverView(str(self.player_1.character_input), self.player_controller_num, self.dummy_controller_num)

                # Change the view to "Game Over" view
                self.window.show_view(game_end)  
            else:
                self.victory_countdown -= delta_time         
        else:
            self.d_health.alpha = 255
            self.d_health.width = int(self.dummy.health * cn.HEALTH_BAR_PIXEL_CONSTANT)
            self.d_health.center_x = int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                        ((self.dummy.health * cn.HEALTH_BAR_PIXEL_CONSTANT)/2))

        if self.dummy.block_health < 1:
            self.d_block.alpha = 0
        else:
            self.d_block.alpha = 255
            self.d_block.width = int(self.dummy.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT)
            self.d_block.center_x = int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                        ((self.dummy.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT) / 2))

        # --- PLAYER UI REFRESH ---
        if self.player_1.health < 1:
            self.p_1_health.alpha = 0

            print("Victory countdown " + str(self.victory_countdown))

            countdown_check = round(self.victory_countdown, 2)

            if (countdown_check <= 0.0):
                game_end = gv.GameOverView(str(self.dummy.character_input), self.player_controller_num, self.dummy_controller_num)

                # Change the view to "Game Over" view
                self.window.show_view(game_end)
            else:
                self.victory_countdown -= delta_time
        else:
            self.p_1_health.alpha = 255
            self.p_1_health.width = int(self.player_1.health * cn.HEALTH_BAR_PIXEL_CONSTANT)
            self.p_1_health.center_x = cn.SCREEN_WIDTH - int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                                            ((self.player_1.health * cn.HEALTH_BAR_PIXEL_CONSTANT) / 2))

        if self.player_1.block_health < 1:
            self.p_1_block.alpha = 0
        else:
            self.p_1_block.alpha = 255
            self.p_1_block.width = int(self.player_1.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT)
            self.p_1_block.center_x = cn.SCREEN_WIDTH - int(int(cn.PORTRAIT_DIMENSIONS[0] * 1.8) +
                                                        ((self.player_1.block_health * cn.BLOCK_BAR_PIXEL_CONSTANT) / 2))
