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
        self.hit_counter = 0
        self.hit_counter_MAX = 0
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
