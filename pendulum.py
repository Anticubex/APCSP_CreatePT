"""
pendulum.py
Defines a pendulum system, with pygame rendering
"""

from math import sqrt
import pygame as pg

GRAVITY = 4.1


class Pendulum:
    """A spring pendulum"""

    l: float
    k: float
    x: float
    y: float
    vx: float
    vy: float

    def __init__(
        self,
        k=7.0,
        l=5.0,
        x=2.0,
        y=2.0,
        vx=5.0,
        vy=5.0,
        engine_prefer="Euler",
    ):
        self.l = l
        self.k = k
        self.x = x
        self.init_x = x
        self.y = y
        self.init_y = y
        self.vx = vx
        self.init_vx = vx
        self.vy = vy
        self.init_vy = vy
        self.engine_prefer = engine_prefer

    def reset(self):
        """Resets the spring to initial conditions"""
        self.x = self.init_x
        self.y = self.init_y
        self.vx = self.init_vx
        self.vy = self.init_vy

    def sim_default(self, dt):
        """Uses the engine preference to simulate a step"""
        match self.engine_prefer:
            case "Midpoint":
                self.sim_midpoint(dt)
            case "RK4":
                self.sim_rk4(dt)
            case _:
                self.sim_euler(dt)

    def forces(self):
        """Gets the forces of the system"""
        dist = sqrt(self.x * self.x + self.y * self.y)
        inv_dist = 1.0 / dist
        spring = self.k * (self.l - dist)
        norm = spring * inv_dist
        fx = norm * self.x
        fy = norm * self.y + GRAVITY
        return fx, fy

    def apply(self, fx, fy, dt):
        """Applies the forces as a basic step"""
        self.vx += fx * dt
        self.vy += fy * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def sim_euler(self, dt):
        """Simulates the spring for a frame using euler's method"""
        self.apply(*self.forces(), dt)

    def sim_midpoint(self, dt):
        """Midpoint method"""
        mid = self.copy()
        mid.apply(*self.forces(), dt * 0.5)
        self.apply(*mid.forces(), dt)

    def sim_rk4(self, dt):
        """Fourth-order Runge-Kutta method"""
        dt2 = dt * 0.5

        k1 = self.forces()

        sk2 = self.copy()
        sk2.apply(*k1, dt2)
        k2 = sk2.forces()

        sk3 = self.copy()
        sk3.apply(*k2, dt2)
        k3 = sk3.forces()

        sk4 = self.copy()
        sk4.apply(*k3, dt)
        k4 = sk4.forces()

        avgx = (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        avgy = (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[0]) / 6

        self.apply(avgx, avgy, dt)

    def copy(self):
        """Returns a copy"""
        return Pendulum(
            self.k,
            self.l,
            self.x,
            self.y,
            self.vx,
            self.vy,
            self.engine_prefer,
        )

    def render(self, screen):
        """Renders the spring-mass-damper to the screen"""
        pg.draw.circle(screen, (255, 255, 255), w2s(0, 0), 10)
        pg.draw.circle(screen, (255, 255, 255), w2s(self.x, self.y), 10)
        dist = sqrt(self.x * self.x + self.y * self.y)
        pg.draw.line(
            screen,
            (255, 0, 0) if dist < self.l else (0, 255, 0),
            w2s(0, 0),
            w2s(self.x, self.y),
            10,
        )


def w2s(x, y):
    """World Coordinates to Screen Coordinates"""
    return (x * 30 + 260), (y * 30 + 170)
