# CS3050-Final-Project

## Input Schema:
### 'Implemented' Keys:
The control scheme is listed below. There are three different schemes, we have the vs. Computer scheme, and the left and right schemes for vs. Player. There are shared keys between both listed below.
- **Look up, move left, move right, crouch:**
    - *PVP Right and PVC: W-A-S-D Keys*
    - *PVP Left: I-J-K-L*
    - **Blocking:** To block, walk backwards (away from enemy)
      - Blocking health-bar beneath regular player health-bar, recharges over time
    - **Dash/ Sprint:**
      - *PVP Right and PVC: Shift Key*
      - *PVP Left: Space*
    - **Jump:**
      - *PVP Right: Left Alt*
      - *PVP Left: Right Alt*
      - *PVC: Space* 
- **Punch Controls:** Basic Attack registers as a heavy punch.
  - *PVP Right: Z*
  - *PVP Left: M*
  - *PVC: J*
  - **Command Normals:**
    - **Forward (Towards Enemy)** and **Punch:** light punch (poke)
      - A simple and fast basic attack.
    - **Look up** and **Punch**: Short Punch
      - A high damage attack, but long startup and short range (easy to punish).
    - **Crouch** and **Punch**: Anti-air Punch
      - Jump punisher, attacks into the air.

### Non-implemented/ Idea Keys:
- X (or ,): kick (longer range, (heavier damage?) than punch)
    - _-X: heavy kick
      - *Counter Low-Profile stuff (overhead smash-down)*
    - d/a(_side-dependent_-X: light kick (poke) **BOXES IMPLEMENTED**
      - *Good range, fast start-up, but easily punishable (long recovery)*
    - w-X: anti-air kick
      - *Good against punches (Kick up, can intersect arm hitboxes?)*
    - s-X: low-profile kick
      - *say goodbye to your toes*
- C Key (or .): Super Move



