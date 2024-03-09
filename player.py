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
        # Sprite list updates
        self.player_hurtboxes.update()
        self.player_hitboxes.update()
        # Main body tracking
        self.player_hurtboxes[0].center_y = self.center_y
        self.player_hurtboxes[0].center_x = self.center_x
        self.player_hurtboxes[0].change_y = self.change_y
        self.player_hurtboxes[0].change_x = self.change_x
        self.player_hurtboxes[0].height = self.height
        self.player_hurtboxes[0].width = self.width

    def hit_cycle(self):  # this one's gonna be a solid brick of code. no joke. true pain.
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
            #   THIS SECTION ~ONLY~ DOES HITBOXES
            screen_side_mod = 0
            if self.right:
                screen_side_mod = 1
            else:
                screen_side_mod = -1
            if self.state == State.l_punch:  # LIGHT PUNCH
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
                    self.player_hitboxes[0].center_y = self.center_y + (cn.L_HIT_LENGTH -
                                                                        self.state_counter)
                    self.player_hitboxes[0].width = 9*(cn.L_HIT_LENGTH-self.state_counter)
                    self.player_hitboxes[0].height = 4*(cn.L_HIT_LENGTH-self.state_counter)
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

    def hurt_cycle(self):  # this one's gonna be a solid brick of code. no joke. true pain.
        if self.state_counter != 0:
            # THIS WILL TRACK PLAYER MOVES TO 'ANIMATE' AND MOVE HURTBOXES
            # TODO: Get the old hurtbox testing code working with only one move (LIGHT PUNCH) before expanding it to
            #   more moves.
            # TODO: Work on the sprite movement. It should not be displayed in terms of state_counter, but rather in
            #   terms of SCREEN_WIDTH and SCREEN_HEIGHT (or self.sprite_hit.width and self.sprite_hit.height)
            #   WE ALSO HAVE 2 BUTTONS NOW, MIGHT AS WELL THROW THAT ALL IN HERE

            # TODO: Setup animations in chunks (START-UP, ACTIVE, AND RECOVERY FRAMES) based on state_counter
            #   THIS SECTION ~ONLY~ DOES HURTBOXES
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
            if self.state == State.lp_punch:
                pass
            if self.state == State.h_punch:
                pass
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
