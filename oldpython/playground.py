
class MultiLine:
    def __init__(self, direction, *lines):
        self.lines: List[Line] = lines
        self.stations = []
        self.direction: Direction = direction
        self.plan = None

    def add_station(self, station, inward_direction: Direction = None):
        # for ln in self.lines:
        #    ln.add_station(station)
        self.stations.append(station)
        station.plan = self.plan

    def change_direction(self, direction):
        self.direction = direction

#     color = random.choice(color_theme.line_colors)
#     re5 = Line('RE 5 Wesel <-> Koblenz', 'RE 5', color=color, shadow=f'0 0 6px 1px {color}', text_displacement=None)
#     newline = bf.add_lines(Direction.SOUTH, Direction.SOUTH, re5)
#     newline.add_station(Station("Dinslaken Bf", weight=StationWeight.REGULAR_STATION),
#                         edge_length=EdgeLength.HUGE)  # center=(975, 800)))
#     newline.add_station(Station("Oberhausen Hbf", weight=StationWeight.REGULAR_STATION),
#                         edge_length=EdgeLength.HUGE)  # center=(975, 800)))
#     newline.change_direction(Direction.SOUTH_WEST)
#     newline.add_station(Station("Duisburg Hbf", weight=StationWeight.MAIN_STATION),
#                         edge_length=EdgeLength.INTER_CITY)  # center=(975, 800)))
#
#     station: Station
