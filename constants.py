# Window Settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Colors (RGB)
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
PURPLE = (0.5, 0.0, 0.5)
CYAN = (0.0, 0.8, 0.8)
ORANGE = (1.0, 0.5, 0.0)
GREY=(0.5, 0.5, 0.5)

# Player Settings
PLAYER_COLOR = WHITE
PLAYER_SIZE = 30
PLAYER_SPEED = 200.0
PLAYER_BULLET_COLOR = BLUE
PLAYER_BULLET_SPEED = 300.0
PLAYER_BULLET_SIZE = 5
INITIAL_LIVES = 3

# Enemy Settings
ENEMY_TYPES = {
    "QUIZ": {
        "color": GREY,
        "size": 20,
        "speed": 100,
        "hp": 1,
        "points": 1,
        "attack_type": "melee",
        "attack_range": 30,
        "attack_cooldown": 1.0,
    },
    "ASSIGNMENT": {
        "color": YELLOW,
        "size": 25,
        "speed": 80,
        "hp": 2,
        "points": 2,
        "attack_type": "single_shot",
        "bullet_speed": 150,
        "attack_cooldown": 2.0,
    },
    "PRESENTATION": {
        "color": RED,
        "size": 35,
        "speed": 50,
        "hp": 4,
        "points": 4,
        "attack_type": "quad_shot",
        "bullet_speed": 250,
        "attack_cooldown": 4.0,
    },
    "MIDTERM": {
        "color": PURPLE,
        "size": 30,
        "speed": 60,
        "hp": 3,
        "points": 3,
        "attack_type": "double_shot",
        "bullet_speed": 200,
        "attack_cooldown": 3.0,
    },
    "FINAL": {
        "color": ORANGE,
        "size": 28,
        "speed": 90,
        "hp": 2,
        "points": 2,
        "attack_type": "burst_shot",
        "bullet_speed": 180,
        "attack_cooldown": 2.5,
    },
}

# Power-up Settings
POWERUP_TYPES = {
    "CHATGPT": {
        "color": CYAN,
        "size": 15,
        "duration": 5.0,
        "effect": "speed_boost",
        "multiplier": 2.0,
    },
    "CHEGG": {
        "color": ORANGE,
        "size": 15,
        "duration": 3.0,
        "effect": "spread_shot",
        "bullets": 8,
    },
    "QUILLBOT": {
        "color": GREEN,
        "size": 15,
        "duration": 4.0,
        "effect": "bullet_speed",
        "multiplier": 1.5,
    },
    "GRAMMARLY": {
        "color": PURPLE,
        "size": 15,
        "duration": 4.0,
        "effect": "bullet_size",
        "multiplier": 1.5,
    },
}

# Wave Settings
WAVE_DURATION = 30.0  # seconds
WAVE_CONFIGS = {
    1: {"enemies": ["QUIZ", "ASSIGNMENT"], "spawn_rate": 2.0, "speed_multiplier": 1.0},
    2: {
        "enemies": ["QUIZ", "ASSIGNMENT", "MIDTERM"],
        "spawn_rate": 1.5,
        "speed_multiplier": 1.2,
    },
    3: {
        "enemies": ["QUIZ", "ASSIGNMENT", "MIDTERM", "PRESENTATION"],
        "spawn_rate": 1.0,
        "speed_multiplier": 1.4,
    },
    4: {
        "enemies": ["QUIZ", "ASSIGNMENT", "MIDTERM", "PRESENTATION", "FINAL"],
        "spawn_rate": 0.8,
        "speed_multiplier": 1.6,
    },
}

# Map Settings
MAP_TILE_SIZE = 40
MAP_MIN_ROOMS = 8
MAP_MAX_ROOMS = 12
MAP_MIN_ROOM_SIZE = 6
MAP_MAX_ROOM_SIZE = 12
MAP_COLORS = {
    "WALL": (0.3, 0.3, 0.3),
    "FLOOR": (0.1, 0.1, 0.1),
    "CORRIDOR": (0.15, 0.15, 0.15),
}

# UI Settings
BUTTON_SIZE = 20
RESTART_BUTTON_COLOR = GREEN
PAUSE_PLAY_BUTTON_COLOR = YELLOW
CROSS_BUTTON_COLOR = RED

# Game Status
GRADE_THRESHOLDS = {
    90: {"grade": "A", "gpa": 4.0, "description": "Excellent"},
    85: {"grade": "A-", "gpa": 3.7, "description": "Very Good"},
    80: {"grade": "B+", "gpa": 3.3, "description": "Good Plus"},
    75: {"grade": "B", "gpa": 3.0, "description": "Good"},
    70: {"grade": "B-", "gpa": 2.7, "description": "Good Minus"},
    65: {"grade": "C+", "gpa": 2.3, "description": "Fair Plus"},
    60: {"grade": "C", "gpa": 2.0, "description": "Fair"},
    57: {"grade": "C-", "gpa": 1.7, "description": "Fair Minus"},
    55: {"grade": "D+", "gpa": 1.3, "description": "Poor Plus"},
    52: {"grade": "D", "gpa": 1.0, "description": "Poor"},
    50: {"grade": "D-", "gpa": 0.7, "description": "Poor Minus"},
    0: {"grade": "F", "gpa": 0.0, "description": "Failure"}
}
