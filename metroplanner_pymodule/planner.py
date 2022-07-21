from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Union, Tuple, Dict
from .constants import ColorTheme, Pixels, LightTheme, InsertPosition, InsertOrder, Vector
from math import sin, cos, radians, sqrt, degrees, atan2
from jinja2 import Environment, select_autoescape, FileSystemLoader
import htmlmin


class Connectible(ABC):
    """Class for lines and line clusters that can be used to connect stations and have properties such as
    line strength, width, and height."""

    @abstractmethod
    def get_line_strength(self) -> Pixels:
        pass


class Coordinates:
    xshift, yshift = 0, 0

    def __init__(self, xy):
        self.x, self.y = xy


# class LineSegment:
#     def __init__(self, left: Pixels, top: Pixels, width: Pixels, height: Pixels, color: str,
#                  rotation: Union[int, float], shadow,
#                  center):
#         self.color = color
#         self.height = height
#         self.width = width
#         self.top = top
#         self.left = left
#         self.rotation = rotation
#         self.shadow = shadow
#         self.center = center
#
#
# class Line:
#     def __init__(self, name, symbol, color, shadow='',
#                  text_displacement=(Pixels(23), Pixels(-17), -45, 'bottom left', 'left')):
#         self.name = name
#         self.symbol = symbol
#         self.color = color
#         self.shadow = shadow
#         self.stations = []
#         self.line_segments = []
#         self.direction: Union[None, Direction] = None
#         self.current_location = None
#         self.plan = None
#
#         self.line_strength = Pixels(7)
#         self.text_displacement = text_displacement
#
#     def add_station(self, station, edge_length: Union[float, int] = EdgeLength.REGULAR,
#                     direction: Union[float, int] = None):
#         self.stations.append(station)
#         station.text_displacement = self.text_displacement
#         station.plan = self.plan
#
#         width = Pixels(edge_length)
#         height = self.line_strength
#
#         self.add_segment(width, height)
#         # TODO
#         self.plan.stations.append(station)
#
#         station.center = [x for x in self.current_location]
#
#         if direction is not None:
#             self.direction = direction
#
#     def add_segment(self, width, height):
#         left = Pixels(self.current_location[0] + math.sin(math.radians(self.direction)) * height.value / 2)
#         top = Pixels(self.current_location[1] - math.cos(math.radians(self.direction)) * height.value / 2)
#         height = Pixels(height.value) if isinstance(height, EdgeLength) else height
#
#         self.line_segments.append(seg := LineSegment(
#             left=left,
#             top=top,
#             width=width,
#             height=height,
#             color=self.color,
#             shadow=self.shadow,
#             rotation=self.direction,
#             center=(self.current_location[0], self.current_location[1])
#         ))
#
#         dir = self.direction if isinstance(self.direction, Direction) else self.direction
#
#         self.current_location = (
#             self.current_location[0] + math.cos(math.radians(dir)) * width.value,
#             self.current_location[1] + math.sin(math.radians(dir)) * width.value
#         )
#
#     def join_line(self, line: Line, edge_length: EdgeLength = EdgeLength.REGULAR, direction: Direction = None,
#                   station: Station = None, direction_change: Direction = None):
#         if direction is not None:
#             self.direction = direction
#
#         station.rotation = self.direction
#         station.plan = self.plan
#
#         # TODO
#         # left = Pixels(station.center[0] + math.sin(math.radians(station.rotation)) * station.get_css_style_attributes()['height'].value )#height.value / 2)
#         # top = Pixels(station.center[1] - math.cos(math.radians(station.rotation)) * station.get_css_style_attributes()['width'].value) #height.value / 2)
#         # station.top = top
#         # station.left = left
#         station.center = station.center[0], station.center[1]
#
#         self.add_segment(height=self.line_strength, width=edge_length)
#         x1, y1 = self.current_location
#         x2, y2 = line.current_location
#         diff = y1 - y2  # sum([x1 - x2, y1 - y2])
#         line.add_segment(height=line.line_strength, width=Pixels(abs(diff)))
#         ml = MultiLine([self, line])
#         ml.plan = self.plan
#         ml.direction = self.direction
#         for ln in ml.lines:
#             ln.direction = direction
#         ml.add_station(station, edge_length=EdgeLength(0))
#         station.center = station.center[0] - 12, station.center[1] + 26
#         print(station.center)
#         return ml
#
#
# class MultiLine:
#     def __init__(self, lines: List[Line], text_displacement=(Pixels(23), Pixels(-17), -45, 'bottom left', 'left')):
#         self.lines = lines
#         self.stations: List[Station] = []
#         self.direction = None
#         self.current_location = None
#         self.plan = None
#         self.text_displacement = text_displacement
#
#     def add_station(self, station: Station, edge_length: EdgeLength = EdgeLength.REGULAR, direction: Direction = None):
#         self.stations.append(station)
#         station.text_displacement = self.text_displacement
#         station.plan = self.plan
#
#         # width = Pixels(edge_length.value if isinstance(edge_length, EdgeLength) else edge_length)
#         # height = self.line_strength
#         # left = Pixels(self.current_location[0] + math.sin(math.radians(self.direction)) * height.value / 2)
#         # top = Pixels(self.current_location[1] - math.cos(math.radians(self.direction)) * height.value / 2)
#
#         # self.add_segment(left, top, width, height)
#
#         self.plan.stations.append(station)
#
#         if direction is not None:
#             station.rotation = (self.direction + direction) / 2
#
#         station.set_css_style_attribute('height', Pixels(
#             (station.get_css_style_attributes().class_css_style['height'].value - (
#                 ls := self.lines[0].line_strength.value)) +
#             (total_width := 5 * (len(self.lines) - 1) + len(self.lines) * ls)
#             # len(self.lines) * station.get_css_style_attributes()['height'].value
#             # len(self.lines) * station.get_css_style_attributes()['height'].value # + 5 * (len(self.lines) - 1)
#         ))
#         station.set_css_style_attribute('transform', 'rotate(' + str(
#             station.rotation
#         ) + 'deg)')
#         station.set_css_style_attribute('transform-origin', 'top left')
#
#         for lineidx, line in enumerate(self.lines):
#             if line.current_location is None:
#                 line.current_location = 0, 0
#             width = Pixels(edge_length.value if isinstance(edge_length, EdgeLength) else edge_length)
#             height = line.line_strength
#             line.add_segment(width, height)
#
#         self.lines[0].stations.append(station)
#         station.center = self.lines[0].current_location
#
#         station.center = station.center[0], station.center[1] - total_width / 2 - ls / 2
#         print(station.center)
#         # print(station.get_css_style_attributes().individual_css_style['height'], station.center, total_width)
#         station.text_displacement = self.lines[0].text_displacement
#
#         if direction is not None:
#             self.direction = direction
#             for ln in self.lines:
#                 ln.direction = self.direction


