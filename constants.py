from enum import IntEnum
import arcade


# Display-based Constants:
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

SPRITE_PLAYER_WIDTH = int(SCREEN_WIDTH/13)
SPRITE_PLAYER_HEIGHT = int(1*SCREEN_HEIGHT/3)
MAX_MATCH_TIME = 60
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 30

MAX_MATCH_TIME = 60.0

COUNTDOWN_TIME = 4.0


# Stage UI Constants:
PORTRAIT_DIMENSIONS = [75, 75]
HEALTH_BAR_PIXEL_CONSTANT = 4.5
BLOCK_BAR_PIXEL_CONSTANT = 5
SUPER_BAR_PIXEL_CONSTANT = 1

# Balance-based Constants:
PLAYER_HEALTH = 100
FULL_BLOCK = int(PLAYER_HEALTH/2)
PLAYER_SPEED = 7
PLAYER_JUMP_SPEED = 30
PLAYER_DASH_TICS = 60
GRAVITY = 1
H_HIT_LENGTH = 60  # Heavy Move Hit Length
L_HIT_LENGTH = 30  # Light Move Hit Length
S_HIT_LENGTH = 50  # Special Move Hit Length (Anti-air and Low-profile)
H_STUN_TIME = 30  # Heavy Move Stun Time
L_STUN_TIME = 15  # Light Move Stun Time
S_STUN_TIME = 25  # Special Move Stun Time (Anti-air and Low-profile)
H_P_HIT_DAMAGE = 25  # Heavy Punch Damage
L_P_HIT_DAMAGE = 10  # Light Punch Damage
S_P_HIT_DAMAGE = 20  # Special Punch Damage (Anti-air and Low-profile)
H_K_HIT_DAMAGE = 25  # Heavy Kick Damage
L_K_HIT_DAMAGE = 10  # Light Kick Damage
S_K_HIT_DAMAGE = 20  # Special Kick Damage (Anti-air and Low-profile)

# Computer Take the Wheel and Become True Evil
#   Constants to drive the dummy controller
SIX_FEET = 100          # ATTACK RANGE
NAPOLEONIC_ANGER = 50   # HEIGHT DRIVER FOR ATTACK RANGE (HELPS CHOOSE ATTACK)
LITERALLY_GHANDI = 250  # HELPS GENERATE AGGRESSIVENESS OF CONTROLLER
GO_TO_THERAPY = 750       # HELPS GENERATE AGGRESSIVENESS OF CONTROLLER
BOILING_BLOOD = 500      # DEFAULT VALUE FOR ATTACK DRIVER
ENTER_THE_FROZONE = 250  # DEFAULT VALUE FOR RETREAT DRIVER


# Enums:
class State(IntEnum):
    idle = 0
    blocking = 1
    hit = 2
    h_punch = 3  # _-q: heavy punch
    l_punch = 4  # d/a(side-dependent_-q: light punch (poke)
    aa_punch = 5  # w-q: anti-air punch
    lp_punch = 6  # s-q: low-profile punch
    h_kick = 7  # _-e: heavy kick
    l_kick = 8  # d/a(side-dependent_-e: light kick (poke)
    aa_kick = 9  # w-e: anti-air kick
    lp_kick = 10  # s-e: low-profile kick
    # super_hit = 11  # f: super move
