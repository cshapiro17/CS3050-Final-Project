import platform
import arcade
import os
from arcade import check_for_collision_with_lists, check_for_collision

import constants as cn
from constants import State

"""
Keymaps: FULL_KEYMAP is for single-player commands,
    SPLIT_KEYMAPs are for split characters.
    Darwin is for Macs, as their keyboards differ from Windows.
"""

FULL_KEYMAP = dict(
    JUMP=arcade.key.SPACE,
    SPRINT=arcade.key.LSHIFT,
    DAFOE=arcade.key.W,
    CROUCH=arcade.key.S,
    LEFT=arcade.key.A,
    RIGHT=arcade.key.D,
    PUNCH=arcade.key.J,
    KICK=arcade.key.K,
    SPECIAL=arcade.key.L
)
if platform.system() == 'Darwin':
    SPLIT_KEYMAP_L = dict(
        JUMP=arcade.key.LCOMMAND,
        SPRINT=arcade.key.LSHIFT,
        DAFOE=arcade.key.W,
        CROUCH=arcade.key.S,
        LEFT=arcade.key.A,
        RIGHT=arcade.key.D,
        PUNCH=arcade.key.Z,
        KICK=arcade.key.X,
        SPECIAL=arcade.key.C
    )
    SPLIT_KEYMAP_R = dict(
        JUMP=arcade.key.RCOMMAND,
        SPRINT=arcade.key.SPACE,
        DAFOE=arcade.key.I,
        CROUCH=arcade.key.K,
        LEFT=arcade.key.J,
        RIGHT=arcade.key.L,
        PUNCH=arcade.key.M,
        KICK=arcade.key.COMMA,
        SPECIAL=arcade.key.PERIOD
    )
else:
    SPLIT_KEYMAP_L = dict(
        JUMP=arcade.key.LALT,
        SPRINT=arcade.key.LSHIFT,
        DAFOE=arcade.key.W,
        CROUCH=arcade.key.S,
        LEFT=arcade.key.A,
        RIGHT=arcade.key.D,
        PUNCH=arcade.key.Z,
        KICK=arcade.key.X,
        SPECIAL=arcade.key.C
    )
    SPLIT_KEYMAP_R = dict(
        JUMP=arcade.key.RALT,
        SPRINT=arcade.key.SPACE,
        DAFOE=arcade.key.I,
        CROUCH=arcade.key.K,
        LEFT=arcade.key.J,
        RIGHT=arcade.key.L,
        PUNCH=arcade.key.M,
        KICK=arcade.key.COMMA,
        SPECIAL=arcade.key.PERIOD
    )

# TODO, maybe? Not sure abt gamepad support.
"""
GAMEPAD_KEYMAP = dict(
    JUMP=arcade.key.?,
    SPRINT=arcade.key.?,
    DAFOE=arcade.key.?,
    CROUCH=arcade.key.?,
    LEFT=arcade.key.?,
    RIGHT=arcade.key.?,
    PUNCH=arcade.key.?,
    KICK=arcade.key.?,
    SPECIAL=arcade.key.?
)
"""