# class Station(ABC):
#     @abstractmethod
#     def get_line_entry_point(self):
#         """Get the point in which a line enters the station"""
#
#     @abstractmethod
#     def get_line_exit_point(self):
#         """Get the point in which a line exits the station"""
#
#     @abstractmethod
#     def get_entry_points(self):
#         """Get all line entry points"""
#
#     @abstractmethod
#     def get_exit_points(self):
#         """Get all line exit points"""
#
#     @abstractmethod
#     def enter_line(self, line):
#         """Try to enter a line to a Station"""
#
#     @abstractmethod
#     def exit_line(self, line):
#         """Try to exit a line from a Station"""
#
#
# class RegularStop(Station):
#     def __init__(self, ):
#         pass
#
#
# class MainStation(Station):
#     pass
#
#
# class NewLine:
#     def __init__(self):
#         pass


# class LargeStation:
#     def __init__(self):
#         pass


# class Station:
#     def __init__(self, name: str, text_displacement=None, subtitle: str = None, center=(0, 0),
#                  weight: StationWeight = StationWeight.REGULAR_STOP):
#         self.weight = weight
#         self.name = name
#         self.subtitle = subtitle
#         self.center = center
#         self._station_css_style = None
#         self.plan = None
#
#         # self.left = None
#         # self.top = None
#         self.rotation = 0
#
#         self.text_displacement = text_displacement
#
#     def set_css_style_attribute(self, attribute, value):
#         # self._station_css_style = self._station_css_style or self.plan.station_css_styles.get_css_style(self.weight)
#         self._station_css_style.individual_css_style[attribute] = value
#
#     def get_css_style_attributes(self):
#         self._station_css_style = self._station_css_style or self.plan.station_css_styles.get_css_style(self.weight)
#         return self._station_css_style
#
#     def get_attributes(self):
#         self._station_css_style = self._station_css_style or self.plan.station_css_styles.get_css_style(self.weight)
#         if hasattr(self._station_css_style, 'border'):
#             border = self._station_css_style.border.value
#         else:
#             border = Pixels(0).value
#         res = {
#             'color': self.plan.color_theme.font_color,
#             'left': f'{self.center[0] - (self._station_css_style.class_css_style["width"].value + 2 * border) / 2}px',
#             'top': f'{self.center[1] - (self._station_css_style.class_css_style["height"].value + 2 * border) / 2}px',
#         }
#         res.update(self._station_css_style.individual_css_style)
#         return res
#
#     def get_text_attributes(self):
#         if self.text_displacement:
#             return {
#                 'transform-origin': self.text_displacement[3],
#                 'transform': f'rotate({self.text_displacement[2]}deg)',
#                 'position': 'absolute',
#                 'left': self.text_displacement[0],
#                 'top': self.text_displacement[1],
#                 'width': (width := Pixels(250)),
#                 'text-align': self.text_displacement[4],
#                 'display': 'inline-block',
#                 'font-weight': 'bold',
#             }
#         else:
#             return {
#
#             }
#
#     def get_line_starting_point(self, direction: Union[Direction, int]):
#         dir = direction if isinstance(direction, Direction) else direction
#         css_style = self._station_css_style
#         origin = [
#             (css_style.class_css_style['width'].value * math.cos(math.radians(dir))) / 2 + self.center[0],
#             (css_style.class_css_style['height'].value * math.sin(math.radians(dir))) / 2 + self.center[1]
#         ]
#         return origin
#
#     def add_lines(self, outward_direction: Union[Direction, int], outward_angle: Union[Direction, int],
#                   lines: Union[MultiLine, Line]) -> Union[Line, MultiLine]:
#         if 3 <= self.weight <= 6:
#             if isinstance(lines, MultiLine):
#                 lines.direction = outward_direction
#                 lines.plan = self.plan
#                 for lnidx, mln in enumerate(lines.lines):
#                     mln.plan = self.plan
#                     mln.direction = outward_direction
#                     x, y = self.get_line_starting_point(outward_angle)
#                     margin = 5
#                     x = x + math.sin(math.radians(outward_angle)) * (
#                             (margin + mln.line_strength.value) * (lnidx - (len(lines.lines) - 1) / 2)
#                             # TODO: may as well be minus
#                             + mln.line_strength.value / 2
#                     )
#                     y = y + math.cos(math.radians(outward_angle)) * (
#                             (margin + mln.line_strength.value) * (lnidx - (len(lines.lines) - 1) / 2)
#                             - mln.line_strength.value / 2
#                     )
#                     mln.current_location = [x, y]
#
#                     self.plan.lines.append(mln)
#
#             else:
#                 lines.plan = self.plan
#                 lines.direction = outward_direction
#                 lines.current_location = self.get_line_starting_point(outward_angle)
#                 if not lines in self.plan.lines:
#                     self.plan.lines.append(lines)
#             return lines
#         else:
#             raise ValueError("This station can't be used as a starting point, please choose a larger station weight")
#


