import arcade
import constants as cn
from constants import State
import player as p
import os
import datetime as dt  # If we operate off of datetime, we can ~kinda~ account for frame-dropping on intensive actions??

# This may also be a terrible idea, I honestly have no clue lol
# TODO: Def bring this up to the group to talk about

# TODO / Important Stuff:
#       Divide up into separate classes (hitbox, hurtbox, master, etc)
#       Hit-stun doesn't work (Dbl hits)
#       Slow-down from collision detection makes tics vary in speed, which can vary the speed of attacks based on
#           how much is happening in the code

# --- Constants ---
SCREEN_TITLE = "Hitbox Testing"

HIT_LENGTH = 25
STUN_TIME = 20  # This is the amount of tics before the Player can land another hit on the Test Dummy.
#   For balance purposes, I think this should generally be less than hit_length, considering:
#   startup frames and stunlock


class Stencil(arcade.Window):
    """
        Main application class.

        NOTE: Go ahead and delete the methods you don't need.
        If you do need a method, delete the 'pass' and replace it
        with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT, SCREEN_TITLE)
        # Player and Computer(?)
        self.player_1 = None
        self.dummy = None

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set up the player info
        self.player_main_hurtbox = None
        self.player_extended_hurtbox = None
        self.player_hitbox = None
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
        p1_center = [4 * cn.SCREEN_WIDTH / 5, 2 * cn.SCREEN_HEIGHT / 5]
        d_center = [cn.SCREEN_WIDTH / 5, 2 * cn.SCREEN_HEIGHT / 5]

        self.player_main_hurtbox = arcade.SpriteSolidColor(cn.SPRITE_PLAYER_WIDTH,  # Main Player Health/Body Hit Box
                                                           cn.SPRITE_PLAYER_HEIGHT,
                                                           [0, 255, 0])
        self.player_main_hurtbox.center_x = p1_center[0]
        self.player_main_hurtbox.center_y = p1_center[1]
        self.player_extended_hurtbox = arcade.SpriteSolidColor(1,  # Extended Player Health/Body Hit Box
                                                               1,
                                                               [0, 255, 0])
        self.player_extended_hurtbox.center_x = p1_center[0]
        self.player_extended_hurtbox.center_y = p1_center[1]
        self.player_hitbox = arcade.SpriteSolidColor(1,  # Player Hit/Damage Hit Box
                                                     1,
                                                     [255, 0, 0])
        self.player_hitbox.center_x = p1_center[0]
        self.player_hitbox.center_y = p1_center[1]

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
        self.dummy_hitbox = arcade.SpriteSolidColor(1,  # Player Hit/Damage Hit Box
                                                    1,
                                                    [255, 0, 0])
        self.dummy_hitbox.center_x = d_center[0]
        self.dummy_hitbox.center_y = d_center[1]

        self.player_1 = p.Player(p1_center[0], p1_center[1],
                                 cn.SPRITE_PLAYER_WIDTH, cn.SPRITE_PLAYER_HEIGHT,
                                 self.player_main_hurtbox, self.player_extended_hurtbox,
                                 self.player_hitbox, 1)
        self.dummy = p.Player(d_center[0], d_center[1],
                              cn.SPRITE_PLAYER_WIDTH, cn.SPRITE_PLAYER_HEIGHT,
                              self.dummy_main_hurtbox, self.dummy_extended_hurtbox,
                              self.dummy_hitbox, 0)

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

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_1.update()
        self.dummy.update()

        # Now the hard part: retooling hit detection for the new inputs
        #   - We don't need to check for moves from the dummy (it doesn't even have inputs)
        #     or the stun on player_1 (it literally can't be hit)

        # Check to see if the player has attacked the dummy,
        #   THIS HAS BEEN RETOOLED FOR NEW CHANGES (constants.py and player.py usage)
        if self.dummy.stun == 0:  # 1st see if Dummy isn't already stunned
            hit_on_dummy = 0
            for hitbox in self.player_1.player_hitboxes:
                if arcade.check_for_collision_with_list(hitbox, self.dummy.player_hurtboxes):
                    hit_on_dummy += 1
            # I will admit the below if statement is a bit wack, as it functions off the fact that
            #   for ints to booleans, 0 will show as False and any other number will show as True,
            #   but, y'know, it works, and I just explained it, so we're good I guess
            if hit_on_dummy:  # IF HIT AND ~NOT STUNNED~
                print("HIT ON " + str(dt.datetime.now()))
                for hitbox in self.player_1.player_hitboxes:
                    hitbox.hit_box_algorithm = 'None'
                    hitbox.center_x = 0  # Move Hit/Damage box away to avoid...
                    hitbox.center_y = 0  # accidentally registering attacks 2x.
                    hitbox.width = 0.1  # Set the width and height to 0 to avoid...
                    hitbox.height = 0.1  # accidentally registering attacks 2x.
                arcade.set_background_color(arcade.color.YELLOW)
                for hurtbox in self.dummy.player_hurtboxes:
                    hurtbox.COLOR = [255, 174, 66]  # TODO: The Dummy color is not set when taking this hit
                if self.player_1.state == State.h_kick | self.player_1.state == State.h_punch:
                    self.dummy.stun = cn.H_STUN_TIME  # Max stun time for heavy moves
                elif ((self.player_1.state == State.aa_punch | self.player_1.state == State.aa_kick) |
                      (self.player_1.state == State.lp_punch | self.player_1.state == State.lp_kick)):
                    self.dummy.stun = cn.S_STUN_TIME  # Max stun time for special moves
                else:
                    self.dummy.stun = cn.L_STUN_TIME  # Max stun time for light moves
            else:  # IF NOT HIT AND ~NOT STUNNED~
                for hitbox in self.player_1.player_hitboxes:
                    hitbox.hit_box_algorithm = 'Simple'
                arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
                for hurtbox in self.dummy.player_hurtboxes:
                    hurtbox.COLOR = [0, 0, 250]
        else:  # IF STUNNED
            for hitbox in self.player_1.player_hitboxes:
                hitbox.hit_box_algorithm = 'None'
            if self.dummy.stun > 0:
                self.dummy.stun -= 1
                arcade.set_background_color(arcade.color.YELLOW)
                for hurtbox in self.dummy.player_hurtboxes:
                    hurtbox.COLOR = [255, 174, 66]  # TODO: The Dummy color is not set when taking this hit
            else:
                self.dummy.stun = 0
                arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
                for hurtbox in self.dummy.player_hurtboxes:
                    hurtbox.COLOR = [0, 0, 250]

        self.player_1.hit_cycle()
        self.player_1.hurt_cycle()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        ### Right now I've tuned it for the directional inputs I came up with in
            potential_control_schema.txt.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if self.player_1.state_counter == 0:  # LET'S BE REAL, THIS SUCKS TO LOOK AT. DECISION MATRIX???
            if not (self.player_1.keymap is None):
                match key:
                    case self.player_1.JUMP:
                        print("JUMPING")
                        self.player_1.jumping = True
                        # JUMP BEHAVIOR GOES HERE
                    case self.player_1.DAFOE:
                        print("DAFOEING")
                        self.player_1.dafoeing = True
                        print(self.player_1.dafoeing)
                        # LOOK UP BEHAVIOR GOES HERE
                    case self.player_1.CROUCH:
                        print("CROUCHING")
                        self.player_1.crouching = True
                        # CROUCH BEHAVIOR GOES HERE
                    case self.player_1.LEFT:
                        print("LEFTING")
                        self.player_1.lefting = True
                        # MOVE LEFT BEHAVIOR GOES HERE
                    case self.player_1.RIGHT:
                        print("RIGHTING")
                        self.player_1.righting = True
                        # MOVE RIGHT BEHAVIOR GOES HERE
                    case self.player_1.PUNCH:
                        print("PUNCH")
                        self.player_1.punching = True
                        if self.player_1.righting | self.player_1.lefting:
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
                        if self.player_1.righting | self.player_1.lefting:
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

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        match key:
            case self.player_1.JUMP:
                print("NO JUMPING")
                self.player_1.jumping = False
            case self.player_1.DAFOE:
                print("NO DAFOEING")
                self.player_1.dafoeing = False
            case self.player_1.CROUCH:
                print("NO CROUCHING")
                self.player_1.crouching = False
            case self.player_1.LEFT:
                print("NO LEFTING")
                self.player_1.lefting = False
            case self.player_1.RIGHT:
                print("NO RIGHTING")
                self.player_1.righting = False
            case self.player_1.PUNCH:
                print("NO PUNCHING")
                self.player_1.punching = False
            case self.player_1.KICK:
                print("NO KICKING")
                self.player_1.kicking = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        for hurtbox in self.player_1.player_hurtboxes:
            hurtbox.center_x = x
            hurtbox.center_y = y
            if int(self.player_1.state) > 2:
                for hitbox in self.player_1.player_hitboxes:
                    hitbox.center_x = x
                    hitbox.center_y = y

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


def main():
    """ Main function """
    game = Stencil(cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
