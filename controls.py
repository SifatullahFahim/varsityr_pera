from OpenGL.GLUT import *
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_BULLET_SPEED
import math


class Controls:
    def __init__(self, game_state, ui) -> None:
        self.game_state = game_state
        self.ui = ui

    def update_movement(self, delta_time: float) -> None:
        if self.game_state.game_over or self.game_state.is_paused:
            return

        speed_powerup = self.game_state.get_active_powerup("speed_boost")
        speed_multiplier = speed_powerup["multiplier"] if speed_powerup else 1.0

        movement_x = movement_y = 0
        if self.game_state.movement["up"]:
            movement_y += self.game_state.player_speed * delta_time
        if self.game_state.movement["down"]:
            movement_y -= self.game_state.player_speed * delta_time
        if self.game_state.movement["left"]:
            movement_x -= self.game_state.player_speed * delta_time
        if self.game_state.movement["right"]:
            movement_x += self.game_state.player_speed * delta_time

        movement_x *= speed_multiplier
        movement_y *= speed_multiplier

        hitbox = self.game_state.player.get_hitbox(
            self.game_state.player_x, self.game_state.player_y
        )
        half_width = hitbox["width"] // 2
        half_height = hitbox["height"] // 2

        new_x = self.game_state.player_x + movement_x
        can_move_x = True

        test_points = [
            (new_x - half_width, self.game_state.player_y - half_height),  # Bottom left
            (
                new_x + half_width,
                self.game_state.player_y - half_height,
            ),  # Bottom right
            (new_x - half_width, self.game_state.player_y + half_height),  # Top left
            (new_x + half_width, self.game_state.player_y + half_height),  # Top right
        ]

        for test_x, test_y in test_points:
            if self.game_state.map_generator.is_wall(test_x, test_y):
                can_move_x = False
                break

        if can_move_x:
            self.game_state.player_x = max(
                half_width, min(WINDOW_WIDTH - half_width, new_x)
            )

        new_y = self.game_state.player_y + movement_y
        can_move_y = True

        test_points = [
            (self.game_state.player_x - half_width, new_y - half_height),  # Bottom left
            (
                self.game_state.player_x + half_width,
                new_y - half_height,
            ),  # Bottom right
            (self.game_state.player_x - half_width, new_y + half_height),  # Top left
            (self.game_state.player_x + half_width, new_y + half_height),  # Top right
        ]

        for test_x, test_y in test_points:
            if self.game_state.map_generator.is_wall(test_x, test_y):
                can_move_y = False
                break

        if can_move_y:
            self.game_state.player_y = max(
                half_height, min(WINDOW_HEIGHT - half_height, new_y)
            )

    def handle_keyboard(self, key: GLubyte, x: int, y: int) -> None:
        if self.game_state.game_over or self.game_state.is_paused:
            return

        key = key.decode("utf-8").lower()

        if key == "w":
            self.game_state.movement["up"] = True
        elif key == "s":
            self.game_state.movement["down"] = True
        elif key == "a":
            self.game_state.movement["left"] = True
        elif key == "d":
            self.game_state.movement["right"] = True

    def handle_keyboard_up(self, key: GLubyte, x: int, y: int) -> None:
        key = key.decode("utf-8").lower()

        if key == "w":
            self.game_state.movement["up"] = False
        elif key == "s":
            self.game_state.movement["down"] = False
        elif key == "a":
            self.game_state.movement["left"] = False
        elif key == "d":
            self.game_state.movement["right"] = False

    def handle_mouse(self, button: int, state: int, x: int, y: int) -> None:
        # Convert mouse coordinates to OpenGL coordinates
        y = WINDOW_HEIGHT - y

        # Handle UI button clicks
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if self.ui.check_button_click(x, y, 30, WINDOW_HEIGHT - 30):
                self.game_state.reset()
                print("Retaking the semester!")
                return

            elif self.ui.check_button_click(
                x, y, WINDOW_WIDTH // 2 - 10, WINDOW_HEIGHT - 30
            ):
                self.game_state.is_paused = not self.game_state.is_paused
                return

            elif self.ui.check_button_click(
                x, y, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 30
            ):
                grade_info = self._calculate_grade()
                print(
                    f"Semester dropped!\n"
                    f"Final Grade: {grade_info['grade']} (GPA: {grade_info['gpa']})\n"
                    f"Performance: {grade_info['description']}"
                )
                glutLeaveMainLoop()
                return

            # Handle shooting only when not paused
            if not self.game_state.is_paused and not self.game_state.game_over:
                self._create_bullet(x, y)

    def _create_bullet(self, target_x: float, target_y: float) -> None:
        # Calculate direction vector
        dx = target_x - self.game_state.player_x
        dy = target_y - self.game_state.player_y

        # Normalize the direction
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx /= length
            dy /= length

            # Calculate angle in radians
            angle = math.atan2(dy, dx)

            # Check for spread shot power-up
            spread_powerup = self.game_state.get_active_powerup("spread_shot")

            if spread_powerup:
                self._create_spread_shot(angle, spread_powerup["bullets"])
            else:
                self._create_single_bullet(angle)

    def _create_single_bullet(self, angle: float) -> None:
        speed_powerup = self.game_state.get_active_powerup("bullet_speed")
        bullet_speed = PLAYER_BULLET_SPEED * (
            speed_powerup["multiplier"] if speed_powerup else 1.0
        )

        self.game_state.player_bullets.append(
            {
                "x": self.game_state.player_x,
                "y": self.game_state.player_y,
                "direction": angle,
                "speed": bullet_speed,
            }
        )

    def _create_spread_shot(self, center_angle: float, num_bullets: int) -> None:
        spread_angle = math.pi / 4  # 45 degrees total spread
        angle_step = spread_angle / (num_bullets - 1) if num_bullets > 1 else 0
        start_angle = center_angle - spread_angle / 2

        for i in range(num_bullets):
            self._create_single_bullet(start_angle + i * angle_step)

    def _calculate_grade(self) -> str:
        from constants import GRADE_THRESHOLDS

        for threshold, grade in sorted(
            GRADE_THRESHOLDS.items(), key=lambda x: x[0], reverse=True
        ):
            if self.game_state.score >= threshold:
                return grade
        return "F"
