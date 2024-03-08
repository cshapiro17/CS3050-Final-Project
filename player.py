import arcade
import constants as cn
from constants import State

KEYMAP = dict(
    JUMP=arcade.key.SPACE,
    DAFOE=arcade.key.W,
    CROUCH=arcade.key.S,
    LEFT=arcade.key.A,
    RIGHT=arcade.key.D,
    PUNCH=arcade.key.Q,
    KICK=arcade.key.E
)


class Player(object):
    def __init__(self,
                 center_x: int, center_y: int,
                 width: int, height: int,
                 main_hurtbox: arcade.SpriteSolidColor, extended_hurtbox: arcade.SpriteSolidColor,
                 hitbox: arcade.SpriteSolidColor,
                 input_map: int):
        # Start-up Stats:
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 0
        self.change_y = 0
        self.height = height
        self.width = width

        # State Accounting:
        self.state = cn.State.idle
        self.health = cn.PLAYER_HEALTH
        self.alive = True
        self.right = True
        # More Precise State Accounting
        self.stun = 0
        self.state_counter = 0
        # Key Accounting:
        self.jumping = False
        self.dafoeing = False
        self.crouching = False
        self.lefting = False
        self.righting = False
        self.punching = False
        self.kicking = False

        # Hurt/Hitbox Setup:
        #   Hurt/Hitbox Lists:
        self.player_hurtboxes = arcade.SpriteList()
        self.player_hitboxes = arcade.SpriteList()
        # Hurt/Hitbox Assignment:
        self.main_hurtbox = main_hurtbox
        self.player_hurtboxes.append(self.main_hurtbox)
        self.extended_hurtbox = extended_hurtbox
        self.player_hurtboxes.append(self.extended_hurtbox)
        self.hitbox = hitbox
        self.player_hitboxes.append(self.hitbox)

        if input_map > 0:
            self.keymap = KEYMAP
            self.JUMP = self.keymap['JUMP']
            self.DAFOE = self.keymap['DAFOE']
            self.CROUCH = self.keymap['CROUCH']
            self.LEFT = self.keymap['LEFT']
            self.RIGHT = self.keymap['RIGHT']
            self.PUNCH = self.keymap['PUNCH']
            self.KICK = self.keymap['KICK']
        else:
            self.keymap = None

    def update(self):
        self.player_hurtboxes.update()
        self.player_hitboxes.update()

    def hit_cycle(self):
        if self.state_counter != 0:
            # THIS WILL TRACK PLAYER MOVES TO 'ANIMATE' AND MOVE HITBOXES
            # TODO: Get the old hitbox testing code working with only one move (LIGHT PUNCH) before expanding it to
            #   more moves.
            # TODO: Work on the sprite movement. It should not be displayed in terms of state_counter, but rather in
            #   terms of SCREEN_WIDTH and SCREEN_HEIGHT (or self.sprite_hit.width and self.sprite_hit.height)
            #   WE ALSO HAVE 2 BUTTONS NOW, MIGHT AS WELL THROW THAT ALL IN HERE

            # EXAMPLE HIT:
            # self.player_hitbox.center_x = self.player_hurtbox.center_x - 6*self.state_counter
            # self.player_hitbox.center_y = self.player_hurtbox.center_y + self.state_counter
            # self.player_hitbox.width = 15*self.state_counter
            # self.player_hitbox.height = 7*self.state_counter
            # TODO: Setup animations in chunks (START-UP, ACTIVE, AND RECOVERY FRAMES) based on state_counter
            if self.state == State.l_punch:  # LIGHT PUNCH
                # START-UP:
                if self.state_counter > 15:
                    self.render_hitbox = False
                    # Player Hurtbox Setup:
                    ###self.player_hurtbox.width = cn.SPRITE_PLAYER_WIDTH + (self.hit_counter_MAX-self.hit_counter)*5
                    ###self.player_hurtbox.height = cn.SPRITE_PLAYER_HEIGHT - (self.hit_counter_MAX-self.hit_counter)*4
                # ACTIVE:
                elif self.state_counter > 9:
                    # Player Hurtbox Setup:
                    ###self.player_hurtbox.width = cn.SPRITE_PLAYER_WIDTH + (self.hit_counter_MAX-self.hit_counter)*5
                    ###self.player_hurtbox.height = cn.SPRITE_PLAYER_HEIGHT - (self.hit_counter_MAX-self.hit_counter)
                    # Player Hitbox Setup:
                    ###self.player_hitbox.center_x = self.player_hurtbox.center_x - 10*(self.hit_counter_MAX -
                    ###                                                                 self.hit_counter)
                    ###self.player_hitbox.center_y = self.player_hurtbox.center_y + (self.hit_counter_MAX -
                    ###                                                              self.hit_counter)
                    ###self.player_hitbox.width = 15*(self.hit_counter_MAX-self.hit_counter)
                    ###self.player_hitbox.height = 7*(self.hit_counter_MAX-self.hit_counter)
                    self.render_hitbox = True
                # RECOVERY:
                elif self.state_counter > 0:
                    ###self.player_hurtbox.width = cn.SPRITE_PLAYER_WIDTH
                    ###self.player_hurtbox.height = cn.SPRITE_PLAYER_HEIGHT
                    self.render_hitbox = False
            self.state_counter -= 1  # Increment cycle
        elif self.state_counter == 0 | self.state_counter < 0:
            self.state_counter = 0  # Reset cycle so it can be started again
            self.state = State.idle

    def hurt_cycle(self):
        if self.state_counter != 0:
            # THIS WILL TRACK PLAYER MOVES TO 'ANIMATE' AND MOVE HURTBOXES
            # TODO: Get the old hurtbox testing code working with only one move (LIGHT PUNCH) before expanding it to
            #   more moves.
            # TODO: Work on the sprite movement. It should not be displayed in terms of state_counter, but rather in
            #   terms of SCREEN_WIDTH and SCREEN_HEIGHT (or self.sprite_hit.width and self.sprite_hit.height)
            #   WE ALSO HAVE 2 BUTTONS NOW, MIGHT AS WELL THROW THAT ALL IN HERE

            # TODO: Setup animations in chunks (START-UP, ACTIVE, AND RECOVERY FRAMES) based on state_counter
            if self.state == State.l_punch:  # LIGHT PUNCH
                # START-UP:
                if self.state_counter > 10:
                    self.render_hitbox = False
                    # Player Hurtbox Setup:
                    ###self.player_hurtbox.width = cn.SPRITE_PLAYER_WIDTH + (self.hit_counter_MAX-self.hit_counter)*5
                    ###self.player_hurtbox.height = cn.SPRITE_PLAYER_HEIGHT - (self.hit_counter_MAX-self.hit_counter)*4
                # ACTIVE:
                elif self.state_counter > 5:
                    # Player Hurtbox Setup:
                    ###self.player_hurtbox.width = cn.SPRITE_PLAYER_WIDTH + (self.hit_counter_MAX-self.hit_counter)*5
                    ###self.player_hurtbox.height = cn.SPRITE_PLAYER_HEIGHT - (self.hit_counter_MAX-self.hit_counter)
                    # Player Hitbox Setup:
                    ###self.player_hitbox.center_x = self.player_hurtbox.center_x - 10*(self.hit_counter_MAX -
                    ###                                                                 self.hit_counter)
                    ###self.player_hitbox.center_y = self.player_hurtbox.center_y + (self.hit_counter_MAX -
                    ###                                                              self.hit_counter)
                    ###self.player_hitbox.width = 15*(self.hit_counter_MAX-self.hit_counter)
                    ###self.player_hitbox.height = 7*(self.hit_counter_MAX-self.hit_counter)
                    self.render_hitbox = True
                # RECOVERY:
                elif self.state_counter > 0:
                    ###self.player_hurtbox.width = cn.SPRITE_PLAYER_WIDTH
                    ###self.player_hurtbox.height = cn.SPRITE_PLAYER_HEIGHT
                    self.render_hitbox = False
            self.state_counter -= 1  # Increment cycle
        elif self.state_counter == 0 | self.state_counter < 0:
            self.state_counter = 0  # Reset cycle so it can be started again
            self.state = State.idle
