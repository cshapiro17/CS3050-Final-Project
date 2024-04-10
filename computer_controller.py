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

    def attack(self, direction):
        if direction == 0:
            # ATTACK FORWARD
            pass
        elif direction < 0:
            # ATTACK DOWN
            pass
        else:
            # ATTACK UP
            pass

    def retreat(self):
        pass

    def advance(self):
        pass
