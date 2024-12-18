import math
from abc import ABC, abstractmethod

import algo.constants as constants


class Command(ABC):
    def __init__(self, time):
        # Time in seconds in which this command is carried out.
        self.time = time

        # the number of frames to update per second
        # Number of frame ticks that this command will take.
        self.ticks = math.ceil(time * constants.FRAMES)
        self.total_ticks = self.ticks  # Keep track of total ticks.

    def tick(self):
        self.ticks -= 1

    @abstractmethod
    def process_one_tick(self, robot):
        """
        Overriding method must call tick().
        """
        pass

    @abstractmethod
    def apply_on_pos(self, curr_pos):
        """
        Apply this command to a Position, such that its attributes will reflect the correct values
        after the command is done.

        This method should return itself.
        """
        pass

    @abstractmethod
    def convert_to_message(self):
        """
        Conversion to a message that is easy to send over the RPi.
        """
        pass