class Player(object):
    def __init__(self,
                 center_x: int, center_y: int,
                 width: int, height: int,
                 main_hurtbox: arcade.SpriteSolidColor, extended_hurtbox: arcade.SpriteSolidColor,
                 hitbox: arcade.SpriteSolidColor,
                 input_map: int):
        """
        CONTAINS ALL SET-UP AND VARIABLE DECLARATION FOR THE PLAYER CLASS
        """
        # Start-up Stats:
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 0
        self.change_y = 0
        self.height = height
        self.width = width

        # State Accounting:
        self.state = cn.State.idle
        self.health = cn.PLAYER_HEALTH     # UI will grab these in stage for bars
        self.block_health = cn.FULL_BLOCK  # UI will grab these in stage for bars
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

        self.blocking = False

        self.sprinting = False
        self.left_dash = False
        self.right_dash = False

        self.mid_dash = False

        self.left_jump = False
        self.right_jump = False
        self.neutral_jump = False

        self.mid_jump = False

        self.being_hit = False
        # Move Inputs accel_vals accounting:
        self.change_x_L = 0  # The change_x value taken from the LEFT key
        self.change_x_R = 0  # The change_x value taken from the RIGHT key
        self.change_x_S = 0  # The change_x value taken from the SPRINT key
        self.change_y_S = 0  # The change_y value taken from the SPRINT key
        self.change_x_J = 0  # The change_x value taken from the JUMP key
        self.change_y_J = 0  # The change_y value taken from the JUMP key

        # Hurt/Hitbox Setup:
        #   Hurt/Hitbox Lists:
        self.player_hurtboxes = arcade.SpriteList()
        self.player_hitboxes = arcade.SpriteList()
        #   Hurt/Hitbox Assignment:
        self.main_hurtbox = main_hurtbox
        self.player_hurtboxes.append(self.main_hurtbox)
        self.extended_hurtbox = extended_hurtbox
        self.player_hurtboxes.append(self.extended_hurtbox)
        self.hitbox = hitbox
        self.player_hitboxes.append(self.hitbox)

        if input_map == 0:
            self.keymap = FULL_KEYMAP
        elif input_map == 1:
            self.keymap = SPLIT_KEYMAP_L
        elif input_map == 2:
            self.keymap = SPLIT_KEYMAP_R
        """
        elif input_map == 3:
            self.keymap = GAMEPAD_KEYMAP
        """
        self.JUMP = self.keymap['JUMP']
        self.SPRINT = self.keymap['SPRINT']
        self.DAFOE = self.keymap['DAFOE']
        self.CROUCH = self.keymap['CROUCH']
        self.LEFT = self.keymap['LEFT']
        self.RIGHT = self.keymap['RIGHT']
        self.PUNCH = self.keymap['PUNCH']
        self.KICK = self.keymap['KICK']

    def update(self, floors):
        """
        Update func:
            - Updates sprite lists
            - Accounts for Jump and Sprint behavior (key presses that affect longer than a single frame)
            - Accounts for movement/ Updates position
            -
        """
        # Sprite list updates
        self.player_hurtboxes.update()
        self.player_hitboxes.update()

        # Jump Behavior
        self.grav_cycle(floors)
        if self.jumping & self.jump_or_nah(floors) & (not self.mid_jump):  # IF jumping, on floor, and not mid-jump
            self.change_y_J += cn.PLAYER_JUMP_SPEED
            self.change_x_J = 0
        elif self.jumping & (not (self.jump_or_nah(floors))):  # IF jumping, not on floor
            if self.neutral_jump:
                self.change_x_J = 0
            elif self.right_jump:
                self.change_x_J = 10
            elif self.left_jump:
                self.change_x_J = -10
            self.mid_jump = True
        elif self.jump_or_nah(floors) & self.jumping & self.mid_jump:  # IF on floor, jumping, and mid-jump
            self.jumping = False
            self.mid_jump = False
            if self.right_jump:
                self.right_jump = False
            if self.left_jump:
                self.left_jump = False
            if self.neutral_jump:
                self.neutral_jump = False
            self.change_y_J = 0

        # Sprint Behavior:
        if self.jump_or_nah(floors):  # IF on floor
            if self.sprinting:
                if not self.mid_dash:
                    self.mid_dash = True
                    self.state_counter = cn.PLAYER_DASH_TICS
                    self.change_y_S = 0
                    if self.right_dash:
                        self.change_x_S = 0.5*cn.PLAYER_SPEED
                    elif self.left_dash:
                        self.change_x_S = 0.5*cn.PLAYER_SPEED
                    else:
                        self.mid_dash = False
                        self.sprinting = False
                        self.left_dash = False
                        self.right_dash = False
                        self.state_counter = 0

                else:
                    self.change_y_S = 0
                    if self.left_dash:
                        if self.state_counter > 50:
                            self.change_x_S = -0.5*cn.PLAYER_SPEED
                        elif self.state_counter > 35:
                            self.change_x_S = -5*cn.PLAYER_SPEED
                        elif self.state_counter > 20:
                            self.change_x_S = -3*cn.PLAYER_SPEED
                        else:
                            self.change_x_S = -0.2*cn.PLAYER_SPEED

                        self.state_counter -= 1
                        if self.state_counter <= 0:
                            self.mid_dash = False
                            self.sprinting = False
                            self.left_dash = False
                            self.right_dash = False
                            self.state_counter = 0

                    elif self.right_dash:
                        if self.state_counter > 90:
                            self.change_x_S = 0.5*cn.PLAYER_SPEED
                        elif self.state_counter > 50:
                            self.change_x_S = 5*cn.PLAYER_SPEED
                        elif self.state_counter > 30:
                            self.change_x_S = 3*cn.PLAYER_SPEED
                        else:
                            self.change_x_S = 0.2*cn.PLAYER_SPEED

                        self.state_counter -= 1
                        if self.state_counter <= 0:
                            self.mid_dash = False
                            self.sprinting = False
                            self.left_dash = False
                            self.right_dash = False
                            self.state_counter = 0
                    else:
                        self.mid_dash = False
                        self.sprinting = False
                        self.left_dash = False
                        self.right_dash = False

        # Movement tracking
        if self.jumping & (not (self.jump_or_nah(floors))):
            self.change_x = self.change_x_J
        elif self.sprinting:
            self.change_x = self.change_x_S
            self.change_y = self.change_y_S
        else:
            self.change_x = self.change_x_L + self.change_x_R
        self.change_y = self.change_y_J

        # Update position
        if self.stun == 0:
            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.dafoeing:
                if self.height + 3 < int(cn.SPRITE_PLAYER_HEIGHT*1.2):
                    self.height += 3
                elif self.height - 3 > int(cn.SPRITE_PLAYER_HEIGHT*1.2):
                    self.height -= 3
                else:
                    self.height = int(cn.SPRITE_PLAYER_HEIGHT*1.2)
                if self.width + 3 < int(cn.SPRITE_PLAYER_WIDTH * 1.1):
                    self.width += 3
                elif self.width - 3 > int(cn.SPRITE_PLAYER_WIDTH * 1.1):
                    self.width -= 3
                else:
                    self.width = int(cn.SPRITE_PLAYER_WIDTH * 1.1)
            elif self.crouching:
                if self.height + 5 < int(cn.SPRITE_PLAYER_HEIGHT/1.3):
                    self.height += 5
                elif self.height - 5 > int(cn.SPRITE_PLAYER_HEIGHT/1.3):
                    self.height -= 5
                else:
                    self.height = int(cn.SPRITE_PLAYER_HEIGHT/1.3)
                if self.width + 5 < int(cn.SPRITE_PLAYER_WIDTH*1.7):
                    self.width += 5
                elif self.width - 5 > int(cn.SPRITE_PLAYER_WIDTH*1.7):
                    self.width -= 5
                else:
                    self.width = int(cn.SPRITE_PLAYER_WIDTH*1.7)
            else:
                if self.height+5 < cn.SPRITE_PLAYER_HEIGHT:
                    self.height += 5
                elif self.height-5 > cn.SPRITE_PLAYER_HEIGHT:
                    self.height -= 5
                else: self.height = cn.SPRITE_PLAYER_HEIGHT
                if self.width+5 < cn.SPRITE_PLAYER_WIDTH:
                    self.width += 5
                elif self.width-5 > cn.SPRITE_PLAYER_WIDTH:
                    self.width -= 5
                else:
                    self.width = cn.SPRITE_PLAYER_WIDTH

        # Main body tracking
        self.player_hurtboxes[0].center_y = self.center_y
        self.player_hurtboxes[0].center_x = self.center_x
        self.player_hurtboxes[0].height = self.height
        self.player_hurtboxes[0].width = self.width

        # Using Extended Hitbox to track direction player is facing
        self.player_hurtboxes[1].center_y = self.center_y
        if self.right:
            self.player_hurtboxes[1].center_x = int(self.center_x - (1.5*cn.SPRITE_PLAYER_WIDTH / 6))
        else:
            self.player_hurtboxes[1].center_x = int(self.center_x + (1.5*cn.SPRITE_PLAYER_WIDTH / 6))

    def hit_cycle(self):  # this one's gonna be a solid brick of code. no joke. true pain.
        """
        Moves the hitbox in accordance with attack commands
        """
        if self.stun == 0:
            if self.state_counter != 0:
                # THIS WILL TRACK PLAYER MOVES TO 'ANIMATE' AND MOVE HITBOXES

                # EXAMPLE HIT:
                # self.player_hitbox.center_x = self.player_hurtbox.center_x - 6*self.state_counter
                # self.player_hitbox.center_y = self.player_hurtbox.center_y + self.state_counter
                # self.player_hitbox.width = 15*self.state_counter
                # self.player_hitbox.height = 7*self.state_counter
                screen_side_mod = 0
                if self.right:
                    screen_side_mod = 1
                else:
                    screen_side_mod = -1
                if self.state == State.l_punch:  # LIGHT PUNCH
                    # START-UP:
                    if self.state_counter > 5*int(cn.L_HIT_LENGTH)/6:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                    # ACTIVE:
                    elif self.state_counter > int(cn.L_HIT_LENGTH)/3:
                        # Player Hitbox Setup:
                        self.player_hitboxes[0].center_x = self.center_x - (8*(cn.L_HIT_LENGTH -
                                                                            self.state_counter)) * screen_side_mod
                        self.player_hitboxes[0].center_y = self.center_y + (cn.L_HIT_LENGTH -
                                                                            self.state_counter)
                        self.player_hitboxes[0].width = 7*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].height = 3*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].render_hitbox = True
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                if self.state == State.h_punch:  # HEAVY PUNCH
                    # START-UP:
                    if self.state_counter > 5*int(cn.H_HIT_LENGTH)/6:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                    # ACTIVE:
                    elif self.state_counter > int(cn.H_HIT_LENGTH)/3:
                        # Player Hitbox Setup:
                        self.player_hitboxes[0].center_x = self.center_x - (4*(cn.H_HIT_LENGTH -
                                                                            self.state_counter)) * screen_side_mod
                        self.player_hitboxes[0].center_y = (1.1 * self.center_y) - (cn.L_HIT_LENGTH - self.state_counter)
                        self.player_hitboxes[0].width = 6*(cn.H_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].height = 2*(cn.H_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].render_hitbox = True
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                if self.state == State.aa_punch:  # ANTI-AIR PUNCH (INVULNERABLE WHEN THE BOX IS OUT?)
                    # START-UP:
                    if self.state_counter > 1*int(cn.L_HIT_LENGTH)/2:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                    # ACTIVE:
                    elif self.state_counter > 1*int(cn.L_HIT_LENGTH)/4:
                        # Player Hitbox Setup:
                        self.player_hitboxes[0].center_x = self.center_x - (4*(cn.L_HIT_LENGTH -
                                                                            self.state_counter)) * screen_side_mod
                        self.player_hitboxes[0].center_y = self.center_y + (cn.L_HIT_LENGTH -
                                                                            self.state_counter)
                        self.player_hitboxes[0].width = 6*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].height = 5*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].render_hitbox = True
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                if self.state == State.lp_punch:  # LOW-PROFILE PUNCH
                    # START-UP:
                    if self.state_counter > 5*int(cn.L_HIT_LENGTH)/6:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                    # ACTIVE:
                    elif self.state_counter > int(cn.L_HIT_LENGTH)/3:
                        # Player Hitbox Setup:
                        self.player_hitboxes[0].center_x = self.center_x - ((self.width/2 + ((cn.L_HIT_LENGTH -
                                                                            self.state_counter))) * screen_side_mod)
                        self.player_hitboxes[0].center_y = self.center_y + (4*(cn.L_HIT_LENGTH -
                                                                            self.state_counter))
                        self.player_hitboxes[0].width = 4*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].height = 9*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].render_hitbox = True
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                if self.state == State.l_kick:  # LIGHT KICK
                    # START-UP:
                    if self.state_counter > 2*int(cn.L_HIT_LENGTH)/3:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                    # ACTIVE:
                    elif self.state_counter > int(cn.L_HIT_LENGTH)/3:
                        # Player Hitbox Setup:
                        self.player_hitboxes[0].center_x = self.center_x - (8*(cn.L_HIT_LENGTH -
                                                                            self.state_counter)) * screen_side_mod
                        self.player_hitboxes[0].center_y = self.center_y - 4*self.state_counter
                        self.player_hitboxes[0].width = 10*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].height = 4*(cn.L_HIT_LENGTH-self.state_counter)
                        self.player_hitboxes[0].render_hitbox = True
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.player_hitboxes[0].center_x = 0
                        self.player_hitboxes[0].center_y = 0
                        self.player_hitboxes[0].width = 1
                        self.player_hitboxes[0].height = 1
                        self.player_hitboxes[0].render_hitbox = False
                self.state_counter -= 1  # Increment cycle
            elif self.state_counter == 0 | self.state_counter < 0:
                self.state_counter = 0  # Reset cycle so it can be started again
                self.state = State.idle
        else:
            self.player_hitboxes[0].render_hitbox = False
            self.state = State.idle
            self.player_hitboxes[0].center_x = 0
            self.player_hitboxes[0].center_y = 0
            self.player_hitboxes[0].width = 1
            self.player_hitboxes[0].height = 1
            self.player_hitboxes[0].render_hitbox = False

    def hurt_cycle(self):  # this one's gonna be a solid brick of code. no joke. true pain.
        """
        Moves the hurtbox in accordance with attack commands
        """
        if self.stun == 0:
            if self.state_counter != 0:
                # THIS WILL TRACK PLAYER MOVES TO 'ANIMATE' AND MOVE HURTBOXES
                screen_side_mod = 0
                if self.right:
                    screen_side_mod = 1
                else:
                    screen_side_mod = -1
                if self.state == State.l_punch:  # LIGHT PUNCH
                    # START-UP:
                    if self.state_counter > 2*int(cn.L_HIT_LENGTH)/3:
                        # Player Hurtbox Setup:
                        self.width = cn.SPRITE_PLAYER_WIDTH + (cn.L_HIT_LENGTH - self.state_counter) * 3
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_x -= 5 * screen_side_mod
                    # ACTIVE:
                    elif self.state_counter > int(cn.L_HIT_LENGTH)/3:
                        # Player Hurtbox Setup:
                        self.width = cn.SPRITE_PLAYER_WIDTH + (cn.L_HIT_LENGTH-self.state_counter)*3
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_x -= 5 * screen_side_mod
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.width = cn.SPRITE_PLAYER_WIDTH
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_x += 10 * screen_side_mod
                if self.state == State.aa_punch:
                    pass
                if self.state == State.lp_punch:  # APPARENTLY THIS SHOULD ACTUALLY BE THE ANTI-AIR??
                    pass
                if self.state == State.h_punch:
                    # START-UP:
                    if self.state_counter > 3 * int(cn.H_HIT_LENGTH) / 5:
                        # Player Hurtbox Setup:
                        self.width = cn.SPRITE_PLAYER_WIDTH + (cn.H_HIT_LENGTH - self.state_counter)
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_x += 5 * screen_side_mod
                    # ACTIVE:
                    elif self.state_counter > int(cn.H_HIT_LENGTH) / 5:
                        # Player Hurtbox Setup:
                        self.width = cn.SPRITE_PLAYER_WIDTH + (cn.H_HIT_LENGTH - self.state_counter)
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_x -= 5 * screen_side_mod
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.width = cn.SPRITE_PLAYER_WIDTH
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_x -= 10 * screen_side_mod
                if self.state == State.l_kick:
                    pre_center_y = self.center_y
                    # START-UP:
                    if self.state_counter > 2*int(cn.L_HIT_LENGTH)/3:
                        # Player Hurtbox Setup:
                        self.width = cn.SPRITE_PLAYER_WIDTH + (cn.L_HIT_LENGTH - self.state_counter) * 3
                        self.height = cn.SPRITE_PLAYER_HEIGHT - (cn.L_HIT_LENGTH - self.state_counter) * 6
                        self.center_y += (cn.L_HIT_LENGTH - self.state_counter) * 6
                        print(self.center_y)
                    # ACTIVE:
                    elif self.state_counter > int(cn.L_HIT_LENGTH)/3:
                        # Player Hurtbox Setup:
                        self.width = cn.SPRITE_PLAYER_WIDTH + (cn.L_HIT_LENGTH - self.state_counter) * 3
                        self.height = cn.SPRITE_PLAYER_HEIGHT - (cn.L_HIT_LENGTH - self.state_counter) * 4
                        self.center_y += int((cn.L_HIT_LENGTH - self.state_counter)*4)
                        print(self.center_y)
                    # RECOVERY:
                    elif self.state_counter > 0:
                        self.width = cn.SPRITE_PLAYER_WIDTH
                        self.height = cn.SPRITE_PLAYER_HEIGHT
                        self.center_y = pre_center_y
                        print(self.center_y)
                    self.center_y = pre_center_y
                if self.state == State.aa_kick:
                    pass
                if self.state == State.lp_kick:
                    pass
                if self.state == State.h_kick:
                    pass
                self.state_counter -= 1  # Increment cycle
            elif self.state_counter == 0 | self.state_counter < 0:
                self.state_counter = 0  # Reset cycle so it can be started again
                self.state = State.idle
        else:
            self.player_hitboxes[0].render_hitbox = False
            self.state = State.idle

    def grav_cycle(self, floors):
        """
        If you aren't on the ground, apply gravity (fall)
        """
        if not (self.jump_or_nah(floors)):
            self.change_y_J -= cn.GRAVITY
        else:
            self.change_y_J = 0

    def jump_or_nah(self, floors):
        """
        Checks if the player is on the ground or not (touching floors)
        """
        hit_list_no_move = 0
        for hurtbox in self.player_hurtboxes:
            if len(floors) > 1:
                if check_for_collision_with_lists(hurtbox, floors):
                    hit_list_no_move += 1
            elif len(floors) == 1:
                if check_for_collision(hurtbox, floors[0]):
                    hit_list_no_move += 1
        if hit_list_no_move:
            #print("IN GROUND")
            self.center_y += cn.GRAVITY
            return True
        else:
            for floor in floors:
                height_diff = (self.center_y-(self.height/2))-(floor.center_y+(floor.height/2))
                # width_diff = ??? (calc at a later date)
                if height_diff < 1.5:
                    #print("ON GROUND: Diff of "+str(height_diff))
                    return True
                else:
                    #print("OFF GROUND: Diff of "+str(height_diff))
                    #print("player y: " + str(self.center_y) + ", player height: " + str(self.height))
                    #print("floor y: " + str(floor.center_y) + ", floor height: " + str(floor.height))
                    return False

    def player_key_press(self, key, key_modifiers):
        """
        Input press affects for player (in stage)
        """
        if self.state_counter == 0:
            # USE EITHER STATE.HIT OR STUN-LOCK TO KEEP TRACK OF WHEN THEY CAN'T START NEW MOVES
            if not self.state == State.hit:
                if not (self.keymap is None):
                    if self.SPRINT == key:
                        if self.right & self.lefting:
                            print("LEFTING SPRINTING")
                            self.sprinting = True
                            self.left_dash = True
                            #self.change_x_L -= cn.PLAYER_SPEED
                        elif (not self.right) & self.righting:
                            print("RIGHTING SPRINTING")
                            self.sprinting = True
                            self.right_dash = True
                            #self.change_x_R += cn.PLAYER_SPEED
                        else:
                            print("DIR INPUT NEEDED BEFORE SPRINT PRESSED")
                            self.sprinting = False
                            self.left_dash = False
                            self.right_dash = False
                    else:
                        match key:
                            case self.JUMP:
                                print("JUMPING")
                                self.state = State.idle
                                if self.lefting:
                                    self.left_jump = True
                                elif self.righting:
                                    self.right_jump = True
                                else:
                                    self.neutral_jump = True
                                self.jumping = True
                            case self.DAFOE:
                                print("DAFOEING")
                                self.dafoeing = True
                                # LOOK UP BEHAVIOR GOES HERE
                            case self.CROUCH:
                                print("CROUCHING")
                                self.crouching = True
                                # CROUCH BEHAVIOR GOES HERE
                            case self.LEFT:
                                print("LEFTING")
                                self.lefting = True
                                self.righting = False
                                # MOVE LEFT BEHAVIOR GOES HERE
                                if not self.right:
                                    self.state = State.blocking
                                    self.blocking = True
                                    print("BLOCKING")
                                    self.change_x_L -= int(3 * cn.PLAYER_SPEED / 5)
                                else:
                                    self.change_x_L -= cn.PLAYER_SPEED
                            case self.RIGHT:
                                print("RIGHTING")
                                self.righting = True
                                self.lefting = False
                                # MOVE RIGHT BEHAVIOR GOES HERE
                                if self.right:
                                    self.state = State.blocking
                                    self.blocking = True
                                    print("BLOCKING")
                                    self.change_x_R += int(3 * cn.PLAYER_SPEED / 5)
                                else:
                                    self.change_x_R += cn.PLAYER_SPEED
                            case self.PUNCH:
                                if self.stun == 0:
                                    print("PUNCH")
                                    self.punching = True
                                    if ((self.righting & (not self.right)) |
                                            (self.lefting & self.right)):
                                        print("light punch")
                                        self.state = State.l_punch  # LIGHT PUNCH
                                        self.state_counter = cn.L_HIT_LENGTH
                                    elif self.dafoeing:
                                        print("anti-air punch")
                                        self.state = State.aa_punch  # ANTI-AIR PUNCH
                                        self.state_counter = cn.S_HIT_LENGTH
                                    elif self.crouching:
                                        print("low-profile punch")
                                        self.state = State.lp_punch  # LOW-PROFILE PUNCH
                                        self.state_counter = cn.L_HIT_LENGTH
                                    else:
                                        print("heavy punch")
                                        self.state = State.h_punch  # HEAVY PUNCH
                                        self.state_counter = cn.H_HIT_LENGTH
                            case self.KICK:
                                if self.stun == 0:
                                    print("KICKING")
                                    self.kicking = True
                                    if ((self.righting & (not self.right)) |
                                            (self.lefting & self.right)):
                                        print("light kick")
                                        self.state = State.l_kick  # LIGHT KICK
                                        self.state_counter = cn.L_HIT_LENGTH
                                    elif self.dafoeing:
                                        print("anti-air kick")
                                        self.state = State.aa_kick  # ANTI-AIR KICK
                                        self.state_counter = cn.S_HIT_LENGTH
                                    elif self.crouching:
                                        print("low-profile kick")
                                        self.state = State.lp_kick  # LOW-PROFILE KICK
                                        self.state_counter = cn.S_HIT_LENGTH
                                    else:
                                        print("heavy kick")
                                        self.state = State.h_kick  # HEAVY KICK
                                        self.state_counter = cn.H_HIT_LENGTH

    def player_key_release(self, key, key_modifiers):
        """
        Input release affects for player (in stage)
        """
        match key:
            case self.SPRINT:
                print("NO SPRINTING")
            case self.JUMP:
                print("NO JUMPING")
            case self.DAFOE:
                print("NO DAFOEING")
                self.dafoeing = False
            case self.CROUCH:
                print("NO CROUCHING")
                self.crouching = False
            case self.LEFT:
                print("NO LEFTING")
                self.lefting = False
                self.change_x_L = 0
                if self.state == State.blocking:
                    self.state = State.idle
                    self.blocking = False
                    print("NO BLOCKING")
            case self.RIGHT:
                print("NO RIGHTING")
                self.righting = False
                self.change_x_R = 0
                if self.state == State.blocking:
                    self.state = State.idle
                    self.blocking = False
                    print("NO BLOCKING")
            case self.PUNCH:
                print("NO PUNCHING")
                self.punching = False
            case self.KICK:
                print("NO KICKING")
                self.kicking = False

    def block_check(self, hit_damage):  # RETURN FALSE IF BLOCK IS INTACT, TRUE IF BROKEN
        """
        Checks the block value when hit, if there is a block value subtract damage from that,
            if not then take damage value from health.
        """
        if self.blocking:
            p_block_health = self.block_health  # prev block health
            c_block_health = self.block_health-hit_damage  # new 'current' block health
            if c_block_health > 0:
                self.block_health -= hit_damage
                print("BLOCK HEALTH = "+str(self.block_health))
                return False  # Block is intact
            elif (p_block_health > 0) & (c_block_health <= 0):
                self.block_health = 0
                print("BLOCK HEALTH = "+str(self.block_health))
                return True  # BLOCK IS BROKEN, STUN!
            elif p_block_health == 0:
                self.health -= hit_damage
                print("BLOCK HEALTH = "+str(self.block_health))
                return True  # Block is already broken
        else:
            self.health -= hit_damage  # Not blocking
            print("BLOCK HEALTH = " + str(self.block_health))
            return True
