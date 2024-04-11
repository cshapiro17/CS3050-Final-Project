import arcade
import constants as cn
import os
import stage as s

class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/backgrounds/csKombat.png")
        self.text= arcade.Text("Welcome to Komputer Science Kombat: A Faculty Fighting Game!\n"
                                "Here are the rules:\n \n"
                                "Player 1 has the controls a-s-d-w, left-crouch-right-jump\n"
                                "Player 2's controls are j-k-l-i, left-crouch-right-jump\n"
                                "Press (p) to pause the fight\n" 
                                "You have 60 seconds to fight, do your best and fight our faculty!\n"
                                "To block, walk backwards (away from enemy), and press (shift) to dash\n"
                                "Press (q) to punch, (-q) for a heavy punch, (e) to kick (-e) to heavy kick,\n"
                                "and beat your opponent with a Heavy Move by pressing (f)\n"
                                "If you run into any issues, press (h) for help, and press (q) to quit",
                                 self.window.width / 12, cn.START_Y +35,
                                 cn.K_RED,
                                 cn.DEFAULT_FONT_SIZE - 10,
                                 multiline=True,
                                 width=1300)
    def on_show_view(self):
        arcade.set_background_color(cn.K_ORANGE)
         # Reset the viewport
        # arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(self.window.width /2, self.window.height /2.25, self.window.width , cn.START_Y -30, arcade.color.WHITE)
        self.text.draw()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height - 130,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        arcade.draw_text("(Click to advance)", self.window.width / 2, self.window.height / 4 - 105,
                         arcade.color.WHITE, font_size=25, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = SelectionScreen()
        game_view.setup()
        self.window.show_view(game_view)


class SelectionScreen(arcade.Window):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
         # Reset the viewport
        # arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def button_clicked(self, _x, _y, _button):
        game_view = s.StageView()
        game_view.setup()
        self.window.show_view(game_view)


    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Start Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = s.StageView()
        game_view.setup()
        self.window.show_view(game_view)


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
            end_game = GameOverView()
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

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#000000"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()

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
            game_view = s.StageView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()