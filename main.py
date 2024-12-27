from OpenGL.GLUT import *

from game_state import GameState
from player import Player
from render import Render
from ui import UI
from controls import Controls
from collision_manager import CollisionManager
from game_loop import GameLoop
from initializer import Initializer
from map_generator import MapGenerator


def main() -> None:
    render = Render()
    player = Player(render)
    map_generator = MapGenerator(render)
    
    game_state = GameState(player, map_generator)
    ui = UI()

    controls = Controls(game_state, ui)
    collision_manager = CollisionManager(game_state)

    game_loop = GameLoop(
        game_state, player, render, ui, 
        collision_manager, controls
    )

    Initializer.init_game(game_loop, controls)
    glutMainLoop()


if __name__ == "__main__":
    main()
