from typing import List, Dict, Optional
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, INITIAL_LIVES, 
    PLAYER_SPEED, PLAYER_SIZE, WAVE_DURATION
)
import time


class GameState:
    def __init__(self, player=None, map_generator=None) -> None:
        # Instances
        self.player = player
        self.map_generator = map_generator
        
        # Game status
        self.score: int = 0
        self.lives: int = INITIAL_LIVES
        self.is_paused: bool = False
        self.game_over: bool = False
        self.current_wave: int = 1
        self.wave_timer: float = WAVE_DURATION
        
        # Time tracking
        self.last_frame_time: float = time.time()
        self.pause_start_time: float = 0.0
        self.total_pause_time: float = 0.0

        # Player state
        self.player_x: float = WINDOW_WIDTH // 2
        self.player_y: float = WINDOW_HEIGHT // 2
        self.player_speed: float = PLAYER_SPEED
        self.player_size: int = PLAYER_SIZE
        self.player_bullets: List[Dict[str, float]] = []

        # Enemy state
        self.enemies: List[Dict] = []
        self.enemy_bullets: List[Dict] = []
        self.enemy_spawn_timer: float = 0

        # Power-ups
        self.active_powerups: List[Dict] = []
        self.available_powerups: List[Dict] = []
        
        # Movement state
        self.movement: Dict[str, bool] = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

    def reset(self) -> None:
        # Keep both player and map_generator instances when resetting
        player = self.player
        map_generator = self.map_generator
        self.__init__(player, map_generator)

    def update_pause_time(self, raw_current_time: float) -> None:
        if self.is_paused:
            if self.pause_start_time == 0:
                self.pause_start_time = raw_current_time
                print("Game Paused")
        else:
            if self.pause_start_time != 0:
                self.total_pause_time += raw_current_time - self.pause_start_time
                self.pause_start_time = 0
                self.last_frame_time = raw_current_time  # Reset frame time
                print("Game Resumed")

    def get_active_powerup(self, effect_type: str) -> Optional[Dict]:
        return next(
            (p for p in self.active_powerups if p["effect"] == effect_type),
            None
        )
