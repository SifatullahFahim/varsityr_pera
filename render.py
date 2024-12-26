from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Render:
    def __init__(self) -> None:
        pass

    def draw_circle(self, x: float, y: float, radius: float) -> None:
        """Midpoint Circle Algorithm"""
        x0, y0 = x, y

        def plot_circle_points(x: float, y: float) -> None:
            glVertex2f(x0 + x, y0 + y)
            glVertex2f(x0 - x, y0 + y)
            glVertex2f(x0 + x, y0 - y)
            glVertex2f(x0 - x, y0 - y)
            glVertex2f(x0 + y, y0 + x)
            glVertex2f(x0 - y, y0 + x)
            glVertex2f(x0 + y, y0 - x)
            glVertex2f(x0 - y, y0 - x)

        d = 1 - radius
        x, y = 0, radius

        glBegin(GL_POINTS)
        while x <= y:
            plot_circle_points(x, y)
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
        glEnd()

    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Midpoint Line Algorithm"""
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if x1 == x2:
            y_start = min(y1, y2)
            y_end = max(y1, y2)
            glBegin(GL_POINTS)
            for y in range(y_start, y_end + 1):
                glVertex2f(x1, y)
            glEnd()
            return

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        x_inc = 1 if x2 > x1 else -1
        y_inc = 1 if y2 > y1 else -1

        x, y = x1, y1

        glBegin(GL_POINTS)

        if dy > dx:
            dx, dy = dy, dx
            p = 2 * dx - dy
            for _ in range(dy):
                glVertex2f(x, y)
                if p > 0:
                    x += x_inc
                    p += 2 * (dx - dy)
                else:
                    p += 2 * dx
                y += y_inc
        else:
            p = 2 * dy - dx
            for _ in range(dx):
                glVertex2f(x, y)
                if p > 0:
                    y += y_inc
                    p += 2 * (dy - dx)
                else:
                    p += 2 * dy
                x += x_inc

        glEnd()
