from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from render import Render
from constants import (
    RESTART_BUTTON_COLOR,
    PAUSE_PLAY_BUTTON_COLOR,
    CROSS_BUTTON_COLOR
)


class UI:
    def __init__(self) -> None:
        self.render: Render = Render()

    def draw_restart_button(self, x: float, y: float) -> None:
        size: int = 20
        glColor3f(*RESTART_BUTTON_COLOR)

        self.render.draw_line(x, y, x + size // 2, y + size // 2)
        self.render.draw_line(x, y, x + size // 2, y - size // 2)
        self.render.draw_line(
            x + size // 2, y + size // 2, x + size // 2, y - size // 2
        )

        self.render.draw_line(x + size // 2 - 1, y, x + size, y)

    def draw_pause_play_button(self, x: float, y: float, is_paused: bool) -> None:
        size: int = 20
        glColor3f(*PAUSE_PLAY_BUTTON_COLOR)
        
        if is_paused:
            # Play Icon
            self.render.draw_line(x, y - size // 2, x + size, y)
            self.render.draw_line(x + size, y, x, y + size // 2)
            self.render.draw_line(x, y + size // 2, x, y - size // 2)
        else:
            # Pause Icon
            self.render.draw_line(x, y - size // 2, x, y + size // 2)
            self.render.draw_line(x + size // 2, y - size // 2, x + size // 2, y + size // 2)

    def draw_cross_button(self, x: float, y: float) -> None:
        size: int = 20
        glColor3f(*CROSS_BUTTON_COLOR)

        self.render.draw_line(x, y - size // 2, x + size, y + size // 2)
        self.render.draw_line(x, y + size // 2, x + size, y - size // 2)

    def check_button_click(
        self,
        mouse_x: float,
        mouse_y: float,
        button_x: float,
        button_y: float,
        size: int = 20,
    ) -> bool:
        return (
            button_x <= mouse_x <= button_x + size
            and button_y - size // 2 <= mouse_y <= button_y + size // 2
        )
