from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from typing import Callable
from game_loop import GameLoop
from controls import Controls


class Initializer:
    @staticmethod
    def init_gl() -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    @staticmethod
    def init_game(game_loop: GameLoop, controls: Controls) -> None:
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow(b"Versity'r Pera")

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)

        glutDisplayFunc(game_loop.display)
        glutTimerFunc(0, game_loop.update, 0)
        glutKeyboardFunc(controls.handle_keyboard)
        glutKeyboardUpFunc(controls.handle_keyboard_up)
        glutMouseFunc(controls.handle_mouse)
