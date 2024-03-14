import socket
import time
from typing import List

import algo.constants
from algo.commands.go_straight_command import StraightCommand
from algo.commands.scan_obstacle_command import ScanCommand
from algo.grid.grid import Grid
from algo.grid.obstacle import Obstacle
from algo.misc.direction import Direction
from algo.misc.positioning import Position
from algo.pygame_app import AlgoMinimal
from algo.robot.robot import Robot
from algo.simulation import Simulation

import os


class Algo:
    def __init__(self):
        self.client = None
        self.commands = None
        self.count = 0

    def parse_obstacle_data(self, data) -> List[Obstacle]:
        obs = []
        for obstacle_params in data:
            if len(obstacle_params) < 4:
                continue
            obs.append(
                Obstacle(
                    Position(
                        obstacle_params[0],
                        obstacle_params[1],
                        Direction(obstacle_params[2]),
                    ),
                    obstacle_params[3],
                )
            )
        return obs

    def run_simulator(self):
        # For simulation testing, change this with the obstacles to test.
        obstacles = []
        i = 0
        for x, y, direction in constants.SIMULATOR_OBSTACLES:
            position: Position = Position(x, y, direction)
            obstacle: Obstacle = Obstacle(position, i)
            i += 1
            obstacles.append(obstacle)
        grid = Grid(obstacles)
        bot = Robot(grid)
        sim = Simulation()
        sim.runSimulation(bot)

    def run_task1(self, obstacles_string):
        print("Running task1 ", obstacles_string)
        d = obstacles_string

        to_return = []
        if d[0:4] == "ALG:":
            d = d[4:]
            d = d.split(";")
            # now split into separate obstacles
            # last will be split into empty string therefore ignore
            for x in range(0, len(d) - 1):
                d_split = d[x].split(",")
                # d_split now holds the 4 values that are needed to create one obstacle
                temp = []
                for y in range(0, len(d_split)):
                    # means it's x or y coordinate so multiply by 10 to correspond to correct coordinate
                    if y <= 1:
                        temp.append(int(d_split[y]) * 10)
                    elif y == 2:
                        if d_split[y] == "N":
                            temp.append(90)
                        elif d_split[y] == "S":
                            temp.append(-90)
                        elif d_split[y] == "E":
                            temp.append(0)
                        else:
                            temp.append(180)
                    else:
                        temp.append(int(d_split[y]))
                to_return.append(temp)
            print("to_return: ", to_return)

            #Parse the obstacles data
            obstacles = self.parse_obstacle_data(to_return)

            #Passed it to hamiltonian path
            app = AlgoMinimal(obstacles)
            app.init()
            app.execute()

            # Send the list of commands over.
            obs_priority = app.robot.hamiltonian.get_simple_hamiltonian()
            # print(obs_priority)
            print("Sending list of commands to RPi...")
            self.commands = app.robot.convert_all_commands()
            print("Commands", self.commands)
            
            return self.commands
        else:
            # this would be strings such as NONE, DONE, BULLSEYE
            print(d)


if __name__ == "__main__":
    a = "ALG:2,17,S,0;16,17,W,1;10,11,S,2;4,6,N,3;9,2,E,4;17,5,W,5;".encode(
                "utf-8"
    )
    # x = 'ALG:10,17,S,0;17,17,W,1;2,16,S,2;16,4,S,3;13,1,W,4;6,6,N,5;9,11,W,6;3,3,E,7;'.encode(
            #     'utf-8')
    # a = "ALG:2,17,S,0;16,17,W,1;10,11,S,2;4,6,N,3;9,2,E,4;17,5,W,5;".encode(
    #     "utf-8"
    # )
    # b = "ALG:4,18,E,0;18,18,S,1;13,13,E,2;15,1,N,3;9,2,W,4;0,14,E,5;7,7,N,6;".encode(
    #     "utf-8"
    # )
    # c = "ALG:2,9,N,0;0,17,E,1;14,15,S,2;6,2,N,3;19,4,W,4;10,5,W,5;17,19,S,6;9,18,W,7;".encode(
    #     "utf-8"
    # )
    # d = "ALG:2,18,S,0;5,18,S,1;8,18,S,2;11,18,S,3;14,18,S,4;".encode("utf-8")
    # e = "ALG:0,18,E,0;18,19,S,1;18,0,W,2;5,0,E,3;10,10,E,4;9,10,W,5;".encode(
    #     "utf-8"
    # )
    # f = "ALG:6,6,N,0;16,4,W,1;9,10,W,2;2,16,S,3;8,17,E,4;17,17,S,5;".encode(
    #     "utf-8"
    # )
    # week8 = "ALG:16,1,L,0;8,5,R,1;6,12,N,2;2,18,S,3;15,16,S,4;".encode("utf-8")
    # testing = (
    #     "ALG:6,6,N,0;16,4,W,1;9,11,W,2;2,16,S,3;10,17,S,4;17,17,W,5;".encode(
    #         "utf-8"
    #     )
    # )
    # g = "ALG:3,11,E,0;7,14,S,1;9,5,N,2;".encode("utf-8")
    # h = "ALG:8,2,E,1;8,6,N,2;17,0,N,3;2,16,E,4;11,11,E,5;8,18,S,6;14,18,S,7;17,14,W,8;".encode(
    #     "utf-8"
    # )
    # z = "ALG:8,2,E,1;8,6,N,2;19,0,N,3;2,16,E,4;11,11,E,5;".encode("utf-8")

    algo = Algo()
    algo.run_task1(a)

    pass
