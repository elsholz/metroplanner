import pytest
import math

from metroplanner.planner import Vector, MetroPlan, InsertPosition, InsertOrder, Pixels


def test_vector():
    a = Vector(xy=(1, 1), direction=0, length=1)
    assert a.get_end() == (2, 1)

    for a, b in [
        (0, (1, 0)),
        (45, (1, -1)),
        (90, (0, -1)),
        (135, (-1, -1)),
        (180, (-1, 0)),
        (225, (-1, 1)),
        (270, (0, 1)),
        (315, (1, 1)),
    ]:
        assert Vector.from_two_points((0, 0), b).direction == a

    a = Vector.from_two_points((0, 0), (1, 0))
    # print(a.length, a.direction)
    assert 1 == pytest.approx(a.get_end()[0])
    assert 0 == pytest.approx(a.get_end()[1])
    assert a.direction == 0
    assert a.length == 1

    a = Vector.from_two_points((0, 0), (-1, 0))
    assert -1 == pytest.approx(a.get_end()[0])
    assert 0 == pytest.approx(a.get_end()[1])
    assert a.direction == 180
    assert a.length == 1

    a = Vector.from_two_points((0, 0), (1, 1))
    assert a.direction == 315
    assert a.length == math.sqrt(2)
    assert 1 == pytest.approx(a.get_end()[0])
    assert 1 == pytest.approx(a.get_end()[1])

    a = Vector.from_two_points((0, 0), (0, -1))
    assert 0 == pytest.approx(a.get_end()[0])
    assert -1 == pytest.approx(a.get_end()[1])
    assert a.direction == 90
    assert a.length == 1

    a = Vector.from_two_points((0, 0), (-1, -1))
    assert -1 == pytest.approx(a.get_end()[0])
    assert -1 == pytest.approx(a.get_end()[1])
    assert a.direction == 135
    assert a.length == math.sqrt(2)

    a = Vector.from_two_points((0, 0), (-1, 1))
    assert -1 == pytest.approx(a.get_end()[0])
    assert 1 == pytest.approx(a.get_end()[1])
    assert a.direction == 225
    assert a.length == math.sqrt(2)


def test_rendering():
    with MetroPlan(
            title='Liniennetzplan Wesel und Umgebung',
            subtitle='Mobilität für Wesel am Rhein',
    ) as mpl:
        weselbf = mpl.RegularStop(name='Wesel Bahnhof')
        weselbf.fix()
        grosser_markt = mpl.RegularStop('Großer Markt')

        line_84 = mpl.Line('Buslinie 85', '85')
        line_84.connect_stations(
            a=weselbf, b=grosser_markt,
            edge_length=Pixels(100),
            direction=0
        )


def test_metro_plan():
    return
    with MetroPlan(
            title='Liniennetzplan Wesel und Umgebung',
            subtitle='Mobilität für Wesel am Rhein',
    ) as mpl:
        assert mpl.file_path == 'output.html'

        weselbf = mpl.LargeStation(name='Wesel Bahnhof')
        weselbf = mpl.RegularStop(name='Wesel Bahnhof')
        grosser_markt = mpl.RegularStop('Großer Markt')
        amtsgericht = mpl.RegularStop('Amtsgericht')
        kreishaus = mpl.RegularStop('Kreishaus')
        assert weselbf.is_fixed() is False
        weselbf.fix()
        assert weselbf.is_fixed() is True
        weselbf.unfix()
        assert weselbf.is_fixed() is False
        weselbf.fix()
        assert weselbf.plan is mpl

        assert weselbf.name == 'Wesel Bahnhof'
        assert weselbf.center == (0, 0)
        line_84 = mpl.Line('Buslinie 85', '85')
        exp = line_84.exit_station(weselbf, insert_position=InsertPosition.LEFT_EDGE, angle=180)
        entrp = line_84.enter_station(grosser_markt, insert_position=InsertPosition.RIGHT_EDGE, angle=180)
        print(exp, entrp)
        line_84.connect_stations(weselbf, grosser_markt)
        grosser_markt.fix()
        line_84.connect_stations(grosser_markt, kreishaus, direction=270, en_route=[amtsgericht])
        # line_84.exit_station(grosser_markt, direction=270)
        # line_84.enter_station(amtsgericht)
        # line_84.enter_station(kreishaus)

        # print(weselbf.get_station_lines())

    # # line84.add_station(Station('Kreishaus'), edge_length=EdgeLength.HUGE)

    # line85 = NewLine('Buslinie 85', '85', color=color, shadow='0 0 6px 1px white')
    # line84 = NewLine('Buslinie 84', '84', color=random.choice(color_theme.line_colors), shadow='0 0 6px 1px white')

    # bf.add_lines(Direction.WEST, Direction.WEST, line84)
    # line84.add_station(NewStation('Großer Markt'), direction=Direction.NORTH_WEST, edge_length=EdgeLength.TINY)
    # line84.add_station(NewStation('Amtsgericht'), edge_length=EdgeLength.SMALL, direction=Direction.NORTH)
