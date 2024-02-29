"""
This simple animation example shows how to bounce a rectangle
on the screen.

If Python and Arcade are installed, this example can be run
from the command line with:
python -m arcade.examples.bouncing_rectangle
"""

import arcade

# --- Set up the constants

# Size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Player Movement"

MOVEMENT_SPEED = 5

# Rectangle info
RECT_WIDTH = 25
RECT_HEIGHT = 75
RECT_COLOR = arcade.color.DARK_BROWN

BACKGROUND_COLOR = arcade.color.AMAZON


class Item:
    """ This class represents our rectangle """

    def __init__(self):

        # Set up attribute variables

        # Where we are
        self.center_x = 0
        self.center_y = 0

        # Where we are going
        self.change_x = 0
        self.change_y = 0

    def update(self):
        """ Move the player """
        
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if (self.center_x - (RECT_WIDTH/2)) < 0:
            self.center_x = RECT_WIDTH/2
        elif (self.center_x + (RECT_WIDTH/2)) > SCREEN_WIDTH - 1:
            self.center_x = SCREEN_WIDTH - 1 - RECT_WIDTH/2

        if (self.center_y - (RECT_HEIGHT/2)) < 0:
            self.center_y = RECT_HEIGHT/2
        elif (self.center_y + (RECT_WIDTH/2)) > SCREEN_HEIGHT - 1:
            self.center_y = SCREEN_HEIGHT - 1 - RECT_WIDTH/2    

    def draw(self):
        # Draw the rectangle
        arcade.draw_rectangle_filled(self.center_x,
                                        self.center_y,
                                        RECT_WIDTH,
                                        RECT_HEIGHT,
                                        RECT_COLOR)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Create our rectangle
        self.item = Item()
        self.item.center_x = 200
        self.item.center_y = 300

        # Set background color
        self.background_color = BACKGROUND_COLOR

    def on_update(self, delta_time):
        # Move the rectangle
        self.item.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear screen
        self.clear()
        # Draw the rectangle
        self.item.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.item.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.item.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.item.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.item.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.item.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.item.change_x = 0


def main():
    """ Main function """
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()