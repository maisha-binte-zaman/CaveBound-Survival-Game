from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
# Controls:
# W - Move forward
# S - Move backward
# A - Turn left
# D - Turn right
# left,right,up,down arrow - change camera angle
# 1 - Eat Apple
# 2 - Eat Banana
# 3 - Eat Mango
# 4 - Use MediKit
# 5 - Use Ammo
# Craft : 6 - Medkit / 7 - Ammo Pack / 8 - Escape Kit 
# Right Mouse Button - Switch FPS/TPS camera
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
GRID_LENGTH = 1400
fovY = 90
PLAYER_COLLISION_RADIUS = 28
CAVE_COLLISION_MARGIN = 55

player_x = 0.0
player_y = -1160.0
player_z = 0.0
player_angle = 270.0
PLAYER_START_X = 0
PLAYER_START_Y = -1160
PLAYER_START_ANGLE = 270
shelter_exit_active = False
shelter_previous_x = 0.0
shelter_previous_y = 0.0
PLAYER_MAX_HEALTH = 100
player_health = PLAYER_MAX_HEALTH
player_dead = False
ENEMY_ATTACK_DAMAGE = 10
ENEMY_DAMAGE_FRAME = 15

player_move_speed = 25.0
player_turn_speed = 15.0
walk_phase = 0.0
walk_step = 0.65
first_person_mode = False

# Third-person camera settings
tps_distance = 500.0
tps_height = 500.0
tps_camera_angle = 270.0
tps_camera_rotate_speed = 8.0

# First-person camera settings
fps_eye_height = 145.0
fps_look_distance = 300.0
fps_camera_angle = 270.0
fps_camera_rotate_speed = 8.0
ROCK_COLLISIONS = [
    (-420, 80, 70),
    (390, 180, 80),
    (-600, 500, 60),
    (620, -100, 75),
    (-850, 760, 90),
    (820, 650, 70),
    (-720, -520, 65),
    (760, -650, 85)
]
PILLAR_COLLISIONS = [
    (-750, 350, 45),
    (720, 430, 45),
    (-900, -180, 45),
    (930, -260, 45)
]
BOUNDARY_TREE_COVER = [

    # FAR BOUNDARY
    (-1200, 1330, 30),
    (-1000, 1330, 30),
    (-800, 1330, 30),
    (-580, 1330, 30),
    (-350, 1330, 30),
    (-100, 1330, 30),
    (150, 1330, 30),
    (390, 1330, 30),
    (620, 1330, 30),
    (850, 1330, 30),
    (1080, 1330, 30),
    (1250, 1330, 30),

    # NEAR BOUNDARY
    (-1200, -1330, 30),
    (-970, -1330, 30),
    (-740, -1330, 30),
    (-510, -1330, 30),
    (-280, -1330, 30),
    (280, -1330, 30),
    (520, -1330, 30),
    (760, -1330, 30),
    (1000, -1330, 30),
    (1220, -1330, 30),

    # LEFT BOUNDARY
    (-1330, -1100, 30),
    (-1330, -850, 30),
    (-1330, -610, 30),
    (-1330, -370, 30),
    (-1330, -120, 30),
    (-1330, 150, 30),
    (-1330, 410, 30),
    (-1330, 680, 30),
    (-1330, 940, 30),
    (-1330, 1160, 30),

    # RIGHT BOUNDARY
    (1330, -1150, 30),
    (1330, -900, 30),
    (1330, -650, 30),
    (1330, -390, 30),
    (1330, -130, 30),
    (1330, 130, 30),
    (1330, 390, 30),
    (1330, 650, 30),
    (1330, 900, 30),
    (1330, 1160, 30),

    # SMALL INNER FAR TREES
    (-1120, 1295, 22),
    (-910, 1295, 22),
    (-700, 1295, 22),
    (-490, 1295, 22),
    (-275, 1295, 22),
    (-40, 1295, 22),
    (190, 1295, 22),
    (420, 1295, 22),
    (650, 1295, 22),
    (880, 1295, 22),
    (1110, 1295, 22),

    # SMALL INNER NEAR TREES
    (-1120, -1295, 22),
    (-890, -1295, 22),
    (-660, -1295, 22),
    (-430, -1295, 22),
    (-200, -1295, 22),
    (180, -1295, 22),
    (410, -1295, 22),
    (640, -1295, 22),
    (870, -1295, 22),
    (1100, -1295, 22),

    # SMALL INNER LEFT TREES
    (-1295, -1080, 22),
    (-1295, -830, 22),
    (-1295, -580, 22),
    (-1295, -330, 22),
    (-1295, -80, 22),
    (-1295, 180, 22),
    (-1295, 440, 22),
    (-1295, 700, 22),
    (-1295, 960, 22),
    (-1295, 1160, 22),

    # SMALL INNER RIGHT TREES
    (1295, -1100, 22),
    (1295, -850, 22),
    (1295, -600, 22),
    (1295, -350, 22),
    (1295, -100, 22),
    (1295, 160, 22),
    (1295, 420, 22),
    (1295, 680, 22),
    (1295, 940, 22),
    (1295, 1150, 22)
]
BUSH_COLLISIONS = [
    (-1050, 850, 50),
    (-820, 620, 40),
    (-520, 950, 48),

    (500, 900, 45),
    (850, 720, 50),
    (1080, 450, 40),

    (-1080, 100, 45),
    (-900, -350, 48),
    (-650, -850, 40),

    (1050, -100, 48),
    (900, -500, 45),
    (650, -900, 50),

    (-350, 650, 35),
    (420, 600, 40),

    (-480, -600, 45),
    (500, -700, 40)
]
CAMPFIRE_COLLISIONS = [
    (-950, 850, 55),
    (900, 900, 55),

    (-1000, 50, 55),
    (1000, 100, 55),

    (-850, -750, 55),
    (850, -800, 55)
]
LOG_COLLISIONS = [
    (-1000, 600, 75),
    (950, 650, 70),
    (-850, -700, 80),
    (900, -600, 65),
    (-400, 1050, 65)
]

STONE_COLLISIONS = [
    (-1100, 800, 22),
    (-900, 500, 18),
    (-700, 900, 20),

    (1050, 750, 20),
    (800, 500, 18),
    (650, 1000, 20),

    (-1050, -450, 20),
    (-750, -850, 18),
    (-450, -1050, 20),

    (1050, -400, 20),
    (800, -850, 22),
    (500, -1050, 18),

    (-300, 500, 16),
    (350, 450, 18),

    (-250, -500, 18),
    (300, -550, 16)
]

STUMP_COLLISIONS = [
    (-900, 250, 32),
    (850, -250, 30),
    (500, 850, 28)
]
SHELTER_CENTER_X = 0
SHELTER_CENTER_Y = -1160
SHELTER_WIDTH = 320
SHELTER_DEPTH = 240
SHELTER_WALL_THICKNESS = 20
SHELTER_DOOR_WIDTH = 120
TORCH_COLLISIONS = [
    (
        SHELTER_CENTER_X - 230,
        SHELTER_CENTER_Y + 20,
        30
    ),
    (
        SHELTER_CENTER_X + 230,
        SHELTER_CENTER_Y + 20,
        30
    )
]
ENEMY_DETECTION_DISTANCE = 320
ENEMY_CHASE_SPEED = 2.0
ENEMY_MOVE_SPEED = 1.2
ENEMY_BOUNDARY_MARGIN = 120
ENEMY_ATTACK_DISTANCE = 75
ENEMY_ATTACK_DURATION = 30
ENEMY_COLLISION_RADIUS = 25
ENEMY_FIELD_OF_VIEW = 120
ENEMY_FIELD_OF_VIEW_DISTANCE = ENEMY_DETECTION_DISTANCE
ENEMY_MEMORY_TIME = 180
ENEMY_SEARCH_DISTANCE = 35

ENEMY_START_DATA = [
    {"x": -700, "y": 700, "angle": 20},
    {"x": 650, "y": 750, "angle": 145},
    {"x": -750, "y": -300, "angle": 300},
    {"x": 800, "y": -400, "angle": 210},
    {"x": 300, "y": 500, "angle": 90}
]
enemies = [
    {
        "x": enemy["x"],
        "y": enemy["y"],
        "angle": enemy["angle"]
    }
    for enemy in ENEMY_START_DATA
]

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_floor():
    tile_size = 100
    x = -GRID_LENGTH
    row = 0

    while x < GRID_LENGTH:
        y = -GRID_LENGTH
        column = 0
        while y < GRID_LENGTH:
            palette = [
                (0.07, 0.22, 0.22),   # deep teal
                (0.08, 0.26, 0.25),   # muted teal
                (0.10, 0.30, 0.28),   # medium teal
                (0.07, 0.24, 0.26)    # blue teal
            ]
            color = palette[(row + column) % 4]
            glColor3f(color[0], color[1], color[2])

            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + tile_size, y, 0)
            glVertex3f(x + tile_size, y + tile_size, 0)
            glVertex3f(x, y + tile_size, 0)
            glEnd()

            y += tile_size
            column += 1
        x += tile_size
        row += 1

def draw_cave_boundaries():
    wall_height = 400
    wall_thickness = 35

    glColor3f(0.07, 0.25, 0.25) #left wall
    glPushMatrix()
    glTranslatef(-GRID_LENGTH, 0, wall_height / 2)
    glScalef(wall_thickness, GRID_LENGTH * 2, wall_height)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.08, 0.28, 0.27) #right wall
    glPushMatrix()
    glTranslatef(GRID_LENGTH, 0, wall_height / 2)
    glScalef(wall_thickness, GRID_LENGTH * 2, wall_height)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.10, 0.34, 0.31) #far wall
    glPushMatrix()
    glTranslatef(0, GRID_LENGTH, wall_height / 2)
    glScalef(GRID_LENGTH * 2, wall_thickness, wall_height)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.06, 0.21, 0.22) #near wall
    glPushMatrix()
    glTranslatef(0, -GRID_LENGTH, wall_height / 2)
    glScalef(GRID_LENGTH * 2, wall_thickness, wall_height)
    glutSolidCube(1)
    glPopMatrix()


def draw_shelter_interior():

    shelter_height = 190

    # ==========================================
    # INTERIOR FLOOR
    # ==========================================
    glColor3f(0.03, 0.28, 0.28)

    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X,
        SHELTER_CENTER_Y,
        3
    )
    glScalef(
        SHELTER_WIDTH - 20,
        SHELTER_DEPTH - 20,
        6
    )
    glutSolidCube(1)
    glPopMatrix()


    # ==========================================
    # BACK WALL
    # ==========================================
    glColor3f(0.27, 0.17, 0.12)

    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X,
        SHELTER_CENTER_Y - SHELTER_DEPTH / 2,
        shelter_height / 2
    )
    glScalef(
        SHELTER_WIDTH,
        15,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()


    # ==========================================
    # LEFT WALL
    # ==========================================
    glColor3f(0.30, 0.20, 0.14)

    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X - SHELTER_WIDTH / 2,
        SHELTER_CENTER_Y,
        shelter_height / 2
    )
    glScalef(
        15,
        SHELTER_DEPTH,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()


    # ==========================================
    # RIGHT WALL
    # ==========================================
    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X + SHELTER_WIDTH / 2,
        SHELTER_CENTER_Y,
        shelter_height / 2
    )
    glScalef(
        15,
        SHELTER_DEPTH,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()


    # ==========================================
    # FRONT WALL WITH OPEN DOOR
    # ==========================================

    front_y = (
        SHELTER_CENTER_Y
        +
        SHELTER_DEPTH / 2
    )

    door_width = SHELTER_DOOR_WIDTH
    door_height = 135

    side_width = (
        SHELTER_WIDTH
        -
        door_width
    ) / 2




    # ABOVE DOOR
    upper_height = (
        shelter_height
        -
        door_height
    )

    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X,
        front_y,
        door_height + upper_height / 2
    )

    glScalef(
        door_width,
        15,
        upper_height
    )

    glutSolidCube(1)
    glPopMatrix()



    # LEFT SIDE OF DOOR
    glColor3f(0.30, 0.20, 0.14)

    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X
        -
        door_width / 2
        -
        side_width / 2,

        front_y,

        shelter_height / 2
    )

    glScalef(
        side_width,
        15,
        shelter_height
    )

    glutSolidCube(1)
    glPopMatrix()


    # RIGHT SIDE OF DOOR
    glPushMatrix()
    glTranslatef(
        SHELTER_CENTER_X
        +
        door_width / 2
        +
        side_width / 2,

        front_y,

        shelter_height / 2
    )

    glScalef(
        side_width,
        15,
        shelter_height
    )

    glutSolidCube(1)
    glPopMatrix()
    # ==========================================
    # CEILING / ROOF
    # ==========================================
    glColor3f(0.14, 0.085, 0.055)

    glPushMatrix()

    glTranslatef(
        SHELTER_CENTER_X,
        SHELTER_CENTER_Y,
        shelter_height
    )

    glScalef(
        SHELTER_WIDTH,
        SHELTER_DEPTH,
        10
    )

    glutSolidCube(1)

    glPopMatrix()
    
def draw_rock(x, y, size):
    glPushMatrix()
    glColor3f(0.16, 0.17, 0.18)
    glTranslatef(x, y, size * 0.30)
    glScalef(1.2, 1.0, 0.8)
    gluSphere(gluNewQuadric(), size, 10, 10)
    glPopMatrix()

def draw_enemy(enemy):
    enemy_x = enemy["x"]
    enemy_y = enemy["y"]
    enemy_angle = enemy["angle"]
    attack_lunge = 0 

    if enemy.get("is_attacking", False):
        attack_frame = enemy.get(
            "attack_frame",
            0
        )
        half_attack = ENEMY_ATTACK_DURATION / 2

        if attack_frame < half_attack:
            attack_lunge = attack_frame * 0.7

        else:
            attack_lunge = (
                ENEMY_ATTACK_DURATION - attack_frame
            ) * 0.7

    glPushMatrix()
    glTranslatef(
        enemy_x,
        enemy_y,
        0
    )
    # Face movement direction
    glRotatef(
        enemy_angle + 90,
        0,
        0,
        1
    )
    # Small forward lunge during attack
    glTranslatef(
        0,
        -attack_lunge,
        0
    )
    glColor3f(0.055, 0.035, 0.035) #left foot
    glPushMatrix()
    glTranslatef(-10, 0, 8)
    glScalef(14, 18, 16)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix() #right foot
    glTranslatef(10, 0, 8)
    glScalef(14, 18, 16)
    glutSolidCube(1)
    glPopMatrix()
   
    glColor3f(0.30, 0.035, 0.045) #Red robe
    glPushMatrix()
    glTranslatef(0, 0, 37)
    glScalef(46, 30, 52)
    glutSolidCube(1)
    glPopMatrix()
    
    glColor3f(0.25, 0.025, 0.035) #bottom robe
    glPushMatrix()
    glTranslatef(0, 0, 20)
    glScalef(58, 34, 22)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.27, 0.025, 0.035) #Robe sleeve
    glPushMatrix() #left sleeve
    glTranslatef(-30, 0, 42)
    glRotatef(-18, 0, 1, 0)
    glScalef(17, 25, 35)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix() #right sleeve
    glTranslatef(30, 0, 42)
    glRotatef(18, 0, 1, 0)
    glScalef(17, 25, 35)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.20, 0.018, 0.028) #Hood back
    glPushMatrix()
    glTranslatef(
        0,
        2,
        83
    )
    glScalef(
        34,
        25,
        35
    )
    gluSphere(
        gluNewQuadric(),
        1,
        10,
        10
    )
    glPopMatrix()

    glColor3f(0.25, 0.022, 0.032) #Hood top
    glPushMatrix()
    glTranslatef(
        0,
        0,
        105
    )
    glScalef(
        29,
        22,
        20
    )
    gluSphere(
        gluNewQuadric(),
        1,
        10,
        10
    )
    glPopMatrix()

    glColor3f(0.24, 0.020, 0.030) #Left hood
    glPushMatrix()
    glTranslatef(
        -25,
        -9,
        84
    )
    glScalef(
        11,
        12,
        27
    )
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix() #Hood right
    glTranslatef(
        25,
        -9,
        84
    )
    glScalef(
        11,
        12,
        27
    )
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.18, 0.015, 0.025) #Hood bottom
    glPushMatrix()
    glTranslatef(
        0,
        -8,
        66
    )
    glScalef(
        40,
        18,
        10
    )
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.82, 0.83, 0.78) #Face
    glPushMatrix()
    glTranslatef(
        0,
        -28,
        84
    )
    glScalef(
        21,
        5,
        22
    )
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.02, 0.02, 0.02) #left eye
    glPushMatrix()
    glTranslatef(
        -8,
        -32,
        89
    )
    glScalef(
        5,
        3,
        6
    )
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix() #right eye
    glTranslatef(
        8,
        -32,
        89
    )
    glScalef(
        5,
        3,
        6
    )
    glutSolidCube(1)
    glPopMatrix()
    
    glPushMatrix() #mouth
    glTranslatef(
        0,
        -32,
        76
    )
    glScalef(
        3,
        3,
        3
    )
    glutSolidCube(1)
    glPopMatrix()
    
    glColor3f(0.78, 0.80, 0.76) #mask
    glPushMatrix()
    glTranslatef(
        0,
        -26,
        84
    )
    glScalef(
        25,
        5,
        25
    )
    glutSolidCube(1)
    glPopMatrix()
    
    glColor3f(0.025, 0.025, 0.025)
    
    glPushMatrix() #left eye
    glTranslatef(
        -9,
        -30,
        89
    )
    glScalef(
        6,
        3,
        7
    )
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix() #right eye
    glTranslatef(
        9,
        -30,
        89
    )
    glScalef(
        6,
        3,
        7
    )
    glutSolidCube(1)
    glPopMatrix()
    
    glPushMatrix() #mouth 
    glTranslatef(
        0,
        -30,
        76
    )
    glScalef(
        4,
        3,
        4
    )
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()

