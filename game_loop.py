import random
import time
import math
from typing import List, Dict, Any
from OpenGL.GL import *
from OpenGL.GLUT import *
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WAVE_DURATION,
    WAVE_CONFIGS,
    ENEMY_TYPES,
    POWERUP_TYPES,
    PLAYER_BULLET_COLOR,
)
from game_state import GameState
from player import Player
from render import Render
from ui import UI
from collision_manager import CollisionManager
from controls import Controls
from map_generator import MapGenerator


class GameLoop:
    def __init__(
        self,
        game_state: GameState,
        player: Player,
        render: Render,
        ui: UI,
        collision_manager: CollisionManager,
        controls: Controls,
    ) -> None:
        self.game_state = game_state
        self.player = player
        self.render = render
        self.ui = ui
        self.collision_manager = collision_manager
        self.controls = controls

        self.enemy_spawn_timer = 0.0
        self.powerup_spawn_timer = 0.0

        self._update_terminal_status()

    def display(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)

        self.game_state.map_generator.draw()

        if not self.game_state.game_over:
            self.player.draw(self.game_state.player_x, self.game_state.player_y)

            glColor3f(*PLAYER_BULLET_COLOR)
            for bullet in self.game_state.player_bullets:
                self.render.draw_circle(bullet["x"], bullet["y"], 3)

            for enemy in self.game_state.enemies:
                glColor3f(*ENEMY_TYPES[enemy["type"]]["color"])
                self.render.draw_circle(
                    enemy["x"], enemy["y"], ENEMY_TYPES[enemy["type"]]["size"]
                )

            for bullet in self.game_state.enemy_bullets:
                glColor3f(*ENEMY_TYPES[bullet["source"]]["color"])
                self.render.draw_circle(bullet["x"], bullet["y"], 2)

            for powerup in self.game_state.available_powerups:
                glColor3f(*POWERUP_TYPES[powerup["type"]]["color"])
                self.render.draw_circle(
                    powerup["x"], powerup["y"], POWERUP_TYPES[powerup["type"]]["size"]
                )

        self.ui.draw_restart_button(30, WINDOW_HEIGHT - 30)
        self.ui.draw_pause_play_button(
            WINDOW_WIDTH // 2 - 10, WINDOW_HEIGHT - 30, self.game_state.is_paused
        )
        self.ui.draw_cross_button(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 30)

        glutSwapBuffers()

    def update(self, value: int) -> None:
        current_time = time.time()

        if not self.game_state.game_over:
            if not self.game_state.is_paused:
                # Only update game logic when not paused
                delta_time = current_time - self.game_state.last_frame_time

                self.game_state.wave_timer -= delta_time
                if self.game_state.wave_timer <= 0:
                    self._advance_wave()

                self.controls.update_movement(delta_time)

                self._update_bullets(delta_time)

                self._update_enemies(delta_time)

                self._handle_enemy_spawning(delta_time)

                self._update_powerups(delta_time)

                self.collision_manager.check_all_collisions()

                self.game_state.last_frame_time = current_time
            else:
                # When unpausing, update the last frame time to prevent large delta
                self.game_state.last_frame_time = current_time

            self._update_terminal_status()

        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0)

    def _update_bullets(self, delta_time: float) -> None:
        for bullet in self.game_state.player_bullets[:]:
            bullet["x"] += math.cos(bullet["direction"]) * bullet["speed"] * delta_time
            bullet["y"] += math.sin(bullet["direction"]) * bullet["speed"] * delta_time

            # Remove bullets that are out of window bounds
            is_player_bullet_out_of_bounds = (
                bullet["x"] < 0
                or bullet["x"] > WINDOW_WIDTH
                or bullet["y"] < 0
                or bullet["y"] > WINDOW_HEIGHT
            )
            if is_player_bullet_out_of_bounds:
                self.game_state.player_bullets.remove(bullet)

        for bullet in self.game_state.enemy_bullets[:]:
            bullet["x"] += math.cos(bullet["direction"]) * bullet["speed"] * delta_time
            bullet["y"] += math.sin(bullet["direction"]) * bullet["speed"] * delta_time

            is_enemy_bullet_out_of_bounds = (
                bullet["x"] < 0
                or bullet["x"] > WINDOW_WIDTH
                or bullet["y"] < 0
                or bullet["y"] > WINDOW_HEIGHT
            )

            if is_enemy_bullet_out_of_bounds:
                self.game_state.enemy_bullets.remove(bullet)

    def _update_enemies(self, delta_time: float) -> None:
        for enemy in self.game_state.enemies[:]:
            dx = self.game_state.player_x - enemy["x"]
            dy = self.game_state.player_y - enemy["y"]
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
                speed = ENEMY_TYPES[enemy["type"]]["speed"]
                speed *= WAVE_CONFIGS[self.game_state.current_wave]["speed_multiplier"]

                enemy["x"] += (dx / distance) * speed * delta_time
                enemy["y"] += (dy / distance) * speed * delta_time

            enemy["attack_cooldown"] -= delta_time
            if enemy["attack_cooldown"] <= 0:
                self._handle_enemy_attack(enemy)
                enemy["attack_cooldown"] = ENEMY_TYPES[enemy["type"]]["attack_cooldown"]

    def _handle_enemy_attack(self, enemy: Dict) -> None:
        attack_type = ENEMY_TYPES[enemy["type"]]["attack_type"]

        if attack_type == "melee":
            # Melee attacks are handled in collision detection
            pass
        elif attack_type == "single_shot":
            self._create_enemy_bullet(enemy, 0)
        elif attack_type == "double_shot":
            self._create_enemy_bullet(enemy, 0)
            self._create_enemy_bullet(enemy, math.pi)
        elif attack_type == "quad_shot":
            for i in range(4):
                angle = i * math.pi / 2
                self._create_enemy_bullet(enemy, angle)
        elif attack_type == "burst_shot":
            for i in range(8):
                angle = i * math.pi / 4
                self._create_enemy_bullet(enemy, angle)

    def _create_enemy_bullet(self, enemy: Dict, angle: float) -> None:
        self.game_state.enemy_bullets.append(
            {
                "x": enemy["x"],
                "y": enemy["y"],
                "direction": angle,
                "speed": ENEMY_TYPES[enemy["type"]]["bullet_speed"],
                "source": enemy["type"],
            }
        )

    def _handle_enemy_spawning(self, delta_time: float) -> None:
        self.enemy_spawn_timer -= delta_time
        if self.enemy_spawn_timer <= 0:
            wave_config = WAVE_CONFIGS[self.game_state.current_wave]
            self.enemy_spawn_timer = wave_config["spawn_rate"]

            enemy_type = random.choice(wave_config["enemies"])
            spawn_pos = self.game_state.map_generator.get_random_floor_position()

            self.game_state.enemies.append(
                {
                    "type": enemy_type,
                    "x": spawn_pos[0],
                    "y": spawn_pos[1],
                    "hp": ENEMY_TYPES[enemy_type]["hp"],
                    "attack_cooldown": 0,
                }
            )

    def _update_powerups(self, delta_time: float) -> None:
        for powerup in self.game_state.active_powerups[:]:
            powerup["duration"] -= delta_time
            if powerup["duration"] <= 0:
                self.game_state.active_powerups.remove(powerup)

        # Spawn new powerups
        self.powerup_spawn_timer -= delta_time
        if self.powerup_spawn_timer <= 0:
            self.powerup_spawn_timer = random.uniform(10.0, 20.0)

            if len(self.game_state.available_powerups) < 3:
                powerup_type = random.choice(list(POWERUP_TYPES.keys()))
                spawn_pos = self.game_state.map_generator.get_random_floor_position()

                self.game_state.available_powerups.append(
                    {"type": powerup_type, "x": spawn_pos[0], "y": spawn_pos[1]}
                )

    def _advance_wave(self) -> None:
        self.game_state.current_wave += 1
        if self.game_state.current_wave > 4:
            self.game_state.game_over = True
            grade_info = self._calculate_grade()
            print(
                f"Congratulations! Semester completed!\n"
                f"Final Grade: {grade_info['grade']} (GPA: {grade_info['gpa']})\n"
                f"Performance: {grade_info['description']}"
            )
        else:
            self.game_state.wave_timer = WAVE_DURATION
            print(f"Starting Semester {self.game_state.current_wave}")

    def _calculate_grade(self) -> Dict:
        from constants import GRADE_THRESHOLDS

        for threshold, grade_info in sorted(
            GRADE_THRESHOLDS.items(), key=lambda x: x[0], reverse=True
        ):
            if self.game_state.score >= threshold:
                return grade_info
        return GRADE_THRESHOLDS[0]  # Return F if below all thresholds

    def _update_terminal_status(self) -> None:
        """Update terminal display only when game state changes"""
        status = (
            f"\033[2J\033[H"  # Clear screen and move cursor to top
            f"Academic Status:\n"
            f"================\n"
            f"Academic Comebacks (Lives): {self.game_state.lives}\n"
            f"Current Score: {self.game_state.score}\n"
            f"Current Month: {self.game_state.current_wave}/4\n"
            f"Days Remaining: {int(self.game_state.wave_timer)} days\n"
            f"Game Status: {'PAUSED' if self.game_state.is_paused else 'ACTIVE'}\n"
            f"Active Power-ups:\n"
        )

        if self.game_state.active_powerups:
            for powerup in self.game_state.active_powerups:
                status += f"- {powerup['type']}: {powerup['duration']:.1f}s remaining\n"
        else:
            status += "- None\n"

        if self.game_state.game_over:
            grade_info = self._calculate_grade()
            status += (
                f"\nGAME OVER!\n"
                f"Final Grade: {grade_info['grade']} (GPA: {grade_info['gpa']})\n"
                f"Performance: {grade_info['description']}\n"
            )

        print(status, end="")