class MetroPlan:
    def __init__(
            self, title: str = '', subtitle: str = '',
            color_theme: ColorTheme = LightTheme(),
            # size=(1600, 900),
            file_path='output.html',
    ):
        self.stations: List[Station] = []
        self.lines: List[Line] = []

        class Station(ABC):
            _parent_plan: MetroPlan = self

            def __init__(self, name: str = '', center=(Pixels(0), Pixels(0))):
                self.plan = Station._parent_plan
                self.plan.stations.append(self)
                self.name = name
                self.center = center

                # self.height: Pixels = Pixels(0)
                # self.width: Pixels = Pixels(0)
                self.rotation: float = 0

                self._station_exits: Dict[Line, Tuple[Vector, str, str, float]] = {}
                self._station_entries: Dict[Line, Tuple[Vector, str, str, float]] = {}

                self._fixed = False

            # def get_station_lines(self, direction: float = None) -> Dict[Line, Vector]:
            #     if direction is not None:
            #         lines = {**self._station_exits[direction], **self._station_entries[direction]}
            #     else:
            #         lines = {}
            #     return lines

            def __str__(self):
                return f'Station {self.name} @ {self.center}'

            def get_entries(self) -> Dict[Line, Tuple[Vector, str, str, float]]:
                """Returns a dictionary mapping lines to a tuple containing entry unit vector,
                insertion position and order, and angle."""
                return self._station_entries

            def get_exits(self) -> Dict[Line, Tuple[Vector, str, str, float]]:
                """Returns a dictionary mapping lines to a tuple containing exit unit vector,
                insertion position and order, and angle."""
                return self._station_exits

            def get_station_entry(self, line: Line) -> Union[None, Vector]:
                """Returns the entry unit vector of a line in a station. If the line is not found, returns `None`"""
                return self.get_entries().get(line, None)

            def set_station_entry(self, line: Line, vector: Vector, insert_position: str,
                                  insert_order: str, angle: float) -> None:
                """Takes a line and a unit vector, an insert position, an insert order, and an angle
                 to add to the station entries."""
                if self.get_station_entry(line):
                    raise RuntimeError(f'Line already enters the station.')
                self._station_entries[line] = vector, insert_position, insert_order, angle

            def get_station_exit(self, line: Line) -> Union[None, Vector]:
                """Returns the exit unit vector of a line in a station. If the line is not found, returns `None`"""
                return self.get_exits().get(line, None)

            def set_station_exit(self, line: Line, vector: Vector, insert_position: str = None,
                                 insert_order: str = None, angle: float = None) -> None:
                """Takes a line and a unit vector, an insert position, an insert order, and an angle
                 to add to the station exits."""
                if self.get_station_exit(line):
                    raise RuntimeError(f'Line already enters the station.')
                self._station_exits[line] = vector, insert_position, insert_order, angle

            def shift(self, xy: Tuple[float, float], ignore: List[Line] = None):
                # TODO: Take vector as input?
                """Shift a station and ist incoming and outcoming lines by a certain amount."""
                if ignore is None:
                    ignore = []
                if self._fixed:
                    pass
                else:
                    pass

            def fix(self):
                """Fixes the station in place."""
                self._fixed = True

            def unfix(self):
                """Unfixes the station such that it can be moved freely."""
                self._fixed = False

            def is_fixed(self):
                """Returns whether or not the station is fixed in place"""
                return self._fixed

            def get_bounds(self) -> Tuple[float, float, float, float]:
                """Returns a quadruple containing the values of the most extreme coordinates of the
                station in each direction."""

            @abstractmethod
            def add_station_entry(
                    self, line: Line, insert_position: str = None,
                    insert_order: str = None, angle: float = None
            ) -> Vector:
                """Lets a line enter the station"""

            @abstractmethod
            def add_station_exit(
                    self, line: Line, insert_position: str = None,
                    insert_order: str = None, angle: float = None
            ) -> Vector:
                """"""

            @property
            @abstractmethod
            def width(self) -> Pixels:
                pass

            @property
            @abstractmethod
            def height(self) -> Pixels:
                pass

            @property
            @abstractmethod
            def css_style(self) -> Dict[str, str]:
                """Return a dictionary that represents a CSS key value pair."""

        class RegularStop(Station):
            """Class for regular stops, where entry and exit points for a line are the same
            and the entry and exit directions can be different."""

            def __init__(self, name: str):
                super(RegularStop, self).__init__(name=name)

            def get_bounds(self) -> Tuple[float, float, float, float]:
                return 0, 0, 0, 0

            def add_station_entry(
                    self, line: Line, insert_position: str = None,
                    insert_order: str = None, angle: float = None
            ) -> Vector:
                # if len(self._station_entries) == 0:
                #    self.width = Pixels(15)
                #    self.height = Pixels(15)
                #    self.rotation = direction
                #    self._station_entries[direction] = {line: (0, 0)}
                vector = Vector((0, 0), 0)
                self.set_station_entry(line, vector, insert_position, insert_order, angle)
                return vector

            def add_station_exit(
                    self, line: Line, insert_position: str = None,
                    insert_order: str = None, angle: float = None
            ) -> Vector:
                # TODO: Fix Docstring
                """If the line already enters the stop, return entry vector.
                If the line doesn't enter the stop, add the line."""
                if entry_vector := self.get_station_entry(line):
                    # TODO: What if angle changes?
                    self.set_station_exit(line, vector=entry_vector)
                    return entry_vector
                else:
                    # TODO: what if station contains no lines?
                    if len(self.get_entries()) + len(self.get_exits()):
                        pass
                    else:
                        exit_vector = Vector((0, 0), 0)
                        self.set_station_exit(line, exit_vector)
                        return exit_vector

            @property
            def width(self) -> Pixels:
                return Pixels(20)

            @property
            def height(self) -> Pixels:
                return Pixels(20)

            @property
            def css_style(self) -> Dict[str, str]:
                border = Pixels(2)
                return {
                    'color': self.plan.color_theme.font_color,
                    'left': str(self.center[0] - (self.width + border * 2) / 2),
                    'top': str(self.center[1] - (self.height + border * 2) / 2),
                    'width': str(self.width),
                    'height': str(self.height),
                }

        class LargeStation(Station):
            """A large station that mostly acts as a reference point for other stations by fixing it in place.
            The Station's dimensions depend on the number of lines entering and exiting the station
            at each end or corner."""

            def __init__(self, name: str):
                super(LargeStation, self).__init__(name=name)

            def get_bounds(self) -> Tuple[float, float, float, float]:
                return 0, 0, 0, 0

            def add_station_entry(
                    self, line: Line, insert_position: str = None,
                    insert_order: str = None, angle: float = None
            ) -> Vector:
                pass

            def add_station_exit(
                    self, line: Line, insert_position: str = None,
                    insert_order: str = None, angle: float = None
            ) -> Vector:
                # # if direction in self._station_exits:
                # exits = self._station_exits.get(direction, {})
                # if direction not in [0, 90, 180, 270]:
                #     raise ValueError()
                # if direction in exits:
                #     pass
                # else:
                #     pass
                # self.width = max(self._station_entries)
                pass
                # self._station_exits[direction] = {line: ()}

        class Line(Connectible):
            _parent_plan: MetroPlan = self

            def __init__(self, full_name: str, short_name: str, ):
                self.plan: MetroPlan = Line._parent_plan
                self.plan.lines.append(self)

                self.full_name = full_name
                self.short_name = short_name

                self._last_exited_station: Union[Station, None] = None
                self._last_entered_station: Union[Station, None] = None

                class Segment:
                    """Part of a connection with a rotation, length and style"""
                    _line: Line = self

                    def __init__(self, vector: Vector, rounded_start: bool = False, rounded_end: bool = False):
                        self.line: Line = self._line
                        self.rounded_end: bool = rounded_end
                        self.rounded_start: bool = rounded_start
                        self.vector: Vector = vector

                        # dir = self.direction.value if isinstance(self.direction, Direction) else self.direction
                        # width = Pixels(edge_length.value if isinstance(edge_length, EdgeLength) else edge_length)
                        # height = self.line_strength
                        # left = Pixels(                            self.current_location[0] + math.sin(math.radians(self.direction.value)) * height.value / 2)
                        # top = Pixels(                            self.current_location[1] - math.cos(math.radians(self.direction.value)) * height.value / 2)

                    @property
                    def width(self) -> Pixels:
                        return Pixels(self.vector.length)

                    @property
                    def height(self) -> Pixels:
                        return self.line.get_line_strength()

                    @property
                    def rotation(self) -> float:
                        return self.vector.direction

                    @property
                    def left(self) -> Pixels:
                        """Returns the number of pixels the CSS Container has to be placed absolutely from left.
                        The calculation takes into account the vector of the line and the rotation as well
                        as whether or not the line segment has rounded corners at end or start."""
                        return Pixels(50)

                    @property
                    def top(self) -> Pixels:
                        """Returns the number of pixels the CSS Container has to be placed absolutely from top."""
                        return Pixels(50)

                    @property
                    def css_style(self) -> Dict[str, str]:
                        return {
                            'position': 'absolute',
                            'top': str(self.top),
                            'left': str(self.left),
                            'transform-origin': 'top left',
                            'transform': f'rotate({self.rotation}deg)',
                            'width': str(self.width),
                            'height': str(self.height),
                            'border-radius': f'{50 if self.rounded_end else 0}%'
                                             f' {50 if self.rounded_start else 0}%'
                                             f' {50 if self.rounded_start else 0}%'
                                             f' {50 if self.rounded_end else 0}%'
                        }

                        # self._entered_station: Station = enter
                        # self._exited_station: Station = exit

                    # def get_entered_station(self) -> Union[None, Station]:
                    #     return self._entered_station

                    # def get_exited_station(self) -> Station:
                    #     return self._exited_station

                self.Segment: type = Segment

                class Connection:
                    """Part of a line connecting two stations"""

                    _line: Line = self

                    def __init__(self, a: Station, b: Station):
                        self.line = self._line
                        self.fr: Station = a
                        self.to: Station = b
                        self.segments: List[Segment] = []

                    def include_point(self, point: Vector) -> None:
                        """Include a point on the connection of two stations."""

                self.Connection: type = Connection

            def get_line_strength(self) -> Pixels:
                """Returns the strength of the line in pixels."""
                return Pixels(10)

            def exit_station(
                    self, station: Station,
                    insert_position: str, insert_order: str = None, angle: float = None
            ):
                # TODO: Docstring
                """Makes a line exit a station."""

                station.add_station_exit(
                    line=self, insert_position=insert_position, insert_order=insert_order, angle=angle
                )
                self._last_exited_station = station
                self._last_entered_station = None

            def enter_station(self, station: Station,
                              insert_position: str, insert_order: str = None, angle: float = None):
                # TODO: Docstring
                """Makes a line enter a station."""

                station.add_station_entry(
                    line=self, insert_position=insert_position, insert_order=insert_order, angle=angle
                )
                self._last_exited_station = None
                self._last_entered_station = station

            def connect_stations(self, a: Station, b: Station, edge_length: Union[float, List[float]] = None,
                                 direction: float = None, en_route: List[Station] = None):
                # TODO: Docstring
                """Build a Line with Segments"""
                if en_route is None:
                    en_route = []
                if isinstance(edge_length, float):
                    assert edge_length > 0
                elif isinstance(edge_length, list):
                    assert len(edge_length) == len(en_route)

                if any(stn.is_fixed() for stn in en_route):
                    raise ValueError(f'Cannot have stations en route with fixed positions. \n'
                                     f'{[stn for stn in en_route if stn.is_fixed()]}')

                if a.is_fixed() and b.is_fixed():
                    print('Both stations fixed.')
                    if edge_length:
                        raise ValueError(f'Cannot define edge length between two stations that have fixed positions.')
                    exit_v = a.add_station_exit(
                        line=self, insert_position=InsertPosition.from_angle(direction), angle=direction
                    )
                    entry_v = b.add_station_entry(
                        line=self, insert_position=InsertPosition.from_angle(-direction % 360), angle=-direction % 360
                    )
                    diff_x, diff_y = exit_v.x - entry_v.x, exit_v.y - entry_v.y
                    print(diff_x, diff_y)
                    quit()

                elif a.is_fixed() or b.is_fixed():
                    print('At least one station fixed.')
                    rev = b.is_fixed()
                    if en_route and rev:
                        en_route = reversed(en_route)
                    # TODO: include en route

                    # TODO: consider rev
                    assert a.is_fixed() and not b.is_fixed()

                    b.shift(b.center[0])

                    b.add_station_entry(
                        line=self,
                        insert_position=None,
                        insert_order=None,
                        angle=0,
                    )

                else:
                    print('None of the stations fixed.')
                    pass

        class LineCluster(Connectible):
            def __init__(self, *lines: Line, margin=Pixels(5)):
                self.lines: Tuple[Line] = lines
                self.margin: Pixels = margin

            def get_line_strength(self) -> Pixels:
                res = self.margin * (len(self.lines) - 1)
                for ln in self.lines:
                    res += ln.get_line_strength()
                return res

        self.Station: type = Station
        self.Line: type = Line
        self.LineCluster: type = LineCluster

        self.RegularStop = RegularStop
        self.LargeStation = LargeStation

        self.title: str = title
        self.subtitle: str = subtitle
        self.file_path = file_path

        self.lines: List[Line] = []
        self.stations: List[Station] = []

        self._dimensions: Tuple[float, float] = (0, 0)

        # self.lines: List[Union[Line, MultiLine]] = []
        # self.width, self.height = size
        # self.center = self.width / 2, self.height / 2
        # self.central_stations = []
        # self.station_styles = station_styles

        self.background_color = color_theme.background_color
        self.color_theme = color_theme

        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape()
        )

        self.template = env.get_template("mpl_template.html")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        rendered = self.template.render(
            stations=self.stations,
            lines=self.lines,
            width=self.width,
            height=self.height,
            background_color=self.background_color,
        )

        with open(self.file_path, 'w') as output:
            # minifier = htmlmin.Minifier(remove_comments=True)
            # minifier.input(rendered)
            # output.write(minifier.output)
            output.write(rendered)
            print(self.stations)
            print(self.lines)

    # def station(self, obj: Station):
    #     self.central_stations.append(obj)
    #     obj.plan = self
    #     obj._station_style = self.station_css_styles.get_css_style(obj.weight)
    #     return obj

    def _calculate_dimensions(self) -> None:
        """ Calculate the dimensions of the resulting map that fits all stations"""
        # if all(self._dimensions):
        #     return
        left, right, top, bottom = [], [], [], []
        for bnd in [stn.get_bounds() for stn in self.stations]:
            l, r, t, b = bnd
            left.append(l), right.append(r), top.append(t), bottom.append(b)
        width = max(right) - min(left)
        height = max(bottom) - min(top)
        self._dimensions = (width, height)

    @property
    def width(self):
        self._calculate_dimensions()
        return self._dimensions[0]

    @property
    def height(self):
        self._calculate_dimensions()
        return self._dimensions[1]
