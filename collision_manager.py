import math
from typing import Dict
from constants import ENEMY_TYPES, POWERUP_TYPES


class CollisionManager:
    def __init__(self, game_state) -> None:
        self.game_state = game_state

    def check_all_collisions(self) -> None:
        self._check_player_bullet_collisions()
        self._check_enemy_bullet_collisions()
        self._check_enemy_melee_collisions()
        self._check_powerup_collisions()

    def _check_player_bullet_collisions(self) -> None:
        for bullet in self.game_state.player_bullets[:]:
            for enemy in self.game_state.enemies[:]:
                if self._check_circle_collision(
                    bullet["x"], bullet["y"], 3,
                    enemy["x"], enemy["y"], 
                    ENEMY_TYPES[enemy["type"]]["size"]
                ):
                    # Remove bullet
                    if bullet in self.game_state.player_bullets:
                        self.game_state.player_bullets.remove(bullet)
                    
                    # Damage enemy
                    enemy["hp"] -= 1
                    if enemy["hp"] <= 0:
                        self.game_state.enemies.remove(enemy)
                        self.game_state.score += ENEMY_TYPES[enemy["type"]]["points"]
                        print(f"Defeated {enemy['type']}! Score: {self.game_state.score}")
                    break

    def _check_enemy_bullet_collisions(self) -> None:
        for bullet in self.game_state.enemy_bullets[:]:
            player_hitbox = self.game_state.player.get_hitbox(
                self.game_state.player_x,
                self.game_state.player_y
            )
            
            if self._check_circle_rect_collision(
                bullet["x"], bullet["y"], 2,
                player_hitbox["x"] - player_hitbox["width"] // 2,
                player_hitbox["y"] - player_hitbox["height"] // 2,
                player_hitbox["width"],
                player_hitbox["height"]
            ):
                self.game_state.enemy_bullets.remove(bullet)
                self._handle_player_hit()

    def _check_enemy_melee_collisions(self) -> None:
        for enemy in self.game_state.enemies:
            if ENEMY_TYPES[enemy["type"]]["attack_type"] != "melee":
                continue
                
            player_hitbox = self.game_state.player.get_hitbox(
                self.game_state.player_x,
                self.game_state.player_y
            )
            
            if self._check_circle_rect_collision(
                enemy["x"], enemy["y"],
                ENEMY_TYPES[enemy["type"]]["attack_range"],
                player_hitbox["x"] - player_hitbox["width"] // 2,
                player_hitbox["y"] - player_hitbox["height"] // 2,
                player_hitbox["width"],
                player_hitbox["height"]
            ):
                self._handle_player_hit()

    def _check_powerup_collisions(self) -> None:
        for powerup in self.game_state.available_powerups[:]:
            player_hitbox = self.game_state.player.get_hitbox(
                self.game_state.player_x,
                self.game_state.player_y
            )
            
            if self._check_circle_rect_collision(
                powerup["x"], powerup["y"],
                POWERUP_TYPES[powerup["type"]]["size"],
                player_hitbox["x"] - player_hitbox["width"] // 2,
                player_hitbox["y"] - player_hitbox["height"] // 2,
                player_hitbox["width"],
                player_hitbox["height"]
            ):
                self._activate_powerup(powerup)
                self.game_state.available_powerups.remove(powerup)

    def _handle_player_hit(self) -> None:
        self.game_state.lives -= 1
        print(f"Hit! Academic Comebacks remaining: {self.game_state.lives}")
        
        if self.game_state.lives <= 0:
            self.game_state.game_over = True
            print("Game Over! Failed the semester.")

    def _activate_powerup(self, powerup: Dict) -> None:
        powerup_type = powerup["type"]
        powerup_data = POWERUP_TYPES[powerup_type].copy()
        powerup_data["type"] = powerup_type
        
        # Remove any existing powerup of the same type
        self.game_state.active_powerups = [
            p for p in self.game_state.active_powerups 
            if p["type"] != powerup_type
        ]
        
        self.game_state.active_powerups.append(powerup_data)
        print(f"Activated {powerup_type}!")

    def _check_circle_collision(
        self, x1: float, y1: float, r1: float,
        x2: float, y2: float, r2: float
    ) -> bool:
        dx = x1 - x2
        dy = y1 - y2
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (r1 + r2)

    def _check_circle_rect_collision(
        self, circle_x: float, circle_y: float, circle_r: float,
        rect_x: float, rect_y: float, rect_w: float, rect_h: float
    ) -> bool:
        # Find closest point on rectangle to circle
        closest_x = max(rect_x, min(circle_x, rect_x + rect_w))
        closest_y = max(rect_y, min(circle_y, rect_y + rect_h))
        
        # Calculate distance between closest point and circle center
        dx = circle_x - closest_x
        dy = circle_y - closest_y
        
        return (dx * dx + dy * dy) < (circle_r * circle_r)