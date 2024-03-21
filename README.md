# CS3050-Final-Project
## TODO:
#### Group 1:
- ***Hit stun***
- ***Implement Hit-boxes for attack moves***
#### Group 2:
- ***UI (Menus (character select/ input schema select, in-game pause, timer)***
#### Extras:
- Super-moves/ Different characters
- Backgrounds (move with players)
- Gamepad???

## Input Schema:
### 'Implemented' Keys:
The control scheme is listed below. Italics are for ideas, bold is for actual implementations. Keep in mind control 
schemes are being updated, and this may not be accurate.
- W-A-S-D Keys (or I-J-K-L): Classic controls (look_up-left-right-crouch) **INPUT IS LOGGED BUT NO MOVEMENT**
    - Blocking: To block, walk backwards (away from enemy)
      - *idea: blocking health-bar beneath regular player health-bar, recharges over time* 
    - Shift Key (or Space): Dash/ Sprint
    - Left Alt (or Right Alt): Jump
- Z (or M): punch (faster startup and recovery than kick)
    - _-Z: heavy punch
      - *Lunge affect?*
    - d/a(_side-dependent_-Z: light punch (poke) **BOXES IMPLEMENTED**
      - *Simple and fast basic attack*
    - w-Z: anti-air punch
      - *Jump punisher*
    - s-Z: low-profile punch
      - *Counter Heavy/ Light Punch*
- X (or ,): kick (longer range, (heavier damage?) than punch)
    - _-X: heavy kick
      - *Counter Low-Profile stuff (overhead smash-down)*
    - d/a(_side-dependent_-X: light kick (poke) **BOXES IMPLEMENTED**
      - *Good range, fast start-up, but easily punishable (long recovery)*
    - w-X: anti-air kick
      - *Good against punches (Kick up, can intersect arm hitboxes?)*
    - s-X: low-profile kick
      - *say goodbye to your toes*

### Non-implemented/ Idea Keys:
- C Key (or .): Super Move



