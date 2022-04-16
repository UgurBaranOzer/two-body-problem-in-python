import math
import argparse
from tkinter import *

# initialConditions
initial_eccentricity = 0
initial_q = 0.2


def get_args():
    parser = argparse.ArgumentParser(description='Two-Body Simulation')
    parser.add_argument('-T', '--step', dest='total_step', type=int, help='Total step (e.g. 10000)', default=1000)
    parser.add_argument('-dt', '--timestep', dest='timestep', type=float, help='Time step (e.g. 0.15)', default=0.15)
    parser.add_argument('-q', '--mass_ratio', dest='mass_ratio', type=float, help='Mass Ratio', default=0.5)
    parser.add_argument('-e', '--eccentricity', dest='eccentricity', type=float, help='Eccentricity', default=0.7)

    return parser.parse_args()


def initial_velocity(q, eccentricity):
    return math.sqrt((1 + q) * (1 + eccentricity))


class BodyModel(object):
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.m = m

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " mass: " + str(self.m)


class TwoBodyController(object):
    def __init__(self, T, dt, q, eccentricity):
        self.T = T
        self.dt = dt
        self.eccentricity = eccentricity
        self.q = q  # current mass ratio m2/m1
        self.body_one = BodyModel(x=0, y=0, m=1)
        self.body_two = BodyModel(x=0, y=0, m=q)
        self.u = [1, 0, 0, initial_velocity(self.q, self.eccentricity)]
        self.m1 = self.body_one.m
        self.m2 = self.body_two.m  # will be set to q
        self.m12 = self.body_one.m + self.body_two.m  # will be set to m1+m2

    def derivative(self):
        du = [None] * len(self.u)

        # x and y coordinates
        r = [self.u[0], self.u[1]]

        # distance between bodies
        rr = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2))

        for i in range(2):
            du[i] = self.u[i + 2]
            du[i + 2] = -(1 + self.q) * r[i] / (math.pow(rr, 3))

        return du

    def runge_kutta_calculate(self, h):  # h: timestep u:variable
        a = [h / 2, h / 2, h, 0]
        b = [h / 6, h / 3, h / 3, h / 6]
        u0 = []
        ut = []
        dimension = len(self.u)

        for i in range(dimension):
            u0.append(self.u[i])
            ut.append(0)

        for j in range(4):
            du = self.derivative()

            for i in range(dimension):
                self.u[i] = u0[i] + a[j] * du[i]
                ut[i] = ut[i] + b[j] * du[i]

        for i in range(dimension):
            self.u[i] = u0[i] + ut[i]

    def update_position(self):
        timestep = self.dt
        self.runge_kutta_calculate(timestep)
        self.calculate_new_position()

    def calculate_new_position(self):
        r = 1
        a1 = (self.m2 / self.m12) * r
        a2 = (self.m1 / self.m12) * r

        self.body_one.x = -a2 * self.u[0]
        self.body_one.y = -a2 * self.u[1]

        self.body_two.x = a1 * self.u[0]
        self.body_two.y = a1 * self.u[1]

    def reset_state_to_initial_conditions(self):
        self.q = initial_q
        self.eccentricity = initial_eccentricity

        self.u[0] = 1
        self.u[1] = 0
        self.u[2] = 0
        self.u[3] = initial_velocity(self.q, self.eccentricity)

        self.m2 = self.q
        self.m12 = self.m1 + self.m2

    def run(self):

        with open('vectors.txt', 'w') as fp:
            for step in range(self.T):
                controller.update_position()
                fp.write('{}, {}, {}, {}\n'.format(str(controller.body_one.x), str(controller.body_one.y),
                                                   str(controller.body_two.x), str(controller.body_two.y)))


if __name__ == '__main__':
    args = get_args()

    total_step = args.total_step
    timestep = args.timestep
    mass_ratio = args.mass_ratio
    eccentricity = args.eccentricity

    controller = TwoBodyController(total_step, timestep, mass_ratio, eccentricity)
    controller.run()