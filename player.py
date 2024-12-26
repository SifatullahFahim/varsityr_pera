from OpenGL.GL import *
from render import Render
from constants import PLAYER_COLOR, PLAYER_SIZE


class Player:
    def __init__(self, render: Render) -> None:
        self.render = render
        self.size = PLAYER_SIZE

    def draw(self, x: float, y: float) -> None:
        glColor3f(*PLAYER_COLOR)
        
        # Head
        head_radius = self.size // 4
        self.render.draw_circle(x, y + self.size - head_radius, head_radius)
        
        # Body
        body_start = y + self.size - (head_radius * 2)
        body_end = y + self.size // 2
        self.render.draw_line(x, body_start, x, body_end)
        
        # Arms
        arm_y = y + self.size - (head_radius * 2.5)
        arm_length = self.size // 3
        # Left arm
        self.render.draw_line(x - arm_length, arm_y, x, arm_y)
        # Right arm
        self.render.draw_line(x, arm_y, x + arm_length, arm_y)
        
        # Legs
        leg_start = body_end
        leg_length = self.size // 2.5
        # Left leg
        self.render.draw_line(x, leg_start, x - leg_length, y)
        # Right leg
        self.render.draw_line(x, leg_start, x + leg_length, y)

    def get_hitbox(self, x: float, y: float) -> dict:
        head_radius = self.size // 4
        total_height = self.size
        total_width = (self.size // 3) * 2  # Based on arm length

        return {
            "x": x,
            "y": y + total_height // 2,  # Center point
            "width": total_width,
            "height": total_height,
            "head_radius": head_radius
        }

    def draw_hitbox(self, x: float, y: float) -> None:
        """Debug method to visualize the hitbox"""
        hitbox = self.get_hitbox(x, y)
        
        glColor3f(1.0, 0.0, 0.0)  # Red color for hitbox
        
        # Draw rectangular hitbox
        half_width = hitbox["width"] // 2
        half_height = hitbox["height"] // 2
        
        # Draw hitbox outline
        self.render.draw_line(
            x - half_width, y + half_height,
            x + half_width, y + half_height
        )
        self.render.draw_line(
            x + half_width, y + half_height,
            x + half_width, y - half_height
        )
        self.render.draw_line(
            x + half_width, y - half_height,
            x - half_width, y - half_height
        )
        self.render.draw_line(
            x - half_width, y - half_height,
            x - half_width, y + half_height
        )
        
        # Draw head hitbox circle
        self.render.draw_circle(
            hitbox["x"],
            hitbox["y"] + hitbox["height"] // 2 - hitbox["head_radius"],
            hitbox["head_radius"]
        ) 