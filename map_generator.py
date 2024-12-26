import random
from typing import List, Dict, Tuple
from OpenGL.GL import *
from render import Render
from constants import (
    MAP_TILE_SIZE,
    MAP_MIN_ROOMS,
    MAP_MAX_ROOMS,
    MAP_MIN_ROOM_SIZE,
    MAP_MAX_ROOM_SIZE,
    MAP_COLORS,
)


class Room:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + width // 2, y + height // 2)

    def intersects(self, other: "Room", padding: int = 1) -> bool:
        return (
            self.x - padding <= other.x + other.width
            and self.x + self.width + padding >= other.x
            and self.y - padding <= other.y + other.height
            and self.y + self.height + padding >= other.y
        )


class MapGenerator:
    def __init__(self, render: Render):
        self.render = render
        self.rooms: List[Room] = []
        self.tiles: List[List[str]] = []
        self.width = 32
        self.height = 18
        self.generate_map()

    def generate_map(self) -> None:
        self.rooms = []
        num_rooms = random.randint(MAP_MIN_ROOMS, MAP_MAX_ROOMS)

        # Initialize all tiles as FLOOR instead of WALL
        self.tiles = [["FLOOR" for _ in range(self.width)] for _ in range(self.height)]

        # Add border walls
        for x in range(self.width):
            self.tiles[0][x] = "WALL"
            self.tiles[self.height - 1][x] = "WALL"
        for y in range(self.height):
            self.tiles[y][0] = "WALL"
            self.tiles[y][self.width - 1] = "WALL"

        # Generate rooms
        attempts = 0
        while len(self.rooms) < num_rooms and attempts < 100:
            room_width = random.randint(MAP_MIN_ROOM_SIZE, MAP_MAX_ROOM_SIZE)
            room_height = random.randint(MAP_MIN_ROOM_SIZE, MAP_MAX_ROOM_SIZE)

            x = random.randint(2, self.width - room_width - 2)
            y = random.randint(2, self.height - room_height - 2)

            new_room = Room(x, y, room_width, room_height)

            # Use a smaller padding (1) for room intersection checks
            if not any(new_room.intersects(room, padding=1) for room in self.rooms):
                self.rooms.append(new_room)

                # Add some strategic walls around the room
                self._add_strategic_walls(new_room)

            attempts += 1

        # Connect rooms with wider corridors
        self._connect_all_rooms()

    def _add_strategic_walls(self, room: Room) -> None:
        # Add some pillars and partial walls for cover
        piller_count = random.randint(1, 5)  # Add random pillars per room
        for _ in range(piller_count):
            px = random.randint(room.x + 1, room.x + room.width - 2)
            py = random.randint(room.y + 1, room.y + room.height - 2)
            self.tiles[py][px] = "WALL"

    def _connect_all_rooms(self) -> None:
        # Connect each room to its nearest neighbor
        for i, room1 in enumerate(self.rooms):
            if i == len(self.rooms) - 1:
                continue

            # Find the nearest room
            min_dist = float("inf")
            nearest_room = None

            for room2 in self.rooms[i + 1 :]:
                dist = (
                    (room1.center[0] - room2.center[0]) ** 2
                    + (room1.center[1] - room2.center[1]) ** 2
                ) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest_room = room2

            if nearest_room:
                self._create_wide_corridor(room1, nearest_room)

    def _create_wide_corridor(self, room1: Room, room2: Room) -> None:
        x1, y1 = room1.center
        x2, y2 = room2.center

        # Create a wider corridor
        for x in range(min(x1, x2) - 1, max(x1, x2) + 2):
            for y in range(y1 - 1, y1 + 2):
                if 0 < y < self.height - 1 and 0 < x < self.width - 1:
                    self.tiles[y][x] = "FLOOR"

        for y in range(min(y1, y2) - 1, max(y1, y2) + 2):
            for x in range(x2 - 1, x2 + 2):
                if 0 < y < self.height - 1 and 0 < x < self.width - 1:
                    self.tiles[y][x] = "FLOOR"

    def draw(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.tiles[y][x]
                glColor3f(*MAP_COLORS[tile_type])

                if tile_type == "WALL":
                    self._draw_tile(x * MAP_TILE_SIZE, y * MAP_TILE_SIZE)

    def _draw_tile(self, x: int, y: int) -> None:
        self.render.draw_line(x, y, x + MAP_TILE_SIZE, y)
        self.render.draw_line(
            x + MAP_TILE_SIZE, y, x + MAP_TILE_SIZE, y + MAP_TILE_SIZE
        )
        self.render.draw_line(
            x + MAP_TILE_SIZE, y + MAP_TILE_SIZE, x, y + MAP_TILE_SIZE
        )
        self.render.draw_line(x, y + MAP_TILE_SIZE, x, y)

    def _convert_pixel_to_tile(self, x: float, y: float) -> Tuple[int, int]:
        return int(x / MAP_TILE_SIZE), int(y / MAP_TILE_SIZE)

    def _is_out_of_bounds(self, x: float, y: float) -> bool:
        tile_x, tile_y = self._convert_pixel_to_tile(x, y)
        return tile_x < 0 or tile_x >= self.width or tile_y < 0 or tile_y >= self.height

    def is_wall(self, x: float, y: float) -> bool:
        tile_x, tile_y = self._convert_pixel_to_tile(x, y)
        if self._is_out_of_bounds(x, y):
            return True

        is_wall = self.tiles[tile_y][tile_x] == "WALL"
        return is_wall

    def get_random_floor_position(self) -> Tuple[float, float]:
        while True:
            room = random.choice(self.rooms)
            x = random.randint(room.x, room.x + room.width - 1)
            y = random.randint(room.y, room.y + room.height - 1)
            if self.tiles[y][x] == "FLOOR":
                return (
                    x * MAP_TILE_SIZE + MAP_TILE_SIZE // 2,
                    y * MAP_TILE_SIZE + MAP_TILE_SIZE // 2,
                )

    def get_tile_type(self, x: float, y: float) -> str:
        tile_x, tile_y = self._convert_pixel_to_tile(x, y)

        if self._is_out_of_bounds(x, y):
            return "WALL"

        return self.tiles[tile_y][tile_x]
