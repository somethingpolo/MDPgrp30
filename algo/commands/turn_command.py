import math

import algo.constants as constants
from algo.commands.command import Command
from algo.misc.direction import Direction
from algo.misc.positioning import Position, RobotPosition
from algo.misc.type_of_turn import TypeOfTurn


class TurnCommand(Command):
    def __init__(self, type_of_turn, left, right, reverse):
        """
        Angle to turn and whether the turn is done in reverse or not. Note that this is in degrees.

        Note that negative angles will always result in the robot being rotated clockwise.
        """
        time = 0
        if type_of_turn == TypeOfTurn.SMALL:
            time = 10  # SOME VALUE TO BE EMPIRICALLY DETERMINED
        elif type_of_turn == TypeOfTurn.MEDIUM:
            time = 20  # SOME VALUE TO BE EMPIRICALLY DETERMINED
        elif type_of_turn == TypeOfTurn.LARGE:
            time = 30  # SOME VALUE TO BE EMPIRICALLY DETERMINED

        if type_of_turn == TypeOfTurn.SMALL:
            time = 10  # SOME VALUE TO BE EMPIRICALLY DETERMINED
        elif type_of_turn == TypeOfTurn.MEDIUM:
            time = 20  # SOME VALUE TO BE EMPIRICALLY DETERMINED
        elif type_of_turn == TypeOfTurn.LARGE:
            time = 30  # SOME VALUE TO BE EMPIRICALLY DETERMINED

        super().__init__(time)
        self.type_of_turn = type_of_turn
        self.left = left
        self.right = right
        self.reverse = reverse

    def __str__(self):
        # return f"TurnCommand:{self.type_of_turn}, {self.total_ticks} ticks, rev={self.reverse}, left={self.left}, right={self.right}) "
        return f"TurnCommand:{self.type_of_turn}, rev={self.reverse}, left={self.left}, right={self.right}) "

    __repr__ = __str__

    def process_one_tick(self, robot):
        if self.total_ticks == 0:
            return

        self.tick()
        robot.turn(self.type_of_turn, self.left, self.right, self.reverse)

    def get_type_of_turn(self):
        return self.type_of_turn

    def apply_on_pos(self, curr_pos: Position):
        """
        changes the robot position according to what command it is and where the robot is currently at
        """
        assert isinstance(curr_pos, RobotPosition), print(
            "Cannot apply turn command on non-robot positions!"
        )

        # Get change in (x, y) coordinate.
        # Changes:
        # Turn left
        # Turn right


        # turn left and forward
        if self.left and not self.right and not self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x -= constants.TURN_SMALL_LEFT_FORWARD[0]
                    curr_pos.y += constants.TURN_SMALL_LEFT_FORWARD[1]
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x -= constants.TURN_SMALL_LEFT_FORWARD[1]
                    curr_pos.y -= constants.TURN_SMALL_LEFT_FORWARD[0]
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x += constants.TURN_SMALL_LEFT_FORWARD[1]
                    curr_pos.y += constants.TURN_SMALL_LEFT_FORWARD[0]
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x += constants.TURN_SMALL_LEFT_FORWARD[0]
                    curr_pos.y -= constants.TURN_SMALL_LEFT_FORWARD[1]
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x -= constants.TURN_MEDIUM_LEFT_FORWARD[0]
                    curr_pos.y += constants.TURN_MEDIUM_LEFT_FORWARD[1]
                    curr_pos.direction = Direction.LEFT
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x -= constants.TURN_MEDIUM_LEFT_FORWARD[1]
                    curr_pos.y -= constants.TURN_MEDIUM_LEFT_FORWARD[0]
                    curr_pos.direction = Direction.BOTTOM
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x += constants.TURN_MEDIUM_LEFT_FORWARD[1]
                    curr_pos.y += constants.TURN_MEDIUM_LEFT_FORWARD[0]
                    curr_pos.direction = Direction.TOP
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x += constants.TURN_MEDIUM_LEFT_FORWARD[0]
                    curr_pos.y -= constants.TURN_MEDIUM_LEFT_FORWARD[1]
                    curr_pos.direction = Direction.RIGHT

        # turn right and forward
        if self.right and not self.left and not self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x += constants.TURN_SMALL_RIGHT_FORWARD[0]
                    curr_pos.y +=  constants.TURN_SMALL_RIGHT_FORWARD[1]
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x -= constants.TURN_SMALL_RIGHT_FORWARD[1]
                    curr_pos.y += constants.TURN_SMALL_RIGHT_FORWARD[0]
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x += constants.TURN_SMALL_RIGHT_FORWARD[1]
                    curr_pos.y -= constants.TURN_SMALL_RIGHT_FORWARD[0]
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x -= constants.TURN_SMALL_RIGHT_FORWARD[0]
                    curr_pos.y -= constants.TURN_SMALL_RIGHT_FORWARD[1]
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x += constants.TURN_MEDIUM_RIGHT_FORWARD[0]
                    curr_pos.y +=  constants.TURN_MEDIUM_RIGHT_FORWARD[1]
                    curr_pos.direction = Direction.RIGHT
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x -= constants.TURN_MEDIUM_RIGHT_FORWARD[1]
                    curr_pos.y += constants.TURN_MEDIUM_RIGHT_FORWARD[0]
                    curr_pos.direction = Direction.TOP
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x += constants.TURN_MEDIUM_RIGHT_FORWARD[1]
                    curr_pos.y -= constants.TURN_MEDIUM_RIGHT_FORWARD[0]
                    curr_pos.direction = Direction.BOTTOM
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x -= constants.TURN_MEDIUM_RIGHT_FORWARD[0]
                    curr_pos.y -= constants.TURN_MEDIUM_RIGHT_FORWARD[1]
                    curr_pos.direction = Direction.LEFT

        # turn front wheels left and reverse
        # Haven't trying measure this out yet
        if self.left and not self.right and self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x -= constants.TURN_SMALL_LEFT_REVERSE[0]
                    curr_pos.y -= constants.TURN_SMALL_LEFT_REVERSE[1]
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x += constants.TURN_SMALL_LEFT_REVERSE[1]
                    curr_pos.y -= constants.TURN_SMALL_LEFT_REVERSE[0]
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x -= constants.TURN_SMALL_LEFT_REVERSE[1]
                    curr_pos.y += constants.TURN_SMALL_LEFT_REVERSE[0]
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x += constants.TURN_SMALL_LEFT_REVERSE[0]
                    curr_pos.y += constants.TURN_SMALL_LEFT_REVERSE[1]
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x -= constants.TURN_MEDIUM_LEFT_REVERSE[0]
                    curr_pos.y -= constants.TURN_MEDIUM_LEFT_REVERSE[1]
                    curr_pos.direction = Direction.RIGHT
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x += constants.TURN_MEDIUM_LEFT_REVERSE[1]
                    curr_pos.y -= constants.TURN_MEDIUM_LEFT_REVERSE[0]
                    curr_pos.direction = Direction.TOP
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x -= constants.TURN_MEDIUM_LEFT_REVERSE[1]
                    curr_pos.y += constants.TURN_MEDIUM_LEFT_REVERSE[0]
                    curr_pos.direction = Direction.BOTTOM
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x += constants.TURN_MEDIUM_LEFT_REVERSE[0]
                    curr_pos.y += constants.TURN_MEDIUM_LEFT_REVERSE[1]
                    curr_pos.direction = Direction.LEFT

        # turn front wheels right and reverse
        if self.right and not self.left and self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x += constants.TURN_SMALL_RIGHT_REVERSE[0]
                    curr_pos.y -= constants.TURN_SMALL_RIGHT_REVERSE[1]
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x += constants.TURN_SMALL_RIGHT_REVERSE[1]
                    curr_pos.y += constants.TURN_SMALL_RIGHT_REVERSE[0]
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x -= constants.TURN_SMALL_RIGHT_REVERSE[1]
                    curr_pos.y -= constants.TURN_SMALL_RIGHT_REVERSE[0]
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x -= constants.TURN_SMALL_RIGHT_REVERSE[0]
                    curr_pos.y += constants.TURN_SMALL_RIGHT_REVERSE[1]
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                if curr_pos.direction == Direction.TOP:
                    curr_pos.x += constants.TURN_MEDIUM_RIGHT_REVERSE[0]
                    curr_pos.y -= constants.TURN_MEDIUM_RIGHT_REVERSE[1]
                    curr_pos.direction = Direction.LEFT
                elif curr_pos.direction == Direction.LEFT:
                    curr_pos.x +=constants.TURN_MEDIUM_RIGHT_REVERSE[1]
                    curr_pos.y += constants.TURN_MEDIUM_RIGHT_REVERSE[0]
                    curr_pos.direction = Direction.BOTTOM
                elif curr_pos.direction == Direction.RIGHT:
                    curr_pos.x -= constants.TURN_MEDIUM_RIGHT_REVERSE[1]
                    curr_pos.y -= constants.TURN_MEDIUM_RIGHT_REVERSE[0]
                    curr_pos.direction = Direction.TOP
                elif curr_pos.direction == Direction.BOTTOM:
                    curr_pos.x -= constants.TURN_MEDIUM_RIGHT_REVERSE[0]
                    curr_pos.y += constants.TURN_MEDIUM_RIGHT_REVERSE[1]
                    curr_pos.direction = Direction.RIGHT

        return self

    def convert_to_message(self):
        if self.left and not self.right and not self.reverse:
            # This is going forward left.
            if self.type_of_turn == TypeOfTurn.SMALL:
                # return ["LF035", "RF035"] # turn left small forward!
                return ["LF035", "SF003","RF035"] 
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                return ["SF005","LF090"]  # turn left medium forward!
            elif self.type_of_turn == TypeOfTurn.LARGE:
                return "LF180"  # turn left large forward!
        elif self.left and not self.right and self.reverse:
            # This is going backward and front wheels are turned to left
            if self.type_of_turn == TypeOfTurn.SMALL:
                return ["LB035", "SB003", "RB035"]  # turn left small reverse!
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                return ["LB090","SB005"]  # turn left medium reverse!
            elif self.type_of_turn == TypeOfTurn.LARGE:
                return "LB180"  # turn left large reverse!
        elif self.right and not self.left and not self.reverse:
            # This is going forward right.
            if self.type_of_turn == TypeOfTurn.SMALL:
                # return ["RF035", "LF035"]  # turn right small forward!
                return ["RF035", "SF003", "LF035"]
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                return ["SF003","RF090","SB003"]  # turn right medium forward!
            elif self.type_of_turn == TypeOfTurn.LARGE:
                return "RF180"  # turn right large forward!
        else:
            # This is going backward and the front wheels turned to the right.
            if self.type_of_turn == TypeOfTurn.SMALL:
                return ["RB035", "SB003", "LB035"] # turn right small reverse!
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                return ["SF003","RB090","SB005"]  # turn right medium reverse!
            elif self.type_of_turn == TypeOfTurn.LARGE:
                return "RB180"  # turn right large reverse!
