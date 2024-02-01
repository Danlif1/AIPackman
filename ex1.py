from typing import Tuple, List, Optional, Callable, Iterable, Any
from collections import OrderedDict

import search
import math
import utils

id = "215985961"

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77
DEAD = 88
WALL = 99

STR_TO_MOVEMENT = OrderedDict({
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0),
})


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def update_locations(self, state):
        for row_index, row in enumerate(state):
            for col_index, square in enumerate(row):
                if square%10 == 1:
                    self.points.append((row_index, col_index))
                elif square%10 == 7:
                    self.locations[7] = (row_index, col_index)
                elif square%10 == 8:
                    self.locations[7] = None


    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman: 
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman."""

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.points = []
        # self.update_locations(initial)
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def find_object(self, state, finder: Callable[[int], int]) -> Optional[Tuple[int, int]]:
        for row_index, row in enumerate(state):
            for col_index, square in enumerate(row):
                if finder(square):
                    return row_index, col_index
        return None

    def successor(self, state):
        """ Generates the successor state """
        # Four possible successors, will be saved in succ.
        # Finding the pacman
        self.update_locations(state)

        pacman_location = self.locations[7]
        if pacman_location is None:
            # Pacman is gone
            return []
        temp_state = []
        for row in state:
            temp_state.append(list(row))
        # TODO: Use for loop over STR_TO_MOVEMENT
        succ = []
        for direction in STR_TO_MOVEMENT.keys():
            res = self.succ_helper(temp_state, direction)
            if res:
                succ.append(res)
        return succ

    def is_valid_location(self, state, location: Tuple[int, int], obstacles: List[int]) -> bool:
        # Check if location in state bounds
        # Check if state at location is not in obstacles.
        return (0 <= location[0] < len(state) and
                0 <= location[1] < len(state[0]) and
                state[location[0]][location[1]] not in obstacles)
    @staticmethod
    def apply_movement(location: Tuple[int, int], movement: Tuple[int, int]) -> Tuple[int, int]:
        return location[0] + movement[0], location[1] + movement[1]

    @staticmethod
    def state_at_location(state, location):
        return state[location[0]][location[1]]

    @staticmethod
    def distance(location_one: Tuple[int,int], location_two: Tuple[int,int]) -> int:
        return abs(location_one[0] - location_two[0]) + abs(location_one[1] - location_two[1])

    def succ_helper(self, state, letter: str) -> Tuple[str, Any]:
        pacman_location = row, col = self.locations[7]
        movement = STR_TO_MOVEMENT[letter]
        row_movement, col_movement = movement
        temp_state = [row.copy() for row in state]
        new_pacman_location = self.apply_movement(pacman_location, movement)
        if self.is_valid_location(state, new_pacman_location, [WALL]):
            # If you move into a ghost.
            if 52 > self.state_at_location(temp_state, new_pacman_location) > 19:
                temp_state[row + row_movement][col + col_movement] = DEAD
            else:
                temp_state[row + row_movement][col + col_movement] = PACMAN
            temp_state[row][col] = 10
        else:
            # TODO: Return empty - could not move in this direction
            return
        self.locations[7] = new_pacman_location
        # Red
        self.move_ghost(temp_state, 2)
        # Blue
        self.move_ghost(temp_state, 3)
        # Yellow
        self.move_ghost(temp_state, 4)
        # Green
        self.move_ghost(temp_state, 5)
        self.locations[7] = pacman_location

        real_state = ()
        for row in temp_state:
            real_state += (tuple(row),)

        return letter, real_state

    def move_ghost(self, state, color: int) -> None:
        ghost_location = self.find_object(state, lambda x: x // 10 == color)
        if not ghost_location:
            return
        # Check which move is valid
        possible_movements = [m for m in ["R", "D", "L", "U"] if
                              self.is_valid_location(state,
                                                     self.apply_movement(ghost_location, STR_TO_MOVEMENT[m]),
                                                     [WALL, 20, 21, 30, 31, 40, 41, 50, 51])]
        if not possible_movements:
            return
        # Calculate distance for all valid movements.
        distances = []
        for movement in possible_movements:
            future_ghost = self.apply_movement(ghost_location, STR_TO_MOVEMENT[movement])
            distances.append(self.distance(future_ghost, self.locations[7]))
        # Choose the best movement - Smallest distance from ghost to pacman, in order.
        best_movement, best_distance = possible_movements[0], distances[0]
        for movement, distance in zip(possible_movements,distances):
            if distance < best_distance:
                best_movement, best_distance = movement, distance
        # Move ghost.
        new_ghost_location = self.apply_movement(ghost_location, STR_TO_MOVEMENT[best_movement])
        if self.state_at_location(state, new_ghost_location) == PACMAN:
            state[new_ghost_location[0]][new_ghost_location[1]] = DEAD
        else:
            state[new_ghost_location[0]][new_ghost_location[1]] %= 2
            state[new_ghost_location[0]][new_ghost_location[1]] += 10 * color
        state[ghost_location[0]][ghost_location[1]] -= 10 * (color - 1)

    def result(self, state, move):
        """given state and an action and return a new state"""
        # TODO: implement
        utils.raiseNotDefined()

    def goal_test(self, state):
        # TODO: oneliner with any(...)
        for row in state:
            for square in row:
                if square % 10 == 1 or square % 10 == 8:
                    # Goal not met.
                    return False
        return True

    def distance_between_two_points(self, two_points):
        return self.distance(two_points[0], two_points[1])

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        pacman_location = self.locations[7]
        if not pacman_location:
            return float('inf')
        if pacman_location in self.points:
            self.points.remove(pacman_location)
        farthest_distance = -1
        farthest_points = None
        if not self.points:
            return 0
        combinations = []
        for point_one in self.points:
            for point_two in self.points:
                comb = (point_one, point_two)
                if farthest_distance < self.distance_between_two_points(comb):
                    farthest_distance = self.distance_between_two_points(comb)
                    farthest_points = comb
        closest_distance_to_pacman = float('inf')
        for point in farthest_points:
            if closest_distance_to_pacman > self.distance_between_two_points((point,pacman_location)):
                closest_distance_to_pacman = self.distance_between_two_points((point, pacman_location))
        return max(closest_distance_to_pacman + farthest_distance, len(self.points))


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
