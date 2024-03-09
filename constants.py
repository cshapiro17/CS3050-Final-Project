from enum import IntEnum


# Display-based Constants:
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
SPRITE_PLAYER_WIDTH = int(SCREEN_WIDTH/20)
SPRITE_PLAYER_HEIGHT = int(1*SCREEN_HEIGHT/5)


# Balance-based Constants:
PLAYER_HEALTH = 100
PLAYER_SPEED = 7
H_HIT_LENGTH = 60  # Heavy Move Hit Length
L_HIT_LENGTH = 30  # Light Move Hit Length
S_HIT_LENGTH = 50  # Special Move Hit Length (Anti-air and Low-profile)
H_STUN_TIME = 35  # Heavy Move Stun Time
L_STUN_TIME = 15  # Light Move Stun Time
S_STUN_TIME = 25  # Special Move Stun Time (Anti-air and Low-profile)
H_P_HIT_DAMAGE = 25  # Heavy Punch Damage
L_P_HIT_DAMAGE = 10  # Light Punch Damage
S_P_HIT_DAMAGE = 20  # Special Punch Damage (Anti-air and Low-profile)
H_K_HIT_DAMAGE = 25  # Heavy Kick Damage
L_K_HIT_DAMAGE = 10  # Light Kick Damage
S_K_HIT_DAMAGE = 20  # Special Kick Damage (Anti-air and Low-profile)


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
