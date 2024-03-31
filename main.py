import arcade
import game_views as gv
import constants as cn

SCREEN_TITLE = "Fighting Faculty"

def main():
    """ Main function """
    window = arcade.Window(cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = gv.InstructionView()    # Will change this to "sg.StartView" eventually
    window.show_view(start_view)
   #start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()