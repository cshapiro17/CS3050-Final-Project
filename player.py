import arcade
from arcade import check_for_collision_with_lists, check_for_collision

import constants as cn
from constants import State

KEYMAP = dict(
    JUMP=arcade.key.SPACE,
    SPRINT=arcade.key.LSHIFT,
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
        self.health = cn.PLAYER_HEALTH               # UI will grab these in stage for bars
        self.block_health = int(cn.PLAYER_HEALTH/2)  # UI will grab these in stage for bars
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
        self.sprinting = False

        self.left_jump = False
        self.right_jump = False
        self.neutral_jump = False

        self.mid_jump = False
        # Move Inputs accel_vals accounting:
        self.change_x_L = 0  # The change_x value taken from the LEFT key
        self.change_x_R = 0  # The change_x value taken from the RIGHT key
        self.change_x_J = 0  # The change_x value taken from the JUMP key
        self.change_y_J = 0  # The change_y value taken from the JUMP key

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
            self.SPRINT = self.keymap['SPRINT']
            self.DAFOE = self.keymap['DAFOE']
            self.CROUCH = self.keymap['CROUCH']
            self.LEFT = self.keymap['LEFT']
            self.RIGHT = self.keymap['RIGHT']
            self.PUNCH = self.keymap['PUNCH']
            self.KICK = self.keymap['KICK']
        else:
            self.keymap = None

    def update(self, floors):  # TODO: MOVEMENT STUFF SHOULD GET ITS OWN DEF SO IT DOESN'T GET TOO CLUTTERED

        # Sprite list updates
        self.player_hurtboxes.update()
        self.player_hitboxes.update()

        # Jump Behavior
        self.grav_cycle(floors)
        if self.jumping & self.jump_or_nah(floors) & (not self.mid_jump):
            self.change_y_J += cn.PLAYER_JUMP_SPEED
            self.change_x_J = 0
        elif self.jumping & (not (self.jump_or_nah(floors))):
            if self.neutral_jump:
                self.change_x_J = 0
            elif self.right_jump:
                self.change_x_J = 10
            elif self.left_jump:
                self.change_x_J = -10
            self.mid_jump = True
        elif self.jump_or_nah(floors) & self.jumping & self.mid_jump:
            self.jumping = False
            self.mid_jump = False
            if self.right_jump:
                self.right_jump = False
            if self.left_jump:
                self.left_jump = False
            if self.neutral_jump:
                self.neutral_jump = False
            self.change_y_J = 0

        # Movement tracking
        if self.jumping & (not (self.jump_or_nah(floors))):
            self.change_x = self.change_x_J
        else:
            self.change_x = self.change_x_L + self.change_x_R
        self.change_y = self.change_y_J

        # Update position
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

    def grav_cycle(self, floors):
        if not (self.jump_or_nah(floors)):
            self.change_y_J -= cn.GRAVITY
        else:
            self.change_y_J = 0

    def jump_or_nah(self, floors):
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
                    print("OFF GROUND: Diff of "+str(height_diff))
                    print("player y: " + str(self.center_y) + ", player height: " + str(self.height))
                    print("floor y: " + str(floor.center_y) + ", floor height: " + str(floor.height))
                    return False
