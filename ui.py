"""
ui.py
A UI system menu for pygame, derived from stack overflow and github user Rabbid76;s work
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import pygame as pg


class UI_Element(ABC):
    """A UI Element"""

    @abstractmethod
    def update(self, event_list):
        ...

    @abstractmethod
    def draw(self, screen):
        ...


class DropDown(UI_Element):
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, screen):
        pg.draw.rect(screen, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        screen.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pg.draw.rect(
                    screen,
                    self.color_option[1 if i == self.active_option else 0],
                    rect,
                    0,
                )
                msg = self.font.render(text, 1, (0, 0, 0))
                screen.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    self.main = self.options[self.active_option]


class Label(UI_Element):
    def __init__(self, font, x, y, text, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.color = color
        self.text_surface = self.font.render(self.text, True, self.color)

    def redraw_surface(self):
        self.text_surface = self.font.render(self.text, True, self.color)

    def update(self, event_list):
        ...

    def draw(self, screen):
        screen.blit(
            self.text_surface,
            (self.x, self.y),
        )


class Textbox(UI_Element):
    def __init__(self, x, y, font, text="", validator=lambda _: True, default=""):
        self.active = False
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.validator = validator
        self.valid = True
        self.default = default
        self.text_surface = font.render(self.text, True, (255, 255, 255))
        self.rect_width = max(140, 10 + self.text_surface.get_width())
        self.input_rect = pg.Rect(x, y, self.rect_width, 32)
        self.input_rect.w = self.text_surface.get_width() + 10

    # Textbox.update
    def update(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                self.active = self.input_rect.collidepoint(e.pos)

            if e.type == pg.KEYDOWN:
                if self.active:
                    if e.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += e.unicode
                    self.text_surface = self.font.render(
                        self.text, True, (255, 255, 255)
                    )
        self.valid = self.validator(self.text)

    def draw(self, screen):
        self.input_rect.w = max(self.text_surface.get_width() + 10, 100)
        pg.draw.rect(screen, (0, 0, 0), self.input_rect, 0)
        pg.draw.rect(
            screen, (255, 255, 255) if self.valid else (255, 0, 0), self.input_rect, 2
        )
        screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))


class NumberInput(Textbox):
    def __init__(self, x, y, font, default="1.00"):
        super().__init__(x, y, font, default, is_float, "0.0")


class Button(pg.sprite.Sprite, UI_Element):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pg.Surface((width, height), flags=pg.SRCALPHA)
        pg.transform.scale(image, (width, height), self.image)
        self.rect = self.image.get_rect(center=(x, y))
        self.group = pg.sprite.Group([self])
        self.clicked = False

    def draw(self, screen):
        self.group.draw(screen)

    def update(self, event_list):
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
                    return
        self.clicked = False


@dataclass
class UI_group:
    elements: Dict[str, UI_Element]

    def update(self, event_list):
        for _, e in self.elements.items():
            e.update(event_list)

    def draw(self, screen):
        for _, e in self.elements.items():
            e.draw(screen)

    def __getitem__(self, key):
        return self.elements[key]


def is_float(element: any) -> bool:
    """Checks whether a value can be converted to a float by python"""
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False
