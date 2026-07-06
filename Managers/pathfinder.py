import heapq
from Entities.buildings import Building
from config import Preview


class Pathfinder:
    grid_size = 20

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @classmethod
    def get_grid_coords(cls, x, y):
        return (int(x // cls.grid_size), int(y // cls.grid_size))

    @classmethod
    def get_world_coords(cls, gx, gy):
        return (gx * cls.grid_size + (cls.grid_size / 2), gy * cls.grid_size + (cls.grid_size / 2))

    @classmethod
    def is_walkable(cls, gx, gy):
        if not (0 <= gx * cls.grid_size < Preview.picture_width and 0 <= gy * cls.grid_size < Preview.picture_height):
            return False

        wx = gx * cls.grid_size
        wy = gy * cls.grid_size

        if Building.check_if_collides(wx + 2, wy + 2, wx + cls.grid_size - 2, wy + cls.grid_size - 2):
            return False

        return True

    @classmethod
    def get_closest_walkable(cls, gx, gy):
        if cls.is_walkable(gx, gy):
            return (gx, gy)

        for r in range(1, 10):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if abs(dx) == r or abs(dy) == r:
                        if cls.is_walkable(gx + dx, gy + dy):
                            return (gx + dx, gy + dy)
        return (gx, gy)

    @classmethod
    def find_path(cls, start_x, start_y, target_x, target_y):
        start = cls.get_grid_coords(start_x, start_y)
        goal = cls.get_grid_coords(target_x, target_y)

        start = cls.get_closest_walkable(*start)
        goal = cls.get_closest_walkable(*goal)

        if not cls.is_walkable(*goal):
            return [(target_x, target_y)]

        if start == goal:
            return [(target_x, target_y)]

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                next_node = (current[0] + dx, current[1] + dy)

                if not cls.is_walkable(*next_node):
                    continue

                step_cost = 1.4 if dx != 0 and dy != 0 else 1.0
                new_cost = cost_so_far[current] + step_cost

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + cls.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from:
            return [(target_x, target_y)]

        path = []
        current = goal
        while current != start:
            path.append(cls.get_world_coords(*current))
            current = came_from[current]

        path.reverse()

        path.append((target_x, target_y))
        return path