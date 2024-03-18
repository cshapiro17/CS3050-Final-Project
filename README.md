# CS3050-Final-Project

## Input Schema:
### 'Implemented' Keys:
The control scheme is listed below. Italics are for ideas, bold is for actual implementations.
- W-A-S-D Keys: Classic controls (look_up-left-right-crouch) **INPUT IS LOGGED BUT NO MOVEMENT**
    - Blocking: To block, walk backwards (away from enemy)
      - *idea: blocking health-bar beneath regular player health-bar, recharges over time* 
    - Shift Key: Dash/ Sprint
    - Jump: Space to jump
- q: punch (faster startup and recovery than kick)
    - _-q: heavy punch
      - *Lunge affect?*
    - d/a(_side-dependent_-q: light punch (poke) **BOXES IMPLEMENTED**
      - *Simple and fast basic attack*
    - w-q: anti-air punch
      - *Jump punisher*
    - s-q: low-profile punch
      - *Counter Heavy/ Light Punch*
- e: kick (longer range, (heavier damage?) than punch)
    - _-q: heavy kick
      - *Counter Low-Profile stuff (overhead smash-down)*
    - d/a(_side-dependent_-q: light kick (poke) **BOXES IMPLEMENTED**
      - *Good range, fast start-up, but easily punishable (long recovery)*
    - w-q: anti-air kick
      - *Good against punches (Kick up, can intersect arm hitboxes?)*
    - s-q: low-profile kick
      - *say goodbye to your toes*

### Non-implemented/ Idea Keys:
- F Key: Super Move



