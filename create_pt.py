"""Spring-damper simulation using pygame."""

import pygame as pg
from ui import DropDown, NumberInput, Label, UI_group, Button
from pendulum import Pendulum

# Pygame configurations
FPS = 60
DT = 1.0 / FPS
W_HEIGHT = 500
W_WIDTH = 800


def options_menu_init():
    """Initializes the options menu. Returns a dictionary with the UI elements"""

    COLOR_INACTIVE = (100, 80, 255)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (255, 100, 100)
    COLOR_LIST_ACTIVE = (255, 150, 150)
    font = pg.font.Font(None, 32)

    return UI_group(
        {
            "strength": NumberInput(660, 110, font, "7.00"),
            "strengthLabel": Label(font, 550, 114, "Strength:"),
            "length": NumberInput(660, 150, font, "5.00"),
            "lengthLabel": Label(font, 550, 154, "Length:"),
            "initSetsLabel": Label(font, 550, 194, "Initial Conditions:"),
            "initVelX": NumberInput(660, 230, font, "5.00"),
            "initVelXLabel": Label(font, 540, 234, "Velocity X:"),
            "initVelY": NumberInput(660, 270, font, "5.00"),
            "initVelYLabel": Label(font, 540, 274, "Velocity Y:"),
            "initPosX": NumberInput(660, 310, font, "2.00"),
            "initPosXLabel": Label(font, 540, 314, "Position X:"),
            "initPosY": NumberInput(660, 350, font, "2.00"),
            "initPosYLabel": Label(font, 540, 354, "Position Y:"),
            "reset": Button(750, 440, 60, 50, pg.image.load("assets/refresh.png")),
            "engine": DropDown(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                550,
                50,
                200,
                50,
                font,
                "Euler",
                ["Euler", "Midpoint", "RK4"],  # Options list
            ),
        }
    )


def options_menu_update(elements, event_list, pendulum):
    """Manages the menu and updates values"""

    elements.update(event_list)

    if (strength := elements["strength"]).valid:
        pendulum.k = float(strength.text)

    if (length := elements["length"]).valid:
        pendulum.l = float(length.text)

    if (initPosX := elements["initPosX"]).valid:
        pendulum.init_x = float(initPosX.text)

    if (initPosY := elements["initPosY"]).valid:
        pendulum.init_y = float(initPosY.text)

    if (initVelX := elements["initVelX"]).valid:
        pendulum.init_vx = float(initVelX.text)

    if (initVelY := elements["initVelY"]).valid:
        pendulum.init_vy = float(initVelY.text)

    if elements["reset"].clicked:
        pendulum.reset()

    pendulum.engine_prefer = elements["engine"].main


def options_menu_draw(elements, screen):
    """Renders the menu"""

    elements.draw(screen)


def main():
    # pygame setup
    pg.init()
    screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))
    clock = pg.time.Clock()

    menu_elements = options_menu_init()
    pendulum = Pendulum()

    while True:
        clock.tick(FPS)

        # poll for events
        event_list = pg.event.get()
        # pygame.QUIT event means the user clicked X to close your window
        for event in event_list:
            if event.type == pg.QUIT:
                return

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((10, 10, 10))

        options_menu_update(menu_elements, event_list, pendulum)
        pendulum.sim_default(DT)

        # RENDER YOUR GAME HERE
        pendulum.render(screen)
        options_menu_draw(menu_elements, screen)

        # flip() the display to put your work on screen
        pg.display.flip()


if __name__ == "__main__":
    main()