def draw_all_enemies():
    for enemy in enemies:
        draw_enemy(enemy)

def draw_pillar(x, y, height):
    # Base
    glPushMatrix()
    glColor3f(0.08, 0.27, 0.25)
    glTranslatef(x, y, 15)
    glScalef(70, 70, 30)
    glutSolidCube(1)
    glPopMatrix()

    # Shaft
    glPushMatrix()
    glColor3f(0.07, 0.23, 0.23)
    glTranslatef(x, y, 30)
    gluCylinder(gluNewQuadric(), 24, 20, height, 10, 10)
    glPopMatrix()

    # Top block
    glPushMatrix()
    glColor3f(0.10, 0.30, 0.27)
    glTranslatef(x, y, height + 35)
    glScalef(70, 70, 24)
    glutSolidCube(1)
    glPopMatrix()

def draw_cyan_pool(x, y, radius):
    # Outer stone ring
    glPushMatrix()
    glColor3f(0.08, 0.18, 0.20)
    glTranslatef(x, y, 4)
    glScalef(1.35, 1.35, 0.18)
    gluSphere(gluNewQuadric(), radius, 12, 12)
    glPopMatrix()

    # Cyan center
    glPushMatrix()
    glColor3f(0.15, 0.65, 0.62)
    glTranslatef(x, y, 7)
    glScalef(1.0, 1.0, 0.10)
    gluSphere(gluNewQuadric(), radius * 0.72, 12, 12)
    glPopMatrix()

def draw_brazier(x, y):
    # Base stones
    glColor3f(0.24, 0.19, 0.15)
    for dx, dy in [
        (-30, 0),
        (30, 0),
        (0, -30),
        (0, 30),
        (-22, -22),
        (22, -22),
        (-22, 22),
        (22, 22)
    ]:
        glPushMatrix()
        glTranslatef(x + dx, y + dy, 8)
        gluSphere(gluNewQuadric(), 16, 8, 8)
        glPopMatrix()

    # Fire lower section
    glPushMatrix()
    glColor3f(0.95, 0.28, 0.03)
    glTranslatef(x, y, 25)
    glScalef(0.8, 0.8, 1.4)
    gluSphere(gluNewQuadric(), 18, 10, 10)
    glPopMatrix()

    # Fire upper section
    glPushMatrix()
    glColor3f(1.0, 0.70, 0.10)
    glTranslatef(x, y, 42)
    glScalef(0.55, 0.55, 1.1)
    gluSphere(gluNewQuadric(), 14, 10, 10)
    glPopMatrix()

def draw_tall_torch(x, y):
    # TALL TORCH POLE
    glColor3f(0.32, 0.25, 0.18)

    glPushMatrix()
    glTranslatef(x, y, 120)
    glScalef(16, 16, 240)
    glutSolidCube(1)
    glPopMatrix()

    # SMALL BASE
    glColor3f(0.22, 0.17, 0.12)

    glPushMatrix()
    glTranslatef(x, y, 8)
    glScalef(32, 32, 16)
    glutSolidCube(1)
    glPopMatrix()

    # DECORATIVE BAND
    glColor3f(0.45, 0.34, 0.22)

    glPushMatrix()
    glTranslatef(x, y, 215)
    glScalef(28, 28, 14)
    glutSolidCube(1)
    glPopMatrix()

    # WIDE FIRE HOLDER
    glColor3f(0.16, 0.12, 0.09)

    glPushMatrix()
    glTranslatef(x, y, 245)
    glScalef(55, 55, 16)
    glutSolidCube(1)
    glPopMatrix()

    #Smaller upper holder
    glColor3f(0.28, 0.20, 0.13)

    glPushMatrix()
    glTranslatef(x, y, 258)
    glScalef(42, 42, 12)
    glutSolidCube(1)
    glPopMatrix()

    #LOWER FLAME
    glColor3f(1.0, 0.25, 0.02)

    glPushMatrix()
    glTranslatef(x, y, 285)
    glScalef(1.0, 1.0, 1.7)
    gluSphere(
        gluNewQuadric(),
        25,
        12,
        10
    )
    glPopMatrix()

    #UPPER FLAME
    glColor3f(1.0, 0.72, 0.08)

    glPushMatrix()
    glTranslatef(x, y, 320)
    glScalef(0.65, 0.65, 1.8)
    gluSphere(
        gluNewQuadric(),
        20,
        12,
        10
    )
    glPopMatrix()

    #SMALL FLAME TIP
    glColor3f(1.0, 0.88, 0.25)

    glPushMatrix()
    glTranslatef(x, y, 350)
    glScalef(0.4, 0.4, 1.6)
    gluSphere(
        gluNewQuadric(),
        14,
        10,
        8
    )
    glPopMatrix()

def draw_shelter_torches():
    #Left side of shelter
    draw_tall_torch(
        SHELTER_CENTER_X - 230,
        SHELTER_CENTER_Y + 20
    )
    #Right side of shelter
    draw_tall_torch(
        SHELTER_CENTER_X + 230,
        SHELTER_CENTER_Y + 20
    )

def draw_environment_campfires():
    draw_brazier(-950, 850) #Upper-left
    draw_brazier(900, 900) #Upper-right
    draw_brazier(-1000, 50) #Middle-left
    draw_brazier(1000, 100)#Middle-right
    draw_brazier(-850, -750) #Lower-left
    draw_brazier(850, -800) #Lower-right

def draw_candle(x, y, height=32):

    candle_sink = -5

    # SMALL CANDLE BASE
    glColor3f(0.32, 0.24, 0.16)

    glPushMatrix()
    glTranslatef(x, y, -2)
    glScalef(14, 14, 4)
    glutSolidCube(1)
    glPopMatrix()


    # CANDLE BODY
    glColor3f(0.88, 0.72, 0.42)

    glPushMatrix()
    glTranslatef(
        x,
        y,
        height / 2 + candle_sink
    )
    glScalef(
        10,
        10,
        height
    )
    glutSolidCube(1)
    glPopMatrix()


    # DARK WICK
    glColor3f(0.16, 0.10, 0.06)

    glPushMatrix()
    glTranslatef(
        x,
        y,
        height + candle_sink
    )
    glScalef(
        2,
        2,
        7
    )
    glutSolidCube(1)
    glPopMatrix()


    # OUTER ORANGE FLAME
    glColor3f(0.95, 0.38, 0.05)

    glPushMatrix()
    glTranslatef(
        x,
        y,
        height + 8 + candle_sink
    )
    glScalef(
        0.55,
        0.55,
        1.0
    )
    gluSphere(
        gluNewQuadric(),
        8,
        8,
        8
    )
    glPopMatrix()


    # INNER YELLOW FLAME
    glColor3f(1.0, 0.78, 0.18)

    glPushMatrix()
    glTranslatef(
        x,
        y,
        height + 10 + candle_sink
    )
    glScalef(
        0.35,
        0.35,
        0.75
    )
    gluSphere(
        gluNewQuadric(),
        6,
        8,
        8
    )
    glPopMatrix()

def draw_candle_group(x, y):
    draw_candle(
        x,
        y,
        32
    )
    draw_candle(
        x + 18,
        y + 5,
        24
    )
    draw_candle(
        x - 16,
        y + 8,
        20
    ) 

def draw_night_sky():
    sky_distance = GRID_LENGTH - 15
    sky_bottom = 400
    sky_top = 3500

    # FAR NIGHT SKY
    glColor3f(0.012, 0.025, 0.075)

    glBegin(GL_QUADS)
    glVertex3f(-sky_distance, sky_distance, sky_bottom)
    glVertex3f(sky_distance, sky_distance, sky_bottom)
    glVertex3f(sky_distance, sky_distance, sky_top)
    glVertex3f(-sky_distance, sky_distance, sky_top)

    glEnd()

    # NEAR NIGHT SKY
    glColor3f(0.014, 0.030, 0.085)
    glBegin(GL_QUADS)

    glVertex3f(sky_distance, -sky_distance, sky_bottom)
    glVertex3f(-sky_distance, -sky_distance, sky_bottom)
    glVertex3f(-sky_distance, -sky_distance, sky_top)
    glVertex3f(sky_distance, -sky_distance, sky_top)

    glEnd()

    # LEFT NIGHT SKY
    glColor3f(0.016, 0.035, 0.095)
    glBegin(GL_QUADS)

    glVertex3f(-sky_distance, -sky_distance, sky_bottom)
    glVertex3f(-sky_distance, sky_distance, sky_bottom)
    glVertex3f(-sky_distance, sky_distance, sky_top)
    glVertex3f(-sky_distance, -sky_distance, sky_top)

    glEnd()

    # RIGHT NIGHT SKY
    glColor3f(0.013, 0.028, 0.082)
    glBegin(GL_QUADS)

    glVertex3f(sky_distance, sky_distance, sky_bottom)
    glVertex3f(sky_distance, -sky_distance, sky_bottom)
    glVertex3f(sky_distance, -sky_distance, sky_top)
    glVertex3f(sky_distance, sky_distance, sky_top)

    glEnd()

    #STARS - FAR SKY
    glColor3f(0.72, 0.84, 0.92)
    far_stars = [
        (-1150, 610), (-1030, 820), (-900, 710),
        (-790, 1020), (-670, 890), (-540, 650),
        (-420, 1130), (-310, 780), (-190, 950),
        (-70, 680), (80, 1080), (210, 830),
        (340, 970), (470, 700), (590, 1160),
        (720, 880), (840, 670), (950, 1040),
        (1060, 790), (1170, 930),

        (-1080, 1280), (-820, 1450), (-560, 1320),
        (-260, 1530), (40, 1370), (330, 1490),
        (620, 1300), (900, 1510), (1120, 1250)
    ]
    for star_x, star_z in far_stars:
        glPushMatrix()
        glTranslatef(
            star_x,
            sky_distance - 8,
            star_z
        )
        glScalef(5, 3, 5)
        glutSolidCube(1)

        glPopMatrix()

    # LEFT-SIDE STARS
    left_stars = [
        (-1100, 650),
        (-850, 920),
        (-600, 760),
        (-350, 1100),
        (-100, 850),
        (180, 1250),
        (430, 710),
        (700, 1030),
        (980, 820)
    ]
    for star_y, star_z in left_stars:
        glPushMatrix()
        glTranslatef(
            -sky_distance + 8,
            star_y,
            star_z
        )
        glScalef(3, 5, 5)
        glutSolidCube(1)

        glPopMatrix()
        
    # RIGHT-SIDE STARS
    right_stars = [
        (-1050, 760),
        (-780, 1050),
        (-500, 690),
        (-220, 1230),
        (60, 880),
        (330, 1110),
        (610, 740),
        (870, 990),
        (1090, 1320)
    ]
    for star_y, star_z in right_stars:
        glPushMatrix()
        glTranslatef(
            sky_distance - 8,
            star_y,
            star_z
        )
        glScalef(3, 5, 5)
        glutSolidCube(1)

        glPopMatrix()
    
    # NEAR-SIDE STARS
    near_stars = [
        (-1050, 720),
        (-820, 960),
        (-590, 1250),
        (-340, 810),
        (-100, 1080),
        (170, 680),
        (420, 1180),
        (680, 870),
        (920, 1090),
        (1120, 760)
    ]
    for star_x, star_z in near_stars:
        glPushMatrix()
        glTranslatef(
            star_x,
            -sky_distance + 8,
            star_z
        )
        glScalef(5, 3, 5)
        glutSolidCube(1)

        glPopMatrix()

    # MOON
    glColor3f(0.72, 0.82, 0.90)
    glPushMatrix()
    glTranslatef(
        480,
        sky_distance - 12,
        900
    )
    gluSphere(
        gluNewQuadric(),
        55,
        16,
        16
    )

    glPopMatrix()

    #CLOUD CLUSTERS
    cloud_color = (0.055, 0.10, 0.18)
    cloud_positions = [
        (-850, sky_distance - 15, 720),
        (-350, sky_distance - 15, 1050),
        (760, sky_distance - 15, 760),

        (-sky_distance + 15, 500, 900),
        (-sky_distance + 15, -550, 1150),

        (sky_distance - 15, 650, 1050),
        (sky_distance - 15, -500, 780)
    ]
    glColor3f(
        cloud_color[0],
        cloud_color[1],
        cloud_color[2]
    )
    for cloud_x, cloud_y, cloud_z in cloud_positions:
        #cloud body
        glPushMatrix()
        glTranslatef(
            cloud_x,
            cloud_y,
            cloud_z
        )
        glScalef(75, 18, 22)
        gluSphere(
            gluNewQuadric(),
            1,
            8,
            8
        )
        glPopMatrix()

        #cloud piece
        glPushMatrix()
        glTranslatef(
            cloud_x + 35,
            cloud_y,
            cloud_z + 8
        )
        glScalef(55, 16, 18)

        gluSphere(
            gluNewQuadric(),
            1,
            8,
            8
        )
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(
            cloud_x - 35,
            cloud_y,
            cloud_z - 4
        )
        glScalef(45, 15, 16)
        gluSphere(
            gluNewQuadric(),
            1,
            8,
            8
        )
        glPopMatrix()

