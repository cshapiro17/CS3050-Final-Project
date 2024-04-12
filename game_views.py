import arcade
import constants as cn
import os
import stage as s
import pyglet


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.enable_computer = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1] * 2),
                                                       int(cn.PORTRAIT_DIMENSIONS[1] * 0.75),
                                                       [255, 255, 100])
        self.enable_computer.center_x = (cn.SCREEN_WIDTH / 2) + 100
        self.enable_computer.center_y = (cn.SCREEN_HEIGHT / 4)
        self.enable_pvp = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1] * 2),
                                                  int(cn.PORTRAIT_DIMENSIONS[1] * 0.75),
                                                  [255, 0, 0])
        self.enable_pvp.center_x = (cn.SCREEN_WIDTH / 2) - 100
        self.enable_pvp.center_y = (cn.SCREEN_HEIGHT / 4)
        self.pointer = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1] * 0.25),
                                               int(cn.PORTRAIT_DIMENSIONS[1] * 0.25),
                                               [255, 255, 255])
        self.pointer.center_x = cn.SCREEN_WIDTH / 2
        self.pointer.center_y = cn.SCREEN_HEIGHT / 2
        self.pointer.alpha = 0

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color_from_hex_string("#000000"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Start Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        self.enable_computer.draw()
        arcade.draw_text("PvC", self.enable_computer.center_x, self.enable_computer.center_y - 20,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        self.enable_pvp.draw()
        arcade.draw_text("PvP", self.enable_pvp.center_x, self.enable_pvp.center_y - 20,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        self.pointer.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if arcade.check_for_collision(self.pointer, self.enable_computer):
            stage_setup_inputs = [0, -1]
            game_view = s.StageView()
            game_view.setup(stage_setup_inputs)
            self.window.show_view(game_view)
        elif arcade.check_for_collision(self.pointer, self.enable_pvp):
            stage_setup_inputs = [2, 1]
            game_view = s.StageView()
            game_view.setup(stage_setup_inputs)
            self.window.show_view(game_view)
        else:
            pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.pointer.center_x = x
        self.pointer.center_y = y


class PauseView(arcade.View):
    """
        Supplementary app class for the fighting arena.
            Called from the StageView
            Will allow user to pause fight, end fight, reset fight, and access the keymap schema
    """

    def __init__(self, stage_view):
        super().__init__()
        self.stage_view = stage_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#000000"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Game Paused ", self.window.width / 2, self.window.height / 2 + 150,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Go back [ESC]", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Reset fight [R]", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Help [H]", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("End game [E]", self.window.width / 2, self.window.height / 2 - 150,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.stage_view)
        elif key == arcade.key.R:  # reset game
            game_view = s.StageView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.H:
            help = HelpView(self)
            self.window.show_view(help)
        elif key == arcade.key.E:
            end_game = GameOverView("manual")
            self.window.show_view(end_game)


class HelpView(arcade.View):
    """
        Supplementary app class for the pause menu.
            Called from the PauseView
            Will show the user a comprehensive list of commands and keymaps
    """

    def __init__(self, pause_view):
        super().__init__()
        self.pause_view = pause_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#000000"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Help Page", self.window.width / 2, self.window.height / 2 + 150,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Go back [ESC]", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Player 1 Commands", self.window.width / 6, self.window.height / 2 + 50,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.draw_text("Jump [Space]", self.window.width / 6, self.window.height / 2 + 20,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Sprint [LShift]", self.window.width / 6, self.window.height / 2 - 10,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.pause_view)

class GameOverView(arcade.View):
    """
        Supplementary app class for the fighting arena. (Place holder for now)
            Called as a result of the end of the game
            Will end the game and allow the user to pick new characters or restart the game
    """

    def __init__(self, game_end_state):
        super().__init__()
        self.game_end_state = game_end_state
        self.lisa_win = None
        self.jackie_win = None
        self.jason_win = None
        self.kombat_theme = None
        self.Player = None


    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#000000"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        if (self.game_end_state == "timeout"):
            self.kombat_theme = arcade.load_sound("SoundEffect/Mortal Kombat.mp3")
            self.Player = arcade.play_sound(self.kombat_theme)
        elif (self.game_end_state == "1"):
            self.lisa_win = arcade.load_sound("SoundEffect/Gonna Fly Now.mp3")
            self.Player = arcade.play_sound(self.lisa_win)
        elif (self.game_end_state == "2"):
            self.jackie_win = arcade.load_sound("SoundEffect/T.N.T..wav")
            self.Player = arcade.play_sound(self.jackie_win)
        elif (self.game_end_state == "3"):
            self.jason_win = arcade.load_sound("SoundEffect/Roadrunner.mp3")
            self.Player = arcade.play_sound(self.jason_win)
        elif (self.game_end_state == "4"):
            self.kombat_theme = arcade.load_sound("SoundEffect/Mortal Kombat.mp3")
            self.Player = arcade.play_sound(self.kombat_theme)
        else:
            self.kombat_theme = arcade.load_sound("SoundEffect/Mortal Kombat.mp3")
            self.Player = arcade.play_sound(self.kombat_theme)
     

    def on_draw(self):
        self.clear()

        if (self.game_end_state == "timeout"):
            arcade.draw_text("Match Timed Out", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        elif (self.game_end_state == "1"):
            arcade.draw_text("Lisa Wins!", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        elif (self.game_end_state == "2"):
            arcade.draw_text("Jackie Wins!", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        elif (self.game_end_state == "3"):
            arcade.draw_text("Jason Wins!", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        elif (self.game_end_state == "4"):
            arcade.draw_text("Chris Wins", self.window.width / 2, self.window.height / 2 + 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        else:
            arcade.draw_text("Game Over", self.window.width / 2, self.window.height / 2 + 75,
                            arcade.color.WHITE, font_size=50, anchor_x="center")
            
        arcade.draw_text("Pick new characters [Y]", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Restart game [R]", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Exit game [ESC]", self.window.width / 2, self.window.height / 2 - 150,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.Y:   # Pick new characters
            start_view = InstructionView()
            self.window.show_view(start_view)
        elif key == arcade.key.R:  # Restart game
            arcade.stop_sound(self.Player)

            game_view = s.StageView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()