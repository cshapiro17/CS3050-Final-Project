import arcade
import constants as cn
import os
import stage as s

'''
WelcomeView represents the first screen that the user interacts with
This view allows the user to choose if they would like to play against
The computer or against another player
'''
class WelcomeView(arcade.View):

    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(True)

        # Set up the solid sprites for the welcome view
        self.enable_computer = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1] * 2),
                                                       int(cn.PORTRAIT_DIMENSIONS[1] * 0.75),
                                                       [255, 255, 255])
        self.enable_computer.center_x = (cn.SCREEN_WIDTH / 2) + 100
        self.enable_computer.center_y = (cn.SCREEN_HEIGHT / 4)
        self.enable_pvp = arcade.SpriteSolidColor(int(cn.PORTRAIT_DIMENSIONS[1] * 2),
                                                  int(cn.PORTRAIT_DIMENSIONS[1] * 0.75),
                                                  [255, 255, 255])
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
        arcade.set_background_color(arcade.color_from_hex_string(cn.START_BACKGROUND_COLOR))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()

        arcade.draw_text("Komputer Science", self.window.width / 2, self.window.height / 2 + 150,
                         arcade.color_from_hex_string(cn.START_TXT_COLOR), font_size=60, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        arcade.draw_text("Kombat", self.window.width / 2, self.window.height / 2 + 20,
                         arcade.color_from_hex_string(cn.START_TXT_COLOR), font_size=60, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color_from_hex_string(cn.START_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        self.enable_computer.draw()
        arcade.draw_text("PvC", self.enable_computer.center_x, self.enable_computer.center_y - 17.5,
                         arcade.color_from_hex_string(cn.START_TXT_COLOR), font_size=25, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        self.enable_pvp.draw()
        arcade.draw_text("PvP", self.enable_pvp.center_x, self.enable_pvp.center_y - 17.5,
                         arcade.color_from_hex_string(cn.START_TXT_COLOR), font_size=25, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        self.pointer.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if arcade.check_for_collision(self.pointer, self.enable_computer):
            game_view = PlayVsComp()
            self.window.show_view(game_view)
        elif arcade.check_for_collision(self.pointer, self.enable_pvp):
            game_view = PlayVsPlay()
            self.window.show_view(game_view)
        else:
            pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.pointer.center_x = x
        self.pointer.center_y = y


'''
The PlayVsPlay view acts as the view which allows the users to select their players in 2 player mode
'''
class PlayVsPlay(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color_from_hex_string(cn.START_BACKGROUND_COLOR))
        self.character_image ={
            "Lisa Dion": arcade.load_texture("images/Lisa/idle.png"),
            "Jackie Horton": arcade.load_texture("images/Jackie/idle.png"),
            "Jason Hibbeler": arcade.load_texture("images/Jason/idle.png"),
            "Chris Skalka": arcade.load_texture("images/Chris/idle.png")
        }
        self.banner_image = arcade.load_texture("images/backgrounds/ChooseUrFighter.png")
        #default is Jason incase no one chooses
        self.p1_character = 3
        self.p2_character = 3

    def on_draw(self):
        arcade.start_render()
        # Create the text for this view
        arcade.draw_texture_rectangle(700, cn.SCREEN_HEIGHT - 100,
                                      self.banner_image.width,
                                      self.banner_image.height,
                                      self.banner_image, 0)
        arcade.draw_text("Player 1 use ASDF and Player 2 Use HJKL", self.window.width / 2, self.window.height / 1.6 + 10,
                         arcade.color.BLACK, font_size=20, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        arcade.draw_text("Click Mouse to Continue", self.window.width / 2, self.window.height / 1.6 - 25,
                         arcade.color.BLACK, font_size=20, anchor_x="center",
                         font_name=cn.START_TXT_FONT)
        

        #character options
        arcade.draw_texture_rectangle(250, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Lisa Dion"].width,
                                      self.character_image["Lisa Dion"].height,
                                      self.character_image["Lisa Dion"], 0)
        arcade.draw_texture_rectangle(550, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Jackie Horton"].width,
                                      self.character_image["Jackie Horton"].height,
                                      self.character_image["Jackie Horton"], 0)
        arcade.draw_texture_rectangle(850, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Jason Hibbeler"].width,
                                      self.character_image["Jason Hibbeler"].height,
                                      self.character_image["Jason Hibbeler"], 0)
        arcade.draw_texture_rectangle(1150, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Chris Skalka"].width,
                                      self.character_image["Chris Skalka"].height,
                                      self.character_image["Chris Skalka"], 0)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.p1_character = 1
        elif key == arcade.key.S:
            self.p1_character = 2
        elif key == arcade.key.D:
            self.p1_character = 3
        elif key == arcade.key.F:
            self.p1_character = 4

        if key == arcade.key.H:
            self.p2_character = 1
        elif key == arcade.key.J:
            self.p2_character = 2
        elif key == arcade.key.K:
            self.p2_character = 3
        elif key == arcade.key.L:
            self.p2_character = 4

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if self.p1_character and self.p2_character:
            character_selection = [self.p1_character, self.p2_character]
            setup_inputs = [1,2]
            game_view = s.StageView()
            game_view.setup(setup_inputs, character_selection)
            self.window.show_view(game_view)



class PlayVsComp(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color_from_hex_string(cn.START_BACKGROUND_COLOR))
        self.character_image ={
            "Lisa Dion": arcade.load_texture("images/Lisa/idle.png"),
            "Jackie Horton": arcade.load_texture("images/Jackie/idle.png"),
            "Jason Hibbeler": arcade.load_texture("images/Jason/idle.png"),
            "Chris Skalka": arcade.load_texture("images/Chris/idle.png")
        }
        self.banner_image = arcade.load_texture("images/backgrounds/ChooseUrFighter.png")
        #default is Jason incase no one chooses
        self.p1_character = 3
        self.p2_character = 3


    def on_draw(self):
        arcade.start_render()
        #Text
        arcade.draw_texture_rectangle(700, cn.SCREEN_HEIGHT - 100,
                                      self.banner_image.width,
                                      self.banner_image.height,
                                      self.banner_image, 0)
        arcade.draw_text("Player 1 use ASDF, Click Mouse to Continue", self.window.width / 2, self.window.height / 1.6,
                         arcade.color.BLACK, font_size=20, anchor_x="center",
                         font_name=cn.START_TXT_FONT)

        #character options
        arcade.draw_texture_rectangle(250, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Lisa Dion"].width,
                                      self.character_image["Lisa Dion"].height,
                                      self.character_image["Lisa Dion"], 0)
        arcade.draw_texture_rectangle(550, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Jackie Horton"].width,
                                      self.character_image["Jackie Horton"].height,
                                      self.character_image["Jackie Horton"], 0)
        arcade.draw_texture_rectangle(850, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Jason Hibbeler"].width,
                                      self.character_image["Jason Hibbeler"].height,
                                      self.character_image["Jason Hibbeler"], 0)
        arcade.draw_texture_rectangle(1150, cn.SCREEN_HEIGHT - 500,
                                      self.character_image["Chris Skalka"].width,
                                      self.character_image["Chris Skalka"].height,
                                      self.character_image["Chris Skalka"], 0)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.p1_character = 1
        elif key == arcade.key.S:
            self.p1_character = 2
        elif key == arcade.key.D:
            self.p1_character = 3
        elif key == arcade.key.F:
            self.p1_character = 4

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if self.p1_character and self.p2_character:
            character_selection = [self.p1_character, -1]
            setup_inputs = [0, -1]
            game_view = s.StageView()
            game_view.setup(setup_inputs, character_selection)
            self.window.show_view(game_view)

class PauseView(arcade.View):
    """
        Supplementary app class for the fighting arena.
            Called from the StageView
            Will allow user to pause fight, end fight, reset fight, and access the keymap schema
    """

    def __init__(self, stage_view, player_controller_num, dummy_controller_num, player1, player2):
        super().__init__()
        self.stage_view = stage_view
        self.setup_inputs = [player_controller_num, dummy_controller_num]
        self.character_selection = [player1, player2]

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string(cn.BACKGROUND_COLOR))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Game Paused ", self.window.width / 2 + 15, self.window.height / 2 + 150,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=50, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Go back [ESC]", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Reset fight [R]", self.window.width / 2, self.window.height / 2 - 25,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Help [H]", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("End game [E]", self.window.width / 2, self.window.height / 2 - 175,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.stage_view)
        elif key == arcade.key.R:  # reset game
            game_view = s.StageView()
            game_view.setup(self.setup_inputs, self.character_selection)
            self.window.show_view(game_view)
        elif key == arcade.key.H:
            help = HelpView(self)
            self.window.show_view(help)
        elif key == arcade.key.E:
            end_game = GameOverView("manual", self.setup_inputs[0], self.setup_inputs[1], self.character_selection[0], self.character_selection[1])
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
        arcade.set_background_color(arcade.color_from_hex_string(cn.BACKGROUND_COLOR))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Help Page", self.window.width / 2, self.window.height - 50,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=30, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Go back [ESC]", self.window.width / 2, self.window.height / 2 + 260,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        
        # PVP Command Text
        arcade.draw_text("PVP Commands   Left Player = [], Right Player = ()", self.window.width / 2, self.window.height / 2 + 225,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Look up", self.window.width / 4, self.window.height / 2 + 195,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[I] (W)", self.window.width / 3, self.window.height / 2 + 195,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Move left", self.window.width / 4, self.window.height / 2 + 170,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[J] (A)", self.window.width / 3, self.window.height / 2 + 170,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Crouch", self.window.width / 4, self.window.height / 2 + 145,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[K] (S)", self.window.width / 3, self.window.height / 2 + 145,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Move right", self.window.width / 4, self.window.height / 2 + 125,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[L] (D)", self.window.width / 3, self.window.height / 2 + 125,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Jump", self.window.width / 4, self.window.height / 2 + 100,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[R ALT] (L ALT)", self.window.width / 3, self.window.height / 2 + 100,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Punch", self.window.width / 4, self.window.height / 2 + 75,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[M] (Z)", self.window.width / 3, self.window.height / 2 + 75,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Dash", self.window.width / 4, self.window.height / 2 + 50,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[Space] (Shift)", self.window.width / 3, self.window.height / 2 + 50,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        
        # PVC Command Text
        arcade.draw_text("PVC Commands", self.window.width / 5 + 40, self.window.height / 2,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Look up", self.window.width / 4, self.window.height / 2 - 30,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[W]", self.window.width / 3, self.window.height / 2 - 30,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Move left", self.window.width / 4, self.window.height / 2 - 55,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[A]", self.window.width / 3, self.window.height / 2 - 55,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Crouch", self.window.width / 4, self.window.height / 2 - 80,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[S]", self.window.width / 3, self.window.height / 2 - 80,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Move right", self.window.width / 4, self.window.height / 2 - 105,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[D]", self.window.width / 3, self.window.height / 2 - 105,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Jump", self.window.width / 4, self.window.height / 2 - 130,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[Space]", self.window.width / 3, self.window.height / 2 - 130,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Punch", self.window.width / 4, self.window.height / 2 - 155,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[J]", self.window.width / 3, self.window.height / 2 - 155,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Dash", self.window.width / 4, self.window.height / 2 - 180,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("[Shift]", self.window.width / 3, self.window.height / 2 - 180,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, width=250, align="right",
                         font_name=cn.GE_TXT_FONT)
        
        arcade.draw_text("Game Notes", self.window.width / 5 + 20, self.window.height / 2 - 225,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center", align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("1. Blocking occurs when moving backwards away from enemy", self.window.width / 4, self.window.height / 2 - 250,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("2. Punching while moving towards enemy produces a light, fast punch", self.window.width / 4, self.window.height / 2 - 275,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("3. Punching while looking up produces a short range, high damage punch", self.window.width / 4, self.window.height / 2 - 300,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("4. Punching while crouching punishes jumping attacks from enemy", self.window.width / 4, self.window.height / 2 - 325,
                         arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=10, align="left",
                         font_name=cn.GE_TXT_FONT)
        
        
        


        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.pause_view)

class GameOverView(arcade.View):
    """
        Supplementary app class for the fighting arena. (Place holder for now)
            Called as a result of the end of the game
            Will end the game and allow the user to pick new characters or restart the game
    """

    def __init__(self, game_end_state, player_num, dummy_num, player1, player2):
        super().__init__()
        self.game_end_state = game_end_state
        self.lisa_win = None
        self.jackie_win = None
        self.jason_win = None
        self.kombat_theme = None
        self.Player = None
        self.setup_inputs = [player_num, dummy_num]
        self.character_selection = [player1, player2]


    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string(cn.BACKGROUND_COLOR))

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

        arcade.set_background_color(arcade.color_from_hex_string(cn.BACKGROUND_COLOR)) # Make background grey

        arcade.draw_text("Pick new characters [Y]", self.window.width / 2, self.window.height / 2 - 25,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=15, anchor_x="center", 
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Restart game [R]", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=15, anchor_x="center",
                         font_name=cn.GE_TXT_FONT)
        arcade.draw_text("Exit game [ESC]", self.window.width / 2, self.window.height / 2 - 175,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=15, anchor_x="center", 
                         font_name=cn.GE_TXT_FONT)

        if (self.game_end_state == "timeout"):
            arcade.draw_text("Match Timed Out", self.window.width / 2, self.window.height / 2 + 115,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=60, anchor_x="center",
                         font_name= cn.GE_TXT_FONT, bold=True)
        elif (self.game_end_state == "1"):
            arcade.set_background_color(arcade.color_from_hex_string(cn.LISA_WIN_COLOR)) # Make background grey

            arcade.draw_text("Lisa Wins!", self.window.width / 2, self.window.height / 2 + 115,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=60, anchor_x="center",
                         font_name=cn.GE_TXT_FONT, bold=True)
        elif (self.game_end_state == "2"):
            arcade.set_background_color(arcade.color_from_hex_string(cn.JACKIE_WIN_COLOR))

            arcade.draw_text("Jackie Wins!", self.window.width / 2, self.window.height / 2 + 115,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=60, anchor_x="center",
                         font_name=cn.GE_TXT_FONT, bold=True)
        elif (self.game_end_state == "3"):
            arcade.set_background_color(arcade.color_from_hex_string(cn.JASON_WIN_COLOR)) 

            arcade.draw_text("Jason Wins!", self.window.width / 2, self.window.height / 2 + 115,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=60, anchor_x="center",
                         font_name=cn.GE_TXT_FONT, bold=True)
        elif (self.game_end_state == "4"):
            arcade.set_background_color(arcade.color_from_hex_string(cn.CHRIS_WIN_COLOR))

            arcade.draw_text("Chris Wins!", self.window.width / 2, self.window.height / 2 + 115,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=60, anchor_x="center",
                         font_name=cn.GE_TXT_FONT, bold=True)
        elif (self.game_end_state == "5"):
            arcade.set_background_color(arcade.color_from_hex_string(cn.ROBOT_WIN_COLOR)) # Make background grey

            arcade.draw_text("Robot Wins!", self.window.width / 2, self.window.height / 2 + 115,
                         arcade.color_from_hex_string("#FFFFFF"), font_size=60, anchor_x="center",
                         font_name=cn.GE_TXT_FONT, bold=True)
        else:
            arcade.draw_text("Game Over", self.window.width / 2, self.window.height / 2 + 115,


                            arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=60, anchor_x="center", 
                            font_name=cn.GE_TXT_FONT, bold=True)
            
            arcade.draw_text("Pick new characters [Y]", self.window.width / 2, self.window.height / 2 - 25,
                            arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center", 
                            font_name=cn.GE_TXT_FONT)
            arcade.draw_text("Restart game [R]", self.window.width / 2, self.window.height / 2 - 100,
                            arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center",

                         font_name=cn.GE_TXT_FONT)
            arcade.draw_text("Exit game [ESC]", self.window.width / 2, self.window.height / 2 - 175,
                            arcade.color_from_hex_string(cn.GE_TXT_COLOR), font_size=15, anchor_x="center", 
                            font_name=cn.GE_TXT_FONT)
        
        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.Y:   # Pick new characters
            arcade.stop_sound(self.Player)

            start_view = WelcomeView()
            self.window.show_view(start_view)
        elif key == arcade.key.R:  # Restart game
            arcade.stop_sound(self.Player)

            game_view = s.StageView()
            game_view.setup(self.setup_inputs, self.character_selection)
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()