def draw_cave_tree(x, y, scale=1.0):
    # TREE TRUNK
    glColor3f(0.12, 0.075, 0.035)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        0
    )
    gluCylinder(
        gluNewQuadric(),
        18 * scale,
        13 * scale,
        180 * scale,
        8,
        8
    )
    glPopMatrix()
    # TREE ROOT BASE
    glColor3f(0.10, 0.055, 0.025)

    glPushMatrix()
    glTranslatef(x, y, 5 * scale)
    glScalef(
        25 * scale,
        25 * scale,
        10 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()
    # LOWER FOLIAGE
    glColor3f(0.035, 0.20, 0.075)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        150 * scale
    )
    glScalef(
        55 * scale,
        50 * scale,
        70 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()

    # MIDDLE FOLIAGE
    glColor3f(0.045, 0.27, 0.095)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        205 * scale
    )
    glScalef(
        48 * scale,
        45 * scale,
        65 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()

    # TOP FOLIAGE
    glColor3f(0.06, 0.34, 0.12)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        250 * scale
    )
    glScalef(
        35 * scale,
        35 * scale,
        55 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()

def draw_small_cave_tree(x, y, scale=1.0):
    # Trunk
    glColor3f(0.11, 0.065, 0.03)

    glPushMatrix()
    glTranslatef(x, y, 0)

    gluCylinder(
        gluNewQuadric(),
        9 * scale,
        6 * scale,
        90 * scale,
        8,
        8
    )
    glPopMatrix()
    # SMALL TREE ROOT BASE
    glColor3f(0.09, 0.05, 0.022)

    glPushMatrix()
    glTranslatef(x, y, 3 * scale)
    glScalef(
        14 * scale,
        14 * scale,
        6 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()
    # Lower leaves
    glColor3f(0.025, 0.16, 0.055)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        75 * scale
    )
    glScalef(
        32 * scale,
        30 * scale,
        42 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()
    # Middle leaves
    glColor3f(0.035, 0.23, 0.075)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        105 * scale
    )
    glScalef(
        26 * scale,
        25 * scale,
        38 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()
    # Top leaves
    glColor3f(0.05, 0.30, 0.095)
    glPushMatrix()
    glTranslatef(
        x,
        y,
        132 * scale
    )
    glScalef(
        19 * scale,
        19 * scale,
        30 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()

def draw_bush(x, y, scale=1.0):
    glPushMatrix()
    glTranslatef(
        x,
        y,
        0
    )
    # CENTER OF BUSH
    glColor3f(
        0.025,
        0.16,
        0.055
    )
    glPushMatrix()
    glTranslatef(
        0,
        0,
        20 * scale
    )
    glScalef(
        35 * scale,
        28 * scale,
        30 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        12,
        12
    )
    glPopMatrix()
    # LEFT SIDE
    glColor3f(
        0.035,
        0.21,
        0.07
    )
    glPushMatrix()
    glTranslatef(
        -25 * scale,
        0,
        17 * scale
    )
    glScalef(
        25 * scale,
        23 * scale,
        23 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        12,
        12
    )
    glPopMatrix()
    # RIGHT SIDE
    glColor3f(
        0.045,
        0.25,
        0.08
    )
    glPushMatrix()
    glTranslatef(
        25 * scale,
        2 * scale,
        18 * scale
    )
    glScalef(
        27 * scale,
        24 * scale,
        25 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        12,
        12
    )
    glPopMatrix()

    glColor3f(
        0.055,
        0.29,
        0.09
    )
    glPushMatrix()
    glTranslatef(
        2 * scale,
        0,
        38 * scale
    )
    glScalef(
        23 * scale,
        20 * scale,
        20 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        12,
        12
    )
    glPopMatrix()

    glPopMatrix()

def draw_fallen_log(x, y, angle, scale=1.0):
    glPushMatrix()
    glTranslatef(x, y, 18 * scale)
    glRotatef(angle, 0, 0, 1)

    glRotatef(90, 0, 1, 0)
    glColor3f(0.18, 0.10, 0.045)

    gluCylinder(
        gluNewQuadric(),
        15 * scale,
        18 * scale,
        110 * scale,
        10,
        10
    )
    glPopMatrix()
    # Small broken branch
    glPushMatrix()
    glTranslatef(
        x + 20 * scale,
        y,
        25 * scale
    )
    glRotatef(angle + 35, 0, 0, 1)
    glRotatef(55, 0, 1, 0)
    glColor3f(0.14, 0.075, 0.03)
    gluCylinder(
        gluNewQuadric(),
        7 * scale,
        4 * scale,
        45 * scale,
        8,
        8
    )
    glPopMatrix()

def draw_environment_logs():
    draw_fallen_log(
        -1000, 600, 25, 1.0
    )

    draw_fallen_log(
        950, 650, -30, 0.9
    )

    draw_fallen_log(
        -850, -700, 60, 1.1
    )

    draw_fallen_log(
        900, -600, -55, 0.85
    )

    draw_fallen_log(
        -400, 1050, 15, 0.8
    )

def draw_small_stone(x, y, scale=1.0):
    glColor3f(
        0.15,
        0.16,
        0.17
    )
    glPushMatrix()

    glTranslatef(
        x,
        y,
        8 * scale
    )
    glScalef(
        18 * scale,
        15 * scale,
        10 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        8,
        8
    )
    glPopMatrix()

def draw_environment_stones():
    stone_positions = [

        (-1100, 800, 1.0),
        (-900, 500, 0.7),
        (-700, 900, 0.8),

        (1050, 750, 0.9),
        (800, 500, 0.7),
        (650, 1000, 0.8),

        (-1050, -450, 0.9),
        (-750, -850, 0.7),
        (-450, -1050, 0.8),

        (1050, -400, 0.8),
        (800, -850, 1.0),
        (500, -1050, 0.7),

        (-300, 500, 0.6),
        (350, 450, 0.7),

        (-250, -500, 0.7),
        (300, -550, 0.6)
    ]
    for stone_x, stone_y, stone_scale in stone_positions:
        draw_small_stone(
            stone_x,
            stone_y,
            stone_scale
        )

def draw_tree_stump(x, y, scale=1.0):
    #MAIN STUMP
    glColor3f(
        0.17,
        0.09,
        0.035
    )
    glPushMatrix()
    glTranslatef(
        x,
        y,
        0
    )
    gluCylinder(
        gluNewQuadric(),
        24 * scale,
        20 * scale,
        45 * scale,
        10,
        10
    )
    glPopMatrix()
    # LIGHTER TOP
    glColor3f(
        0.32,
        0.20,
        0.10
    )
    glPushMatrix()
    glTranslatef(
        x,
        y,
        45 * scale
    )
    glScalef(
        20 * scale,
        20 * scale,
        4 * scale
    )
    gluSphere(
        gluNewQuadric(),
        1,
        10,
        8
    )
    glPopMatrix()
    # SMALL ROOT
    glColor3f(
        0.13,
        0.065,
        0.025
    )
    glPushMatrix()
    glTranslatef(
        x + 15 * scale,
        y,
        5
    )
    glRotatef(
        65,
        0,
        1,
        0
    )
    gluCylinder(
        gluNewQuadric(),
        6 * scale,
        3 * scale,
        30 * scale,
        8,
        8
    )
    glPopMatrix()

def draw_environment_stumps():
    draw_tree_stump(
        -900,
        250,
        1.0
    )
    draw_tree_stump(
        850,
        -250,
        0.9
    )
    draw_tree_stump(
        500,
        850,
        0.8
    )

def draw_environment_bushes():
    bush_positions = [
        (-1050, 850, 1.1),
        (-820, 620, 0.8),
        (-520, 950, 1.0),

        (500, 900, 0.9),
        (850, 720, 1.1),
        (1080, 450, 0.8),

        (-1080, 100, 0.9),
        (-900, -350, 1.0),
        (-650, -850, 0.8),

        (1050, -100, 1.0),
        (900, -500, 0.9),
        (650, -900, 1.1),

        (-350, 650, 0.7),
        (420, 600, 0.8),

        (-480, -600, 0.9),
        (500, -700, 0.8)
    ]
    for bush_x, bush_y, bush_scale in bush_positions:
        draw_bush(
            bush_x,
            bush_y,
            bush_scale
        )

def draw_forest_boundary():
    edge = GRID_LENGTH - 70
    # FAR SIDE
    far_trees = [
        (-1200, edge, 1.15),
        (-1000, edge, 0.95),
        (-800, edge, 1.10),
        (-580, edge, 0.90),
        (-350, edge, 1.20),
        (-100, edge, 0.95),
        (150, edge, 1.10),
        (390, edge, 0.90),
        (620, edge, 1.18),
        (850, edge, 1.00),
        (1080, edge, 1.15),
        (1250, edge, 0.90)
    ]

    for tree_x, tree_y, tree_scale in far_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )

    # NEAR SIDE
    near_trees = [
        (-1200, -edge, 0.95),
        (-970, -edge, 1.15),
        (-740, -edge, 0.90),
        (-510, -edge, 1.05),
        (-280, -edge, 1.15),
        (280, -edge, 1.05),
        (520, -edge, 0.95),
        (760, -edge, 1.15),
        (1000, -edge, 0.90),
        (1220, -edge, 1.10)
    ]
    for tree_x, tree_y, tree_scale in near_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # LEFT SIDE
    left_trees = [
        (-edge, -1100, 1.10),
        (-edge, -850, 0.90),
        (-edge, -610, 1.15),
        (-edge, -370, 0.95),
        (-edge, -120, 1.10),
        (-edge, 150, 0.90),
        (-edge, 410, 1.20),
        (-edge, 680, 0.95),
        (-edge, 940, 1.10),
        (-edge, 1160, 0.90)
    ]

    for tree_x, tree_y, tree_scale in left_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )

    # RIGHT SIDE
    right_trees = [
        (edge, -1150, 0.95),
        (edge, -900, 1.15),
        (edge, -650, 0.90),
        (edge, -390, 1.10),
        (edge, -130, 0.95),
        (edge, 130, 1.15),
        (edge, 390, 0.90),
        (edge, 650, 1.10),
        (edge, 900, 0.95),
        (edge, 1160, 1.15)
    ]
    for tree_x, tree_y, tree_scale in right_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
       
    #SECOND TREE ROW
    back_edge = GRID_LENGTH - 20
    # FAR BACK ROW
    far_back_trees = [
        (-1100, back_edge, 0.85),
        (-900, back_edge, 1.05),
        (-690, back_edge, 0.90),
        (-460, back_edge, 1.08),
        (-220, back_edge, 0.88),
        (20, back_edge, 1.05),
        (270, back_edge, 0.92),
        (510, back_edge, 1.10),
        (740, back_edge, 0.88),
        (970, back_edge, 1.05),
        (1170, back_edge, 0.90)
    ]

    for tree_x, tree_y, tree_scale in far_back_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    #NEAR BACK ROW
    near_back_trees = [
        (-1100, -back_edge, 0.90),
        (-880, -back_edge, 1.05),
        (-650, -back_edge, 0.85),
        (-420, -back_edge, 1.10),
        (-180, -back_edge, 0.90),
        (160, -back_edge, 1.05),
        (400, -back_edge, 0.88),
        (640, -back_edge, 1.10),
        (880, -back_edge, 0.90),
        (1110, -back_edge, 1.05)
    ]
    for tree_x, tree_y, tree_scale in near_back_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # LEFT BACK ROW
    left_back_trees = [
        (-back_edge, -1020, 0.88),
        (-back_edge, -760, 1.05),
        (-back_edge, -500, 0.90),
        (-back_edge, -250, 1.10),
        (-back_edge, 20, 0.88),
        (-back_edge, 280, 1.05),
        (-back_edge, 540, 0.90),
        (-back_edge, 800, 1.08),
        (-back_edge, 1060, 0.90)
    ]
    for tree_x, tree_y, tree_scale in left_back_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # RIGHT BACK ROW
    right_back_trees = [
        (back_edge, -1040, 0.90),
        (back_edge, -780, 1.08),
        (back_edge, -520, 0.88),
        (back_edge, -260, 1.05),
        (back_edge, 10, 0.92),
        (back_edge, 270, 1.10),
        (back_edge, 530, 0.88),
        (back_edge, 790, 1.05),
        (back_edge, 1050, 0.92)
    ]
    for tree_x, tree_y, tree_scale in right_back_trees:
        draw_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    
    # SMALL TREES 
    small_edge = GRID_LENGTH - 105

    # FAR SIDE
    small_far_trees = [
        (-1120, small_edge, 0.90),
        (-910, small_edge, 1.05),
        (-700, small_edge, 0.82),
        (-490, small_edge, 1.00),
        (-275, small_edge, 0.88),
        (-40, small_edge, 1.08),
        (190, small_edge, 0.85),
        (420, small_edge, 1.00),
        (650, small_edge, 0.90),
        (880, small_edge, 1.05),
        (1110, small_edge, 0.85)
    ]
    for tree_x, tree_y, tree_scale in small_far_trees:
        draw_small_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # NEAR SIDE
    small_near_trees = [
        (-1120, -small_edge, 0.85),
        (-890, -small_edge, 1.00),
        (-660, -small_edge, 0.90),
        (-430, -small_edge, 1.08),
        (-200, -small_edge, 0.82),
        (180, -small_edge, 1.05),
        (410, -small_edge, 0.88),
        (640, -small_edge, 1.00),
        (870, -small_edge, 0.85),
        (1100, -small_edge, 1.05)
    ]
    for tree_x, tree_y, tree_scale in small_near_trees:
        draw_small_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # LEFT SIDE
    small_left_trees = [
        (-small_edge, -1080, 0.90),
        (-small_edge, -830, 1.05),
        (-small_edge, -580, 0.82),
        (-small_edge, -330, 1.00),
        (-small_edge, -80, 0.88),
        (-small_edge, 180, 1.05),
        (-small_edge, 440, 0.85),
        (-small_edge, 700, 1.00),
        (-small_edge, 960, 0.90),
        (-small_edge, 1160, 0.85)
    ]
    for tree_x, tree_y, tree_scale in small_left_trees:
        draw_small_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # RIGHT SIDE
    small_right_trees = [
        (small_edge, -1100, 0.85),
        (small_edge, -850, 1.05),
        (small_edge, -600, 0.90),
        (small_edge, -350, 1.00),
        (small_edge, -100, 0.82),
        (small_edge, 160, 1.08),
        (small_edge, 420, 0.88),
        (small_edge, 680, 1.00),
        (small_edge, 940, 0.85),
        (small_edge, 1150, 1.05)
    ]
    for tree_x, tree_y, tree_scale in small_right_trees:
        draw_small_cave_tree(
            tree_x,
            tree_y,
            tree_scale
        )
    # ROCKS BETWEEN TREES
    boundary_rocks = [
        (-1080, edge - 40, 65),
        (-690, edge - 35, 75),
        (-220, edge - 45, 60),
        (300, edge - 35, 70),
        (760, edge - 40, 65),
        (1140, edge - 35, 75),

        (-edge + 40, -950, 70),
        (-edge + 35, -450, 60),
        (-edge + 40, 250, 75),
        (-edge + 35, 800, 65),

        (edge - 40, -1000, 65),
        (edge - 35, -500, 75),
        (edge - 40, 230, 60),
        (edge - 35, 820, 70)
    ]
    for rock_x, rock_y, rock_size in boundary_rocks:
        draw_rock(
            rock_x,
            rock_y,
            rock_size
        )

def draw_environment():
    draw_night_sky()
    draw_floor()

    draw_forest_boundary()
   
    draw_shelter_torches()
    draw_environment_bushes()
    draw_all_enemies()
    draw_environment_campfires()
    draw_environment_logs()
    draw_environment_stones()
    draw_environment_stumps()

    # Large cave rocks
    draw_rock(-420, 80, 70)
    draw_rock(390, 180, 80)
    draw_rock(-600, 500, 60)
    draw_rock(620, -100, 75)
    draw_rock(-850, 760, 90)
    draw_rock(820, 650, 70)
    draw_rock(-720, -520, 65)
    draw_rock(760, -650, 85)

    # Ancient pillars
    draw_pillar(-750, 350, 210)
    draw_pillar(720, 430, 230)
    draw_pillar(-900, -180, 190)
    draw_pillar(930, -260, 200)

    # Cool cyan accent pools
    draw_cyan_pool(-520, -180, 55)
    draw_cyan_pool(470, 540, 45)

    # Warm orange cave accent near one side
    draw_brazier(600, 150)

    # WARM CANDLES 
    # Left side
    draw_candle_group(-1180, 650)
    draw_candle_group(-1200, 150)
    draw_candle_group(-1170, -420)
    draw_candle_group(-1100, -850)

    # Right side
    draw_candle_group(1180, 720)
    draw_candle_group(1200, 250)
    draw_candle_group(1170, -350)
    draw_candle_group(1110, -820)

    # Far cave
    draw_candle_group(-650, 1180)
    draw_candle_group(0, 1210)
    draw_candle_group(650, 1180)

    # Around safe shelter
    draw_candle_group(-220, -1020)
    draw_candle_group(220, -1020)
    # ==========================================
# SHELTER DRAWN AFTER WORLD OBJECTS
# ==========================================

    if is_player_inside_shelter():
        draw_shelter_interior()

    else:
        draw_safe_haven()
        draw_shelter_torches()
        # =====================================================
    # SHELTER INTERIOR MUST BE DRAWN LAST
    # =====================================================
    # We do not have depth testing in the provided template.
    # Therefore the interior walls are drawn after the
    # outside environment so they visually cover objects
    # that should be hidden behind the walls.

    if is_player_inside_shelter():
        draw_shelter_interior()
def draw_safe_haven():
    center_x = 0
    center_y = -1160
    shelter_width = 320
    shelter_depth = 240
    shelter_height = 190
    wall_thickness = 20
    door_width = SHELTER_DOOR_WIDTH
    door_height = 135

    front_y = center_y + shelter_depth / 2
    back_y = center_y - shelter_depth / 2

    # BACK WALL
    glColor3f(0.33, 0.22, 0.16)

    glPushMatrix()
    glTranslatef(
        center_x,
        back_y,
        shelter_height / 2
    )
    glScalef(
        shelter_width,
        wall_thickness,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()

    # LEFT WALL
    glColor3f(0.29, 0.19, 0.14)

    glPushMatrix()
    glTranslatef(
        center_x - shelter_width / 2,
        center_y,
        shelter_height / 2
    )
    glScalef(
        wall_thickness,
        shelter_depth,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()

    # RIGHT WALL
    glPushMatrix()
    glTranslatef(
        center_x + shelter_width / 2,
        center_y,
        shelter_height / 2
    )
    glScalef(
        wall_thickness,
        shelter_depth,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()

    # FRONT WALL LEFT SIDE OF DOOR
    side_width = (shelter_width - door_width) / 2

    glColor3f(0.34, 0.23, 0.16)

    glPushMatrix()
    glTranslatef(
        center_x - door_width / 2 - side_width / 2,
        front_y,
        shelter_height / 2
    )
    glScalef(
        side_width,
        wall_thickness,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()

    # FRONT WALL RIGHT SIDE OF DOOR
    glPushMatrix()
    glTranslatef(
        center_x + door_width / 2 + side_width / 2,
        front_y,
        shelter_height / 2
    )
    glScalef(
        side_width,
        wall_thickness,
        shelter_height
    )
    glutSolidCube(1)
    glPopMatrix()

    # FRONT WALL ABOVE DOOR
    upper_height = shelter_height - door_height

    glPushMatrix()
    glTranslatef(
        center_x,
        front_y,
        door_height + upper_height / 2
    )
    glScalef(
        door_width,
        wall_thickness,
        upper_height
    )
    glutSolidCube(1)
    glPopMatrix()

    # ROOF
    glColor3f(0.21, 0.13, 0.09)

    glPushMatrix()
    glTranslatef(
        center_x,
        center_y,
        shelter_height + 12
    )
    glScalef(
        shelter_width + 40,
        shelter_depth + 40,
        24
    )
    glutSolidCube(1)
    glPopMatrix()

def draw_arm(side, swing_angle, show_lower=True):
    glPushMatrix()

    # Shoulder pivot
    glTranslatef(side * 33, 0, 108)

    # Arms swing opposite to the legs.
    glRotatef(swing_angle, 1, 0, 0)

    # Upper arm
    glPushMatrix()
    glColor3f(0.18, 0.40, 0.22)
    glTranslatef(0, 0, -20)
    glScalef(14, 18, 40)
    glutSolidCube(1)
    glPopMatrix()

    if show_lower:
        glPushMatrix()
        glColor3f(0.68, 0.53, 0.42)
        glTranslatef(0, 0, -48)
        glRotatef(8, 1, 0, 0)
        glScalef(13, 16, 32)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glColor3f(0.76, 0.60, 0.47)
        glTranslatef(0, 3, -68)
        gluSphere(gluNewQuadric(), 8, 10, 10)
        glPopMatrix()

    glPopMatrix()

def draw_leg(side, hip_angle):
    # Bend the knee more when the leg swings backward.
    knee_bend = max(0.0, -hip_angle) * 0.75

    glPushMatrix()

    # HIP PIVOT
    glTranslatef(side * 13, 0, 60)
    glRotatef(hip_angle, 1, 0, 0)

    # THIGH
    glPushMatrix()
    glColor3f(0.16, 0.17, 0.20)
    glTranslatef(0, 0, -21)
    glScalef(20, 24, 42)
    glutSolidCube(1)
    glPopMatrix()

    # Move to knee.
    glTranslatef(0, 0, -42)

    # KNEE BEND
    glRotatef(knee_bend, 1, 0, 0)

    # LOWER LEG
    glPushMatrix()
    glColor3f(0.12, 0.13, 0.15)
    glTranslatef(0, 0, -19)
    glScalef(18, 21, 38)
    glutSolidCube(1)
    glPopMatrix()

    # FOOT
    glPushMatrix()
    glColor3f(0.07, 0.07, 0.08)
    glTranslatef(0, 9, -39)
    glScalef(20, 34, 10)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()

def draw_player():

    # Hide player normally in FPS.
    # If dead, allow fallen body to be drawn.
    if first_person_mode and not player_dead:
        return

    # Stop walking animation when dead.
    if player_dead:
        leg_swing = 0
        arm_swing = 0

    else:
        leg_swing = math.sin(walk_phase) * 28.0
        arm_swing = math.sin(walk_phase) * 20.0

    # Main player matrix
    glPushMatrix()

    glTranslatef(
        player_x,
        player_y,
        player_z
    )

    glRotatef(
        player_angle + 90,
        0,
        0,
        1
    )

    # ==========================================
    # GAME OVER - PLAYER LIES DOWN
    # ==========================================
    if player_dead:

        glTranslatef(
            0,
            0,
            25
        )

        glRotatef(
            90,
            1,
            0,
            0
        )

    draw_leg(-1, leg_swing)
    draw_leg(1, -leg_swing)


    glPushMatrix()
    glColor3f(0.15, 0.16, 0.19)
    glTranslatef(0, 0, 60)
    glScalef(45, 28, 20)
    glutSolidCube(1)
    glPopMatrix()

    camera_radian_for_arms = math.radians(tps_camera_angle)

    camera_arm_x = player_x + math.cos(camera_radian_for_arms) * tps_distance
    camera_arm_y = player_y + math.sin(camera_radian_for_arms) * tps_distance

    player_forward_radian = math.radians(player_angle)

    player_right_x = math.sin(player_forward_radian)
    player_right_y = -math.cos(player_forward_radian)

    arm_to_camera_x = camera_arm_x - player_x
    arm_to_camera_y = camera_arm_y - player_y

    side_dot = (
        player_right_x * arm_to_camera_x +
        player_right_y * arm_to_camera_y
    )

    player_forward_x = -math.cos(player_forward_radian)
    player_forward_y = -math.sin(player_forward_radian)

    front_back_dot = (
        player_forward_x * arm_to_camera_x +
        player_forward_y * arm_to_camera_y
    )

    side_view = abs(side_dot) > abs(front_back_dot)

    if side_view:
        if side_dot > 0:
            draw_arm(1, arm_swing, False)
        else:
            draw_arm(-1, -arm_swing, False)

    glPushMatrix()
    glColor3f(0.20, 0.48, 0.27)
    glTranslatef(0, 0, 88)
    glScalef(56, 32, 58)
    glutSolidCube(1)
    glPopMatrix()

    # Shoulders
    glPushMatrix()
    glColor3f(0.18, 0.42, 0.23)
    glTranslatef(0, 0, 108)
    glScalef(70, 32, 17)
    glutSolidCube(1)
    glPopMatrix()

    if side_view:
        if side_dot > 0:
            draw_arm(-1, -arm_swing)

        else:
            draw_arm(1, arm_swing)

    else:
        draw_arm(-1, -arm_swing)
        draw_arm(1, arm_swing)

    glPushMatrix()
    glColor3f(0.72, 0.56, 0.44)
    glTranslatef(0, 0, 117)
    gluCylinder(gluNewQuadric(), 8, 8, 14, 10, 10)
    glPopMatrix()

    camera_radian = math.radians(tps_camera_angle)

    camera_world_x = player_x + math.cos(camera_radian) * tps_distance
    camera_world_y = player_y + math.sin(camera_radian) * tps_distance

    forward_radian = math.radians(player_angle)

    # Same visible forward direction used by W.
    forward_x = -math.cos(forward_radian)
    forward_y = -math.sin(forward_radian)

    to_camera_x = camera_world_x - player_x
    to_camera_y = camera_world_y - player_y
    front_dot = forward_x * to_camera_x + forward_y * to_camera_y

    # Main face/head
    glPushMatrix()
    glColor3f(0.77, 0.60, 0.46)
    glTranslatef(0, 0, 146)
    glScalef(30, 28, 36)
    glutSolidCube(1)
    glPopMatrix()

    hair_r = 0.16
    hair_g = 0.075
    hair_b = 0.025

    # Top hair
    glPushMatrix()
    glColor3f(hair_r, hair_g, hair_b)
    glTranslatef(0, -2, 166)
    glScalef(32, 31, 10)
    glutSolidCube(1)
    glPopMatrix()

    if front_dot <= 0:
        glPushMatrix()
        glColor3f(hair_r, hair_g, hair_b)
        glTranslatef(0, -15, 157)
        glScalef(30, 6, 25)
        glutSolidCube(1)
        glPopMatrix()

    if front_dot > 0:
        # Eyes
        glColor3f(0.03, 0.03, 0.03)

        glPushMatrix()
        glTranslatef(-6, 14.7, 151)
        gluSphere(gluNewQuadric(), 1.7, 8, 8)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(6, 14.7, 151)
        gluSphere(gluNewQuadric(), 1.7, 8, 8)
        glPopMatrix()

        # Tiny nose
        glPushMatrix()
        glColor3f(0.68, 0.50, 0.38)
        glTranslatef(0, 14.8, 145)
        glScalef(2.5, 2.5, 5)
        glutSolidCube(1)
        glPopMatrix()

        # Small mouth
        glPushMatrix()
        glColor3f(0.24, 0.07, 0.06)
        glTranslatef(0, 14.8, 137)
        glScalef(7, 1.5, 1.5)
        glutSolidCube(1)
        glPopMatrix()

    glPopMatrix()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(fovY, 1.25, 0.1, 4000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person_mode:

        angle_radian = math.radians(
            fps_camera_angle
        )

        direction_x = math.cos(
            angle_radian
        )

        direction_y = math.sin(
            angle_radian
        )
        camera_x = player_x
        camera_y = player_y
        camera_z = player_z + fps_eye_height

        look_x = (
            player_x
            -
            direction_x * fps_look_distance
        )

        look_y = (
            player_y
            -
            direction_y * fps_look_distance
        )

        look_z = (
            player_z
            +
            fps_eye_height
        )

        gluLookAt(
            camera_x,
            camera_y,
            camera_z,

            look_x,
            look_y,
            look_z,

            0,
            0,
            1
        )

    else:

    # =====================================================
    # THIRD PERSON CAMERA WHILE INSIDE SHELTER
    # =====================================================
          if is_player_inside_shelter():

    # ==========================================
    # SHELTER CAMERA
    # ==========================================

    # Camera stays near the back of the room.
    # It looks toward the doorway.

            camera_x = SHELTER_CENTER_X

            camera_y = (
                SHELTER_CENTER_Y
                -
                75
            )

            camera_z = 105


    # Look toward the open doorway
            look_x = SHELTER_CENTER_X

            look_y = (
                SHELTER_CENTER_Y
                +
                SHELTER_DEPTH / 2
                +
                100
            )

            look_z = 90


            gluLookAt(
                camera_x,
                camera_y,
                camera_z,

                look_x,
                look_y,
                look_z,

                0,
                0,
                1
            )

    # =====================================================
    # NORMAL OUTDOOR THIRD PERSON CAMERA
    # =====================================================
          else:

            camera_radian = math.radians(
                    tps_camera_angle
                )

            camera_x = (
                player_x
                +
                math.cos(camera_radian)
                *
                tps_distance
            )

            camera_y = (
                player_y
                +
                math.sin(camera_radian)
                *
                tps_distance
            )

            camera_z = (
                player_z
                +
                tps_height
            )

            look_x = player_x
            look_y = player_y
            look_z = player_z + 80

            gluLookAt(
                camera_x,
                camera_y,
                camera_z,

                look_x,
                look_y,
                look_z,

                0,
                0,
                1
            )

def is_colliding_with_circle(new_x, new_y, object_x, object_y, object_radius):
    distance_x = new_x - object_x
    distance_y = new_y - object_y

    distance_squared = (
        distance_x * distance_x
        +
        distance_y * distance_y
    )

    combined_radius = PLAYER_COLLISION_RADIUS + object_radius

    if distance_squared <= combined_radius * combined_radius:
        return True

    return False

def is_enemy_colliding_with_circle(
        new_x,
        new_y,
        object_x,
        object_y,
        object_radius
    ):

    distance_x = new_x - object_x
    distance_y = new_y - object_y

    distance_squared = (
        distance_x * distance_x
        +
        distance_y * distance_y
    )
    combined_radius = (
        ENEMY_COLLISION_RADIUS
        +
        object_radius
    )
    if distance_squared <= combined_radius * combined_radius:
        return True

    return False

def is_colliding_with_rectangle(
        new_x,
        new_y,
        center_x,
        center_y,
        width,
        depth
    ):
    half_width = width / 2
    half_depth = depth / 2

    closest_x = max(
        center_x - half_width,
        min(new_x, center_x + half_width)
    )

    closest_y = max(
        center_y - half_depth,
        min(new_y, center_y + half_depth)
    )
    distance_x = new_x - closest_x
    distance_y = new_y - closest_y
    distance_squared = (
        distance_x * distance_x
        +
        distance_y * distance_y
    )
    if distance_squared <= PLAYER_COLLISION_RADIUS * PLAYER_COLLISION_RADIUS:
        return True
    return False

def is_enemy_colliding_with_rectangle(
        new_x,
        new_y,
        center_x,
        center_y,
        width,
        depth
    ):

    half_width = width / 2
    half_depth = depth / 2

    closest_x = max(
        center_x - half_width,
        min(new_x, center_x + half_width)
    )

    closest_y = max(
        center_y - half_depth,
        min(new_y, center_y + half_depth)
    )

    distance_x = new_x - closest_x
    distance_y = new_y - closest_y

    distance_squared = (
        distance_x * distance_x
        +
        distance_y * distance_y
    )

    if distance_squared <= (
        ENEMY_COLLISION_RADIUS
        *
        ENEMY_COLLISION_RADIUS
    ):
        return True

    return False

def is_player_inside_shelter():
    half_width = SHELTER_WIDTH / 2
    half_depth = SHELTER_DEPTH / 2

    left = SHELTER_CENTER_X - half_width
    right = SHELTER_CENTER_X + half_width

    back = SHELTER_CENTER_Y - half_depth

    # Roof extends 20 units farther than the wall.
    roof_front = (
        SHELTER_CENTER_Y
        +
        (SHELTER_DEPTH + 40) / 2
    )

    # Keep indoor camera until the entire player
    # has cleared the front edge of the roof.
    front = (
        roof_front
        +
        PLAYER_COLLISION_RADIUS
        +
        15
    )

    if (
        player_x > left
        and player_x < right
        and
        player_y > back
        and player_y < front
    ):
        return True

    return False
def is_camera_behind_shelter():

    if first_person_mode:
        return False

    if is_player_inside_shelter():
        return False

    camera_radian = math.radians(tps_camera_angle)

    camera_y = (
        player_y
        +
        math.sin(camera_radian) * tps_distance
    )

    back_y = (
        SHELTER_CENTER_Y
        -
        SHELTER_DEPTH / 2
    )

    if camera_y < back_y:
        return True

    return False
def is_cover_between_enemy_and_player(enemy):

    enemy_x = enemy["x"]
    enemy_y = enemy["y"]

    line_x = player_x - enemy_x
    line_y = player_y - enemy_y

    line_length_squared = (
        line_x * line_x
        +
        line_y * line_y
    )

    if line_length_squared == 0:
        return False


    def cover_blocks_view(
        cover_x,
        cover_y,
        cover_radius
    ):

        cover_from_enemy_x = (
            cover_x - enemy_x
        )

        cover_from_enemy_y = (
            cover_y - enemy_y
        )

        # Find where the cover lies on
        # the enemy -> player line
        t = (
            cover_from_enemy_x * line_x
            +
            cover_from_enemy_y * line_y
        ) / line_length_squared


        # Cover must actually be BETWEEN
        # the enemy and player
        if t <= 0 or t >= 1:
            return False


        closest_x = (
            enemy_x
            +
            t * line_x
        )

        closest_y = (
            enemy_y
            +
            t * line_y
        )


        distance_x = (
            cover_x - closest_x
        )

        distance_y = (
            cover_y - closest_y
        )


        distance_squared = (
            distance_x * distance_x
            +
            distance_y * distance_y
        )


       # Use a slightly smaller hiding radius.
# This prevents Hide Mode from remaining active
# when the player moves around the side of the object.
        hide_radius = cover_radius * 0.75

        if distance_squared <= (
            hide_radius
            *
            hide_radius
        ):
            return True


        return False


    # ==========================================
    # BIG ROCKS
    # ==========================================
    for rock_x, rock_y, rock_radius in ROCK_COLLISIONS:

        if cover_blocks_view(
            rock_x,
            rock_y,
            rock_radius
        ):
            return True


    # ==========================================
    # PILLARS
    # ==========================================
    for pillar_x, pillar_y, pillar_radius in PILLAR_COLLISIONS:

        if cover_blocks_view(
            pillar_x,
            pillar_y,
            pillar_radius
        ):
            return True


    return False



def is_player_hiding():

    if is_player_inside_shelter():
        return False

    enemy_found = False
    blocked_enemy_found = False

    for enemy in enemies:

        if not enemy.get("active", True):
            continue

        distance_x = player_x - enemy["x"]
        distance_y = player_y - enemy["y"]

        distance_squared = (
            distance_x * distance_x
            +
            distance_y * distance_y
        )

        # Only consider enemies close enough
        # to actually be a threat.
        if distance_squared > (
            ENEMY_FIELD_OF_VIEW_DISTANCE
            *
            ENEMY_FIELD_OF_VIEW_DISTANCE
        ):
            continue

        enemy_found = True

        # If this enemy has a CLEAR line to the player,
        # player is NOT hiding.
        if not is_cover_between_enemy_and_player(enemy):
            return False

        # This enemy's view is blocked.
        blocked_enemy_found = True


    # Hide mode activates only if:
    # 1. there is a nearby enemy
    # 2. rock/pillar blocks the enemy view
    if enemy_found and blocked_enemy_found:
        return True

    return False
def can_player_move_to(new_x, new_y):
    limit = GRID_LENGTH - CAVE_COLLISION_MARGIN

    if new_x - PLAYER_COLLISION_RADIUS <= -limit:
        return False

    if new_x + PLAYER_COLLISION_RADIUS >= limit:
        return False

    if new_y - PLAYER_COLLISION_RADIUS <= -limit:
        return False

    if new_y + PLAYER_COLLISION_RADIUS >= limit:
        return False
    
    for rock_x, rock_y, rock_radius in ROCK_COLLISIONS:
        if is_colliding_with_circle(
            new_x,
            new_y,
            rock_x,
            rock_y,
            rock_radius
        ):
            return False

    for pillar_x, pillar_y, pillar_radius in PILLAR_COLLISIONS:
        if is_colliding_with_circle(
            new_x,
            new_y,
            pillar_x,
            pillar_y,
            pillar_radius
        ):
            return False

    for tree_x, tree_y, tree_radius in BOUNDARY_TREE_COVER:
        if is_colliding_with_circle(
           new_x,
           new_y,
           tree_x,
           tree_y,
           tree_radius
        ):
            return False
    
    for object_x, object_y, object_radius in BUSH_COLLISIONS:

        if is_colliding_with_circle(
            new_x,
            new_y,
            object_x,
            object_y,
            object_radius
        ):
            return False

    for object_x, object_y, object_radius in CAMPFIRE_COLLISIONS:
        if is_colliding_with_circle(
            new_x,
            new_y,
            object_x,
            object_y,
            object_radius
        ):
            return False

    for object_x, object_y, object_radius in LOG_COLLISIONS:
        if is_colliding_with_circle(
            new_x,
            new_y,
            object_x,
            object_y,
            object_radius
        ):
            return False

 

    for object_x, object_y, object_radius in STUMP_COLLISIONS:
        if is_colliding_with_circle(
            new_x,
            new_y,
            object_x,
            object_y,
            object_radius
        ):
            return False

    for object_x, object_y, object_radius in TORCH_COLLISIONS:
        if is_colliding_with_circle(
            new_x,
            new_y,
            object_x,
            object_y,
            object_radius
        ):
            return False
        
    front_y = SHELTER_CENTER_Y + SHELTER_DEPTH / 2
    back_y = SHELTER_CENTER_Y - SHELTER_DEPTH / 2

    left_x = SHELTER_CENTER_X - SHELTER_WIDTH / 2
    right_x = SHELTER_CENTER_X + SHELTER_WIDTH / 2

    if is_colliding_with_rectangle(
        new_x,
        new_y,
        SHELTER_CENTER_X,
        back_y,
        SHELTER_WIDTH,
        SHELTER_WALL_THICKNESS
    ):
        return False

    if is_colliding_with_rectangle(
        new_x,
        new_y,
        left_x,
        SHELTER_CENTER_Y,
        SHELTER_WALL_THICKNESS,
        SHELTER_DEPTH
    ):
        return False

    if is_colliding_with_rectangle(
        new_x,
        new_y,
        right_x,
        SHELTER_CENTER_Y,
        SHELTER_WALL_THICKNESS,
        SHELTER_DEPTH
    ):
        return False

    front_side_width = (
        SHELTER_WIDTH - SHELTER_DOOR_WIDTH
    ) / 2

    front_left_x = (
        SHELTER_CENTER_X
        - SHELTER_DOOR_WIDTH / 2
        - front_side_width / 2
    )

    if is_colliding_with_rectangle(
        new_x,
        new_y,
        front_left_x,
        front_y,
        front_side_width,
        SHELTER_WALL_THICKNESS
    ):
        return False

    front_right_x = (
        SHELTER_CENTER_X
        + SHELTER_DOOR_WIDTH / 2
        + front_side_width / 2
    )

    if is_colliding_with_rectangle(
        new_x,
        new_y,
        front_right_x,
        front_y,
        front_side_width,
        SHELTER_WALL_THICKNESS
    ):
        return False
    
    return True
def can_enemy_move_to(new_x, new_y):
    limit = GRID_LENGTH - ENEMY_BOUNDARY_MARGIN

    if new_x - ENEMY_COLLISION_RADIUS <= -limit:
        return False

    if new_x + ENEMY_COLLISION_RADIUS >= limit:
        return False

    if new_y - ENEMY_COLLISION_RADIUS <= -limit:
        return False

    if new_y + ENEMY_COLLISION_RADIUS >= limit:
        return False

    for rock_x, rock_y, rock_radius in ROCK_COLLISIONS:

        if is_enemy_colliding_with_circle(
            new_x,
            new_y,
            rock_x,
            rock_y,
            rock_radius
        ):
            return False

    for pillar_x, pillar_y, pillar_radius in PILLAR_COLLISIONS:
        if is_enemy_colliding_with_circle(
            new_x,
            new_y,
            pillar_x,
            pillar_y,
            pillar_radius
        ):
            return False
    for tree_x, tree_y, tree_radius in BOUNDARY_TREE_COVER: 
        if is_enemy_colliding_with_circle(
           new_x,
           new_y,
           tree_x,
           tree_y,
           tree_radius
        ):
            return False
    
    collision_groups = [
        BUSH_COLLISIONS,
        CAMPFIRE_COLLISIONS,
        LOG_COLLISIONS,
        STONE_COLLISIONS,
        STUMP_COLLISIONS,
        TORCH_COLLISIONS
    ]

    for collision_group in collision_groups:
        for object_x, object_y, object_radius in collision_group:
            if is_enemy_colliding_with_circle(
                new_x,
                new_y,
                object_x,
                object_y,
                object_radius
            ):
                return False
    front_y = (
        SHELTER_CENTER_Y
        +
        SHELTER_DEPTH / 2
    )
    back_y = (
        SHELTER_CENTER_Y
        -
        SHELTER_DEPTH / 2
    )
    left_x = (
        SHELTER_CENTER_X
        -
        SHELTER_WIDTH / 2
    )
    right_x = (
        SHELTER_CENTER_X
        +
        SHELTER_WIDTH / 2
    )
    # Back wall
    if is_enemy_colliding_with_rectangle(
        new_x,
        new_y,
        SHELTER_CENTER_X,
        back_y,
        SHELTER_WIDTH,
        SHELTER_WALL_THICKNESS
    ):
        return False
    # Left wall
    if is_enemy_colliding_with_rectangle(
        new_x,
        new_y,
        left_x,
        SHELTER_CENTER_Y,
        SHELTER_WALL_THICKNESS,
        SHELTER_DEPTH
    ):
        return False
    # Right wall
    if is_enemy_colliding_with_rectangle(
        new_x,
        new_y,
        right_x,
        SHELTER_CENTER_Y,
        SHELTER_WALL_THICKNESS,
        SHELTER_DEPTH
    ):
        return False
    if is_enemy_colliding_with_rectangle(
        new_x,
        new_y,
        SHELTER_CENTER_X,
        front_y,
        SHELTER_WIDTH,
        SHELTER_WALL_THICKNESS
    ):
        return False
    return True

def restart_game():
    global player_x
    global player_y
    global player_angle
    global player_health
    global player_dead
    global walk_phase
    global tps_camera_angle
    global tps_height
    global enemies
    global shelter_exit_active
    global shelter_previous_x
    global shelter_previous_y
    # Reset player
    player_x = PLAYER_START_X
    player_y = PLAYER_START_Y
    player_angle = PLAYER_START_ANGLE
    walk_phase = 0
    shelter_exit_active = False
    shelter_previous_x = 0.0
    shelter_previous_y = 0.0
    tps_camera_angle = 270.0
    tps_height = 500.0
    # Reset health
    player_health = PLAYER_MAX_HEALTH
    player_dead = False
    # Reset enemies
    enemies = [
        {
            "x": enemy["x"],
            "y": enemy["y"],
            "angle": enemy["angle"]
        }
        for enemy in ENEMY_START_DATA
    ]

def keyboardListener(key, x, y):
    global fps_camera_angle
    global player_x
    global player_y
    global player_angle
    global walk_phase

    global shelter_exit_active
    global shelter_previous_x
    global shelter_previous_y


    # ==========================================
    # RESTART AFTER GAME OVER
    # ==========================================
    if player_dead:
        if key == b'r':
            restart_game()
            glutPostRedisplay()

        return


    if first_person_mode:
        angle_radian = math.radians(
            fps_camera_angle
        )
    else:
        angle_radian = math.radians(
            player_angle
        )

    direction_x = math.cos(
        angle_radian
    )

    direction_y = math.sin(
        angle_radian
    )


    # ==========================================
    # W - MOVE FORWARD
    # ==========================================
    if key == b'w':

        # --------------------------------------
        # SPECIAL SHELTER EXIT
        # --------------------------------------
        if is_player_inside_shelter():

            # Remember exact position inside.
            shelter_previous_x = player_x
            shelter_previous_y = player_y

            # Door is at the FRONT of shelter.
            shelter_front_y = (
                SHELTER_CENTER_Y
                +
                SHELTER_DEPTH / 2
            )

            # Place player completely outside.
            player_x = SHELTER_CENTER_X

            player_y = (
                shelter_front_y
                +
                PLAYER_COLLISION_RADIUS
                +
                35
            )

            shelter_exit_active = True

            walk_phase += walk_step


        # --------------------------------------
        # NORMAL OUTDOOR FORWARD MOVEMENT
        # --------------------------------------
        else:

            new_x = (
                player_x
                -
                direction_x
                *
                player_move_speed
            )

            new_y = (
                player_y
                -
                direction_y
                *
                player_move_speed
            )

            if can_player_move_to(
                new_x,
                new_y
            ):
                player_x = new_x
                player_y = new_y

                walk_phase += walk_step

                # Player continued walking,
                # so S should now behave normally.
                shelter_exit_active = False


    # ==========================================
    # S - MOVE BACKWARD
    # ==========================================
    elif key == b's':

        # --------------------------------------
        # UNDO SHELTER EXIT
        # --------------------------------------
        if shelter_exit_active:

            player_x = shelter_previous_x
            player_y = shelter_previous_y

            shelter_exit_active = False

            walk_phase -= walk_step


        # --------------------------------------
        # NORMAL BACKWARD MOVEMENT
        # --------------------------------------
        else:

            new_x = (
                player_x
                +
                direction_x
                *
                player_move_speed
            )

            new_y = (
                player_y
                +
                direction_y
                *
                player_move_speed
            )

            if can_player_move_to(
                new_x,
                new_y
            ):
                player_x = new_x
                player_y = new_y

                walk_phase -= walk_step


    # ==========================================
    # A - TURN LEFT
    # ==========================================
    elif key == b'a':

        player_angle += player_turn_speed

        if first_person_mode:
            fps_camera_angle += player_turn_speed

        shelter_exit_active = False


    # ==========================================
    # D - TURN RIGHT
    # ==========================================
    elif key == b'd':

        player_angle -= player_turn_speed

        if first_person_mode:
            fps_camera_angle -= player_turn_speed

        shelter_exit_active = False


    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global tps_camera_angle
    global tps_height
    global fps_camera_angle
    global player_angle
    # ==========================================
    # FIRST PERSON CAMERA
    # ==========================================
    if first_person_mode:

        if key == GLUT_KEY_LEFT:
            fps_camera_angle += fps_camera_rotate_speed
            player_angle += fps_camera_rotate_speed

        elif key == GLUT_KEY_RIGHT:
            fps_camera_angle -= fps_camera_rotate_speed
            player_angle -= fps_camera_rotate_speed

        if fps_camera_angle >= 360:
            fps_camera_angle -= 360

        elif fps_camera_angle < 0:
            fps_camera_angle += 360


    # ==========================================
    # THIRD PERSON CAMERA
    # ==========================================
    else:

        if key == GLUT_KEY_LEFT:
            tps_camera_angle += tps_camera_rotate_speed

        elif key == GLUT_KEY_RIGHT:
            tps_camera_angle -= tps_camera_rotate_speed

        elif key == GLUT_KEY_UP:
            tps_height += 10

        elif key == GLUT_KEY_DOWN:
            tps_height -= 10

            if tps_height < 70:
                tps_height = 70

    glutPostRedisplay()
def mouseListener(button, state, x, y):
    global first_person_mode

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

        if first_person_mode:
            first_person_mode = False
            print("Camera Mode: Third Person")
        else:
            first_person_mode = True
            print("Camera Mode: First Person")
        glutPostRedisplay()

def get_distance_between_points(x1, y1, x2, y2):
    distance_x = x2 - x1
    distance_y = y2 - y1

    return math.sqrt(
        distance_x * distance_x
        +
        distance_y * distance_y
    )

def damage_player(amount):
    global player_health
    global player_dead
    global first_person_mode

    if player_dead:
        return

    player_health -= amount

    if player_health <= 0:

        player_health = 0
        player_dead = True

        # Switch to TPS so the dead
        # player's fallen body is visible
        first_person_mode = False
def enemy_attack(enemy):
    distance_x = player_x - enemy["x"]
    distance_y = player_y - enemy["y"]

    # Face the player
    enemy["angle"] = math.degrees(
        math.atan2(
            distance_y,
            distance_x
        )
    )

    enemy["is_attacking"] = True

    if "attack_frame" not in enemy:
        enemy["attack_frame"] = 0

    if "damage_given" not in enemy:
        enemy["damage_given"] = False

    enemy["attack_frame"] += 1

    if (
        enemy["attack_frame"] >= ENEMY_DAMAGE_FRAME
        and
        not enemy["damage_given"]
    ):

        damage_player(
            ENEMY_ATTACK_DAMAGE
        )

        enemy["damage_given"] = True

    if enemy["attack_frame"] >= ENEMY_ATTACK_DURATION:

        enemy["attack_frame"] = 0
        enemy["damage_given"] = False

def chase_player(enemy):
    enemy["is_attacking"] = False
    enemy["attack_frame"] = 0
    enemy["damage_given"] = False

    distance_x = player_x - enemy["x"]
    distance_y = player_y - enemy["y"]

    distance = math.sqrt(
        distance_x * distance_x
        +
        distance_y * distance_y
    )

    if distance == 0:
        return

    direction_x = distance_x / distance
    direction_y = distance_y / distance
    new_x = (
        enemy["x"]
        +
        direction_x * ENEMY_CHASE_SPEED
    )
    new_y = (
        enemy["y"]
        +
        direction_y * ENEMY_CHASE_SPEED
    )
    if can_enemy_move_to(new_x, new_y):

        enemy["x"] = new_x
        enemy["y"] = new_y

    elif can_enemy_move_to(
        new_x,
        enemy["y"]
    ):

        enemy["x"] = new_x

    elif can_enemy_move_to(
        enemy["x"],
        new_y
    ):
        enemy["y"] = new_y
    enemy["angle"] = math.degrees(
        math.atan2(
            direction_y,
            direction_x
        )
    )

def is_point_near_line(
        point_x,
        point_y,
        line_start_x,
        line_start_y,
        line_end_x,
        line_end_y,
        radius
    ):

    line_x = line_end_x - line_start_x
    line_y = line_end_y - line_start_y

    point_from_start_x = point_x - line_start_x
    point_from_start_y = point_y - line_start_y

    line_length_squared = (
        line_x * line_x
        +
        line_y * line_y
    )

    if line_length_squared == 0:
        return False

    t = (
        point_from_start_x * line_x
        +
        point_from_start_y * line_y
    ) / line_length_squared

    if t < 0 or t > 1:
        return False

    closest_x = (
        line_start_x
        +
        t * line_x
    )

    closest_y = (
        line_start_y
        +
        t * line_y
    )
    distance_x = point_x - closest_x
    distance_y = point_y - closest_y

    distance_squared = (
        distance_x * distance_x
        +
        distance_y * distance_y
    )

    return distance_squared <= radius * radius

def does_line_cross_rectangle(
        line_start_x,
        line_start_y,
        line_end_x,
        line_end_y,
        center_x,
        center_y,
        width,
        depth
    ):
    half_width = width / 2
    half_depth = depth / 2

    left = center_x - half_width
    right = center_x + half_width
    bottom = center_y - half_depth
    top = center_y + half_depth
    steps = 20

    for i in range(1, steps):
        t = i / steps
        check_x = (
            line_start_x
            +
            (line_end_x - line_start_x) * t
        )
        check_y = (
            line_start_y
            +
            (line_end_y - line_start_y) * t
        )
        if (
            left <= check_x <= right
            and
            bottom <= check_y <= top
        ):
            return True

    return False

def is_player_inside_enemy_view(enemy):
    distance_x = player_x - enemy["x"]
    distance_y = player_y - enemy["y"]
    distance_squared = (
        distance_x * distance_x
        +
        distance_y * distance_y
    )
    if distance_squared > (
        ENEMY_FIELD_OF_VIEW_DISTANCE
        *
        ENEMY_FIELD_OF_VIEW_DISTANCE
    ):
        return False

    angle_to_player = math.degrees(
        math.atan2(
            distance_y,
            distance_x
        )
    )

    angle_difference = (
        angle_to_player
        -
        enemy["angle"]
    )

    while angle_difference > 180:
        angle_difference -= 360

    while angle_difference < -180:
        angle_difference += 360

    half_fov = ENEMY_FIELD_OF_VIEW / 2
    if abs(angle_difference) <= half_fov:
        return True
    return False

def enemy_can_see_player(enemy):

    # ==========================================
    # HIDE MODE
    # ==========================================
    # If player is hiding behind/near valid cover,
    # enemies cannot see the player.
    if is_player_hiding():
        return False
    enemy_x = enemy["x"]
    enemy_y = enemy["y"]
    if not is_player_inside_enemy_view(enemy):
        return False

    for rock_x, rock_y, rock_radius in ROCK_COLLISIONS:
        if is_point_near_line(
            rock_x,
            rock_y,
            enemy_x,
            enemy_y,
            player_x,
            player_y,
            rock_radius
        ):

            return False
        
    for pillar_x, pillar_y, pillar_radius in PILLAR_COLLISIONS:
        if is_point_near_line(
            pillar_x,
            pillar_y,
            enemy_x,
            enemy_y,
            player_x,
            player_y,
            pillar_radius
        ):
            return False
        
    if does_line_cross_rectangle(
        enemy_x,
        enemy_y,
        player_x,
        player_y,
        SHELTER_CENTER_X,
        SHELTER_CENTER_Y,
        SHELTER_WIDTH,
        SHELTER_DEPTH
    ):
        return False
    return True

def search_for_player(enemy):
    target_x = enemy["last_seen_x"]
    target_y = enemy["last_seen_y"]
    distance_x = target_x - enemy["x"]
    distance_y = target_y - enemy["y"]

    distance = math.sqrt(
        distance_x * distance_x
        +
        distance_y * distance_y
    )
    if distance <= ENEMY_SEARCH_DISTANCE:
        enemy["memory_timer"] -= 1
        enemy["angle"] += 1.5

        if enemy["angle"] >= 360:
            enemy["angle"] -= 360
        return
    
    direction_x = distance_x / distance
    direction_y = distance_y / distance

    enemy["angle"] = math.degrees(
        math.atan2(
            direction_y,
            direction_x
        )
    )
    new_x = (
        enemy["x"]
        +
        direction_x * ENEMY_MOVE_SPEED
    )
    new_y = (
        enemy["y"]
        +
        direction_y * ENEMY_MOVE_SPEED
    )
    if can_enemy_move_to(
        new_x,
        new_y
    ):

        enemy["x"] = new_x
        enemy["y"] = new_y

    elif can_enemy_move_to(
        new_x,
        enemy["y"]
    ):

        enemy["x"] = new_x

    elif can_enemy_move_to(
        enemy["x"],
        new_y
    ):

        enemy["y"] = new_y

    enemy["memory_timer"] -= 1

def update_enemy_wandering():
    for enemy in enemies:
        if not enemy.get("active", True):
            continue
        if player_dead:
            enemy["is_attacking"] = False
            enemy["attack_frame"] = 0
            enemy["damage_given"] = False
            continue

        distance_to_player = get_distance_between_points(
            enemy["x"],
            enemy["y"],
            player_x,
            player_y
        )

        can_see_player = enemy_can_see_player(
            enemy
        )

        if (
            distance_to_player <= ENEMY_DETECTION_DISTANCE
            and
            can_see_player
        ):
            enemy["last_seen_x"] = player_x
            enemy["last_seen_y"] = player_y
            enemy["memory_timer"] = ENEMY_MEMORY_TIME

            if distance_to_player <= ENEMY_ATTACK_DISTANCE:
                enemy_attack(enemy)
                continue

            else:
                chase_player(enemy)
                continue

        elif enemy.get("memory_timer", 0) > 0:
            enemy["is_attacking"] = False
            enemy["attack_frame"] = 0
            enemy["damage_given"] = False
            search_for_player(enemy)

            continue
        enemy["is_attacking"] = False
        enemy["attack_frame"] = 0
        enemy["damage_given"] = False
        enemy["memory_timer"] = 0
        angle_radian = math.radians(
            enemy["angle"]
        )
        direction_x = math.cos(
            angle_radian
        )
        direction_y = math.sin(
            angle_radian
        )
        new_x = (
            enemy["x"]
            +
            direction_x * ENEMY_MOVE_SPEED
        )
        new_y = (
            enemy["y"]
            +
            direction_y * ENEMY_MOVE_SPEED
        )
        if can_enemy_move_to(
            new_x,
            new_y
        ):
            enemy["x"] = new_x
            enemy["y"] = new_y

        else:
            enemy["angle"] += 135
            if enemy["angle"] >= 360:
                enemy["angle"] -= 360

def draw_health_hud():
    health_text = (
        "Health : "
        +
        str(player_health)
        +
        " / "
        +
        str(PLAYER_MAX_HEALTH)
    )
    draw_text(
        20,
        720,
        health_text
    )

def draw_game_over():
    if not player_dead:
        return
    draw_text(
        450,
        400,
        "GAME OVER.PRESS R TO RESTART"
    )

def idle():
    update_enemy_wandering() 

    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    setupCamera()

    draw_environment()

# Outside = normal third-person character
    if not is_player_inside_shelter():
        draw_player()


# ==========================================
# HOUSE MUST COVER OBJECTS WHEN CAMERA
# IS BEHIND THE HOUSE
# ==========================================
    if is_camera_behind_shelter():

    # Redraw house AFTER enemies and player.
    # This prevents them appearing on the roof.
        draw_safe_haven()

    # Torches belong in front of the house.
        draw_shelter_torches()

    
        

    draw_text(10, 770, "CaveBound : Survival Game")
    if first_person_mode:
        draw_text(15, 742, "View : FPS")
    else:
        draw_text(15, 742, "View : TPS")
    draw_health_hud() 
    if not player_dead and is_player_hiding():
        draw_text(
            20,
            692,
            "Hide mode:Activated"
        )
    draw_game_over()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )
    glutInitWindowSize(
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
    glutInitWindowPosition(0, 0)
    glutCreateWindow(
        b"CaveBound: A 3D Survival Game"
    )
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

# ============================================================
# FEATURES 6-10 EXTENSION LAYER
# Existing Feature 1-5 code above is intentionally left intact.
# ============================================================

# FEATURE 6 - HUNGER / SURVIVAL
PLAYER_MAX_HUNGER = 100
player_hunger = PLAYER_MAX_HUNGER
HUNGER_DECREASE_FRAME = 120
hunger_frame = 0
STARVATION_DAMAGE_FRAME = 60
starvation_frame = 0

# FEATURE 7 - INVENTORY
INVENTORY_CAPACITY = 8
inventory = {
    "apple": 0, "banana": 0, "mango": 0, "medkit": 0,
    "ammo_pack": 0, "wood": 0, "stone": 0, "supplies": 0
}
inventory_open = False
feature_message = ""
feature_message_frame = 0
FEATURE_MESSAGE_DURATION = 120

# FEATURE 8 - PROJECTILE COMBAT
current_ammo = 10
AMMO_PER_PACK = 10
BULLET_SPEED = 24.0
BULLET_DAMAGE = 10
BULLET_MAX_DISTANCE = 1500
BULLET_HIT_RADIUS = 38
bullets = []
ENEMY_MAX_HEALTH = 30

# FEATURE 9 - RESOURCE GATHERING
# Resources use fixed positions for the first game.
# After pressing R, all collectible food / medicine / ammunition /
# wood / stone / supplies are generated at new random valid places.
import random

FOOD_PICKUP_RADIUS = 42
ITEM_PICKUP_RADIUS = 45

RESOURCE_RANDOM_MIN = -1100
RESOURCE_RANDOM_MAX = 1100
RESOURCE_MIN_SEPARATION = 110
RESOURCE_SHELTER_MARGIN = 120
RESOURCE_RANDOM_ATTEMPTS = 500
# ==========================================
# RESOURCE RESPAWN SETTINGS
# ==========================================

# About 15 seconds depending on game/frame speed.
RESOURCE_RESPAWN_FRAMES = 900

# Prevent an item from respawning directly
# beside the player.
RESOURCE_RESPAWN_PLAYER_CLEAR_RADIUS = 180
FOOD_START_DATA = [
    {"type": "apple", "x": -300, "y": -650},
    {"type": "apple", "x": 550, "y": -250},
    {"type": "apple", "x": -700, "y": 300},
    {"type": "banana", "x": 350, "y": 250},
    {"type": "banana", "x": -450, "y": 750},
    {"type": "banana", "x": 750, "y": 850},
    {"type": "mango", "x": 250, "y": 950},
    {"type": "mango", "x": -850, "y": -150},
    {"type": "mango", "x": 850, "y": -550}
]
ITEM_START_DATA = [
    {"type": "medkit", "x": -600, "y": 600},
    {"type": "medkit", "x": 650, "y": 450},
    {"type": "ammo_pack", "x": -500, "y": -250},
    {"type": "ammo_pack", "x": 600, "y": 100},
    {"type": "wood", "x": -250, "y": 450},
    {"type": "wood", "x": 450, "y": 700},
    {"type": "wood", "x": -750, "y": -500},
    {"type": "stone", "x": 200, "y": 550},
    {"type": "stone", "x": -650, "y": 100},
    {"type": "stone", "x": 750, "y": -350},
    {"type": "supplies", "x": -150, "y": 850},
    {"type": "supplies", "x": 700, "y": 250}
]
foods = [{"type": f["type"], "x": f["x"], "y": f["y"], "active": True} for f in FOOD_START_DATA]
world_items = [{"type": i["type"], "x": i["x"], "y": i["y"], "active": True} for i in ITEM_START_DATA]


def is_resource_position_valid(x, y, used_positions):
    # Keep resources well away from the Safe Haven.
    shelter_left = (
        SHELTER_CENTER_X
        -
        SHELTER_WIDTH / 2
        -
        RESOURCE_SHELTER_MARGIN
    )

    shelter_right = (
        SHELTER_CENTER_X
        +
        SHELTER_WIDTH / 2
        +
        RESOURCE_SHELTER_MARGIN
    )

    shelter_back = (
        SHELTER_CENTER_Y
        -
        SHELTER_DEPTH / 2
        -
        RESOURCE_SHELTER_MARGIN
    )

    shelter_front = (
        SHELTER_CENTER_Y
        +
        SHELTER_DEPTH / 2
        +
        RESOURCE_SHELTER_MARGIN
    )

    if (
        shelter_left <= x <= shelter_right
        and
        shelter_back <= y <= shelter_front
    ):
        return False

    # Reuse Feature 2's existing collision rules so a collectible
    # does not spawn inside a large obstacle or cave boundary.
    if not can_player_move_to(x, y):
        return False

    # Keep collectible objects separated from one another.
    for used_x, used_y in used_positions:
        distance_x = x - used_x
        distance_y = y - used_y

        distance_squared = (
            distance_x * distance_x
            +
            distance_y * distance_y
        )

        if distance_squared < (
            RESOURCE_MIN_SEPARATION
            *
            RESOURCE_MIN_SEPARATION
        ):
            return False

    return True


def get_random_resource_position(used_positions):
    for attempt in range(RESOURCE_RANDOM_ATTEMPTS):

        random_x = random.randint(
            RESOURCE_RANDOM_MIN,
            RESOURCE_RANDOM_MAX
        )

        random_y = random.randint(
            RESOURCE_RANDOM_MIN,
            RESOURCE_RANDOM_MAX
        )

        if is_resource_position_valid(
            random_x,
            random_y,
            used_positions
        ):
            used_positions.append(
                (
                    random_x,
                    random_y
                )
            )

            return random_x, random_y

    # Very unlikely fallback.
    # It prevents restart from failing even if many random attempts
    # happen to land on invalid locations.
    fallback_positions = [
        (-1000, -600),
        (-800, 0),
        (-1000, 500),
        (-500, 900),
        (0, 900),
        (500, 900),
        (1000, 500),
        (900, 0),
        (1000, -600),
        (-500, 300),
        (500, 300),
        (-700, -500),
        (700, -500),
        (-300, 600),
        (300, 600),
        (0, 300),
        (-900, 900),
        (900, 900),
        (-1050, -150),
        (1050, -150),
        (-600, 1050),
        (600, 1050)
    ]

    for fallback_x, fallback_y in fallback_positions:
        if is_resource_position_valid(
            fallback_x,
            fallback_y,
            used_positions
        ):
            used_positions.append(
                (
                    fallback_x,
                    fallback_y
                )
            )

            return fallback_x, fallback_y

    return 0, 700


def create_random_resource_layout():
    random_foods = []
    random_world_items = []

    used_positions = []

    # Keep the same number and types of fruits,
    # but give every fruit a new valid location.
    for food_data in FOOD_START_DATA:
        random_x, random_y = (
            get_random_resource_position(
                used_positions
            )
        )

        random_foods.append(
            {
                "type": food_data["type"],
                "x": random_x,
                "y": random_y,
                "active": True
            }
        )

    # Keep the same number and types of medicine,
    # ammunition and resources, but randomize locations.
    for item_data in ITEM_START_DATA:
        random_x, random_y = (
            get_random_resource_position(
                used_positions
            )
        )

        random_world_items.append(
            {
                "type": item_data["type"],
                "x": random_x,
                "y": random_y,
                "active": True
            }
        )

    return random_foods, random_world_items


# FEATURE 10 - SAFE HAVEN
secured_resources = {"wood": 0, "stone": 0, "supplies": 0}
was_inside_safe_haven = True


def set_feature_message(text):
    global feature_message, feature_message_frame
    feature_message = text
    feature_message_frame = FEATURE_MESSAGE_DURATION


def update_feature_message():
    global feature_message, feature_message_frame
    if feature_message_frame > 0:
        feature_message_frame -= 1
        if feature_message_frame <= 0:
            feature_message_frame = 0
            feature_message = ""


def get_inventory_count():
    total = 0
    for item_name in inventory:
        total += inventory[item_name]
    return total


def is_inventory_full():
    return get_inventory_count() >= INVENTORY_CAPACITY


def get_item_display_name(item_type):
    if item_type == "ammo_pack":
        return "Ammo Pack"
    return item_type.capitalize()


# ---------------- FEATURE 6 ----------------
def update_hunger():
    global player_hunger, hunger_frame, starvation_frame
    if player_dead:
        return
    hunger_frame += 1
    if hunger_frame >= HUNGER_DECREASE_FRAME:
        hunger_frame = 0
        if player_hunger > 0:
            player_hunger -= 1
    if player_hunger <= 0:
        starvation_frame += 1
        if starvation_frame >= STARVATION_DAMAGE_FRAME:
            starvation_frame = 0
            damage_player(1)
    else:
        starvation_frame = 0


def use_food_from_inventory(food_type):
    global player_hunger
    if player_dead:
        return
    if inventory[food_type] <= 0:
        set_feature_message("No " + food_type.capitalize() + " in inventory")
        return
    if player_hunger >= PLAYER_MAX_HUNGER:
        set_feature_message("Hunger already full")
        return
    restore_amount = 15 if food_type == "apple" else 20 if food_type == "banana" else 25
    inventory[food_type] -= 1
    player_hunger += restore_amount
    if player_hunger > PLAYER_MAX_HUNGER:
        player_hunger = PLAYER_MAX_HUNGER
    set_feature_message(food_type.capitalize() + " eaten! +" + str(restore_amount) + " Hunger")


def use_medkit():
    global player_health
    if player_dead:
        return
    if inventory["medkit"] <= 0:
        set_feature_message("No Medkit in inventory")
        return
    if player_health >= PLAYER_MAX_HEALTH:
        set_feature_message("Health already full")
        return
    inventory["medkit"] -= 1
    player_health += 30
    if player_health > PLAYER_MAX_HEALTH:
        player_health = PLAYER_MAX_HEALTH
    set_feature_message("Medkit used! +30 Health")


# ---------------- FEATURE 7 ----------------
def load_ammo_pack():
    global current_ammo
    if inventory["ammo_pack"] <= 0:
        set_feature_message("No Ammo Pack in inventory")
        return
    inventory["ammo_pack"] -= 1
    current_ammo += AMMO_PER_PACK
    set_feature_message("Ammo Pack used! +" + str(AMMO_PER_PACK) + " bullets")


def draw_inventory_hud():
    draw_text(650, 720, "Inventory : " + str(get_inventory_count()) + " / " + str(INVENTORY_CAPACITY))
    draw_text(650, 692, "Ammo : " + str(current_ammo))
    if not inventory_open:
        draw_text(650, 664, "Press I to view inventory")
        return
    draw_text(650, 630, "----- INVENTORY -----")
    draw_text(650, 600, "1 Apple : " + str(inventory["apple"]))
    draw_text(650, 572, "2 Banana : " + str(inventory["banana"]))
    draw_text(650, 544, "3 Mango : " + str(inventory["mango"]))
    draw_text(650, 516, "4 Medkit : " + str(inventory["medkit"]))
    draw_text(650, 488, "5 Ammo Pack : " + str(inventory["ammo_pack"]))
    draw_text(650, 460, "Wood : " + str(inventory["wood"]))
    draw_text(650, 432, "Stone : " + str(inventory["stone"]))
    draw_text(650, 404, "Supplies : " + str(inventory["supplies"]))
    draw_text(650, 368, "SECURED Wood : " + str(secured_resources["wood"]))
    draw_text(650, 340, "SECURED Stone : " + str(secured_resources["stone"]))
    draw_text(650, 312, "SECURED Supplies : " + str(secured_resources["supplies"]))


# ---------------- FEATURE 8 ----------------
def initialize_enemy_feature_data():
    for enemy in enemies:
        if "health" not in enemy:
            enemy["health"] = ENEMY_MAX_HEALTH
        if "active" not in enemy:
            enemy["active"] = True


def fire_bullet():
    global current_ammo
    if player_dead:
        return
    if is_player_inside_shelter():
        set_feature_message("Cannot shoot inside Safe Haven")
        return
    if current_ammo <= 0:
        set_feature_message("No ammunition")
        return
    angle_radian = math.radians(player_angle)
    direction_x = -math.cos(angle_radian)
    direction_y = -math.sin(angle_radian)
    bullets.append({
        "x": player_x + direction_x * 45,
        "y": player_y + direction_y * 45,
        "z": player_z + 95,
        "dx": direction_x,
        "dy": direction_y,
        "travelled": 0
    })
    current_ammo -= 1


def update_bullets():
    initialize_enemy_feature_data()
    bullets_to_remove = []
    for bullet in bullets:
        bullet["x"] += bullet["dx"] * BULLET_SPEED
        bullet["y"] += bullet["dy"] * BULLET_SPEED
        bullet["travelled"] += BULLET_SPEED
        hit_enemy = False
        for enemy in enemies:
            if not enemy.get("active", True):
                continue
            dx = bullet["x"] - enemy["x"]
            dy = bullet["y"] - enemy["y"]
            if dx * dx + dy * dy <= BULLET_HIT_RADIUS * BULLET_HIT_RADIUS:
                enemy["health"] -= BULLET_DAMAGE
                if enemy["health"] <= 0:
                    enemy["health"] = 0
                    enemy["active"] = False

                    if enemy.get("is_alpha", False):
                        set_feature_message("Alpha Creature defeated!")
                    else:
                        set_feature_message("Enemy defeated!")

                else:
                    if enemy.get("is_alpha", False):
                        set_feature_message("Alpha hit! Health: "+ str(enemy["health"])+ " / "+ str(ALPHA_MAX_HEALTH))
                    else:
                        set_feature_message("Enemy hit! Health: " + str(enemy["health"]) + " / " + str(ENEMY_MAX_HEALTH))

                hit_enemy = True
                break
        if hit_enemy or bullet["travelled"] >= BULLET_MAX_DISTANCE:
            bullets_to_remove.append(bullet)
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)


def draw_bullets():
    for bullet in bullets:
        glColor3f(1.0, 0.75, 0.12)
        glPushMatrix()
        glTranslatef(bullet["x"], bullet["y"], bullet["z"])
        glScalef(8, 18, 8)
        glutSolidCube(1)
        glPopMatrix()


# ---------------- FEATURE 9 ----------------
def draw_feature_apple(x, y):
    glColor3f(0.82, 0.06, 0.05)
    glPushMatrix(); glTranslatef(x, y, 20); glScalef(20, 20, 22); gluSphere(gluNewQuadric(), 1, 10, 10); glPopMatrix()
    glColor3f(0.25, 0.12, 0.04)
    glPushMatrix(); glTranslatef(x, y, 40); glScalef(4, 4, 12); glutSolidCube(1); glPopMatrix()


def draw_feature_banana(x, y):
    glColor3f(0.95, 0.78, 0.08)
    glPushMatrix(); glTranslatef(x - 10, y, 18); glRotatef(-25, 0, 1, 0); glScalef(12, 10, 24); gluSphere(gluNewQuadric(), 1, 10, 10); glPopMatrix()
    glPushMatrix(); glTranslatef(x + 10, y, 18); glRotatef(25, 0, 1, 0); glScalef(12, 10, 24); gluSphere(gluNewQuadric(), 1, 10, 10); glPopMatrix()


def draw_feature_mango(x, y):
    glColor3f(0.95, 0.48, 0.06)
    glPushMatrix(); glTranslatef(x, y, 22); glScalef(20, 17, 28); gluSphere(gluNewQuadric(), 1, 10, 10); glPopMatrix()


def draw_feature_medkit(x, y):
    glColor3f(0.90, 0.90, 0.90)
    glPushMatrix(); glTranslatef(x, y, 18); glScalef(35, 25, 25); glutSolidCube(1); glPopMatrix()
    glColor3f(0.80, 0.05, 0.05)
    glPushMatrix(); glTranslatef(x, y - 13, 19); glScalef(7, 2, 20); glutSolidCube(1); glPopMatrix()
    glPushMatrix(); glTranslatef(x, y - 13, 19); glScalef(20, 2, 7); glutSolidCube(1); glPopMatrix()


def draw_feature_ammo_pack(x, y):
    glColor3f(0.18, 0.28, 0.12)
    glPushMatrix(); glTranslatef(x, y, 15); glScalef(35, 25, 25); glutSolidCube(1); glPopMatrix()
    glColor3f(0.75, 0.65, 0.18)
    glPushMatrix(); glTranslatef(x, y - 13, 15); glScalef(18, 2, 5); glutSolidCube(1); glPopMatrix()


def draw_feature_wood(x, y):
    glColor3f(0.35, 0.18, 0.06)
    glPushMatrix(); glTranslatef(x - 6, y, 12); glRotatef(25, 0, 0, 1); glScalef(10, 35, 10); glutSolidCube(1); glPopMatrix()
    glPushMatrix(); glTranslatef(x + 6, y, 12); glRotatef(-25, 0, 0, 1); glScalef(10, 35, 10); glutSolidCube(1); glPopMatrix()


def draw_feature_stone(x, y):
    glColor3f(0.48, 0.48, 0.50)
    glPushMatrix(); glTranslatef(x, y, 14); glScalef(22, 18, 15); gluSphere(gluNewQuadric(), 1, 10, 10); glPopMatrix()


def draw_feature_supplies(x, y):
    glColor3f(0.36, 0.24, 0.12)
    glPushMatrix(); glTranslatef(x, y, 20); glScalef(42, 34, 34); glutSolidCube(1); glPopMatrix()
    glColor3f(0.70, 0.55, 0.20)
    glPushMatrix(); glTranslatef(x, y - 18, 20); glScalef(30, 3, 6); glutSolidCube(1); glPopMatrix()


def draw_feature_world_items():
    for food in foods:
        if not food["active"]:
            continue
        if food["type"] == "apple": draw_feature_apple(food["x"], food["y"])
        elif food["type"] == "banana": draw_feature_banana(food["x"], food["y"])
        elif food["type"] == "mango": draw_feature_mango(food["x"], food["y"])
    for item in world_items:
        if not item["active"]:
            continue
        if item["type"] == "medkit": draw_feature_medkit(item["x"], item["y"])
        elif item["type"] == "ammo_pack": draw_feature_ammo_pack(item["x"], item["y"])
        elif item["type"] == "wood": draw_feature_wood(item["x"], item["y"])
        elif item["type"] == "stone": draw_feature_stone(item["x"], item["y"])
        elif item["type"] == "supplies": draw_feature_supplies(item["x"], item["y"])


def try_collect_feature_item(item, pickup_radius):
    if player_dead or not item["active"]:
        return False

    dx = player_x - item["x"]
    dy = player_y - item["y"]

    if dx * dx + dy * dy > pickup_radius * pickup_radius:
        return False

    if is_inventory_full():
        set_feature_message(
            "Inventory full! "
            + str(INVENTORY_CAPACITY)
            + " / "
            + str(INVENTORY_CAPACITY)
        )
        return False

    item_type = item["type"]

    inventory[item_type] += 1

    # Remove collected item from playground
    item["active"] = False

    # Start respawn countdown
    item["respawn_timer"] = RESOURCE_RESPAWN_FRAMES

    set_feature_message(
        get_item_display_name(item_type)
        + " collected!"
    )

    return True
def update_resource_gathering():
    
    for food in foods:
        if try_collect_feature_item(food, FOOD_PICKUP_RADIUS):
            return
    for item in world_items:
        if try_collect_feature_item(item, ITEM_PICKUP_RADIUS):
            return
def update_resource_respawning():

    # ==========================================
    # GET POSITIONS OF ALL ACTIVE ITEMS
    # ==========================================

    used_positions = []

    for food in foods:

        if food.get("active", True):

            used_positions.append(
                (
                    food["x"],
                    food["y"]
                )
            )


    for item in world_items:

        if item.get("active", True):

            used_positions.append(
                (
                    item["x"],
                    item["y"]
                )
            )


    # ==========================================
    # CHECK ALL COLLECTIBLES
    # ==========================================

    all_collectibles = (
        foods
        +
        world_items
    )


    for item in all_collectibles:

        # Item still exists on playground.
        # No respawn needed.
        if item.get("active", True):
            continue


        # ======================================
        # RESPAWN TIMER
        # ======================================

        timer = item.get(
            "respawn_timer",
            RESOURCE_RESPAWN_FRAMES
        )


        if timer > 0:

            item["respawn_timer"] = (
                timer - 1
            )

            continue


        # ======================================
        # FIND NEW RANDOM VALID POSITION
        # ======================================

        for attempt in range(
            RESOURCE_RANDOM_ATTEMPTS
        ):

            random_x = random.randint(
                RESOURCE_RANDOM_MIN,
                RESOURCE_RANDOM_MAX
            )

            random_y = random.randint(
                RESOURCE_RANDOM_MIN,
                RESOURCE_RANDOM_MAX
            )


            # ==================================
            # DON'T SPAWN BESIDE PLAYER
            # ==================================

            dx = random_x - player_x
            dy = random_y - player_y

            player_distance_squared = (
                dx * dx
                +
                dy * dy
            )


            if player_distance_squared < (
                RESOURCE_RESPAWN_PLAYER_CLEAR_RADIUS
                *
                RESOURCE_RESPAWN_PLAYER_CLEAR_RADIUS
            ):

                continue


            # ==================================
            # USE YOUR EXISTING FEATURE 9
            # VALID POSITION CHECK
            # ==================================

            if is_resource_position_valid(
                random_x,
                random_y,
                used_positions
            ):

                item["x"] = random_x
                item["y"] = random_y

                item["active"] = True

                item["respawn_timer"] = 0


                # Reserve this position so another
                # respawning item cannot use it.
                used_positions.append(
                    (
                        random_x,
                        random_y
                    )
                )


       


                break

# ---------------- FEATURE 10 ----------------
def secure_expedition_resources():
    secured_anything = False
    for resource_name in ["wood", "stone", "supplies"]:
        amount = inventory[resource_name]
        if amount > 0:
            secured_resources[resource_name] += amount
            inventory[resource_name] = 0
            secured_anything = True
    if secured_anything:
        set_feature_message("SAFE HAVEN - Expedition resources secured")


def update_safe_haven_state():
    global was_inside_safe_haven
    inside_now = is_player_inside_shelter()
    if inside_now and not was_inside_safe_haven:
        secure_expedition_resources()
    was_inside_safe_haven = inside_now


# ============================================================
# EXTENSIONS OF EXISTING FEATURE 1-5 FUNCTIONS
# The originals above stay untouched; these wrappers add 6-10.
# ============================================================

_original_draw_all_enemies = draw_all_enemies
def draw_all_enemies():
    initialize_enemy_feature_data()
    for enemy in enemies:
        if enemy.get("active", True):
            draw_enemy(enemy)


_original_enemy_can_see_player = enemy_can_see_player
def enemy_can_see_player(enemy):
    if is_player_inside_shelter():
        return False
    if not enemy.get("active", True):
        return False
    return _original_enemy_can_see_player(enemy)


_original_keyboardListener = keyboardListener
def keyboardListener(key, x, y):
    global inventory_open
    if player_dead:
        _original_keyboardListener(key, x, y)
        return
    if key == b'i' or key == b'I':
        inventory_open = not inventory_open
        glutPostRedisplay(); return
    if key == b'1':
        use_food_from_inventory("apple"); glutPostRedisplay(); return
    if key == b'2':
        use_food_from_inventory("banana"); glutPostRedisplay(); return
    if key == b'3':
        use_food_from_inventory("mango"); glutPostRedisplay(); return
    if key == b'4':
        use_medkit(); glutPostRedisplay(); return
    if key == b'5':
        load_ammo_pack(); glutPostRedisplay(); return
    _original_keyboardListener(key, x, y)


_original_mouseListener = mouseListener
def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet(); glutPostRedisplay(); return
    _original_mouseListener(button, state, x, y)


_original_restart_game = restart_game
def restart_game():
    global player_hunger, hunger_frame, starvation_frame
    global inventory, inventory_open, current_ammo, bullets
    global foods, world_items, secured_resources
    global feature_message, feature_message_frame, was_inside_safe_haven
    global first_person_mode
    global fps_camera_angle 

    _original_restart_game()

    # Always restart in the original starting camera mode.
    first_person_mode = False
    fps_camera_angle=270.0 
    player_hunger = PLAYER_MAX_HUNGER
    hunger_frame = 0
    starvation_frame = 0
    inventory = {"apple": 0, "banana": 0, "mango": 0, "medkit": 0, "ammo_pack": 0, "wood": 0, "stone": 0, "supplies": 0}
    inventory_open = False
    current_ammo = 10
    bullets = []
    # FEATURE 9:
    # After pressing R, create a completely new resource layout.
    foods, world_items = create_random_resource_layout()

    secured_resources = {"wood": 0, "stone": 0, "supplies": 0}
    feature_message = ""
    feature_message_frame = 0
    was_inside_safe_haven = True
    initialize_enemy_feature_data()


_original_idle = idle
def idle():
    _original_idle()
    update_hunger()
    update_resource_gathering()
    update_resource_respawning()
    update_bullets()
    update_safe_haven_state()
    update_feature_message()
    glutPostRedisplay()


def draw_survival_and_state_hud():

    draw_text(
        20,
        664,
        "Hunger : "
        +
        str(player_hunger)
        +
        " / "
        +
        str(PLAYER_MAX_HUNGER)
    )

    if is_player_inside_shelter():

        draw_text(
            20,
            636,
            "State : SAFE HAVEN"
        )

    else:

        draw_text(
            20,
            636,
            "State : EXPEDITION"
        )


    # ==========================================
    # TEMPORARY GAME MESSAGE
    # ==========================================
    # Kept far away from Hunger, State,
    # Escape Kit and Inventory HUD.
    if feature_message != "":
        draw_text(
            20,
            590,
            feature_message
        )


_original_showScreen = showScreen
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setupCamera()
    draw_environment()

    if not is_player_inside_shelter():
        draw_feature_world_items()

    draw_bullets()

    if not is_player_inside_shelter():
        draw_player()

    if is_camera_behind_shelter():
        draw_safe_haven()
        draw_shelter_torches()

    draw_text(10, 770, "CaveBound : Survival Game")
    if first_person_mode:
        draw_text(15, 742, "View : FPS")
    else:
        draw_text(15, 742, "View : TPS")

    draw_health_hud()
    if not player_dead and is_player_hiding():
        draw_text(20, 692, "Hide mode:Activated")

    draw_survival_and_state_hud()
    draw_inventory_hud()
    draw_game_over()
    glutSwapBuffers()


initialize_enemy_feature_data()


# ============================================================
# FEATURES 11-15 
# ============================================================

# ---------------- FEATURE 11 - EXPEDITION / EXTRACTION ----------------
# Feature 10 already banks wood/stone/supplies whenever the player
# walks back into the Safe Haven alive (see secure_expedition_resources).
# This adds the other half: dying on an expedition wipes out whatever
# expedition resources had not been secured yet.
was_dead_last_frame_for_extraction = False


def handle_expedition_extraction():
    global was_dead_last_frame_for_extraction
    if player_dead and not was_dead_last_frame_for_extraction:
        lost_anything = False
        for resource_name in ["wood", "stone", "supplies"]:
            if inventory[resource_name] > 0:
                inventory[resource_name] = 0
                lost_anything = True
        if lost_anything:
            set_feature_message("You died! Unsecured resources were lost.")
        was_dead_last_frame_for_extraction = True
    elif not player_dead:
        was_dead_last_frame_for_extraction = False


# ---------------- FEATURE 12 - ADAPTIVE ENEMY WAVE SYSTEM ----------------
WAVE_BASE_ENEMY_COUNT = len(ENEMY_START_DATA)
WAVE_ENEMY_INCREMENT = 2
TOTAL_NORMAL_WAVES = 3
WAVE_TRANSITION_DELAY = 90
ENEMY_SPAWN_CLEAR_RADIUS = 500

wave_number = 1
waiting_for_next_wave = False
wave_transition_timer = 0


def get_random_enemy_spawn_position(used_positions):
    limit = GRID_LENGTH - CAVE_COLLISION_MARGIN - 40
    for attempt in range(300):
        random_x = random.randint(-int(limit), int(limit))
        random_y = random.randint(-int(limit), int(limit))

        shelter_dx = random_x - SHELTER_CENTER_X
        shelter_dy = random_y - SHELTER_CENTER_Y
        if (shelter_dx * shelter_dx + shelter_dy * shelter_dy) < (ENEMY_SPAWN_CLEAR_RADIUS * ENEMY_SPAWN_CLEAR_RADIUS):
            continue

        if not can_enemy_move_to(random_x, random_y):
            continue

        too_close = False
        for used_x, used_y in used_positions:
            dx = random_x - used_x
            dy = random_y - used_y
            if dx * dx + dy * dy < 150 * 150:
                too_close = True
                break
        if too_close:
            continue

        used_positions.append((random_x, random_y))
        return random_x, random_y

    # Fallback: reuse one of the original starting spots.
    fallback = ENEMY_START_DATA[len(used_positions) % len(ENEMY_START_DATA)]
    used_positions.append((fallback["x"], fallback["y"]))
    return fallback["x"], fallback["y"]


def spawn_wave(wave_num):
    global enemies
    enemy_count = WAVE_BASE_ENEMY_COUNT + (wave_num - 1) * WAVE_ENEMY_INCREMENT
    used_positions = []
    new_enemies = []
    for _ in range(enemy_count):
        spawn_x, spawn_y = get_random_enemy_spawn_position(used_positions)
        new_enemies.append({
            "x": spawn_x,
            "y": spawn_y,
            "angle": random.uniform(0, 360),
            "health": ENEMY_MAX_HEALTH,
            "active": True
        })
    enemies = new_enemies
    set_feature_message("Wave " + str(wave_num) + " incoming! (" + str(enemy_count) + " enemies)")


def is_current_wave_cleared():
    if not enemies:
        return True
    return all(not enemy.get("active", True) for enemy in enemies)


def update_wave_system():
    global wave_number, waiting_for_next_wave, wave_transition_timer
    if player_dead:
        return
    if alpha_spawned:
        # Boss encounter replaces normal wave spawning entirely.
        return
    if not is_current_wave_cleared():
        waiting_for_next_wave = False
        return

    if not waiting_for_next_wave:
        waiting_for_next_wave = True
        wave_transition_timer = WAVE_TRANSITION_DELAY
        return

    wave_transition_timer -= 1
    if wave_transition_timer <= 0:
        waiting_for_next_wave = False
        if wave_number >= TOTAL_NORMAL_WAVES:
            spawn_alpha_creature()
        else:
            wave_number += 1
            spawn_wave(wave_number)


# ---------------- FEATURE 13 - RESOURCE CRAFTING ----------------
CRAFTING_RECIPES = {
    "medkit": {"wood": 1, "supplies": 1},
    "ammo_pack": {"wood": 1, "stone": 1, "supplies": 0},
    "escape_kit": {"wood": 1, "stone": 1, "supplies": 1}
}
if "escape_kit" not in inventory:
    inventory["escape_kit"] = 0


def has_required_materials(recipe):

    for material, required_amount in recipe.items():

        current_amount = secured_resources.get(
            material,
            0
        )

        if current_amount < required_amount:
            return False

    return True


def craft_item(item_name):

    if player_dead or player_won:
        return

    # Craft only at Safe Haven
    if not is_player_inside_shelter():

        set_feature_message(
            "Return to Safe Haven to craft"
        )

        return


    recipe = CRAFTING_RECIPES.get(
        item_name
    )

    if recipe is None:
        return


    # Check SECURED resources
    if not has_required_materials(recipe):

        set_feature_message(
            "Not enough secured materials"
        )

        return


    # Check inventory space
    if get_inventory_count() >= INVENTORY_CAPACITY:

        set_feature_message(
            "Inventory full"
        )

        return


    # Remove materials from SECURED resources
    for material, required_amount in recipe.items():

        secured_resources[material] -= required_amount


    # Add crafted item
    inventory[item_name] = (
        inventory.get(item_name, 0)
        + 1
    )


    set_feature_message(
        get_item_display_name(item_name)
        + " crafted!"
    )


# ---------------- FEATURE 14 - ALPHA CREATURE / BOSS ----------------
ALPHA_MAX_HEALTH = 150
ALPHA_ATTACK_DAMAGE = 22
ALPHA_CHASE_SPEED = 2.6
ALPHA_MOVE_SPEED = 1.6
ALPHA_ATTACK_DISTANCE = 95
ALPHA_DETECTION_DISTANCE = 420
ALPHA_SCALE = 1.9
ALPHA_REWARD_RESOURCE_AMOUNT = 5

alpha_spawned = False
alpha_defeated = False
alpha_enemy = None


def spawn_alpha_creature():
    global enemies, alpha_spawned, alpha_enemy
    spawn_x, spawn_y = get_random_enemy_spawn_position([])
    boss = {
        "x": spawn_x,
        "y": spawn_y,
        "angle": 0.0,
        "health": ALPHA_MAX_HEALTH,
        "active": True,
        "is_alpha": True,
        "memory_timer": 0
    }
    enemies = [boss]
    alpha_enemy = boss
    alpha_spawned = True
    set_feature_message("THE ALPHA CREATURE HAS AWAKENED!")


def alpha_chase_player(enemy):
    enemy["is_attacking"] = False
    enemy["attack_frame"] = 0
    enemy["damage_given"] = False

    dx = player_x - enemy["x"]
    dy = player_y - enemy["y"]
    distance = math.sqrt(dx * dx + dy * dy)
    if distance == 0:
        return

    ux = dx / distance
    uy = dy / distance
    new_x = enemy["x"] + ux * ALPHA_CHASE_SPEED
    new_y = enemy["y"] + uy * ALPHA_CHASE_SPEED

    if can_enemy_move_to(new_x, new_y):
        enemy["x"] = new_x
        enemy["y"] = new_y
    elif can_enemy_move_to(new_x, enemy["y"]):
        enemy["x"] = new_x
    elif can_enemy_move_to(enemy["x"], new_y):
        enemy["y"] = new_y

    enemy["angle"] = math.degrees(math.atan2(uy, ux))


def alpha_attack(enemy):
    dx = player_x - enemy["x"]
    dy = player_y - enemy["y"]
    enemy["angle"] = math.degrees(math.atan2(dy, dx))
    enemy["is_attacking"] = True

    if "attack_frame" not in enemy:
        enemy["attack_frame"] = 0
    if "damage_given" not in enemy:
        enemy["damage_given"] = False

    enemy["attack_frame"] += 1
    if enemy["attack_frame"] >= ENEMY_DAMAGE_FRAME and not enemy["damage_given"]:
        damage_player(ALPHA_ATTACK_DAMAGE)
        enemy["damage_given"] = True
    if enemy["attack_frame"] >= ENEMY_ATTACK_DURATION:
        enemy["attack_frame"] = 0
        enemy["damage_given"] = False


def alpha_wander(enemy):
    enemy["is_attacking"] = False
    enemy["attack_frame"] = 0
    enemy["damage_given"] = False
    angle_radian = math.radians(enemy["angle"])
    direction_x = math.cos(angle_radian)
    direction_y = math.sin(angle_radian)
    new_x = enemy["x"] + direction_x * ALPHA_MOVE_SPEED
    new_y = enemy["y"] + direction_y * ALPHA_MOVE_SPEED
    if can_enemy_move_to(new_x, new_y):
        enemy["x"] = new_x
        enemy["y"] = new_y
    else:
        enemy["angle"] += 135
        if enemy["angle"] >= 360:
            enemy["angle"] -= 360


def update_alpha_creature():
    if alpha_enemy is None or not alpha_enemy.get("active", True):
        return
    if player_dead:
        alpha_enemy["is_attacking"] = False
        alpha_enemy["attack_frame"] = 0
        alpha_enemy["damage_given"] = False
        return

    distance_to_player = get_distance_between_points(
        alpha_enemy["x"], alpha_enemy["y"], player_x, player_y
    )
    can_see_player = enemy_can_see_player(alpha_enemy)

    if distance_to_player <= ALPHA_DETECTION_DISTANCE and can_see_player:
        if distance_to_player <= ALPHA_ATTACK_DISTANCE:
            alpha_attack(alpha_enemy)
        else:
            alpha_chase_player(alpha_enemy)
    else:
        alpha_wander(alpha_enemy)


def check_alpha_defeat():
    global alpha_defeated
    if not alpha_spawned or alpha_defeated:
        return
    if alpha_enemy is not None and not alpha_enemy.get("active", True):
        alpha_defeated = True
        secured_resources["wood"] += ALPHA_REWARD_RESOURCE_AMOUNT
        secured_resources["stone"] += ALPHA_REWARD_RESOURCE_AMOUNT
        secured_resources["supplies"] += ALPHA_REWARD_RESOURCE_AMOUNT
        inventory["escape_kit"] = inventory.get("escape_kit", 0) + 1
        set_feature_message("ALPHA CREATURE DEFEATED! Escape Kit obtained!")


def draw_alpha_aura(enemy):
    glPushMatrix()
    glColor3f(0.65, 0.05, 0.75)
    glTranslatef(enemy["x"], enemy["y"], 3)
    glScalef(1.4, 1.4, 0.12)
    gluSphere(gluNewQuadric(), 55, 14, 14)
    glPopMatrix()


def draw_scaled_enemy(enemy, scale):
    glPushMatrix()
    glTranslatef(enemy["x"], enemy["y"], 0)
    glScalef(scale, scale, scale)
    glTranslatef(-enemy["x"], -enemy["y"], 0)
    draw_enemy(enemy)
    glPopMatrix()


def draw_alpha_health_bar():
    if alpha_enemy is None or not alpha_enemy.get("active", True):
        return
    draw_text(340, 770, "ALPHA : " + str(alpha_enemy["health"]) + " / " + str(ALPHA_MAX_HEALTH))


# ---------------- FEATURE 15 - MISSION / ESCAPE PROGRESSION ----------------
player_won = False


def is_escape_ready():
    return alpha_defeated and inventory.get("escape_kit", 0) >= 1


def attempt_escape():
    global player_won
    if player_dead or player_won:
        return
    if not is_player_inside_shelter():
        set_feature_message("Return to the Safe Haven to escape")
        return
    if not alpha_defeated:
        set_feature_message("Defeat the Alpha Creature before you can escape")
        return
    if inventory.get("escape_kit", 0) < 1:
        set_feature_message("You need an Escape Kit to escape (craft one or defeat the Alpha)")
        return
    inventory["escape_kit"] -= 1
    player_won = True
    set_feature_message("YOU ESCAPED CAVEBOUND!")

def draw_mission_hud():

    # Don't show anything until player
    # actually has an Escape Kit
    if inventory.get("escape_kit", 0) <= 0:
        return

    # Don't overlap temporary messages
    if feature_message != "":
        return

    draw_text(
        20,
        590,
        "Escape Kit : "
        +
        str(
            inventory.get(
                "escape_kit",
                0
            )
        )
    )

def draw_enemy_count_hud():

    enemy_count = 0

    for enemy in enemies:

        if enemy.get("active", True):
            enemy_count += 1

    draw_text(
        20,
        562,
        "Enemies : "
        +
        str(enemy_count)
    )
def draw_victory_screen():
    if not player_won:
        return
    draw_text(400, 420, "MISSION COMPLETE - YOU ESCAPED CAVEBOUND!")
    draw_text(430, 392, "PRESS R TO PLAY AGAIN")


# ============================================================
# These wrappers add 11-15 on top of it.
# ============================================================

_original_update_enemy_wandering = update_enemy_wandering
def update_enemy_wandering():
    if alpha_spawned:
        update_alpha_creature()
        return
    _original_update_enemy_wandering()


_original_draw_all_enemies_11_15 = draw_all_enemies
def draw_all_enemies():
    initialize_enemy_feature_data()
    for enemy in enemies:
        if not enemy.get("active", True):
            continue
        if enemy.get("is_alpha", False):
            draw_alpha_aura(enemy)
            draw_scaled_enemy(enemy, ALPHA_SCALE)
        else:
            draw_enemy(enemy)


_original_keyboardListener_11_15 = keyboardListener
def keyboardListener(key, x, y):
    if player_won:
        if key == b'r':
            restart_game()
            glutPostRedisplay()
        return

    if player_dead:
        _original_keyboardListener_11_15(key, x, y)
        return

    if key == b'6':
        craft_item("medkit"); glutPostRedisplay(); return
    if key == b'7':
        craft_item("ammo_pack"); glutPostRedisplay(); return
    if key == b'8':
        craft_item("escape_kit"); glutPostRedisplay(); return
    if key == b'e' or key == b'E':
        attempt_escape(); glutPostRedisplay(); return

    _original_keyboardListener_11_15(key, x, y)


_original_restart_game_11_15 = restart_game
def restart_game():
    global wave_number, waiting_for_next_wave, wave_transition_timer
    global alpha_spawned, alpha_defeated, alpha_enemy
    global player_won, was_dead_last_frame_for_extraction

    _original_restart_game_11_15()

    wave_number = 1
    waiting_for_next_wave = False
    wave_transition_timer = 0
    alpha_spawned = False
    alpha_defeated = False
    alpha_enemy = None
    player_won = False
    was_dead_last_frame_for_extraction = False
    inventory["escape_kit"] = 0


_original_idle_11_15 = idle
def idle():
    _original_idle_11_15()
    if not player_won:
        handle_expedition_extraction()
        update_wave_system()
        check_alpha_defeat()
    glutPostRedisplay()


_original_showScreen_11_15 = showScreen
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setupCamera()
    draw_environment()

    if not is_player_inside_shelter():
        draw_feature_world_items()

    draw_bullets()

    if not is_player_inside_shelter():
        draw_player()

    if is_camera_behind_shelter():
        draw_safe_haven()
        draw_shelter_torches()

    draw_text(10, 770, "CaveBound : Survival Game")
    if first_person_mode:
        draw_text(15, 742, "View : FPS")
    else:
        draw_text(15, 742, "View : TPS")

    draw_health_hud()
    draw_alpha_health_bar()
    if not player_dead and is_player_hiding():
        draw_text(20, 692, "Hide mode:Activated")

    draw_survival_and_state_hud()
    draw_inventory_hud()
    draw_enemy_count_hud()
    draw_mission_hud()
    draw_game_over()
    draw_victory_screen()
    glutSwapBuffers()


if __name__ == "__main__":
    main()