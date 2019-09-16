from random import shuffle, randint

import constants
from models.maze import Maze
from models.object import Object
from models.macgyver import MacGyver


class ViewModel:
    DIRECTION_UP = 1
    DIRECTION_RIGHT = 2
    DIRECTION_DOWN = 3
    DIRECTION_LEFT = 4

    def __init__(self):
        self.__maze = Maze(constants.MAZE_WIDTH, constants.MAZE_HEIGHT)
        self.__macgyver = MacGyver((0, 1))
        self.__objects = []
        self.__game_won = False
        self.__game_over = False

        self.__maze.generate_board()

        # Step 0 : init
        free_blocks_xy_positions: [(int, int)] = []

        # Step 1 : getting all empty blocks of board
        for x in range(constants.MAZE_WIDTH):
            for y in range(constants.MAZE_HEIGHT):
                if self.__maze.get_board()[y][x] == ' ':
                    free_blocks_xy_positions.append((x, y))

        # Popping first and last list item (MacGyver and Guardian positions respectively)
        free_blocks_xy_positions.pop(0)
        free_blocks_xy_positions.pop(len(free_blocks_xy_positions) - 1)

        # Shuffle the array to mix the positions
        shuffle(free_blocks_xy_positions)

        # Random zones
        zone_length = (len(free_blocks_xy_positions) - 1) // 3

        # Step 2 : choosing place of element A
        element_a_index = randint(0, zone_length)
        self.__objects.append(Object(free_blocks_xy_positions[element_a_index]))

        # Step 3 : choosing place of element B
        element_b_index = randint(zone_length, 2 * zone_length)
        self.__objects.append(Object(free_blocks_xy_positions[element_b_index]))

        # Step 4 : choosing place of element C
        element_c_index = randint(2 * zone_length, 3 * zone_length)
        self.__objects.append(Object(free_blocks_xy_positions[element_c_index]))

    def move_mg(self, direction: int):
        """
        Handle the movement of MacGyver on the board
        Reset the __mg_xy_position property of the class with new position coordinated
        :param direction:
            Must be DIRECTION_UP or DIRECTION_RIGHT or DIRECTION_DOWN or DIRECTION_LEFT
        """
        board = self.__maze.get_board()
        macgyver = self.__macgyver

        if direction == self.DIRECTION_UP:
            if board[macgyver.get_position()[1] - 1][macgyver.get_position()[0]] == ' ':
                macgyver.move(macgyver.DIRECTION_UP)

        elif direction == self.DIRECTION_RIGHT:
            # This line prevents out of range exception at maze exit
            if macgyver.get_position()[0] < constants.MAZE_WIDTH - 1:
                if board[macgyver.get_position()[1]][macgyver.get_position()[0] + 1] == 'G':
                    objects_collected = []
                    for obj in self.__objects:
                        objects_collected.append(obj.is_collected())
                    self.__game_won = all(objects_collected)
                    self.__game_over = not any(objects_collected)

                elif board[macgyver.get_position()[1]][macgyver.get_position()[0] + 1] == ' ':
                    macgyver.move(macgyver.DIRECTION_RIGHT)

        elif direction == self.DIRECTION_DOWN:
            if board[macgyver.get_position()[1] + 1][macgyver.get_position()[0]] == ' ':
                macgyver.move(macgyver.DIRECTION_DOWN)

        elif direction == self.DIRECTION_LEFT:
            if board[macgyver.get_position()[1]][macgyver.get_position()[0] - 1] == ' ':
                macgyver.move(macgyver.DIRECTION_LEFT)

        for obj in self.__objects:
            if macgyver.get_position() == obj.get_position():
                obj.collect()

    def get_maze(self):
        return self.__maze

    def get_macgyver(self):
        return self.__macgyver

    def get_objects(self):
        return self.__objects

    def get_game_over(self):
        return self.__game_over

    def get_game_won(self):
        return self.__game_won