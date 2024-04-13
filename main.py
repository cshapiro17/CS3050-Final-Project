import arcade
import game_views as gv
import stage as s
import constants as cn

SCREEN_TITLE = "Fighting Faculty"


def main():
    """ Main function """
    window = arcade.Window(cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = gv.PlayVsPlay()
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()
