#!/usr/bin/python3

from metroplanner.planner import MetroPlan
from metroplanner.constants import Direction, LightTheme
import random

color_theme = LightTheme()
with MetroPlan(
        "Nahverkehrsplan Wesel",
        subtitle="Mobilitat fur den Niederrhein.",
        # size=(2500, 2500),
        # station_styles=StationStyles(),
) as plan:
    # bf = plan.station(Station("Wesel Bahnhof", weight=StationWeight.LARGE_STATION, center=plan.center))

    
    color = random.choice(color_theme.line_colors)
    # line85 = Line('Buslinie 85', '85', color=color, shadow='0 0 6px 1px white')
    #line84 = Line('Buslinie 84', '84', color=random.choice(color_theme.line_colors), shadow='0 0 6px 1px white')
    # line8485 = MultiLine([line84, line85])

    #bf.add_lines(Direction.WEST, Direction.WEST, line84)
    # line84.add_station(Station('Großer Markt'), direction=Direction.NORTH_WEST, edge_length=EdgeLength.TINY)
    # line84.add_station(Station('Amtsgericht'),edge_length=EdgeLength.SMALL, direction=Direction.NORTH)

    # # bf.add_lines(Direction.WEST, Direction.WEST, line8485)

    # # # 85 -> Flueren Waldstrasse
    # # # 84 -> Bislich Ortsmitte
    # # station = line8485.add_station(wallstr := Station('Wallstraße', ), EdgeLength.HUGE)#, direction=Direction.NORTH)
    # # wallstr.center = wallstr.center[0] - 12 , wallstr.center[1] + 24
    # # line84.direction = Direction.SOUTH_WEST
    # # line84.add_station(Station('Stettiner Straße'), direction=Direction.WEST, edge_length=EdgeLength.TINY)
    # # line84.add_station(Station('Großer Markt'), direction=Direction.NORTH_WEST, edge_length=EdgeLength.TINY)
    # # line84.add_station(Station('Amtsgericht'),edge_length=EdgeLength.SMALL, direction=Direction.NORTH)
    # # line84.add_station(Station('Kreishaus'), edge_length=EdgeLength.HUGE)
    # # line84.add_station(Station('Arbeitsagentur'), edge_length=EdgeLength.HUGE)
    # # # line84.add_station(Station('Großer Markt'), direction=Direction.WEST)

    # # line85.direction = Direction.NORTH
    # # line85.add_station(Station('Mathenakreuz', ), edge_length=EdgeLength.TINY)
    # # line85.add_station(Station('Mölderplatz', ), direction=Direction.NORTH_EAST, edge_length=EdgeLength.TINY)
    # # line85.add_station(Station('Blankenburgstraße', ), direction=Direction.NORTH, edge_length=EdgeLength.SMALL)
    # # line85.add_station(Station('Breiter Weg', ), direction=Direction.NORTH_WEST, edge_length=EdgeLength.SMALL)
    # # line85.add_station(Station('Kartäuserweg', ), edge_length=EdgeLength.SMALL)
    # # line85.add_station(Station('Rastenburger Straße', ), edge_length=EdgeLength.SMALL)
    # # line85.add_station(Station('Tilsiter Straße', ), edge_length=EdgeLength.SMALL)

    # # line8485 = line85.join_line(line84, station=Station('Feldmark Marktplatz'), direction=Direction.NORTH)#, direction_change=Direction.WEST)
    # # #line8485 = line85.join_line(line84, station=Station('Feldmark Marktplatz'), direction=Direction.NORTH, direction_change=Direction.NORTH_WEST)

    # # line8485.add_station(Station('Feldmark Marktplatz', ), direction=Direction.NORTH_WEST)
    # # line8485.add_station(Station('Friedrich-Geselschap-Str.', ), )
    # # line8485.add_station(Station('Ackerstraße', ), )
    # # line8485.add_station(Station('Barthel-Bruyn-Weg', ), )
    # # line8485.add_station(Station('Eissporthalle', ), direction=Direction.WEST)
    # # line8485.add_station(Station('Glückauf', ), )
    # # line8485.add_station(Station('Flürener Weg', ), )
    # # line8485.add_station(Station('Flüren Beethovenstraße', ), )
    # # line8485.add_station(Station('Flüren Markt', ), )
    # # line8485.add_station(Station('Flüren Waldschenke', ), direction=Direction.SOUTH_WEST)
    # # line8485.text_displacement = (Pixels(27), Pixels(15), 45, 'top left')
    # # line8485.add_station(Station('Flüren Drosselstraße', ), )

    # # line85.direction = Direction.WEST
    # # line85.add_station(Station('Flüren Kiebitzstraße', ), )
    # # line85.add_station(Station('Flüren Waldstraße', ), )

    # # line84.add_station(Station('Flüren Firedhof', ), direction=Direction.WEST)
    # # line84.add_station(Station('Diersfordt Rosenallee'))
    # # line84.add_station(Station('Mars'), direction=Direction.NORTH_WEST)
    # # line84.add_station(Station('Westerheide'), direction=Direction.NORTH)
    # # line84.add_station(Station('Schüttwich'), direction=Direction.WEST)
    # # line84.add_station(Station('Mühlenfeld'))
    # # line84.add_station(Station('Harsumer Weg'))
    # # line84.add_station(Station('Bislich Ortsmitte'))

    # bf.add_lines(Direction.NORTH, Direction.NORTH + 30, line85)
    # # line85.color = random.choice(color_theme.line_colors)

    # # 85 -> Im Buttendicksfeld

    # line85.text_displacement = StationLabelStyle(StationLabelStyle.Rotation.RIGHT_DOWN).get_style()# (Pixels(25), Pixels(10), 45, 'top left')
    # line85.add_station(Station('Isselstraße', weight=StationWeight.REGULAR_STOP), EdgeLength.HUGE, direction=Direction.NORTH_EAST)
    # line85.add_station(Station('Brüner Landstraße', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Franziskusstraße', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Schepersweg', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Am Schwan', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Kanstanienstraße', weight=StationWeight.REGULAR_STOP), direction=Direction.EAST)
    # line85.text_displacement = StationLabelStyle(StationLabelStyle.Rotation.RIGHT_UP).get_style()# (Pixels(25), Pixels(10), 45, 'top left')
    # # line85.text_displacement = (Pixels(23), Pixels(-17), -45, 'bottom left')
    # line85.add_station(Station('Am Lauerhaas', weight=StationWeight.REGULAR_STOP), direction=Direction.SOUTH_EAST)
    # line85.add_station(Station('Tannenstraße', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Eichenstraße', weight=StationWeight.REGULAR_STOP), direction=Direction.SOUTH)
    # line85.text_displacement = StationLabelStyle(StationLabelStyle.Rotation.LEFT_UP).get_style()# (Pixels(25), Pixels(10), 45, 'top left')
    # # line85.text_displacement = (Pixels(-65), Pixels(65), -45, 'bottom left')
    # """ 84:
    # Am Friedenshof, Wesel 	an 16:19 	ab 16:19
    # Voßhöveler Straße, Wesel 	an 16:20 	ab 16:20
    # Rudolf-Diesel-Straße, Wesel 	an 16:21 	ab 16:21
    # Im Buttendicksfeld, Wesel"""
    # line85.add_station(Station('Friedhofsweg', weight=StationWeight.REGULAR_STOP), direction=Direction.SOUTH_EAST)
    # line85.add_station(Station('Rosenstraße', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Ev. Krankenhaus', weight=StationWeight.REGULAR_STOP),)
    # line85.text_displacement = StationLabelStyle(StationLabelStyle.Rotation.RIGHT_DOWN).get_style()
    # # line85.text_displacement = (Pixels(27), Pixels(15), 45, 'top left')
    # line85.add_station(Station('Aaper Weg', weight=StationWeight.REGULAR_STOP), direction=Direction.EAST)
    # line85.add_station(Station('Alex.-von-Humboldt-Str.', weight=StationWeight.REGULAR_STOP))
    # line85.add_station(Station('Am Buttendick', weight=StationWeight.REGULAR_STOP), direction=Direction.NORTH)
    # line85.add_station(Station('Im Buttendicksfeld', weight=StationWeight.REGULAR_STOP))


    # line64 = Line('Buslinie 64', '64', color=random.choice(color_theme.line_colors), shadow='0 0 6px 1px white')
    # bf.add_lines(outward_direction=Direction.WEST, outward_angle=Direction.WEST+ 30, lines=line64)

    # line64.add_station(Station('Rathaus, Wesel' 	, weight=StationWeight.REGULAR_STOP), )
    # line64.add_station(Station('Amtsgericht, Wesel', weight=StationWeight.REGULAR_STOP), direction=Direction.NORTH)
    # line64.add_station(Station('Kreishaus, Wesel' 	, weight=StationWeight.REGULAR_STOP), )
    # line64.add_station(Station('Arbeitsagentur, Wesel' 	, weight=StationWeight.REGULAR_STOP), )
    # line64.add_station(Station('Feldmark Marktplatz, Wesel' 	, weight=StationWeight.REGULAR_STOP), )
    # line64.add_station(Station('Feldmark Berufskolleg, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.text_displacement = StationLabelStyle(rotation=180).get_style()
    # line64.add_station(Station('Karl-Straube-Straße, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Blumenkamp Hermann-Hesse-Str., Wesel' , weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Blumenkamp Feuerdornstr., Wesel' , weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Blumenkamp Schillkaserne, Wesel' 	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Strauchheide, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Weißenstein, Hamminkeln' 	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Diersfordter Weg, Hamminkeln' 	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Bergfrede, Hamminkeln' 	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Markt, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('An der Windmühle, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Weststraße, Hamminkeln'	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Ringenberg Siedlung, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Ringenberg Ort, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Dingden Ishorst, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Kampstraße, Hamminkeln' 	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Dingden Schule, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Veilchenweg, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Akademie Klausenhof, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Kindergarten, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Dingden Freibad, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Dingden Neustraße, Hamminkeln' , weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Lankern Gasthaus Ridder, Hamminkeln', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Lankern Schmiede Weyer, Bocholt', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Mussum Zum Waldschlößchen, Bocholt', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Biemenh. Birkenallee, Bocholt'	, weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('BEW, Bocholt' , weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Friesenstr., Bocholt', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)
    # line64.add_station(Station('Bahnhof, Bocholt'	, weight=StationWeight.SPECIAL_STOP), edge_length=EdgeLength.REGULAR)
    # line64.add_station(Station('Kinodrom, Bocholt' , weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # line64.add_station(Station('Bustreff (1/A1), Bocholt', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.SMALL)

    # linesb21 = Line('Schnellbus 21', 'SB21', color=random.choice(color_theme.line_colors), shadow='0 0 6px 1px white')
    # bf.add_lines(outward_direction=Direction.WEST, outward_angle=Direction.WEST , lines=linesb21)

    # a = linesb21.text_displacement
    # linesb21.text_displacement  = StationLabelStyle(rotation=135).get_style()
    # linesb21.add_station(Station('Schulzentrum-Mitte, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Feldmark Marktplatz, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Schulzentrum Nord, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)

    # bf.add_lines(outward_direction=Direction.NORTH_EAST, outward_angle=Direction.NORTH_EAST+ 0, lines=linesb21)

    # linesb21.text_displacement  = StationLabelStyle(45).get_style()
    # linesb21.add_station(Station('Post, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=90, direction=Direction.EAST)
    # linesb21.add_station(Station('Drevenacker Straße, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.HUGE + 7)
    # linesb21.text_displacement  = StationLabelStyle(225).get_style()
    # linesb21.add_station(Station('Raesfelder Straße, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.HUGE)
    # linesb21.add_station(Station(' ' or 'Ev. Krankenhaus, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.HUGE, direction=Direction.NORTH_EAST)
    # linesb21.add_station(Station('Am langen Reck, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Am Dülmen, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR, direction=Direction.EAST)
    # linesb21.add_station(Station('Loher Weg, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Drevenack Gühnen, Hünxe', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Drevenack Strütchensweg, Hünxe', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Drevenack Schürmann, Hünxe', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Drevenack Wachtenbrink, Hünxe', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Damm Wortelkamp, Schermbeck', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Damm Molkerei, Schermbeck', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Bricht, Schermbeck', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Hecheltjen, Schermbeck', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb21.add_station(Station('Rathaus, Schermbeck', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)

    # linesb8 = Line('Schnellbus 8', 'SB8', color=random.choice(color_theme.line_colors), shadow='0 0 6px 1px white')
    # bf.add_lines(outward_direction=Direction.WEST, outward_angle=Direction.SOUTH_WEST, lines=linesb8)

    # linesb8.add_station(Station('Bahnhof, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Wallstraße, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Stettiner Straße, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Großer Markt, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Norbertstraße, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('LVR-Niederrheinmuseum, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Restaurant Lindenwirtin, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Ginderich Post, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Ginderich Poll, Wesel', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Birten Gindericher Straße, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Birten Gewerbegebiet Birten, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Haus Lau, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Viktorstraße, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Friedhof, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Gymnasium, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Bahnhofstraße, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)
    # linesb8.add_station(Station('Bahnhof, Xanten', weight=StationWeight.REGULAR_STOP), edge_length=EdgeLength.REGULAR)