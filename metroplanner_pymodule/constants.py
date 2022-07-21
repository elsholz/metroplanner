from __future__ import annotations
from math import sin, cos, radians, sqrt, degrees, atan2
from typing import Tuple
import random
from typing import Union


class Pixels:
    def __init__(self, value: Union[int, float]):
        self.value = value

    def __str__(self):
        return f'{round(self.value, 4)}px'

    def __sub__(self, other) -> Pixels:
        if isinstance(other, Pixels):
            return Pixels(self.value - other.value)
        elif isinstance(other, (float, int)):
            return Pixels(self.value - other)
        else:
            raise ValueError(f"Can't subtract object of type {type(other)} from Pixels object.")

    def __add__(self, other) -> Pixels:
        if isinstance(other, Pixels):
            return Pixels(self.value + other.value)
        elif isinstance(other, (float, int)):
            return Pixels(self.value + other)
        else:
            raise ValueError(f"Can't add object of type {type(other)} to Pixels object.")

    def __mul__(self, other) -> Pixels:
        if isinstance(other, Pixels):
            return Pixels(self.value * other.value)
        elif isinstance(other, (float, int)):
            return Pixels(self.value * other)
        else:
            raise ValueError(f"Can't multiply object of type {type(other)} with Pixels object.")

    def __truediv__(self, other) -> Pixels:
        if isinstance(other, Pixels):
            return Pixels(self.value / other.value)
        elif isinstance(other, (float, int)):
            return Pixels(self.value / other)
        else:
            raise ValueError(f"Can't divide Pixels object by object of type {type(other)}.")


class Direction:
    EAST = 0
    SOUTH_EAST = 45
    SOUTH = 90
    SOUTH_WEST = 135
    WEST = 180
    NORTH_WEST = 225
    NORTH = 270
    NORTH_EAST = 315


class ColorTheme:
    def __init__(self, theme_name, colors: dict):
        self.colors = colors
        self.line_colors = colors['lines']
        self.font_color = colors['font']
        self.background_color = colors['background']
        self.theme_name = theme_name

    def get_random_shade(self):
        return random.choice(self.line_colors)


class DarkTheme(ColorTheme):
    def __init__(self):
        super(DarkTheme, self).__init__(
            theme_name='dark',
            colors={
                'font': '#ffffff',
                'background': '#002',
                'lines': [
                    '#fe009a',
                    '#f500ff',
                    '#ff0001',
                    '#ff6600',
                    '#fcff00',
                    '#96ff00',
                    '#009e00',
                    '#0000ff',
                    '#379cde',
                    '#00ffef',
                ]
            },
        )


class LightTheme(ColorTheme):
    def __init__(self):
        super(LightTheme, self).__init__(
            theme_name='light',
            colors={
                'font': '#000',
                'background': '#eef',
                'lines': [
                    '#ae005a',
                    '#a500af',
                    '#af0001',
                    '#af6600',
                    '#fcaf00',
                    '#96af00',
                    '#009e00',
                    '#0000af',
                    '#379cde',
                    '#00afef',
                ]
            },
        )


class Vector:
    """A Vector has a starting point, a length, a direction, and a calculated ending point."""

    def __init__(self, xy: Tuple[float, float], direction: float, length: float = 1):
        """
        xy: coordinates
        dir: direction as angle
        length: length in Pixels as number
        """
        self.x, self.y = xy
        self.direction = direction
        self.length = length

    @staticmethod
    def unit_vector(xy: Tuple[float, float], direction: float):
        return Vector(xy, direction)

    @staticmethod
    def position_vector(xy: Tuple[float, float]):
        return Vector.from_two_points((0, 0), xy)

    def is_unit_vector(self) -> bool:
        """Checks if the length of the vector is 1 and hence is a unit vector."""
        return self.length == 1

    def is_position_vector(self) -> bool:
        """Checks if the vetor starts in the origin and hence is a position vector."""
        return self.get_start() == (0, 0)

    def get_start(self) -> Tuple[float, float]:
        """Returns the starting point of the vector."""
        return self.x, self.y

    def get_end(self) -> Tuple[float, float]:
        """Returns the end point calculated by adding the direction and length to the starting point."""
        return (
            self.x + cos(radians(-self.direction)) * self.length,
            self.y + sin(radians(-self.direction)) * self.length
        )

    def get_coord_delta(self) -> Tuple[float, float]:
        """Returns the delta between the starting and ending points as a tuple."""
        return cos(radians(-self.direction)) * self.length, sin(radians(-self.direction)) * self.length

    @staticmethod
    def from_two_points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Vector:
        """Creates a vector object with starting point, direction and length given two points.
        The call of the method get_end shall yield the second point"""
        dx = xy2[0] - xy1[0]
        dy = xy2[1] - xy1[1]

        # print('dx', dx, 'dy', dy, degrees(atan2(dx, dy)) - 90)
        return Vector(
            xy=xy1,
            direction=(360 - 90 + degrees(atan2(dx, dy))) % 360,
            length=sqrt(dx ** 2 + dy ** 2)
        )

    def __add__(self, other: Vector) -> Vector:
        """Add together two position vectors."""
        if self.is_position_vector() and other.is_position_vector():
            x1, y1 = self.get_end()
            x2, y2 = other.get_end()
            return Vector.position_vector((x1 + x2, y1 + y2))
        else:
            raise ValueError()


class InsertOrder(str):
    BEFORE: str = 'before'
    AFTER: str = 'after'


class InsertPosition(str):
    TOP_LEFT_CORNER = 'top_left'
    TOP_EDGE = 'top'
    TOP_RIGHT_CORNER = 'top_right'
    RIGHT_EDGE = 'right'
    BOTTOM_RIGHT_CORNER = 'bottom_right'
    BOTTOM_EDGE = 'bottom'
    BOTTOM_LEFT_CORNER = 'bottom_left'
    LEFT_EDGE = 'left'

    @staticmethod
    def from_angle(angle: float) -> str:
        """Find a suitable insertion position from a given angle."""
        if 330 <= angle or 0 <= angle <= 30:
            return InsertPosition.RIGHT_EDGE
        elif 30 < angle < 60:
            return InsertPosition.BOTTOM_RIGHT_CORNER
        elif 60 <= angle <= 120:
            return InsertPosition.BOTTOM_EDGE
        elif 120 < angle < 150:
            return InsertPosition.BOTTOM_LEFT_CORNER
        elif 150 <= angle <= 210:
            return InsertPosition.LEFT_EDGE
        elif 210 < angle < 240:
            return InsertPosition.TOP_LEFT_CORNER
        elif 240 <= angle <= 300:
            return InsertPosition.TOP_EDGE
        elif 300 < angle < 330:
            return InsertPosition.TOP_RIGHT_CORNER
        raise Exception(angle)
