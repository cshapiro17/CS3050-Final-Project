import arcade
import os
import datetime as dt  # If we operate off of datetime, we can ~kinda~ account for frame-dropping on intensive actions??
                       # This may also be a terrible idea, I honestly have no clue lol

#  TODO / Important Stuff:
#       Currently Hit-stun doesn't work, as well as attack delay (doesn't work), need to find work-arounds for that

# --- Constants ---
TEST_SCALING_PLAYER = 0.2
SPRITE_PLAYER_WIDTH = 80
SPRITE_PLAYER_HEIGHT = 200

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Hitbox Testing"

HIT_LENGTH = 25
STUN_TIME = 20  # This is the amount of tics before the Player can land another hit on the Test Dummy.
                    # For balance purposes, I think this should generally be less than hit_length, considering:
                    # startup frames and stunlock


class Stencil(arcade.Window):
    """
        Main application class.

        NOTE: Go ahead and delete the methods you don't need.
        If you do need a method, delete the 'pass' and replace it
        with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        self.hit_counter = 0
        self.test_dummy_stun = 0
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_body_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite_body = None
        self.player_sprite_hit = None
        self.test_dummy_body = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BATTLESHIP_GREY)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.player_body_list = arcade.SpriteList()

        self.player_sprite_body = arcade.SpriteSolidColor(SPRITE_PLAYER_WIDTH,  # Player Health/Body Hit Box
                                                          SPRITE_PLAYER_HEIGHT,
                                                          [0, 255, 0])
        self.player_sprite_body.center_x = -64
        self.player_sprite_body.center_y = -64
        self.player_body_list.append(self.player_sprite_body)
        self.player_sprite_hit = arcade.SpriteSolidColor(SPRITE_PLAYER_WIDTH,  # Player Hit/Damage Hit Box
                                                         int(SPRITE_PLAYER_HEIGHT/3),
                                                         [255, 0, 0])
        self.player_sprite_hit.center_x = 64
        self.player_sprite_hit.center_y = 128

        self.test_dummy_body = arcade.SpriteSolidColor(SPRITE_PLAYER_WIDTH,  # Test Dummy Health/Body Hit Box
                                                            SPRITE_PLAYER_HEIGHT,
                                                            [0, 0, 250])
        self.test_dummy_body.center_x = SCREEN_WIDTH/5
        self.test_dummy_body.center_y = 2*SCREEN_HEIGHT/5
        self.player_body_list.append(self.test_dummy_body)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.player_body_list.draw()  # Draws the Health/Body Hit Boxes for both the Player and Test Dummy
        # TODO: THE BELOW IF STATEMENT SHOULD ONLY STARTUP THE HIT/DAMAGE BOX LOOP IF IT HAS NOT ALREADY STARTED AND
        #       THE TEST DUMMY'S STUN IS NOT ACTIVE, HOWEVER THIS IS NOT WORKING
        #       (LOOPS START TOO FAST/ CAN BE STARTED DURING STUN)
        if self.hit_counter != 0 & self.test_dummy_stun == 0:
            self.player_sprite_hit.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_body_list.update()
        self.player_sprite_hit.update()

        if self.hit_counter != 0:  # If a hit tic cycle/ animation is started
            if self.hit_counter == HIT_LENGTH:  # If tic cycle has completed and is at max length
                self.hit_counter = 0  # Reset cycle so it can be started again
            else:  # Move the player_sprite_hit to the correct spot and 'animate' it
                self.player_sprite_hit.center_x = self.player_sprite_body.center_x - 6*self.hit_counter
                self.player_sprite_hit.center_y = self.player_sprite_body.center_y + self.hit_counter
                self.player_sprite_hit.width = 15*self.hit_counter
                self.player_sprite_hit.height = 7*self.hit_counter
                self.hit_counter += 1  # Increment cycle

        # Check to see if the player has attacked the dummy
        if self.test_dummy_stun == 0:  # 1st see if Dummy isn't already stunned
            hit_on_dummy = (arcade.check_for_collision(self.player_sprite_hit, self.test_dummy_body))
            if hit_on_dummy:  # IF HIT AND ~NOT STUNNED~
                print("HIT ON " + str(dt.datetime.now()))
                self.player_sprite_hit.hit_box_algorithm = 'None'
                arcade.set_background_color(arcade.color.YELLOW)
                self.test_dummy_body.COLOR = [255, 174, 66]  # TODO: The Dummy color is not set when taking this hit
                self.player_sprite_hit.center_x = 0  # Move Hit/Damage box away to avoid...
                self.player_sprite_hit.center_y = 0  # accidentally registering attacks 2x.
                self.player_sprite_hit.width = 0.1   # Set the width and height to 0 to avoid...
                self.player_sprite_hit.height = 0.1  # accidentally registering attacks 2x.
                self.test_dummy_stun = STUN_TIME  # Set stun time to max to start that loop
            else:  # IF NOT HIT AND ~NOT STUNNED~
                self.player_sprite_hit.hit_box_algorithm = 'Simple'
                arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
                self.test_dummy_body.COLOR = [0, 0, 255]
        else:  # IF STUNNED
            self.player_sprite_hit.hit_box_algorithm = 'None'
            if self.test_dummy_stun > 0:
                self.test_dummy_stun -= 1
                arcade.set_background_color(arcade.color.YELLOW)
                self.test_dummy_body.COLOR = [255, 174, 66]  # TODO: The Dummy color is not set when taking this hit
            else:
                self.test_dummy_stun = 0
                arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
                self.test_dummy_body.COLOR = [0, 0, 255]

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite_body.center_x = x
        self.player_sprite_body.center_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.hit_counter == 0:
            self.hit_counter = 1

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = Stencil(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
