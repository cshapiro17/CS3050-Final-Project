import arcade
import player as p
import constants as cn
import random as rn


class Controller(object):
    def __init__(self,
                 marionette: p.Player,
                 the_actual_devil: p.Player):
        """
        CONTAINS ALL SET-UP AND VARIABLE DECLARATION FOR THE PLAYER CLASS
        """
        # Start-up Stats:
        self.puppet = marionette
        self.opponent = the_actual_devil

        self.social_distancing = None
        self.height_diff = None

        self.anger_management = None
        self.boiling_point = None
        self.freezing_point = None

    def setup(self):
        self.boiling_point = cn.BOILING_BLOOD
        self.freezing_point = cn.ENTER_THE_FROZONE
        if self.puppet.right:
            self.social_distancing = self.puppet.center_x - self.opponent.center_x
        else:
            self.social_distancing = self.opponent.center_x - self.puppet.center_x
        self.height_diff = self.puppet.center_y - self.opponent.center_y
        self.anger_management = rn.randint(cn.LITERALLY_GHANDI, cn.GO_TO_THERAPY)

    def update(self):
        if (self.puppet.state_counter <= 0) & (self.puppet.stun <= 0):  # If able:
            self.puppet.state_counter = 0
            self.puppet.stun = 0
            if self.social_distancing > cn.SIX_FEET:
                if self.anger_management > self.freezing_point:  # Decrease freezing_point when hit
                    self.freezing_point += 1
                    self.retreat()
                else:
                    self.boiling_point += 1
                    self.advance()
            else:
                # In coughing distance, make a decision
                if self.anger_management < self.boiling_point:
                    self.boiling_point -= 2
                    if abs(self.height_diff) < cn.NAPOLEONIC_ANGER:  # Height diff isn't significant
                        self.attack(0)
                        pass
                    if (self.height_diff < 0) & (abs(self.height_diff) > cn.NAPOLEONIC_ANGER):  # Dummy is shorter,
                        # Napoleon's Wrath has been Incurred
                        self.attack(1)
                        pass
                    else:
                        self.attack(-1)
                        pass
                    pass
                elif self.anger_management > self.freezing_point:  # Decrease freezing_point when hit
                    self.freezing_point += 1
                    self.retreat()
                else:
                    self.boiling_point += 1
                    self.advance()

    def whermst(self):
        dir_mod = 0
        if self.puppet.right:
            dir_mod = 1
        else:
            dir_mod = -1
        return dir_mod

    def reset_states(self):
        self.puppet.jumping = False

        self.puppet.sprinting = False

        self.puppet.lefting = False
        self.puppet.righting = False
        self.puppet.blocking = False

    def attack(self, direction):
        pos = self.whermst()
        if direction > 0:
            # ATTACK UP
            self.puppet.state = p.State.lp_punch  # LOW-PROFILE PUNCH
            self.puppet.state_counter = cn.L_HIT_LENGTH
        else:
            # ATTACK FORWARD
            choice = rn.randint(0, 100)
            if choice < 10:  # Special
                self.puppet.state = p.State.aa_punch  # ANTI-AIR PUNCH
                self.puppet.state_counter = cn.S_HIT_LENGTH
            elif choice < 35:  # Heavy
                self.puppet.state = p.State.h_punch  # HEAVY PUNCH
                self.puppet.state_counter = cn.H_HIT_LENGTH
            else:  # Poke
                self.puppet.state = p.State.l_punch  # LIGHT PUNCH
                self.puppet.state_counter = cn.L_HIT_LENGTH

    def retreat(self):
        meth = rn.randint(0, 100)
        if meth <= 2:
            # JUMP
            self.puppet.jumping = True
            if self.puppet.right:
                self.puppet.right_jump = True
            else:
                self.puppet.left_jump = True
        else:
            # WALK
            if self.puppet.right:
                self.puppet.lefting = True
                self.puppet.righting = False
                self.puppet.state = p.State.blocking
                self.puppet.blocking = True
                self.puppet.change_x = -int(3 * cn.PLAYER_SPEED / 5)
            else:
                self.puppet.righting = True
                self.puppet.lefting = False
                self.puppet.state = p.State.blocking
                self.puppet.blocking = True
                self.puppet.change_x = int(3 * cn.PLAYER_SPEED / 5)

    def advance(self):
        meth = rn.randint(0, 100)
        if meth <= 1:
            # DASH
            self.puppet.sprinting = True
            if self.puppet.right:
                self.puppet.left_dash = True
            else:
                self.puppet.right_dash = True
        elif meth <= 3:
            # JUMP
            self.puppet.jumping = True
            if self.puppet.right:
                self.puppet.left_jump = True
            else:
                self.puppet.right_jump = True
        else:
            # WALK
            if self.puppet.right:
                self.puppet.lefting = True
                self.puppet.righting = False
                self.puppet.change_x = -cn.PLAYER_SPEED
            else:
                self.puppet.righting = True
                self.puppet.lefting = False
                self.puppet.change_x = cn.PLAYER_SPEED
